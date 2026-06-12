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
- Codex가 정리한 문서는 `20_WIKI/`에 저장합니다.
- 결정 사항은 ADR로 `30_DECISIONS/`에 저장합니다.
- 에러 기록은 ERR로 `40_ERRORS/`에 저장합니다.
- 작업 후 [[INDEX]]와 [[LOG]]를 갱신합니다.

## 문서 갱신 규칙

- 새 원문을 추가하면 `10_RAW_SOURCE/_MANIFEST.md`에 기록합니다.
- 새 위키 문서를 추가하면 [[INDEX]]에 링크합니다.
- 확정되지 않은 내용은 [[open-questions]]에 남깁니다.
- 개발 레포가 생기면 [[REPO_LINKS]]를 갱신합니다.
