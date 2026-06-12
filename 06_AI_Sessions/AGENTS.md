# AGENTS

---
tags:
  - type/project
  - status/active
---

`06_AI_Sessions/`에서 Codex가 따라야 할 전역 AI 업무 규칙입니다.

## 절대 규칙

- `raw/` 아래 원본 파일은 수정하지 않습니다.
- 원본에서 판단할 수 없는 내용은 사실처럼 쓰지 않습니다.
- `.obsidian/`은 수정하지 않습니다.
- 기존 `scripts/`는 명시 요청 없이 수정하지 않습니다.
- 영상에서 말하는 `CLAUDE.md` 역할은 이 vault에서는 루트 `AGENTS.md`와 이 파일이 담당합니다.

## 저장 규칙

- AI와 나눈 중요한 대화 기록은 `conversations/`에 저장합니다.
- 원본 아티클, 논문, 회의록, 메모, 스크린샷은 `raw/`에 저장합니다.
- AI가 정리한 업무 지식은 `wiki/`에 저장합니다.
- 최종 산출물은 `output/`에 저장합니다.
- 저장 전 [[SAVE_FILTERS]]의 5필터를 적용합니다.

## Raw Source 규칙

- `raw/articles/`: 웹 글, 블로그, 문서 원문
- `raw/assets/`: 이미지, 스크린샷, 첨부자료
- `raw/inbox/`: 아직 분류하지 않은 원문
- `raw/notes/`: 사용자가 붙여넣은 원본 메모
- `raw/papers/`: 논문, PDF 요약 전 원문

## Wiki 규칙

- `wiki/concepts/`: 정제된 개념
- `wiki/decisions/`: 전역 의사결정과 이유
- `wiki/entities/`: 사람, 회사, 도구, 시스템 같은 대상 정보
- `wiki/errors/`: 반복 가능한 문제와 해결 기록
- `wiki/playbooks/`: 반복 업무 절차
- `wiki/projects/`: 여러 프로젝트에 걸친 프로젝트 요약
- `wiki/sources/`: 원본 자료에 대한 정리본
- `wiki/synthesis/`: 여러 자료를 종합한 결론

## 로그 규칙

- 의미 있는 구조 변경, 대화 정리, 산출물 생성 후 `log.md`를 갱신합니다.
- 새 핵심 문서를 만들면 `index.md`에 링크를 추가합니다.
- 프로젝트 전용 내용이면 `04_Projects/{project}/00_SCHEMA/LOG.md`도 갱신합니다.

## 자연어 명령 규칙

- `Save`: [[SAVE_FILTERS]]를 통과한 내용만 저장합니다.
- `Reference`: [[REFERENCE_RESTORE]]에 따라 `index.md`와 `log.md`부터 읽습니다.
- `Ingest`: 원문은 `raw/`에 보존하고 정리본은 `wiki/`에 작성합니다.
- `Lint`: [[LINT_RULES]]에 따라 맥락 오염을 점검합니다.
