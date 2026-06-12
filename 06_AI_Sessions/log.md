# log

---
tags:
  - type/project
  - status/active
---

AI 업무 작업 타임라인입니다. 세션이 끊겨도 이 문서와 [[index]]를 읽으면 최근 맥락을 복구할 수 있게 작성합니다.

## 2026-06-12

### Task

- 영상의 AI 업무 위키 구조를 vault에 맞게 적용

### Changed

- `06_AI_Sessions/` 전역 AI 작업 공간을 생성했다.
- `raw/`, `wiki/`, `conversations/`, `output/` 구조를 추가했다.
- 전역 `index.md`, `log.md`, `AGENTS.md`를 추가했다.

### Evidence

- Raw Source와 Wiki를 분리했다.
- 프로젝트 전용 문서는 계속 `04_Projects/{project}/`를 기준으로 관리한다.

### Decisions

- 영상 구조는 전역 AI 작업장으로 적용한다.
- 기존 프로젝트 허브 구조는 삭제하지 않고 프로젝트별 업무 위키로 유지한다.

### Errors

- 없음

### Next

- AI와 나눈 중요한 대화는 `conversations/`에 저장한다.
- 프로젝트를 넘는 공통 개념과 플레이북은 `wiki/`에 정리한다.
