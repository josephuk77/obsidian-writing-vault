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

# Issue #193 measured-window insert-triggered autovacuum

## J partial rejected evidence

Actual-before attempt J 식별자는 `I193_BEFORE_20260716_J / I193_FIXTURE_20260716_J / EXEC193_BEFORE_20260716_J`다. 승인된 3-table ANALYZE를 warmup 전에 완료했고 measured 16 cases를 failure 0으로 완료했다. `charge_items` analyzeCount/autoanalyzeCount/lastAnalyze는 before/after 안정적이어서 I의 autoanalyze 문제는 해소됐다.

`campus_members` before는 `lastAnalyze=2026-07-16T05:31:18.323492Z`, `autovacuumCount=5`, `lastAutovacuum=2026-07-16T02:50:09.214337Z`, `nModSinceAnalyze=0`이었다. After는 `autovacuumCount=6`, `lastAutovacuum=2026-07-16T05:32:16.798376Z`, `nModSinceAnalyze=0`이었다. Measurement state before는 `2026-07-16T05:31:31.009787Z`, after는 `2026-07-16T05:34:40.811198Z`이며 insert-triggered autovacuum이 measured 시작 약 45초 뒤 실행돼 strict integrity가 거부했다.

측정 계정 15026/15027은 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. J namespace, DB rows, report는 partial rejected evidence로 보존하고 재사용하지 않는다. J의 latency·throughput·resource 수치를 baseline 또는 개선 성과로 채택하지 않는다.

## Read-only 근거

- `autovacuum_naptime=60s`
- `autovacuum_vacuum_insert_threshold=1000`
- `autovacuum_vacuum_insert_scale_factor=0.2`
- J autovacuum 완료 후 `campus_members.n_ins_since_vacuum=0`
- 현재 `charge_items.n_ins_since_vacuum=105000`, live row 534011
- 다음 fresh 35,000-row fixture도 insert-triggered vacuum을 유발할 수 있음

## 승인된 재발 방지

사용자는 기존 ANALYZE-only command를 fixture COMMIT 직후 exact `VACUUM (ANALYZE) campus_members, payment_accounts, charge_items;`로 교체하도록 승인했다. Runner는 immutable PostgreSQL ID의 psql stdin으로 transaction 밖에서 이를 실행하고 dataset binding·expectations·preflight·warmup 전에 exact table completion evidence를 남긴다.

`users`나 다른 table, `VACUUM FULL`, `FREEZE`, 데이터 삭제, schema/index/Flyway/config/reset/extension 변경은 허용하지 않는다. Measured before/after vacuum/analyze/auto-maintenance continuity도 완화하지 않는다.

Fresh K 제안 식별자는 `I193_BEFORE_20260716_K / I193_FIXTURE_20260716_K / EXEC193_BEFORE_20260716_K`다. 개발 세션은 actual Docker/DB/k6를 실행하지 않으며 PM finding 0 뒤 PM 단독 실행만 허용된다.

## 관련 이슈

- #193
