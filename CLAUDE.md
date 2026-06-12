# CLAUDE.md

---
tags:
  - type/project
  - status/active
---

이 파일은 Claude Code가 이 Obsidian vault에서 작업할 때 먼저 읽어야 하는 규칙입니다. Codex는 `AGENTS.md`를 우선 사용하지만, 두 에이전트는 같은 운영 문서를 기준으로 작업합니다.

## 먼저 읽을 문서

1. [[AGENTS]]
2. [[VAULT_RULES]]
3. [[AI_WIKI_ARCHITECTURE]]
4. [[COMMANDS]]
5. [[SAVE_FILTERS]]
6. [[REFERENCE_RESTORE]]
7. [[LINT_RULES]]

## 핵심 규칙

- Raw Source는 수정하지 않습니다.
- `.obsidian/`은 수정하지 않습니다.
- `scripts/`는 명시 요청 없이 수정하지 않습니다.
- 프로젝트가 명확하면 `04_Projects/{project}/`에 저장합니다.
- 프로젝트를 넘나드는 AI 업무는 `06_AI_Sessions/`에 저장합니다.
- 저장 전 [[SAVE_FILTERS]]를 적용합니다.
- 세션 복원은 [[REFERENCE_RESTORE]]를 따릅니다.
- 맥락 오염 검사는 [[LINT_RULES]]를 따릅니다.

## 명령어

- `Save`: 저장 필터 통과 후 Raw/Wiki/Core에 저장
- `Reference`: index/log를 읽고 맥락 복원
- `Ingest`: 원문을 Raw에 보존하고 정리본을 Wiki/Core에 생성
- `Lint`: 맥락 오염, 출처, 결정 기록, 인덱스/로그 누락 검사

## 언어 규칙

- 사람에게 보이는 설명과 가이드는 한국어로 작성합니다.
- 실행 명령 키워드는 `Save`, `Reference`, `Ingest`, `Lint`로 유지합니다.
