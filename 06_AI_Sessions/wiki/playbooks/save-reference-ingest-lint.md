# save-reference-ingest-lint

---
tags:
  - type/project
  - status/active
---

AI 에이전트가 이 vault에서 자연어 명령을 실행하는 플레이북입니다.

## Commands

- [[COMMANDS]]
- [[SAVE_FILTERS]]
- [[REFERENCE_RESTORE]]
- [[LINT_RULES]]

## Save

저장 전 [[SAVE_FILTERS]]를 적용합니다. 필터를 통과하지 못한 1회성 답변은 Wiki/Core에 승격하지 않습니다.

## Reference

전역 업무는 `06_AI_Sessions/index.md`와 `log.md`를 읽고, 프로젝트 업무는 프로젝트별 `00_SCHEMA/INDEX.md`와 `LOG.md`를 읽습니다.

## Ingest

원문은 Raw Source에 저장하고, 정리본은 Wiki/Core에 분리합니다. Raw Source는 수정하지 않습니다.

## Lint

맥락 오염, 출처 없는 결정, 오래된 규칙, 인덱스/로그 누락을 점검합니다.
