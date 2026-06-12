# REFERENCE_RESTORE

---
tags:
  - type/project
  - status/active
---

세션이 끊긴 뒤 AI 에이전트가 Obsidian을 참조해 업무 맥락을 복원하는 규칙입니다.

## Reference 순서

### 전역 AI 업무

1. `06_AI_Sessions/index.md`
2. `06_AI_Sessions/log.md`
3. `06_AI_Sessions/AGENTS.md`
4. 관련 `wiki/` 문서
5. 필요한 경우 `raw/_MANIFEST.md`

### 프로젝트 업무

1. `04_Projects/{project}/00_SCHEMA/INDEX.md`
2. `04_Projects/{project}/00_SCHEMA/LOG.md`
3. `04_Projects/{project}/00_SCHEMA/PROJECT_RULES.md`
4. `04_Projects/{project}/20_CORE/README.md`
5. `04_Projects/{project}/20_CORE/project-facts.md`
6. `04_Projects/{project}/20_CORE/current-plan.md`
7. 필요한 경우 `20_WIKI/`, `30_DECISIONS/`, `40_ERRORS/`
8. 근거 확인이 필요하면 `10_RAW_SOURCE/_MANIFEST.md`

## 복원 시 답변 형식

Reference 후에는 아래를 구분해 답합니다.

```text
확인한 맥락:
- 

확정된 사실:
- 

아직 불확실한 점:
- 

바로 이어서 할 일:
- 
```

## 금지

- Raw Source를 읽지 않고 원문 근거가 있는 척하지 않습니다.
- `20_CORE/`에 없는 내용을 확정 사실처럼 말하지 않습니다.
- 오래된 로그를 최신 상태처럼 말하지 않습니다.
- 프로젝트가 다른 문서를 섞어 맥락을 오염시키지 않습니다.
