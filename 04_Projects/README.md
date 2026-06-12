# 04_Projects

---
tags:
  - type/project
  - status/active
---

`04_Projects/`는 현재 기획 중인 프로젝트를 관리하는 허브입니다. 아직 실제 개발 레포가 없는 프로젝트도 이곳에서 기획, 원문, 정리본, 결정 사항, 산출물을 관리합니다.

## 핵심 문서

- [[PROJECT_INDEX]]
- [[PROJECT_DASHBOARD]]
- [[NOTION_SYNC_GUIDE]]

## 프로젝트별 폴더 구조

| 폴더 | 역할 |
| --- | --- |
| `00_SCHEMA/` | 프로젝트 인덱스, 로그, 규칙, repo 연결 정보 |
| `10_RAW_SOURCE/` | Notion 원문, 대화, 회의록, 참고자료 원본 |
| `15_MY_DOCUMENTS/` | 사용자가 프로젝트를 하면서 직접 작성한 문서 |
| `16_AI_CONTEXT/` | AI가 작업하며 필요한 맥락, 가정, 조사 큐, 핸드오프 |
| `20_CORE/` | 프로젝트 실행에 실제로 필요한 핵심 데이터, 정보, 해결사항, 결정사항의 현재판 |
| `20_WIKI/` | 설명형 프로젝트 위키와 상세 정리 |
| `30_DECISIONS/` | ADR 형식의 의사결정 기록 |
| `40_ERRORS/` | 에러, 장애, 시행착오 기록 |
| `90_OUTPUTS/` | spec, prompt, report 같은 산출물 |

## 프로젝트 내부 정보 분리

- 내가 직접 작성한 문서: `15_MY_DOCUMENTS/`
- AI가 생각하고 작업하는 데 필요한 보조 맥락: `16_AI_CONTEXT/`
- 실제 프로젝트 진행에 필요한 핵심 기준 정보: `20_CORE/`
- 자세한 설명과 정리형 위키: `20_WIKI/`
- 정식 결정 기록: `30_DECISIONS/`
- 상세 문제 해결 기록: `40_ERRORS/`

## 영상식 3-Layer와의 연결

| Layer | 프로젝트 내부 위치 | 설명 |
| --- | --- | --- |
| Raw Source | `10_RAW_SOURCE/` | Notion 원문, 대화, 회의록, 참고자료 원본. 수정 금지 |
| Wiki | `20_WIKI/`, `20_CORE/`, `30_DECISIONS/`, `40_ERRORS/` | 정리된 지식, 핵심 기준, 결정, 해결 기록 |
| Schema | `00_SCHEMA/` | INDEX, LOG, PROJECT_RULES, REPO_LINKS |

프로젝트를 넘나드는 AI 업무 기록은 [[AI_WIKI_ARCHITECTURE]] 기준으로 `06_AI_Sessions/`에 둡니다.

## Notion 기획 정리 흐름

1. Notion의 기획 원문을 프로젝트 `10_RAW_SOURCE/notion/`에 저장한다.
2. Raw Source는 원본 보존용이므로 수정하지 않는다.
3. Codex가 읽고 정리한 상세 문서는 `20_WIKI/`에 저장한다.
4. 실제 진행에 필요한 확정 정보는 `20_CORE/`에 요약한다.
5. 결정 사항은 `20_CORE/key-decisions.md`에 요약하고, 정식 기록이 필요하면 `30_DECISIONS/`에 ADR로 남긴다.
6. 해결한 중요한 문제는 `20_CORE/solved-issues.md`에 요약하고, 상세 기록이 필요하면 `40_ERRORS/`에 남긴다.
7. 전체 현황은 [[PROJECT_DASHBOARD]]에 반영한다.

## 개발 레포 생성 이후

실제 코드 레포가 생기면 프로젝트별 `00_SCHEMA/REPO_LINKS.md`에 GitHub repo, 로컬 repo 경로, repo wiki 경로, 배포 URL, API 문서 URL을 채웁니다.

vault는 기획과 맥락의 장기 기억을 맡고, 개발 레포는 구현과 실행 가능한 소스코드를 맡습니다.
