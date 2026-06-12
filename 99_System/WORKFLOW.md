# WORKFLOW

---
tags:
  - type/project
  - status/active
---

## 일상 캡처

1. 떠오른 아이디어나 임시 메모는 `00_Inbox/`에 작성한다.
2. 하루 작업은 `01_Daily/`에 남긴다.
3. 프로젝트 작업이면 해당 프로젝트 `00_SCHEMA/LOG.md`에도 요약한다.

## Notion 기획 정리

1. Notion 원문을 프로젝트의 `10_RAW_SOURCE/notion/`에 저장한다.
2. 원문 파일에는 [[raw-source]] 템플릿을 사용한다.
3. Codex에게 원문을 바탕으로 `20_WIKI/` 문서를 갱신하게 한다.
4. 새 결정이 생기면 `30_DECISIONS/`에 ADR로 남긴다.
5. 막힌 점은 `20_WIKI/open-questions.md`와 `PROJECT_DASHBOARD.md`에 반영한다.

## 프로젝트 갱신

- 전체 목록은 [[PROJECT_INDEX]]에서 관리한다.
- 전체 현황은 [[PROJECT_DASHBOARD]]에서 관리한다.
- 프로젝트별 맥락은 각 프로젝트의 `00_SCHEMA/INDEX.md`와 `00_SCHEMA/LOG.md`를 기준으로 복구한다.

## 개발 레포 생성 이후

1. 프로젝트의 `00_SCHEMA/REPO_LINKS.md`에 repo 정보를 채운다.
2. vault 위키에는 기획 맥락과 의사결정을 유지한다.
3. repo wiki에는 구현, 운영, 배포, API 문서를 연결한다.
