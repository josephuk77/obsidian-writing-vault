# AGENTS.md

## Repository purpose

This repository is an Obsidian vault for Korean developer notes, study logs, troubleshooting records, coding test solutions, project documentation, and blog drafts.

이 저장소는 개발 공부 기록, 에러 해결 기록, 코딩테스트 풀이, 프로젝트 문서, 벨로그 글 초안을 관리하는 Obsidian Vault입니다.

## Important folders

- `00_Inbox/`: temporary ideas, quick notes, and uncategorized notes
- `01_Daily/`: daily study logs, TIL, weekly assignments, and retrospectives
- `02_Study/`: study notes for React, Next.js, Spring, Database, Security, AI, Git, and other technical concepts
- `03_Blog/`: blog ideas, drafts, revisions, and published writing
- `04_Projects/`: project documentation, architecture notes, feature specs, and portfolio material
- `05_CodingTest/`: coding test solutions, problem summaries, personal code, lecture code, and comparison notes
- `06_Resources/`: source notes, references, links, images, PDFs, and quoted material
- `90_Templates/`: Obsidian templates
- `99_System/`: indexes, dashboards, writing boards, study boards, and review logs

## Writing rules

- Write in Korean unless the target file explicitly says otherwise.
- Preserve YAML frontmatter.
- Do not edit `.obsidian/` unless explicitly asked.
- Do not edit files inside `90_Templates/` unless the task is about templates.
- Do not invent citations, sources, quotes, statistics, book/page references, official documentation, or external links.
- If a draft uses source notes, cite them as Obsidian links like `[[Source Title]]`.
- Prefer clear structure, short paragraphs, and concrete examples.
- Keep the author's voice. Improve clarity without making the prose sound too generic or overly polished.
- Do not add emojis unless explicitly asked.
- Do not add numbers in front of section titles unless explicitly asked.
- For Velog-style writing, write in a natural first-person Korean study-log tone.
- For Notion/TIL-style writing, use the structure: 학습 내용, 해결한 에러, 나의 한 줄 평.

## Coding test writing rules

- Use Java as the default language unless another language is specified.
- Include the user's code, corrected code, and lecture/alternative code when available.
- Clearly compare the user's approach and the lecture/alternative approach.
- Explain why an error occurred before showing the fixed code.
- Include time complexity and space complexity when possible.

## Project documentation rules

- When documenting a project, include:
  - project overview
  - reason for building it
  - core features
  - tech stack
  - user's role
  - technical decisions
  - troubleshooting
  - portfolio-ready summary
- Prefer practical explanations that can be reused in a portfolio or interview.

## Workflow

- For major rewrites, propose an outline first.
- For edits, summarize changed files and the reason for each change.
- When creating a new blog draft, place it under `03_Blog/Drafts/` unless instructed otherwise.
- When creating a new study note, place it under the appropriate subfolder of `02_Study/`.
- When creating a coding test note, place it under the appropriate platform folder inside `05_CodingTest/`.
- Before finishing, check for:
  - unsupported claims
  - repeated ideas
  - weak title
  - unclear opening
  - abrupt ending
  - missing code explanation
  - missing troubleshooting explanation

## Vault hub rules

- Treat this vault as a personal knowledge base, project planning hub, and future bridge to development repository wikis.
- Do not delete existing files or folders unless the user explicitly asks.
- Do not modify `.obsidian/` unless the user explicitly asks.
- Do not delete or change existing files in `scripts/` unless the user explicitly asks.
- Preserve existing file contents when updating documents; append or add clearly named sections when possible.
- Keep `.DS_Store` ignored by git.

## Project hub rules

- `04_Projects/` is the hub for projects that are currently being planned.
- Project folders are not code repositories unless `00_SCHEMA/REPO_LINKS.md` says otherwise.
- New project folders must use kebab-case and follow `04_Projects/_Project_Template/`.
- Every project must have:
  - `00_SCHEMA/INDEX.md`
  - `00_SCHEMA/LOG.md`
  - `00_SCHEMA/PROJECT_RULES.md`
  - `00_SCHEMA/REPO_LINKS.md`
  - `10_RAW_SOURCE/_MANIFEST.md`
  - `20_WIKI/project-brief.md`
  - `20_WIKI/requirements.md`
  - `20_WIKI/roadmap.md`
  - `20_WIKI/open-questions.md`
- After changing a project, update that project's `00_SCHEMA/INDEX.md` if new core documents were added.
- After changing a project, update that project's `00_SCHEMA/LOG.md` with Task, Changed, Evidence, Decisions, Errors, and Next.
- Keep the global project list in `04_Projects/PROJECT_INDEX.md`.
- Keep the global status view in `04_Projects/PROJECT_DASHBOARD.md`.

## Raw Source and Notion rules

- Raw Source is for original source preservation and must not be rewritten.
- Notion planning originals go in `04_Projects/{project}/10_RAW_SOURCE/notion/`.
- Conversations go in `04_Projects/{project}/10_RAW_SOURCE/conversations/`.
- Meeting notes go in `04_Projects/{project}/10_RAW_SOURCE/meetings/`.
- References go in `04_Projects/{project}/10_RAW_SOURCE/references/`.
- Codex summaries, interpretations, and structured planning documents go in `04_Projects/{project}/20_WIKI/`.
- When processing Notion content, keep the original raw file unchanged and create or update wiki documents separately.
- If a claim cannot be verified from the Raw Source, mark it as an open question instead of presenting it as fact.

## Repo link rules

- Leave repo fields blank while no development repo exists.
- When a repo is created, update `00_SCHEMA/REPO_LINKS.md` with:
  - Notion planning link
  - GitHub repo link
  - local repo path
  - repo wiki path
  - deploy URL
  - API docs URL
  - other reference links
- Keep planning context in this vault and implementation-specific documentation in the repo or repo wiki.

## File, tag, and link rules

- Top-level folders should keep the current `number_English` style.
- Project folders must use kebab-case.
- ADR files must use `ADR-0001-title.md`.
- Error files must use `ERR-0001-title.md`.
- Date files must use `YYYY-MM-DD-title.md`.
- Write tags in YAML frontmatter.
- Use the approved tags from `99_System/TAG_RULES.md`.
- Prefer Obsidian internal links like `[[document-name]]` when linking between notes.
- Add new core documents to the relevant `INDEX.md`.

## Maintenance rules

- When changing vault structure, update `99_System/MAINTENANCE_LOG.md`.
- When adding or changing templates, update `90_Templates/README.md`.
- When adding a project, update `04_Projects/PROJECT_INDEX.md` and `04_Projects/PROJECT_DASHBOARD.md`.
