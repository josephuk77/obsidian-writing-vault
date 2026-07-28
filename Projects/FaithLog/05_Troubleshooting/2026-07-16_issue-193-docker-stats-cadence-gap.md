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

# Issue #193 Docker stats cadence maximum gap

## G partial rejected evidence

Actual-before attempt G 식별자는 `I193_BEFORE_20260716_G / I193_FIXTURE_20260716_G / EXEC193_BEFORE_20260716_G`다. Fresh fixture는 campus ID 27에 ACTIVE membership 1,000개와 charge item 35,000개를 COMMIT했다. Warmup은 5 iterations와 80 HTTP request를 failure 0으로 완료했다.

Measured phase는 16 cases 각각 request count 239, custom failure value 0이었다. Resource sample 90개가 `2026-07-16T04:54:06.025Z`부터 `2026-07-16T04:57:16.941Z`까지 수집됐고 관찰 gap은 최소 1.869초, 최대 4.807초였다. Measured summary, counter-after, measurement-state-after, PostgreSQL-after evidence는 존재하지만 resource validator에서 중단돼 runtime-final과 adoption/classification은 생성되지 않았다.

측정 계정 15020/15021은 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. G namespace, DB rows, report는 partial rejected evidence로만 보존하고 재사용하지 않는다. G의 warmup·measured 요청 수·latency·throughput·resource 수치를 baseline 또는 개선 성과로 채택하지 않는다.

## 원인

`docker stats --no-stream`은 실제로 약 1.37~4.31초 동안 blocking됐다. 기존 sampler는 각 capture 뒤 nominal interval의 절반인 0.5초를 무조건 sleep했고, `DOCKER_STATS_SAMPLING_INTERVAL_SECONDS=1`을 nominal cadence와 maximum gap 양쪽에 사용했다. 그 결과 인접 timestamp gap이 1.869~4.807초가 되어 1초 validation gate를 구조적으로 통과할 수 없었다.

## 보정 계약

- `DOCKER_STATS_SAMPLING_INTERVAL_SECONDS=1`은 nominal requested cadence metadata로 유지한다.
- Runtime-required `DOCKER_STATS_MAX_GAP_SECONDS=5`를 별도로 두고 누락·비정상 값·nominal 미만을 fail-closed 처리한다.
- Sampler는 blocking capture 완료 직후 다음 capture를 시작하며 unconditional post-capture sleep을 두지 않는다.
- Validator는 인접 observed gap이 5초를 초과하면 거부하고, run conditions와 validation output에 nominal interval과 maximum gap을 모두 기록한다.
- Capture failure, stop/reap, final synchronous sample, immutable runtime continuity, `automaticAdoption=false` 경계는 유지한다.

후속 H는 PM 독립 리뷰와 사용자 승인 후 별도 fresh namespace로 실행됐으며 resource validation을 통과했지만 pre-boundary cumulative stats 사유로 rejected됐다. H 상세와 I 제안은 [[2026-07-16_issue-193-pre-boundary-stats-stabilization]]에 기록한다.

## 관련 이슈

- #193
