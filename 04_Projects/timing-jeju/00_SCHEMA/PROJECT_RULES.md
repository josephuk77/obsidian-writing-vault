# PROJECT_RULES

---
tags:
  - type/project
  - status/planning
---

## 기본 규칙

- 이 프로젝트 폴더는 실제 코드 레포가 아니라 기획 위키/허브입니다.
- Raw Source는 원본 보존용이므로 수정하지 않습니다.
- Notion 원문은 `10_RAW_SOURCE/notion/`에 저장합니다.
- 사용자가 직접 작성한 프로젝트 문서는 `15_MY_DOCUMENTS/`에 저장합니다.
- AI가 작업하며 필요한 가정, 조사 큐, 핸드오프는 `16_AI_CONTEXT/`에 저장합니다.
- 프로젝트 실행에 필요한 핵심 기준 정보는 `20_CORE/`에 저장합니다.
- Codex가 정리한 문서는 `20_WIKI/`에 저장합니다.
- 중요한 결정은 `20_CORE/key-decisions.md`에 요약하고, 정식 기록이 필요하면 `30_DECISIONS/`에 ADR로 저장합니다.
- 중요한 해결사항은 `20_CORE/solved-issues.md`에 요약하고, 상세 기록이 필요하면 `40_ERRORS/`에 저장합니다.
- 결정 사항은 ADR로 `30_DECISIONS/`에 저장합니다.
- 에러 기록은 ERR로 `40_ERRORS/`에 저장합니다.
- 작업 후 [[INDEX]]와 [[LOG]]를 갱신합니다.

## 문서 갱신 규칙

- 새 원문을 추가하면 `10_RAW_SOURCE/_MANIFEST.md`에 기록합니다.
- 새 위키 문서를 추가하면 [[INDEX]]에 링크합니다.
- 확정되지 않은 내용은 [[open-questions]]에 남깁니다.
- 개발 레포가 생기면 [[REPO_LINKS]]를 갱신합니다.

## 에이전트 명령 규칙

- `Save`: 저장 전 [[SAVE_FILTERS]]를 적용합니다.
- `Reference`: 이 프로젝트의 [[INDEX]]와 [[LOG]]를 먼저 읽습니다.
- `Ingest`: 원문은 `10_RAW_SOURCE/`에 보존하고 정리본은 `20_WIKI/`와 `20_CORE/`에 분리합니다.
- `Lint`: [[LINT_RULES]] 기준으로 출처, 결정 근거, 인덱스/로그 누락을 검사합니다.
