# LOG

---
tags:
  - type/project
  - status/planning
---

프로젝트 작업 기록입니다. 세션이 끊겨도 이 문서와 [[INDEX]]를 읽으면 맥락을 복구할 수 있게 작성합니다.

## 2026-06-12

### Task

- 프로젝트 내부 문서 공간을 사용자 문서, AI 맥락, 핵심 정보로 분리

### Changed

- `15_MY_DOCUMENTS/`를 추가했다.
- `16_AI_CONTEXT/`를 추가했다.
- `20_CORE/`를 추가했다.
- [[INDEX]]와 [[PROJECT_RULES]]를 새 구조에 맞게 갱신했다.

### Evidence

- 기존 `20_WIKI/`, `30_DECISIONS/`, `40_ERRORS/`는 유지했다.

### Decisions

- 사용자가 직접 쓴 프로젝트 문서는 `15_MY_DOCUMENTS/`에 둔다.
- AI 작업 가정과 조사 큐는 `16_AI_CONTEXT/`에 둔다.
- 실제 진행 기준 정보는 `20_CORE/`에 둔다.

### Errors

- 없음

### Next

- Notion 원문 수집 후 [[project-facts]], [[core-data]], [[current-plan]]을 갱신한다.

## 2026-06-12

### Task

- 프로젝트 기획 허브 초기 구조 생성

### Changed

- `_Project_Template` 기준으로 프로젝트 폴더 구조와 기본 문서를 생성했다.

### Evidence

- 아직 실제 개발 레포는 연결하지 않았다.
- Notion 원문은 아직 추가하지 않았다.

### Decisions

- Raw Source는 `10_RAW_SOURCE/notion/`에 원문 그대로 보존한다.
- Codex 정리본은 `20_WIKI/`에 저장한다.

### Errors

- 없음

### Next

- Notion 기획 원문을 `10_RAW_SOURCE/notion/`에 추가한다.
- [[project-brief]], [[requirements]], [[roadmap]], [[open-questions]]를 실제 기획 내용으로 갱신한다.
