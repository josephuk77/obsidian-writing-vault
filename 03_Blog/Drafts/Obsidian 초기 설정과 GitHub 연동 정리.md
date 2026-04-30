---
title: "Obsidian 초기 설정과 GitHub 연동 정리"
created: "2026-04-30"
updated: "2026-04-30"
type: blog
status: draft
tags: [Obsidian, Markdown, GitHub, Git, Codex]
source_notes:
  - "[[obsidian-setup-raw]]"
publish_url:
---

# Obsidian 초기 설정과 GitHub 연동 정리

## 글을 쓰는 이유

개발 공부를 하다 보면 기록해야 할 내용이 생각보다 금방 늘어난다.

처음에는 에러 해결 기록, TIL, 코딩테스트 풀이, 프로젝트 문서, 블로그 초안이 여기저기 흩어져 있었다. 그때마다 "이 내용을 어디에 적어뒀지?" 하고 다시 찾는 시간이 생겼다.

그래서 이번에는 Obsidian을 단순한 메모 앱으로 쓰기보다, 개발 공부 기록을 계속 쌓아가는 공간으로 만들어보기로 했다. Vault를 만들고, 폴더 구조를 잡고, 템플릿을 연결하고, GitHub까지 연동하면서 배운 내용을 정리해보려고 한다.

## 먼저 결론부터

이번에 설정한 흐름은 간단히 말하면 이렇다.

- Obsidian Vault를 만든다.
- 공부 기록 성격에 맞게 폴더를 나눈다.
- Templates 플러그인으로 반복해서 쓸 글 형식을 만든다.
- Git 플러그인과 GitHub repository를 연결한다.
- GitHub에 올리면 안 되는 파일은 `.gitignore`로 제외한다.
- Codex를 이용해 원본 메모를 Velog 글 초안으로 다듬는다.

처음부터 완벽한 시스템을 만들려고 한 것은 아니다. 일단 내가 매일 공부하면서 바로 쓸 수 있는 구조를 만드는 것이 목표였다.

## Obsidian을 쓰기로 한 이유

Obsidian은 Markdown 기반이라 개발 공부 기록과 잘 맞는다고 느꼈다.

코드 블록을 넣기도 쉽고, 제목 구조를 잡기도 편하고, 나중에 Velog 글로 옮길 때도 Markdown 형태를 그대로 활용할 수 있다. 특히 공부 기록은 한 번 쓰고 끝나는 글보다, 나중에 다시 찾아보고 연결하는 일이 많다.

예를 들어 Spring 에러를 해결한 기록이 나중에 프로젝트 문서나 블로그 글의 재료가 될 수 있다. 코딩테스트 풀이도 처음에는 단순 풀이지만, 나중에는 내 접근 방식과 다른 풀이를 비교하는 글이 될 수 있다.

그래서 Obsidian을 단순 메모장이 아니라, 공부 기록을 모으고 재가공하는 공간으로 생각하고 설정했다.

## Vault와 폴더 구조 잡기

먼저 Vault 위치를 정했다.

Vault 위치는 `C:\Users\사용자\Documents\Obsidian Vault`로 잡았다.

그리고 기록의 성격에 따라 폴더를 나눴다.

```text
00_Inbox
01_Daily
02_Study
03_Blog
04_Projects
05_CodingTest
06_Resources
90_Templates
99_System
```

각 폴더는 이런 용도로 생각했다.

- `00_Inbox`: 아직 정리하지 않은 메모나 빠르게 적어둔 아이디어
- `01_Daily`: 하루 공부 기록, TIL, 회고
- `02_Study`: React, Spring, Database, Security 같은 개념 정리
- `03_Blog`: Velog 글 아이디어, 초안, 수정본
- `04_Projects`: 프로젝트 문서, 기능 명세, 포트폴리오 정리
- `05_CodingTest`: 코딩테스트 문제 풀이와 비교 정리
- `06_Resources`: 참고 자료, 링크, 이미지, PDF
- `90_Templates`: 반복해서 쓸 Obsidian 템플릿
- `99_System`: 대시보드, 인덱스, 관리용 문서

처음에는 폴더를 너무 많이 나누는 것이 아닌가 싶었는데, 기록 종류가 명확하게 다르기 때문에 오히려 나중에 찾기 쉬울 것 같았다.

## 처음 헷갈렸던 Obsidian 개념

Obsidian을 처음 설정하면서 가장 먼저 헷갈린 것은 편집 모드와 읽기 모드였다.

Markdown 파일을 작성하는 것은 익숙했지만, Obsidian에서는 같은 문서도 편집할 때와 읽을 때 보이는 방식이 조금 다르다. 처음에는 "왜 방금 쓴 문법이 다르게 보이지?"라는 생각이 들었다.

또 하나 헷갈렸던 것은 대시보드였다.

처음에는 대시보드가 실제 파일을 옮겨 담는 공간인 줄 알았다. 그런데 써보니 대시보드는 파일을 저장하는 곳이라기보다, 자주 보는 문서 링크나 todo, 요약 정보를 모아두는 화면에 가깝다.

그래서 실제 노트는 각 폴더에 두고, `99_System`에는 인덱스나 대시보드 역할을 하는 문서를 두는 식으로 생각을 바꿨다.

## Templates 플러그인 설정하기

반복해서 쓰는 글 형식은 매번 새로 만들기보다 템플릿으로 관리하는 것이 좋다고 생각했다.

그래서 Obsidian의 기본 Templates 플러그인을 켰고, 템플릿 폴더를 `90_Templates`로 설정했다.

설정 흐름은 대략 이렇다.

- Obsidian 설정에서 Core plugins로 이동한다.
- Templates 플러그인을 켠다.
- Template folder location을 `90_Templates`로 지정한다.
- 자주 쓸 글 형식을 템플릿 파일로 만든다.

이번에는 `Blog Draft` 템플릿을 기준으로 블로그 초안을 작성할 수 있게 했다. 글을 쓸 때마다 frontmatter, 제목, 글을 쓰는 이유, 결론, 헷갈렸던 부분, 정리 같은 구조를 반복해서 만들 수 있어서 편했다.

## Templates와 Templater 차이

설정하면서 헷갈렸던 것 중 하나가 Templates와 Templater의 차이였다.

이름이 비슷해서 같은 기능처럼 보였지만, 기본 Templates는 Obsidian에 포함된 간단한 템플릿 기능이고, Templater는 더 복잡한 자동화가 가능한 별도 플러그인에 가깝다.

처음부터 복잡한 자동화가 필요한 상황은 아니었다. 지금은 글의 기본 구조를 빠르게 불러오는 정도면 충분했기 때문에 기본 Templates 플러그인만 사용했다.

나중에 날짜, 파일명, 동적 값 등을 더 세밀하게 다뤄야 한다면 Templater를 추가로 봐도 될 것 같다.

## GitHub와 Obsidian Vault 연결하기

Obsidian에 기록한 내용을 로컬에만 두면 백업이 불안하다. 그리고 공부 기록이 쌓이면 GitHub에 커밋 로그로 남기는 것도 의미가 있다고 생각했다.

그래서 Git 플러그인을 설치하고 GitHub repository를 만들어 Vault와 연결했다.

터미널에서 직접 연결한다면 흐름은 대략 아래와 비슷하다.

```powershell
git init
git add .
git commit -m "Initial Obsidian vault setup"
git branch -M main
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

macOS나 Linux 환경이라면 같은 흐름을 bash에서 실행할 수 있다.

```bash
git init
git add .
git commit -m "Initial Obsidian vault setup"
git branch -M main
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

Obsidian Git 플러그인을 쓰면 앱 안에서 commit, push, pull을 할 수 있어서 편하다. 다만 처음 repository를 연결하거나 문제가 생겼을 때는 터미널 명령어를 알고 있는 편이 더 안전하다고 느꼈다.

## Troubleshooting: GitHub push protection 오류

GitHub에 push하는 과정에서 `.obsidian/plugins` 때문에 push protection 오류가 발생했다.

처음에는 단순히 Obsidian 설정 파일도 같이 올리면 되는 줄 알았다. 그런데 플러그인 폴더 안에는 외부 플러그인의 코드나 설정이 들어갈 수 있고, 경우에 따라 GitHub에서 위험한 파일로 판단할 수 있다.

그래서 `.gitignore`에 아래 내용을 추가했다.

```gitignore
.obsidian/plugins/
```

이미 Git이 추적하고 있던 상태라면 캐시에서 제거하는 과정도 필요할 수 있다.

```powershell
git rm -r --cached .obsidian/plugins
git add .gitignore
git commit -m "Ignore Obsidian plugins"
git push
```

bash에서는 같은 명령을 아래처럼 실행할 수 있다.

```bash
git rm -r --cached .obsidian/plugins
git add .gitignore
git commit -m "Ignore Obsidian plugins"
git push
```

이번 일을 겪으면서 Obsidian Vault 전체를 무조건 GitHub에 올리는 것보다, 어떤 파일을 버전 관리할지 먼저 정하는 것이 중요하다는 것을 배웠다.

내가 직접 작성한 Markdown 문서와 템플릿은 관리 대상이지만, 플러그인 내부 파일이나 불필요한 캐시성 파일은 제외하는 편이 낫다.

## Notion export Markdown이 깨질 수 있는 이유

Notion에서 export한 Markdown을 Obsidian으로 가져올 때도 주의할 점이 있었다.

Markdown 파일이라고 해서 항상 깔끔한 순수 Markdown만 들어 있는 것은 아니었다. Notion에서 내보낸 파일에는 `aside` 같은 HTML 태그가 섞여 있을 수 있다.

이런 태그가 Obsidian이나 Velog에서 기대한 방식으로 렌더링되지 않으면 글 모양이 깨지거나, 불필요한 태그가 그대로 보일 수 있다.

그래서 Notion에서 가져온 글은 바로 발행하기보다 한 번 정리하는 과정이 필요하다.

- 불필요한 HTML 태그가 있는지 확인한다.
- 제목 구조가 자연스러운지 본다.
- 코드 블록 언어가 제대로 지정되어 있는지 확인한다.
- Obsidian 링크와 Velog용 Markdown 문법이 섞이지 않았는지 확인한다.

특히 Velog에 올릴 글이라면 Obsidian 내부 링크나 Notion export 흔적을 그대로 두지 않는 것이 좋다.

## AGENTS.md로 글 작성 규칙 정리하기

이번 Vault에는 `AGENTS.md`도 만들었다.

이 파일에는 Obsidian Vault에서 글을 작성할 때 지켜야 할 규칙을 정리했다. 예를 들어 한국어로 작성하기, YAML frontmatter 보존하기, 출처를 지어내지 않기, Velog 스타일은 너무 딱딱하지 않게 쓰기 같은 규칙이다.

처음에는 이런 규칙까지 파일로 남겨야 하나 싶었지만, Codex 같은 도구를 같이 사용할 때는 기준이 있는 편이 훨씬 좋다.

내가 어떤 톤으로 글을 쓰고 싶은지, 어떤 폴더에 어떤 글을 만들어야 하는지, 어떤 내용은 조심해야 하는지를 미리 정해두면 글을 다듬을 때 방향이 덜 흔들린다.

## Codex로 글을 다듬는 흐름

마지막으로 이번 글도 Codex를 이용해 초안을 잡는 방식으로 작성했다.

흐름은 이렇다.

- `00_Inbox`에 내가 직접 설정하면서 적은 원본 메모를 둔다.
- Codex에게 원본 메모를 읽고 Velog 글 목차를 먼저 만들게 한다.
- 목차가 괜찮으면 `Blog Draft` 템플릿 형식에 맞춰 초안을 작성하게 한다.
- 초안에서 어색한 표현, 반복되는 내용, 부족한 설명을 다시 다듬는다.
- 최종 글은 내가 직접 읽고 경험과 다르게 보이는 부분이 없는지 확인한다.

중요한 것은 Codex가 글을 대신 지어내게 하는 것이 아니라, 내가 직접 설정하면서 남긴 메모를 바탕으로 글의 구조와 문장을 정리하게 하는 것이다.

특히 에러 해결 기록이나 설정 글은 실제로 겪은 흐름이 중요하다. 그래서 GitHub push protection 오류처럼 내가 겪은 문제는 Troubleshooting 형태로 남기고, 외부 문서나 통계 같은 것은 함부로 추가하지 않는 식으로 정리했다.

## 정리

이번에 Obsidian을 설정하면서 단순히 메모 앱 하나를 설치한 것이 아니라, 앞으로 공부 기록을 어떻게 쌓을지에 대한 기본 구조를 만든 느낌이었다.

폴더 구조를 잡고, 템플릿을 만들고, GitHub와 연결하고, `.gitignore`까지 정리하면서 기록도 하나의 작은 프로젝트처럼 관리해야 한다는 생각이 들었다.

아직 처음 만든 구조라서 쓰다 보면 계속 바뀔 것 같다. 그래도 일단 지금은 `00_Inbox`에 빠르게 적고, 필요한 글은 `03_Blog/Drafts`에서 초안으로 다듬고, 프로젝트나 코딩테스트 기록은 각 폴더에 쌓아가는 방식으로 시작해보려고 한다.

이 글도 그 첫 번째 정리다. 앞으로 Obsidian을 쓰면서 불편한 점이 생기면 구조를 조금씩 고쳐가면서, 공부 기록을 블로그 글과 포트폴리오 자료로 이어갈 수 있게 만들어보고 싶다.
