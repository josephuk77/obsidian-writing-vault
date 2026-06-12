# MAINTENANCE_LOG

---
tags:
  - type/project
  - status/active
---

## 2026-06-12

### Task

- 프로젝트 폴더 안에 사용자 작성 문서, AI 작업 맥락, 실제 핵심 정보 공간을 분리했다.

### Changed

- `_Project_Template/`, `church-devotion-app/`, `timing-jeju/`에 `15_MY_DOCUMENTS/`, `16_AI_CONTEXT/`, `20_CORE/`를 추가했다.
- `20_CORE/`에 `project-facts.md`, `core-data.md`, `key-decisions.md`, `solved-issues.md`, `current-plan.md`를 추가했다.
- `16_AI_CONTEXT/`에 `ai-brief.md`, `assumptions.md`, `research-queue.md`, `handoff.md`를 추가했다.
- 프로젝트 `INDEX.md`, [[WORKFLOW]], [[VAULT_RULES]], [[NOTION_SYNC_GUIDE]], `AGENTS.md`를 새 분류에 맞게 갱신했다.

### Evidence

- 기존 `20_WIKI/`, `30_DECISIONS/`, `40_ERRORS/`는 삭제하지 않고 역할을 상세 문서/정식 기록으로 유지했다.
- `.obsidian/`과 `scripts/`는 수정하지 않았다.

### Next

- 사용자가 직접 쓴 프로젝트 문서는 `15_MY_DOCUMENTS/`에 넣는다.
- AI 작업 가정과 핸드오프는 `16_AI_CONTEXT/`에 넣는다.
- 실제 프로젝트 진행 기준은 `20_CORE/`에 요약한다.

---

### Task

- vault를 개인 지식, 프로젝트 기획 허브, 향후 개발 레포 wiki 연결 구조로 정리했다.

### Changed

- `04_Projects/`에 프로젝트 인덱스, 대시보드, Notion sync guide를 추가했다.
- `_Project_Template/`, `church-devotion-app/`, `timing-jeju/`에 공통 프로젝트 구조를 생성했다.
- `99_System/`에 vault 운영 규칙, 네이밍 규칙, 태그 규칙, 워크플로, 유지보수 로그를 추가했다.
- `90_Templates/`에 공통 Markdown 템플릿을 추가했다.
- 최상위 `README.md`와 `AGENTS.md`를 보강했다.
- Git에서 빈 하위 폴더가 유지되도록 새 빈 폴더에 `.gitkeep`을 추가했다.

### Evidence

- `.obsidian/`은 수정하지 않았다.
- `scripts/`는 수정하지 않았다.
- 기존 파일과 폴더는 삭제하지 않았다.

### Next

- Notion 기획 원문을 각 프로젝트의 `10_RAW_SOURCE/notion/`에 추가한다.
- Codex로 `20_WIKI/` 문서를 프로젝트 실제 내용에 맞게 채운다.
- 실제 개발 레포가 생성되면 `REPO_LINKS.md`를 갱신한다.
