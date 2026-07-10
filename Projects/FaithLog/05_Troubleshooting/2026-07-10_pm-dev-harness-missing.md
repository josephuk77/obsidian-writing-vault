---
project: FaithLog
type: troubleshooting
created: 2026-07-10
tags:
  - FaithLog
  - troubleshooting
  - codex
---

# pm-dev 개발 게이트의 저장소 harness 파일 부재

## 문제 상황

Issue #147 구현 전에 `pm-dev`의 `dev_gate.py`를 실행했으나 표준 `python` 명령이 없었고, `python3` 재실행에서도 개발 게이트가 실패했다. 구현 후 `score_code.py`와 `review_gate.py`도 같은 harness 부재 영향을 받았다.

## 에러 메시지

- `zsh: command not found: python`
- `harness.yaml`, `.harness/subagent-workflow.md`, `.harness/spec.md`, `.harness/data-model.md`, `.harness/api-contract.md`, `.harness/architecture.md`, `.harness/planning-scorecard.md`, `.harness/policies/*`, `.codex/agents/*`, `docs/00-index.md` 부재.
- `review-score.json`: `overall=null`, `passed=false`, `harness.yaml has no selected specialist harnesses`.
- `review_gate.py`: quality score/TDD evidence 파일 부재로 실패.

## 원인 분석

pm-dev 공통 스킬은 backward-compatible PM harness 파일을 요구하지만 FaithLog 저장소에는 해당 harness가 설치되어 있지 않다. 이는 #147 코드의 컴파일이나 테스트 실패가 아니다.

## 해결 방법

게이트 실패를 그대로 기록하고, Issue/정책 문서 확인, TDD RED/GREEN, focused/full test, build, Asciidoctor, 격리 Docker health를 독립 검증했다.

## 재발 방지

FaithLog에 PM harness를 도입하기 전까지 `dev_gate.py`, `score_code.py`, `review_gate.py` 실패는 코드 품질 결과와 분리해서 보고한다. harness 파일을 임의 생성하거나 validator를 약화하지 않는다.

## 관련 이슈

- #147
