# NOTION_SYNC_GUIDE

---
tags:
  - type/project
  - status/active
---

Notion에서 기획 내용을 가져올 때는 원문과 정리본을 분리합니다.

## 저장 위치

- Notion 원문: `04_Projects/{project}/10_RAW_SOURCE/notion/`
- 사용자가 직접 작성한 프로젝트 문서: `04_Projects/{project}/15_MY_DOCUMENTS/`
- AI 작업 맥락: `04_Projects/{project}/16_AI_CONTEXT/`
- 프로젝트 핵심 기준 정보: `04_Projects/{project}/20_CORE/`
- Codex 정리본: `04_Projects/{project}/20_WIKI/`
- 결정 기록: `04_Projects/{project}/30_DECISIONS/`
- 에러/시행착오 기록: `04_Projects/{project}/40_ERRORS/`

## 원문 처리 규칙

- Notion에서 가져온 원문은 가능한 한 그대로 저장합니다.
- Raw Source는 원본 보존용이므로 수정하지 않습니다.
- 원문 파일에는 출처, 캡처 날짜, Notion 링크, 가져온 범위를 남깁니다.
- 원문을 바탕으로 해석, 요약, 구조화를 할 때는 별도 문서로 작성합니다.
- 확정된 핵심 정보는 `20_CORE/`에 요약합니다.
- AI의 가정이나 확인 전 추론은 `16_AI_CONTEXT/`에 둡니다.

## 원문과 정리본을 분리하는 이유

- 나중에 정리본의 판단이 틀렸을 때 원문으로 되돌아갈 수 있습니다.
- Codex가 만든 요약과 실제 기획 원문을 구분할 수 있습니다.
- 프로젝트 기획 변경 이력을 추적하기 쉽습니다.
- 개발 레포가 생긴 뒤에도 기획의 근거를 유지할 수 있습니다.

## 붙여넣기 후 Codex 프롬프트 예시

```text
다음 Notion 원문을 이 프로젝트의 Raw Source로 보고 정리해줘.

규칙:
- 원문 파일은 수정하지 마라.
- 20_WIKI/project-brief.md, requirements.md, roadmap.md, open-questions.md를 갱신해라.
- 20_CORE/project-facts.md, core-data.md, key-decisions.md, solved-issues.md, current-plan.md를 갱신해라.
- AI가 추론한 가정은 16_AI_CONTEXT/assumptions.md에 분리해라.
- 확정되지 않은 내용은 open-questions.md에 남겨라.
- 새 결정이 필요하면 30_DECISIONS에 ADR 초안을 만들어라.
- 작업 후 00_SCHEMA/LOG.md에 Task, Changed, Evidence, Decisions, Errors, Next 형식으로 기록해라.
```

## 체크리스트

- [ ] 원문을 `10_RAW_SOURCE/notion/`에 저장했다.
- [ ] 원문 파일에 Notion 링크와 캡처 날짜를 적었다.
- [ ] `20_WIKI/` 정리본을 갱신했다.
- [ ] `20_CORE/` 핵심 기준 정보를 갱신했다.
- [ ] AI 가정과 조사 큐를 `16_AI_CONTEXT/`에 분리했다.
- [ ] `00_SCHEMA/INDEX.md`에 새 문서 링크를 추가했다.
- [ ] `00_SCHEMA/LOG.md`에 작업 기록을 남겼다.
- [ ] [[PROJECT_DASHBOARD]]를 갱신했다.
