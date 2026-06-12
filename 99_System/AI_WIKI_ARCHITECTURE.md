# AI_WIKI_ARCHITECTURE

---
tags:
  - type/project
  - status/active
---

이 vault의 AI 업무 위키 구조는 영상의 3-layer 구조를 프로젝트 허브에 맞게 확장한 형태입니다.

## 영상 구조와 현재 구조 비교

| 영상 구조 | 이 vault 적용 | 역할 |
| --- | --- | --- |
| Raw Source | `06_AI_Sessions/raw/`, `04_Projects/{project}/10_RAW_SOURCE/` | 수정하지 않는 원본 |
| Wiki | `06_AI_Sessions/wiki/`, `04_Projects/{project}/20_WIKI/` | AI가 정리하는 지식 공간 |
| Schema | `06_AI_Sessions/index.md`, `log.md`, `AGENTS.md`, `04_Projects/{project}/00_SCHEMA/`, `99_System/` | 운영 규칙과 지도 |

## 더 좋은 적용 방식

영상 구조를 그대로 최상위에만 두면 프로젝트별 맥락이 섞이기 쉽습니다. 이 vault는 다음처럼 나눕니다.

- 전역 AI 업무: `06_AI_Sessions/`
- 프로젝트 기획과 실행 기준: `04_Projects/{project}/`
- vault 운영 규칙: `99_System/`

## 저장 기준

| 상황 | 저장 위치 |
| --- | --- |
| 프로젝트가 명확한 Notion 원문 | `04_Projects/{project}/10_RAW_SOURCE/notion/` |
| 프로젝트가 명확한 사용자 작성 문서 | `04_Projects/{project}/15_MY_DOCUMENTS/` |
| 프로젝트가 명확한 핵심 기준 정보 | `04_Projects/{project}/20_CORE/` |
| 프로젝트가 명확한 상세 위키 | `04_Projects/{project}/20_WIKI/` |
| 프로젝트를 넘나드는 AI 대화 | `06_AI_Sessions/conversations/` |
| 프로젝트를 넘나드는 원문 | `06_AI_Sessions/raw/` |
| 프로젝트를 넘나드는 정리 지식 | `06_AI_Sessions/wiki/` |
| 프로젝트를 넘나드는 산출물 | `06_AI_Sessions/output/` |

## 핵심 원칙

- Raw Source는 수정하지 않습니다.
- AI의 정리와 추론은 Wiki에 둡니다.
- 실제 프로젝트 진행 기준은 `20_CORE/`에 둡니다.
- 세션 복구는 `index.md`와 `log.md`를 기준으로 합니다.
- 프로젝트별 세션 복구는 `04_Projects/{project}/00_SCHEMA/INDEX.md`와 `LOG.md`를 기준으로 합니다.

## 운영 명령

- [[COMMANDS]]
- [[SAVE_FILTERS]]
- [[REFERENCE_RESTORE]]
- [[LINT_RULES]]

## Claude/Codex 규칙 파일

- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- 전역 AI 업무: `06_AI_Sessions/AGENTS.md`, `06_AI_Sessions/CLAUDE.md`
