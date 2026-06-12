# COMMANDS

---
tags:
  - type/project
  - status/active
---

이 문서는 AI 에이전트가 이 vault에서 사용할 자연어 명령 규칙입니다. 사람이 읽는 설명은 한국어로 쓰고, 에이전트가 실행 키워드로 인식할 명령어는 영어로 고정합니다.

## 명령어 원칙

- 명령어 키워드는 `Save`, `Reference`, `Ingest`, `Lint`를 사용합니다.
- 사용자가 한국어로 말해도 에이전트는 아래 명령 의미로 해석합니다.
- 명령 실행 전 관련 규칙 파일을 먼저 확인합니다.
- 실행 후 필요한 `index.md`, `log.md`, 프로젝트별 `INDEX.md`, `LOG.md`를 갱신합니다.

## Save

사용자가 말할 수 있는 표현:

- "Obsidian에 저장해 줘"
- "이번 작업 내용 저장해 줘"
- "이 결정 위키에 남겨줘"
- "Save this to the vault"

에이전트 처리 규칙:

1. [[SAVE_FILTERS]]의 5가지 저장 필터를 적용합니다.
2. 원문이면 Raw Source에 저장합니다.
3. 반복 재사용 가능한 지식이면 Wiki에 저장합니다.
4. 프로젝트 실행 기준이면 해당 프로젝트 `20_CORE/`에 저장합니다.
5. 중요한 결정이면 `key-decisions.md`에 요약하고 필요 시 ADR을 만듭니다.
6. 중요한 실패/해결이면 `solved-issues.md` 또는 에러 노트에 저장합니다.
7. 관련 `index.md`와 `log.md`를 갱신합니다.

## Reference

사용자가 말할 수 있는 표현:

- "Obsidian 참고해서 이어서 해줘"
- "지난 맥락 복원해 줘"
- "Reference the vault"

에이전트 처리 규칙:

1. [[REFERENCE_RESTORE]]를 따릅니다.
2. 전역 작업이면 `06_AI_Sessions/index.md`와 `log.md`를 먼저 읽습니다.
3. 프로젝트 작업이면 해당 프로젝트 `00_SCHEMA/INDEX.md`와 `LOG.md`를 먼저 읽습니다.
4. 관련 `20_CORE/`, `20_WIKI/`, `raw/_MANIFEST.md`를 확인합니다.
5. 확인한 근거와 아직 모르는 점을 구분해 답합니다.

## Ingest

사용자가 말할 수 있는 표현:

- "이 원문 ingest 해줘"
- "이 Notion 내용을 가져와서 정리해줘"
- "이 자료를 Raw와 Wiki로 나눠줘"

에이전트 처리 규칙:

1. 원문을 Raw Source에 저장합니다.
2. Raw Source는 수정하지 않습니다.
3. `_MANIFEST.md`에 원문 위치와 요약을 기록합니다.
4. 정리본을 Wiki 또는 프로젝트 `20_WIKI/`에 작성합니다.
5. 확정된 실행 기준은 프로젝트 `20_CORE/`에 요약합니다.
6. 불확실한 가정은 `16_AI_CONTEXT/assumptions.md` 또는 `wiki/synthesis/`에 분리합니다.

## Lint

사용자가 말할 수 있는 표현:

- "위키 lint 해줘"
- "맥락 오염 검사해줘"
- "Obsidian 구조 점검해줘"

에이전트 처리 규칙:

1. [[LINT_RULES]]를 따릅니다.
2. Raw Source가 수정되었는지 확인합니다.
3. Wiki에 검증되지 않은 추측이 사실처럼 들어갔는지 확인합니다.
4. 결정 근거, 결정자, 날짜가 빠진 결정 문서를 찾습니다.
5. 오래된 규칙이나 충돌하는 규칙을 찾습니다.
6. `index.md`와 `log.md` 누락을 확인합니다.

## 하이브리드 언어 규칙

- 사람이 편집하는 정책, 금지 표현, 톤, 업무 가이드는 한국어로 씁니다.
- 에이전트 명령 키워드는 `Save`, `Reference`, `Ingest`, `Lint`로 유지합니다.
- 파일명은 기존 vault 규칙을 따릅니다.
