# MAINTENANCE_LOG

---
tags:
  - type/project
  - status/active
---

## 2026-06-12

### Task

- 비어 있는 폴더도 Git에 올라갈 수 있도록 `.gitkeep`을 추가했다.

### Changed

- `03_Blog/Drafts/AI-ML/.gitkeep`을 추가했다.

### Evidence

- `.obsidian/`과 `scripts/`는 수정하지 않았다.
- `.git`과 `.obsidian`을 제외하고 비어 있는 폴더를 확인한 뒤 작업했다.

### Next

- 새 빈 폴더를 만들면 `.gitkeep`을 함께 추가한다.

---

### Task

- 영상의 Obsidian 기반 AI 업무 위키 구조와 현재 vault 구조를 비교해 더 나은 혼합 구조로 확장했다.

### Changed

- 전역 AI 작업 공간 `06_AI_Sessions/`를 추가했다.
- `06_AI_Sessions/`에 `conversations/`, `output/`, `raw/`, `wiki/`, `index.md`, `log.md`, `AGENTS.md`를 추가했다.
- 영상의 Raw Source / Wiki / Schema 구조를 이 vault의 프로젝트 허브 구조와 연결하는 [[AI_WIKI_ARCHITECTURE]]를 추가했다.
- 저장 위치 판단용 플레이북 [[ai-session-triage]]를 추가했다.
- 최상위 [[README]], [[VAULT_RULES]], [[WORKFLOW]], `AGENTS.md`, `04_Projects/README.md`를 새 구조에 맞게 갱신했다.

### Evidence

- 기존 `04_Projects/` 구조는 삭제하지 않고 프로젝트별 업무 위키로 유지했다.
- `.obsidian/`과 `scripts/`는 수정하지 않았다.

### Decision

- 영상 구조는 `06_AI_Sessions/` 전역 공간에 적용한다.
- 프로젝트가 명확한 내용은 계속 `04_Projects/{project}/`에 저장한다.
- 프로젝트 실행 기준 정보는 `20_CORE/`, 원문은 `10_RAW_SOURCE/`, 세션 복구는 `00_SCHEMA/INDEX.md`와 `LOG.md`를 기준으로 한다.

### Next

- 프로젝트와 무관하거나 여러 프로젝트에 걸친 AI 대화는 `06_AI_Sessions/conversations/`에 저장한다.
- 전역 원문은 `06_AI_Sessions/raw/`, 정리 지식은 `06_AI_Sessions/wiki/`에 저장한다.

---

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
