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
| `20_WIKI/` | Codex와 사용자가 정리한 프로젝트 위키 |
| `30_DECISIONS/` | ADR 형식의 의사결정 기록 |
| `40_ERRORS/` | 에러, 장애, 시행착오 기록 |
| `90_OUTPUTS/` | spec, prompt, report 같은 산출물 |

## Notion 기획 정리 흐름

1. Notion의 기획 원문을 프로젝트 `10_RAW_SOURCE/notion/`에 저장한다.
2. Raw Source는 원본 보존용이므로 수정하지 않는다.
3. Codex가 읽고 정리한 결과는 `20_WIKI/`에 저장한다.
4. 결정 사항은 `30_DECISIONS/`에 ADR로 남긴다.
5. 전체 현황은 [[PROJECT_DASHBOARD]]에 반영한다.

## 개발 레포 생성 이후

실제 코드 레포가 생기면 프로젝트별 `00_SCHEMA/REPO_LINKS.md`에 GitHub repo, 로컬 repo 경로, repo wiki 경로, 배포 URL, API 문서 URL을 채웁니다.

vault는 기획과 맥락의 장기 기억을 맡고, 개발 레포는 구현과 실행 가능한 소스코드를 맡습니다.
