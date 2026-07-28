---
project: FaithLog
type: troubleshooting
created: 2026-07-16
tags:
  - FaithLog
  - troubleshooting
  - performance
  - postgresql
---

# Issue #193 measured-login update counter ACK

## L partial rejected evidence

Actual-before L 식별자는 `I193_BEFORE_20260716_L / I193_FIXTURE_20260716_L / EXEC193_BEFORE_20260716_L`이다. Fresh measured login 뒤 users VACUUM(ANALYZE)을 완료했고 measured 16-case summary까지 생성됐지만 최초 validator가 users `nModSinceAnalyze` 변경을 거부했다.

Users before는 0, after는 1이었고 `lastVacuum`, `lastAnalyze`, vacuum/analyze counts는 안정적이었다. Login `last_login_at` commit은 `2026-07-16T06:00:28.808644Z`, users VACUUM start는 약 166ms 뒤인 `2026-07-16T06:00:28.974009Z`, ANALYZE는 `2026-07-16T06:00:29.394557Z`였다. App backend의 login UPDATE 통계가 flush되기 전에 VACUUM이 시작됐고 delayed +1이 measured 중 반영됐다.

측정 계정 15030/15031은 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. L namespace, DB rows, report는 보존하며 재사용하지 않는다. L latency·throughput·resource 수치는 baseline 또는 개선 성과로 채택하지 않는다.

JWT tokenVersion checker는 read-only `findById`이며 measured 6,000 GET 자체가 users를 썼다는 증거는 없다. 현재 근거는 measured login 통계 flush 지연이다.

## 보정

- Measured login 직전 `pg_stat_user_tables.users.n_tup_upd`를 canonical decimal string으로 캡처한다.
- Login 뒤 immutable PostgreSQL ID의 read-only polling에서 exact `before + 1`만 ACK한다.
- `+0`은 기존 1초/최대 5회 안에서만 pending이다.
- 감소, `>+1`, timeout, malformed, PostgreSQL bigint 범위 초과는 fail-closed한다.
- ACK 이후에만 existing exact `VACUUM (ANALYZE) users;`를 실행한다.
- ACK와 users maintenance는 before evidence, stable-pair, counter, sampler, measured window보다 앞선다.
- Fixture 3-table VACUUM, stable-pair, measured strict continuity는 유지한다.
- `src/main`, Flyway, schema/index/config/reset/extension은 변경하지 않는다.

Fresh M 제안은 `I193_BEFORE_20260716_M / I193_FIXTURE_20260716_M / EXEC193_BEFORE_20260716_M`이다. 개발 세션은 actual Docker/DB/k6를 실행하지 않는다.

## N partial rejected evidence

Actual-before N 식별자는 `I193_BEFORE_20260716_N / I193_FIXTURE_20260716_N / EXEC193_BEFORE_20260716_N`이다. Fixture, exact 3-table VACUUM(ANALYZE), preflight와 warmup을 완료했다. Measured login 직전 users `n_tup_upd`는 113이었고 login 뒤 1초 간격 attempts 1~5가 모두 113이라 exact `+1` ACK 없이 중단됐다.

Measured k6는 0건이며 `measurement-state-before`, counter/resource, summary, classification도 생성되지 않았다. 측정 계정 15034/15035는 모두 USER로 복구됐다. N namespace, DB rows, report를 보존하며 재사용하지 않는다. N latency·throughput·baseline·성과 수치는 없다.

App login backend의 cumulative stats는 단순 5초 sleep으로 flush되지 않을 수 있다. 이 실패는 product GET workload가 users를 쓰는 증거가 아니라 warmup 뒤 두 번째 ADMIN login이 불안정한 pre-window write를 만든 측정 경계 문제다.

## N 이후 보정

- Measured 직전 두 번째 ADMIN authenticate를 제거한다.
- 최초 ADMIN token을 preflight, warmup, measured까지 재사용한다.
- 최초 token은 warmup max+measured duration+safety를 요구하고 preflight 뒤 같은 합계, measured 직전 measured duration+safety를 다시 검증한다.
- 최초 ADMIN·DUTY login 전에 users `n_tup_upd`를 캡처한다.
- 두 login, fixture, preflight, warmup 뒤 exact `before+2`만 ACK한다. `+0/+1`은 pending이며 감소, `>+2`, malformed, timeout은 fail-closed한다.
- ACK 뒤에만 exact users VACUUM(ANALYZE), stable-pair, counter/resource/measured boundary를 진행한다.
- Report 생성 뒤 non-zero 종료는 credential/token/path 없는 최초 `measurement-rejection.json`을 exclusive-create하고 `automaticAdoption=false`를 유지한다.
- Existing source/API/Flyway/runtime, k6 summary math, PostgreSQL/pgss, resource, fixture/correctness, final continuity gates는 완화하지 않는다.
- `src/main`, Flyway, dependency, schema/index, Docker lifecycle은 변경하지 않는다.

Fresh O 제안은 `I193_BEFORE_20260716_O / I193_FIXTURE_20260716_O / EXEC193_BEFORE_20260716_O`이다. 개발 세션은 actual Docker/DB/k6를 실행하지 않는다.

## 관련 이슈

- #193
