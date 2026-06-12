# CLAUDE

---
tags:
  - type/project
  - status/active
---

Claude Code가 `06_AI_Sessions/`에서 전역 AI 업무를 수행할 때 읽는 규칙입니다.

## 역할

- `raw/`: 수정하지 않는 원본 저장소
- `wiki/`: AI가 정리하고 연결하는 업무 지식
- `conversations/`: AI 대화 기록
- `output/`: 프롬프트, 리포트, 스펙 산출물
- `index.md`: 전체 지도
- `log.md`: 작업 타임라인
- `AGENTS.md`: Codex용 규칙
- `CLAUDE.md`: Claude Code용 규칙

## 명령어 규칙

- `Save`: [[SAVE_FILTERS]]를 통과한 내용만 Wiki/Core에 저장합니다.
- `Reference`: [[REFERENCE_RESTORE]] 기준으로 `index.md`와 `log.md`를 먼저 읽습니다.
- `Ingest`: 원문은 `raw/`에 보존하고 정리본은 `wiki/`에 작성합니다.
- `Lint`: [[LINT_RULES]] 기준으로 맥락 오염을 검사합니다.

## 금지

- `raw/` 파일 수정 또는 삭제
- 출처 없는 결정을 확정 사실처럼 저장
- 세션 로그 없이 중요한 구조 변경
- 프로젝트 전용 내용을 전역 Wiki에만 저장하고 프로젝트 허브에 연결하지 않는 것
