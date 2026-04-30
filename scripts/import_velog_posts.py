#!/usr/bin/env python3
"""
Import published Velog posts into this Obsidian vault.

Usage from the vault root:

    python scripts/import_velog_posts.py
    python scripts/import_velog_posts.py --username josephuk77 --method graphql
    python scripts/import_velog_posts.py --username josephuk77 --method rss --dry-run

The script uses public Velog endpoints only. It does not read .env files and
does not require secrets or API keys.

Default behavior:
- username: josephuk77
- output: 03_Blog/Published/
- method: auto, which tries GraphQL first and falls back to RSS
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


DEFAULT_USERNAME = "josephuk77"
DEFAULT_OUTPUT_DIR = Path("03_Blog/Published")
GRAPHQL_ENDPOINT = "https://v2.velog.io/graphql"
RSS_URLS = (
    "https://v2.velog.io/rss/{username}",
    "https://api.velog.io/rss/{username}",
    "https://v2.velog.io/rss/@{username}",
)
USER_AGENT = "ObsidianVelogImporter/1.0"


POSTS_QUERY = """
query Posts($username: String!, $limit: Int, $cursor: ID) {
  posts(username: $username, limit: $limit, cursor: $cursor) {
    id
    title
    url_slug
    released_at
    updated_at
  }
}
"""


POST_QUERY = """
query Post($username: String!, $url_slug: String!) {
  post(username: $username, url_slug: $url_slug) {
    id
    title
    body
    url_slug
    released_at
    updated_at
  }
}
"""


@dataclass
class VelogPost:
    title: str
    body: str
    published_at: str
    publish_url: str
    source: str


class SimpleHtmlToMarkdown(HTMLParser):
    """Small dependency-free HTML to Markdown converter for RSS content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.list_stack: list[dict[str, Any]] = []
        self.link_stack: list[dict[str, Any]] = []
        self.in_pre = False
        self.in_inline_code = False
        self.pre_lang = ""
        self.pre_parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value or "" for key, value in attrs}

        if tag in {"script", "style"}:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        if self.in_pre:
            if tag == "code":
                self.pre_lang = self._language_from_class(attr_map.get("class", ""))
            return

        if tag == "pre":
            self._append("\n\n")
            self.in_pre = True
            self.pre_lang = ""
            self.pre_parts = []
            return

        if tag == "code":
            self.in_inline_code = True
            self._append("`")
            return

        if tag in {"p", "div", "section", "article"}:
            self._append("\n\n")
        elif tag in {"br", "hr"}:
            self._append("\n" if tag == "br" else "\n\n---\n\n")
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self._append("\n\n" + ("#" * level) + " ")
        elif tag in {"strong", "b"}:
            self._append("**")
        elif tag in {"em", "i"}:
            self._append("*")
        elif tag == "blockquote":
            self._append("\n\n> ")
        elif tag == "ul":
            self.list_stack.append({"type": "ul", "index": 0})
            self._append("\n")
        elif tag == "ol":
            self.list_stack.append({"type": "ol", "index": 0})
            self._append("\n")
        elif tag == "li":
            prefix = "- "
            if self.list_stack and self.list_stack[-1]["type"] == "ol":
                self.list_stack[-1]["index"] += 1
                prefix = f"{self.list_stack[-1]['index']}. "
            indent = "  " * max(len(self.list_stack) - 1, 0)
            self._append("\n" + indent + prefix)
        elif tag == "a":
            href = attr_map.get("href", "").strip()
            self.link_stack.append({"href": href, "text": []})
        elif tag == "img":
            src = attr_map.get("src", "").strip()
            alt = attr_map.get("alt", "").strip()
            if src:
                self._append(f"![{alt}]({src})")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return

        if self.skip_depth:
            return

        if tag == "pre" and self.in_pre:
            code = "".join(self.pre_parts).strip("\n")
            fence = self._code_fence_for(code)
            lang = self.pre_lang.strip()
            self.parts.append(f"{fence}{lang}\n{code}\n{fence}\n\n")
            self.in_pre = False
            self.pre_lang = ""
            self.pre_parts = []
            return

        if self.in_pre:
            return

        if tag == "code" and self.in_inline_code:
            self._append("`")
            self.in_inline_code = False
        elif tag in {"p", "div", "section", "article", "blockquote"}:
            self._append("\n\n")
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._append("\n\n")
        elif tag in {"strong", "b"}:
            self._append("**")
        elif tag in {"em", "i"}:
            self._append("*")
        elif tag in {"ul", "ol"} and self.list_stack:
            self.list_stack.pop()
            self._append("\n")
        elif tag == "a" and self.link_stack:
            link = self.link_stack.pop()
            text = "".join(link["text"]).strip()
            href = link["href"]
            if text and href:
                self._append(f"[{text}]({href})")
            elif text:
                self._append(text)

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return

        if self.in_pre:
            self.pre_parts.append(data)
        else:
            self._append(data)

    def get_markdown(self) -> str:
        return normalize_markdown("".join(self.parts))

    def _append(self, value: str) -> None:
        if self.link_stack:
            self.link_stack[-1]["text"].append(value)
        else:
            self.parts.append(value)

    @staticmethod
    def _language_from_class(class_name: str) -> str:
        for token in class_name.split():
            if token.startswith("language-"):
                return token.removeprefix("language-")
            if token.startswith("lang-"):
                return token.removeprefix("lang-")
        return ""

    @staticmethod
    def _code_fence_for(code: str) -> str:
        longest = max((len(match.group(0)) for match in re.finditer(r"`+", code)), default=0)
        return "`" * max(3, longest + 1)


def main() -> int:
    args = parse_args()
    username = normalize_username(args.username)
    output_dir = Path(args.out_dir)

    if args.method == "graphql":
        posts = fetch_graphql_posts(username, args.max_posts)
    elif args.method == "rss":
        posts = fetch_rss_posts(username, args.max_posts)
    else:
        try:
            posts = fetch_graphql_posts(username, args.max_posts)
            print(f"Fetched {len(posts)} post(s) via GraphQL.")
        except Exception as exc:
            print(f"GraphQL import failed, falling back to RSS: {exc}", file=sys.stderr)
            posts = fetch_rss_posts(username, args.max_posts)
            print(f"Fetched {len(posts)} post(s) via RSS.")

    output_dir.mkdir(parents=True, exist_ok=True)
    existing_urls = load_existing_publish_urls(output_dir)

    created = 0
    skipped = 0
    for post in posts:
        normalized_url = normalize_url(post.publish_url)
        if normalized_url in existing_urls:
            skipped += 1
            print(f"skip duplicate: {post.title} ({post.publish_url})")
            continue

        target = unique_target_path(output_dir, post)
        content = render_markdown_file(post)

        if args.dry_run:
            print(f"dry-run create: {target}")
        else:
            target.write_text(content, encoding="utf-8", newline="\n")
            print(f"created: {target}")

        existing_urls.add(normalized_url)
        created += 1

    print(f"Done. created={created}, skipped={skipped}, output={output_dir}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Velog posts into Obsidian Markdown files.")
    parser.add_argument("--username", default=DEFAULT_USERNAME, help="Velog username without @.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory.")
    parser.add_argument(
        "--method",
        choices=("auto", "graphql", "rss"),
        default="auto",
        help="Import method. auto tries GraphQL first and RSS second.",
    )
    parser.add_argument(
        "--max-posts",
        type=int,
        default=0,
        help="Maximum number of posts to import. 0 means no explicit limit.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing them.")
    return parser.parse_args()


def normalize_username(username: str) -> str:
    return username.strip().removeprefix("@")


def fetch_graphql_posts(username: str, max_posts: int = 0) -> list[VelogPost]:
    """Fetch public posts through Velog's GraphQL endpoint.

    Velog's public GraphQL endpoint is not an officially versioned API, so the
    schema may change. The auto mode falls back to RSS when this fails.
    """

    page_size = 20
    cursor: str | None = None
    summaries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    while True:
        data = graphql_request(
            POSTS_QUERY,
            {
                "username": username,
                "limit": page_size,
                "cursor": cursor,
            },
        )
        page = data.get("posts") or []
        if not isinstance(page, list):
            raise RuntimeError("Unexpected GraphQL posts response.")

        new_items = []
        for item in page:
            item_id = str(item.get("id") or item.get("url_slug") or "")
            if not item_id or item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            new_items.append(item)

        summaries.extend(new_items)

        if max_posts and len(summaries) >= max_posts:
            summaries = summaries[:max_posts]
            break
        if len(page) < page_size or not new_items:
            break

        cursor = str(new_items[-1].get("id") or "")
        if not cursor:
            break

    posts: list[VelogPost] = []
    for summary in summaries:
        slug = str(summary.get("url_slug") or "").strip()
        if not slug:
            continue

        detail = graphql_request(POST_QUERY, {"username": username, "url_slug": slug}).get("post")
        if not detail:
            continue

        title = str(detail.get("title") or summary.get("title") or slug).strip()
        body = str(detail.get("body") or "").strip()
        released_at = str(detail.get("released_at") or summary.get("released_at") or "").strip()
        updated_at = str(detail.get("updated_at") or summary.get("updated_at") or "").strip()
        published_at = normalize_date(released_at or updated_at)
        publish_url = velog_post_url(username, str(detail.get("url_slug") or slug))

        posts.append(
            VelogPost(
                title=title,
                body=body,
                published_at=published_at,
                publish_url=publish_url,
                source="graphql",
            )
        )

    return posts


def graphql_request(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        response_body = response.read().decode("utf-8")

    parsed = json.loads(response_body)
    if parsed.get("errors"):
        messages = "; ".join(str(error.get("message", error)) for error in parsed["errors"])
        raise RuntimeError(messages)
    data = parsed.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("GraphQL response did not include data.")
    return data


def fetch_rss_posts(username: str, max_posts: int = 0) -> list[VelogPost]:
    """Fetch posts from Velog RSS.

    RSS is simple and public, but it can have platform-level limits: it may
    return only recent posts, and the body can be HTML, shortened, or missing.
    For better body fidelity, prefer GraphQL when it is available.
    """

    last_error: Exception | None = None
    for url_template in RSS_URLS:
        url = url_template.format(username=username)
        try:
            xml_text = http_get_text(url)
            posts = parse_rss(xml_text, username)
            if posts:
                return posts[:max_posts] if max_posts else posts
        except Exception as exc:
            last_error = exc

    if last_error:
        raise RuntimeError(f"RSS import failed: {last_error}") from last_error
    return []


def http_get_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{url} returned HTTP {exc.code}") from exc


def parse_rss(xml_text: str, username: str) -> list[VelogPost]:
    root = ET.fromstring(xml_text)
    items = root.findall(".//item")

    posts: list[VelogPost] = []
    for item in items:
        title = child_text(item, "title") or "Untitled"
        link = child_text(item, "link") or ""
        pub_date = child_text(item, "pubDate") or child_text(item, "date") or ""
        body_html = child_text(item, "encoded") or child_text(item, "description") or ""
        body = html_to_markdown(body_html)
        slug = link.rstrip("/").split("/")[-1] if link else slugify_for_url(title)
        publish_url = link or velog_post_url(username, slug)

        posts.append(
            VelogPost(
                title=title.strip(),
                body=body.strip(),
                published_at=normalize_date(pub_date),
                publish_url=publish_url.strip(),
                source="rss",
            )
        )

    return posts


def child_text(parent: ET.Element, local_name: str) -> str:
    for child in parent:
        name = child.tag.rsplit("}", 1)[-1]
        if name == local_name:
            return child.text or ""
    return ""


def html_to_markdown(html: str) -> str:
    if not html.strip():
        return ""

    parser = SimpleHtmlToMarkdown()
    parser.feed(html)
    parser.close()
    return parser.get_markdown()


def normalize_date(value: str) -> str:
    value = value.strip()
    if not value:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        return parsedate_to_datetime(value).date().isoformat()
    except (TypeError, ValueError, IndexError):
        pass

    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date().isoformat()
    except ValueError:
        pass

    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    if match:
        return match.group(0)

    return datetime.now().strftime("%Y-%m-%d")


def render_markdown_file(post: VelogPost) -> str:
    body = post.body.strip()
    title = post.title.strip() or "Untitled"

    if body:
        content = f"# {title}\n\n{body}\n"
    else:
        content = f"# {title}\n\n"

    return (
        "---\n"
        f'title: "{yaml_escape(title)}"\n'
        f'created: "{yaml_escape(post.published_at)}"\n'
        "type: blog\n"
        "status: published\n"
        "tags:\n"
        "  - velog\n"
        f'publish_url: "{yaml_escape(post.publish_url)}"\n'
        "---\n\n"
        f"{content}"
    )


def load_existing_publish_urls(output_dir: Path) -> set[str]:
    urls: set[str] = set()
    if not output_dir.exists():
        return urls

    for path in output_dir.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig", errors="replace")

        frontmatter = extract_frontmatter(text)
        if not frontmatter:
            continue

        match = re.search(r"(?m)^publish_url:\s*(.+?)\s*$", frontmatter)
        if not match:
            continue

        value = match.group(1).strip().strip('"').strip("'")
        if value:
            urls.add(normalize_url(value))

    return urls


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end]


def unique_target_path(output_dir: Path, post: VelogPost) -> Path:
    date_part = post.published_at or datetime.now().strftime("%Y-%m-%d")
    title_part = sanitize_filename(post.title) or "untitled"
    base_name = f"{date_part}_{title_part}"
    target = output_dir / f"{base_name}.md"

    counter = 2
    while target.exists():
        target = output_dir / f"{base_name}-{counter}.md"
        counter += 1

    return target


def sanitize_filename(value: str, max_length: int = 120) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.rstrip(". ")
    if len(value) > max_length:
        value = value[:max_length].rstrip(". ")
    return value


def normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def velog_post_url(username: str, slug: str) -> str:
    return f"https://velog.io/@{username}/{slug}"


def slugify_for_url(value: str) -> str:
    return re.sub(r"\s+", "-", value.strip())


def normalize_markdown(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    result: list[str] = []
    in_fence = False
    blank_count = 0

    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            result.append(line.rstrip())
            blank_count = 0
            continue

        if in_fence:
            result.append(line.rstrip())
            continue

        stripped = line.rstrip()
        if not stripped:
            blank_count += 1
            if blank_count <= 1:
                result.append("")
            continue

        blank_count = 0
        result.append(stripped)

    return "\n".join(result).strip() + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
