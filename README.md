# Obsidian Writing Vault

---
tags:
  - type/project
  - status/active
---

이 vault는 개인 지식, 학습 기록, 블로그 초안, 프로젝트 기획을 한곳에서 관리하기 위한 Obsidian vault입니다. 현재는 실제 개발 레포가 없는 프로젝트도 `04_Projects/`에서 기획 허브로 관리하고, 나중에 코드 레포가 생기면 각 프로젝트의 `REPO_LINKS.md`에서 로컬 경로, GitHub repo, repo 내부 wiki를 연결합니다.

## 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `00_Inbox/` | 아직 분류하지 않은 아이디어, 원문, 빠른 메모 |
| `01_Daily/` | 일일 기록, TIL, 회고, 작업 로그 |
| `02_Study/` | 개발/커리어/학습 개념 정리 |
| `03_Blog/` | 블로그 아이디어, 초안, 발행 기록 |
| `04_Projects/` | 현재 기획 중인 프로젝트 허브와 프로젝트별 위키 |
| `05_Resources/` | 주제별 참고자료, 링크, 인용, 장기 보관 자료 |
| `06_AI_Sessions/` | 프로젝트를 넘나드는 AI 업무 위키, 대화, 원문, 산출물 |
| `90_Templates/` | 공통 노트 템플릿 |
| `99_System/` | vault 운영 규칙, 네이밍, 태그, 워크플로, 유지보수 로그 |

## AI 업무 위키 구조

이 vault는 영상의 AI 업무 위키 구조를 그대로 복사하지 않고, 개인 지식 vault와 프로젝트 허브에 맞게 확장해서 사용합니다.

| Layer | 전역 위치 | 프로젝트별 위치 | 역할 |
| --- | --- | --- | --- |
| Raw Source | `06_AI_Sessions/raw/` | `04_Projects/{project}/10_RAW_SOURCE/` | 수정하지 않는 원본 |
| Wiki | `06_AI_Sessions/wiki/` | `04_Projects/{project}/20_WIKI/` | AI가 정리하고 연결하는 지식 |
| Schema | `06_AI_Sessions/index.md`, `log.md`, `AGENTS.md` | `04_Projects/{project}/00_SCHEMA/` | 운영 규칙, 지도, 작업 히스토리 |

프로젝트가 명확하지 않은 AI 대화와 자료는 `06_AI_Sessions/`에 두고, 프로젝트가 명확한 자료는 `04_Projects/{project}/`에 둡니다.

## 프로젝트 기획 흐름

1. Notion에서 프로젝트 기획 원문을 가져온다.
2. 각 프로젝트의 `10_RAW_SOURCE/notion/`에 원문 그대로 저장한다.
3. Raw Source는 원본 보존용이므로 직접 수정하지 않는다.
4. Codex나 사용자가 정리한 문서는 `20_WIKI/`에 저장한다.
5. 결정 사항은 `30_DECISIONS/`, 에러와 장애 기록은 `40_ERRORS/`, 산출물은 `90_OUTPUTS/`에 둔다.
6. 프로젝트별 `00_SCHEMA/INDEX.md`와 `00_SCHEMA/LOG.md`를 갱신해 세션이 끊겨도 맥락을 복구할 수 있게 한다.

자세한 규칙은 [[NOTION_SYNC_GUIDE]], [[PROJECT_INDEX]], [[PROJECT_DASHBOARD]]를 기준으로 관리합니다.

## 개발 레포 연결 방식

아직 이 vault의 프로젝트 폴더는 실제 코드 레포가 아닙니다. 개발 레포가 생성되면 각 프로젝트의 `00_SCHEMA/REPO_LINKS.md`에 다음 항목을 채웁니다.

- Notion 기획 링크
- GitHub repo 링크
- 로컬 repo 경로
- repo 내부 wiki 경로
- 배포 URL
- API 문서 URL
- 기타 참고 링크

프로젝트 위키는 vault에서 기획과 맥락을 보존하고, 코드 레포 wiki는 구현과 운영에 가까운 내용을 담도록 분리합니다.

## 핵심 문서

- [[PROJECT_INDEX]]: 전체 프로젝트 목록
- [[PROJECT_DASHBOARD]]: 전체 프로젝트 현황
- [[NOTION_SYNC_GUIDE]]: Notion 원문 가져오기 규칙
- [[AI_WIKI_ARCHITECTURE]]: AI 업무 위키 구조 비교와 저장 기준
- [[VAULT_RULES]]: vault 운영 원칙
- [[NAMING_RULES]]: 파일명 규칙
- [[TAG_RULES]]: 태그 규칙
- [[WORKFLOW]]: 일상 작업 흐름
- [[MAINTENANCE_LOG]]: 구조 변경 및 유지보수 기록
