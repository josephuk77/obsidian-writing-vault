# 20_CORE

---
tags:
  - type/project
  - status/planning
---

프로젝트를 실제로 진행하는 데 필요한 핵심 정보의 현재판을 보관하는 공간입니다.

## 역할

- 프로젝트 핵심 사실
- 실제 필요한 데이터와 정보
- 중요한 해결사항
- 중요한 결정사항
- 다음 행동 기준

## 핵심 문서

- [[project-facts]]
- [[core-data]]
- [[key-decisions]]
- [[solved-issues]]
- [[current-plan]]

## 다른 폴더와의 차이

| 폴더 | 목적 |
| --- | --- |
| `10_RAW_SOURCE/` | 원문 보존 |
| `15_MY_DOCUMENTS/` | 사용자가 직접 작성한 문서 보관 |
| `16_AI_CONTEXT/` | AI가 작업하며 필요한 맥락과 가정 |
| `20_CORE/` | 프로젝트 실행에 필요한 핵심 정보의 현재판 |
| `20_WIKI/` | 설명형 위키와 상세 정리 |
| `30_DECISIONS/` | 정식 ADR 기록 |
| `40_ERRORS/` | 상세 에러 기록 |

## 규칙

- 이 폴더의 내용은 프로젝트를 실제로 진행할 때 먼저 확인하는 기준 정보입니다.
- 확정된 내용만 작성하고, 불확실한 내용은 [[open-questions]]나 [[assumptions]]로 보냅니다.
- 중요한 결정은 [[key-decisions]]에 요약하고, 필요하면 `30_DECISIONS/`에 ADR을 만듭니다.
- 중요한 해결사항은 [[solved-issues]]에 요약하고, 필요하면 `40_ERRORS/`에 상세 기록을 둡니다.
