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

# Issue #193 fixture ANALYZE boundary

## I partial rejected evidence

Actual-before attempt I 식별자는 `I193_BEFORE_20260716_I / I193_FIXTURE_20260716_I / EXEC193_BEFORE_20260716_I`다. Measured 16 cases를 failure 0으로 완료했고 users `nModSinceAnalyze`는 before/after 59→59로 안정적이었다.

`charge_items` before는 `nModSinceAnalyze=70000`, `lastAutoanalyze=2026-07-16T04:54:17.632105Z`, `autoanalyzeCount=10`이었다. After는 `nModSinceAnalyze=0`, `lastAutoanalyze=2026-07-16T05:20:17.275926Z`, `autoanalyzeCount=11`이었다. Measured start 후 PostgreSQL autoanalyze가 실행돼 기존 strict maintenance continuity가 measurement-integrity를 거부했다.

측정 계정 15024/15025는 모두 USER로 복구됐고 canonical lock free가 확인됐다. I namespace, DB rows, report는 partial rejected evidence로 보존하고 재사용하지 않는다. I의 latency·throughput·resource 수치를 baseline 또는 개선 성과로 채택하지 않는다.

## 승인된 보정 계약

- Fixture transaction은 기존대로 COMMIT까지 데이터 생성과 exact cardinality만 담당한다.
- COMMIT 직후, dataset binding·expectations·preflight·warmup 전에 별도 stdin SQL로 exact `ANALYZE campus_members, payment_accounts, charge_items;`를 실행한다.
- 완료 marker/report를 남긴다.
- `users`는 bulk fixture 대상이 아니므로 ANALYZE하지 않고 fresh measured login stats는 기존 pre-boundary stable-pair gate가 담당한다.
- 다른 table, VACUUM, reset/config/extension, 데이터/schema/index/Flyway는 변경하지 않는다.
- Measured before/after analyze/autoanalyze continuity는 기존 strict 검증을 유지한다.

후속 J는 PM 독립 리뷰와 사용자 승인 후 별도 fresh namespace로 실행됐다. 3-table ANALYZE로 I의 `charge_items` autoanalyze 문제는 해소됐지만 measured-window `campus_members` insert-triggered autovacuum 사유로 rejected됐다. 상세는 [[2026-07-16_issue-193-insert-triggered-autovacuum]]에 기록한다.

## 관련 이슈

- #193
