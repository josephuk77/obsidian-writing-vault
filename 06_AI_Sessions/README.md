# 06_AI_Sessions

---
tags:
  - type/project
  - status/active
---

`06_AI_Sessions/`는 특정 프로젝트에 바로 넣기 애매한 AI 업무 기록, 원문, 정리본, 산출물을 관리하는 전역 AI 작업 공간입니다.

이 구조는 영상의 AI 업무 위키 구조를 이 vault에 맞게 적용한 것입니다. 프로젝트 전용 내용은 `04_Projects/{project}/`에 두고, 프로젝트를 넘나드는 대화, 참고자료, 개념 정리, 작업 로그는 이곳에 둡니다.

## 3-Layer 구조

| Layer | Folder | 역할 |
| --- | --- | --- |
| Raw Source | `raw/` | 수정하지 않는 원본 저장소 |
| Wiki | `wiki/` | AI가 정리하고 연결하는 업무 지식 공간 |
| Schema | `index.md`, `log.md`, `AGENTS.md` | 운영 규칙, 지도, 작업 히스토리 |

## 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `conversations/` | AI와 나눈 중요한 대화 기록 |
| `output/` | AI가 만든 산출물, 프롬프트, 리포트, 스펙 |
| `raw/` | 아티클, 논문, 메모, 스크린샷 등 원본 |
| `wiki/` | 정제된 개념, 결정, 에러, 플레이북, 종합 문서 |

## 사용 기준

- 프로젝트가 명확하면 `04_Projects/{project}/`에 저장합니다.
- 여러 프로젝트에서 쓰는 AI 업무 지식은 `06_AI_Sessions/`에 저장합니다.
- Raw Source는 수정하지 않습니다.
- Wiki 문서는 Raw Source를 바탕으로 AI가 정리하고 연결할 수 있습니다.
- 작업 후 `log.md`를 갱신합니다.

## 핵심 문서

- [[index]]
- [[log]]
- [[AGENTS]]
- [[AI_WIKI_ARCHITECTURE]]
