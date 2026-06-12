# SAVE_FILTERS

---
tags:
  - type/project
  - status/active
---

AI 에이전트가 `Save`를 수행하기 전 반드시 통과해야 하는 저장 필터입니다. 목적은 맥락 오염을 막는 것입니다.

## 저장 5필터

아래 질문 중 하나 이상에 `예`라고 답할 수 있을 때만 Wiki 또는 Core에 승격합니다.

| 질문 | 저장 위치 힌트 |
| --- | --- |
| 반복해서 재사용 가능한 데이터인가? | `wiki/`, `20_WIKI/`, `20_CORE/` |
| 다른 에이전트나 동료가 이어받기 위해 반드시 읽어야 하는가? | `index.md`, `log.md`, `20_CORE/` |
| 의사결정의 근거와 결정자를 나중에 추적해야 하는가? | `wiki/decisions/`, `30_DECISIONS/`, `key-decisions.md` |
| 실패한 방식이라 다시 시도하면 안 되는 리스크 정보인가? | `wiki/errors/`, `40_ERRORS/`, `solved-issues.md` |
| 팀 전체를 맞춰야 하는 공통 규칙이나 가이드인가? | `99_System/`, `wiki/playbooks/`, `PROJECT_RULES.md` |

## 저장하지 말아야 할 것

- 1회성 중간 답변
- 검증되지 않은 초안
- 출처 없는 추측
- 사용자가 확정하지 않은 결정
- 이미 더 정확한 문서가 있는 중복 내용

## Raw에는 저장해도 되는 것

Wiki나 Core로 승격하지 않더라도 근거 보존이 필요한 것은 Raw Source에 저장할 수 있습니다.

- 회의록 원문
- 대화 로그
- Notion 원문
- 외부 분석 원문
- 스크린샷
- 에러 로그 원문

## 승격 규칙

- Raw Source: 원본 보존
- Wiki: 정리된 재사용 지식
- Core: 프로젝트 실행 기준
- Decisions: 결정과 근거
- Errors: 실패와 해결
- Output: 산출물

## Save 결과 기록

저장 후 반드시 다음을 갱신합니다.

- 전역 작업: `06_AI_Sessions/index.md`, `06_AI_Sessions/log.md`
- 프로젝트 작업: `04_Projects/{project}/00_SCHEMA/INDEX.md`, `LOG.md`
- Raw Source 추가: `_MANIFEST.md`
