# ai-session-triage

---
tags:
  - type/project
  - status/active
---

AI 업무 기록을 어디에 넣을지 결정하는 플레이북입니다.

## 저장 위치 결정

| 질문 | Yes | No |
| --- | --- | --- |
| 특정 프로젝트에만 관련된 내용인가? | `04_Projects/{project}/` | `06_AI_Sessions/` |
| 원문 보존이 필요한가? | `raw/` 또는 `10_RAW_SOURCE/` | Wiki/Core로 정리 |
| AI의 가정이나 작업 맥락인가? | `16_AI_CONTEXT/` 또는 `06_AI_Sessions/wiki/synthesis/` | 다음 질문 |
| 실제 프로젝트 진행 기준인가? | `20_CORE/` | `20_WIKI/` |
| 여러 프로젝트에서 재사용 가능한 절차인가? | `06_AI_Sessions/wiki/playbooks/` | 관련 프로젝트 문서 |

## 기본 규칙

- 원문은 수정하지 않습니다.
- 정리본은 원문과 분리합니다.
- 프로젝트 실행 기준은 `20_CORE/`에 둡니다.
- 세션 복구 정보는 `log.md` 또는 프로젝트별 `00_SCHEMA/LOG.md`에 남깁니다.
