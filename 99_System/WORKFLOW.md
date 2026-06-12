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
3. Codex에게 원문을 바탕으로 `20_WIKI/` 상세 문서를 갱신하게 한다.
4. 실제 진행에 필요한 확정 정보는 `20_CORE/`에 요약한다.
5. 새 결정이 생기면 `20_CORE/key-decisions.md`에 먼저 요약하고, 정식 기록이 필요하면 `30_DECISIONS/`에 ADR로 남긴다.
6. 해결한 중요한 문제는 `20_CORE/solved-issues.md`에 요약하고, 상세 기록이 필요하면 `40_ERRORS/`에 남긴다.
7. 막힌 점은 `20_WIKI/open-questions.md`, `16_AI_CONTEXT/research-queue.md`, `PROJECT_DASHBOARD.md`에 반영한다.

## 프로젝트 문서 분리

- 사용자가 직접 작성한 문서와 초안은 `15_MY_DOCUMENTS/`에 둔다.
- AI가 작업하며 필요한 가정, 추론, 조사 큐, 핸드오프는 `16_AI_CONTEXT/`에 둔다.
- 프로젝트 실행 기준으로 먼저 봐야 하는 핵심 정보는 `20_CORE/`에 둔다.
- 긴 설명, 배경, 정리형 문서는 `20_WIKI/`에 둔다.

## 전역 AI 업무 정리

1. 프로젝트가 명확하지 않은 AI 대화는 `06_AI_Sessions/conversations/`에 저장한다.
2. 프로젝트를 넘나드는 원문은 `06_AI_Sessions/raw/`에 저장한다.
3. 원문을 정리한 지식은 `06_AI_Sessions/wiki/`에 저장한다.
4. 재사용 가능한 프롬프트, 리포트, 스펙은 `06_AI_Sessions/output/`에 저장한다.
5. 의미 있는 작업 후 `06_AI_Sessions/log.md`와 `06_AI_Sessions/index.md`를 갱신한다.
6. 프로젝트 전용으로 정리할 내용이 생기면 해당 프로젝트의 `20_CORE/` 또는 `20_WIKI/`에 연결한다.

## 자연어 명령 운영

- `Save`: [[SAVE_FILTERS]]를 통과한 내용만 저장한다.
- `Reference`: [[REFERENCE_RESTORE]] 순서로 맥락을 복원한다.
- `Ingest`: 원문은 Raw에 보존하고 정리본은 Wiki/Core에 분리한다.
- `Lint`: [[LINT_RULES]] 기준으로 맥락 오염을 검사한다.

## 프로젝트 갱신

- 전체 목록은 [[PROJECT_INDEX]]에서 관리한다.
- 전체 현황은 [[PROJECT_DASHBOARD]]에서 관리한다.
- 프로젝트별 맥락은 각 프로젝트의 `00_SCHEMA/INDEX.md`와 `00_SCHEMA/LOG.md`를 기준으로 복구한다.

## 개발 레포 생성 이후

1. 프로젝트의 `00_SCHEMA/REPO_LINKS.md`에 repo 정보를 채운다.
2. vault의 `20_CORE/`에는 프로젝트 핵심 기준 정보를 유지한다.
3. repo wiki에는 구현, 운영, 배포, API 문서를 연결한다.
