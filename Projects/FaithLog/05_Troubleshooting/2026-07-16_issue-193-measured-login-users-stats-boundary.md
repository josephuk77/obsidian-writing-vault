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

# Issue #193 measured-login users stats boundary

## K partial rejected evidence

Actual-before K 식별자는 `I193_BEFORE_20260716_K / I193_FIXTURE_20260716_K / EXEC193_BEFORE_20260716_K`다. Campus/fixture와 exact 3-table VACUUM(ANALYZE), warmup, measured 16 cases를 완료했고 measured HTTP는 총 6,000건, failure 0이었다. Exact measured window는 `2026-07-16T05:48:51Z`부터 `2026-07-16T05:52:00Z` 부근이다.

`charge_items`, `campus_members`, `payment_accounts`는 `nModSinceAnalyze=0`과 maintenance state가 안정적이었다. Users도 analyze/vacuum/auto-maintenance timestamp/count는 안정적이었지만 `nModSinceAnalyze`가 before 72, after 73으로 바뀌어 strict validator가 `PostgreSQL planner/analyze/vacuum maintenance state changed for users.nModSinceAnalyze`로 거부했다.

측정 계정 15028/15029는 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. K namespace, DB rows, report는 보존하며 재사용하지 않는다. K latency·throughput·resource 수치는 baseline 또는 개선 성과로 채택하지 않는다.

## 원인

Fresh measured login은 `LoginCommandService`에서 `users.last_login_at`을 UPDATE한다. PostgreSQL cumulative stats가 해당 app backend의 UPDATE를 늦게 반영해 기존 1초 stable pair는 72/72로 통과했지만 measured 뒤 73으로 나타났다. Measured GET workload의 users write로 해석하지 않는다.

`pg_stat_clear_snapshot()`은 관측 backend snapshot만 비우며, `pg_stat_force_next_flush()`도 호출 backend 자체 통계만 강제하므로 app login backend의 지연 통계를 확실히 정리하지 못한다.

## 보정

- Fresh measured login 직후 exact `VACUUM (ANALYZE) users;`를 실행한다.
- Immutable PostgreSQL ID의 psql stdin으로 transaction 밖에서 실행한다.
- PostgreSQL before evidence, stable-pair, counter, resource sampler, measured window보다 앞서 실행한다.
- Users-only completion marker를 남긴다.
- 다른 table, `VACUUM FULL`, `FREEZE`, 데이터/schema/index/Flyway/config/reset/extension 변경은 금지한다.
- Fixture COMMIT 직후 exact 3-table VACUUM(ANALYZE), stable-pair, measured before/after strict continuity는 유지한다.

Fresh L 제안은 `I193_BEFORE_20260716_L / I193_FIXTURE_20260716_L / EXEC193_BEFORE_20260716_L`이다. 개발 세션은 actual Docker/DB/k6를 실행하지 않는다.

## 관련 이슈

- #193
