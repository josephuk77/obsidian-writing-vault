---
project: FaithLog
type: troubleshooting
created: 2026-07-16
tags:
  - FaithLog
  - troubleshooting
  - performance
  - docker
---

# Issue #193 Docker memory rounding evidence

## F partial evidence

actual-before attempt F 식별자는 `I193_BEFORE_20260716_F / I193_FIXTURE_20260716_F / EXEC193_BEFORE_20260716_F`다. Report는 `build/reports/k6/issue-193/I193_BEFORE_20260716_F/I193_FIXTURE_20260716_F/EXEC193_BEFORE_20260716_F`에 보존한다.

Fresh fixture는 campus ID 25에 ACTIVE membership 1,000개와 charge item 35,000개를 COMMIT했다. Warmup은 5 iterations와 80 HTTP request를 failure 0으로 완료했다. Measured load 전 첫 resource normalization에서 중단되어 measured k6 summary와 adoption/classification은 생성되지 않았다.

측정 계정 15018/15019는 모두 USER로 복구됐고 canonical performance lock이 비어 있으며 실행 중인 k6가 없음을 확인했다. F namespace, DB rows, report는 partial rejected evidence로만 보존하며 재사용하지 않는다. Warmup, latency, throughput, baseline 또는 개선 성과로 채택하지 않는다.

## 원인

Docker Desktop은 `501.7MiB`, `499.7MiB / 7.653GiB`처럼 표시 정밀도에서 반올림된 값을 출력한다. 기존 parser는 이 값을 exact integer bytes 한 점으로 환산하려 했고, binary unit의 소수 표현이 정수 byte로 나누어떨어지지 않으면 정상 evidence를 거부했다.

## 보정 계약

- `memoryUsed`와 `memoryLimit`은 원본 표시값과 가능한 inclusive integer-byte min/max decimal-string 범위를 저장한다.
- `memoryPercent`는 원본 표시값과 exact numerator/denominator rounding interval을 저장한다.
- 가능한 used/limit ratio 구간과 MemPerc 구간이 겹치는지 `BigInt` rational 비교로 검증한다.
- Full immutable container ID, app/PostgreSQL/Redis role set, positive limit, used≤limit, CPU, memory percent 0..100, safe magnitude, unit/schema 검증은 fail-closed로 유지한다.
- Scalar `memoryUsedBytes`, `memoryLimitBytes`, `memoryPercent` 수치로 false precision을 만들지 않는다.

후속 G는 PM 독립 리뷰와 사용자 승인 후 별도 fresh namespace로 실행됐으며, memory rounding 보정은 통과했지만 별도 resource cadence validator 사유로 rejected됐다. G 상세와 H 제안은 [[2026-07-16_issue-193-docker-stats-cadence-gap]]에 기록한다.

## 관련 이슈

- #193
