---
project: FaithLog
type: troubleshooting
created: 2026-07-14
tags:
  - FaithLog
  - troubleshooting
  - k6
  - performance
---

# k6 summary export metric shape 불일치

## 문제 상황

#192 네 mode 실측과 DB verification은 모두 완료됐지만 마지막 summary 생성 단계가 실패했다.

## 에러 메시지

`Error: Missing k6 metric coffee_settlement_duration.`

## 원인 분석

요약기가 custom metric을 `metrics[name].values` 구조로 가정했다. 현재 로컬 k6 v2.0.0의 `--summary-export` JSON은 `metrics[name]` 아래에 `p(50)`, `p(95)`, `max`, `value`를 직접 둔다. raw summary에는 custom Trend와 failure rate가 정상 존재했고 k6 네 실행과 DB row는 이미 성공했다.

## 해결 방법

parser가 `metric.values || metric`을 모두 지원하고 Rate는 `rate ?? value`를 사용하도록 수정했다. preserved raw summary 네 개로 summary를 다시 생성해 재측정 없이 p50/p95/max/failure를 복구했다.

## 재발 방지

- contract test와 Node syntax 검증 유지
- k6 버전별 summary export shape를 parser에서 양쪽 지원
- raw k6 summary/log와 verification report를 summary보다 먼저 보존

## 관련 이슈

- #192
