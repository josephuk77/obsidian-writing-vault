---
project: FaithLog
type: troubleshooting
created: 2026-07-16
tags:
  - FaithLog
  - troubleshooting
  - performance
  - provenance
---

# Issue #193 host-exclusive provenance rejection

## M technical pass

Actual-before M 식별자는 `I193_BEFORE_20260716_M / I193_FIXTURE_20260716_M / EXEC193_BEFORE_20260716_M`이다. Exact login `n_tup_upd +1` ACK와 users VACUUM 뒤 strict users `nModSinceAnalyze` 안정성, 모든 metric/DB/resource/runtime/final continuity validator를 통과했다.

Classification은 `conditional-shared-stack`, `automaticAdoption=false`다. Measured HTTP는 2,720건, failure 0이며 16 cases 각각 170건이었다. 관찰값은 whole avg `673.748ms`, p50 `583.891ms`, p95 `1378.754ms`, p99 `2085.566ms`, max `4763.404ms`, throughput `14.678 req/s`다.

## PM rejection

같은 host에서 #192/#194~#199 개발 세션들이 병렬 static/Node 작업을 시작해 CPU exclusive-use provenance를 입증할 수 없었다. Technical validator 통과와 host 독점 증명은 별도 조건이므로 M은 conditional supporting evidence로만 보존하고 위 수치를 valid before baseline 또는 개선 성과로 채택하지 않는다.

측정 계정 15032/15033은 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. M namespace, DB rows, report는 보존하며 재사용하지 않는다.

Fresh N 제안은 `I193_BEFORE_20260716_N / I193_FIXTURE_20260716_N / EXEC193_BEFORE_20260716_N`이다. PM은 다른 개발 세션을 일시 정지한 뒤 host-exclusive actual을 단독 실행한다. 개발 세션은 Docker/DB/k6를 실행하지 않는다.

## O valid before baseline

N은 measured 전 ACK timeout으로 rejected됐고, runner 보정 뒤 fresh O를 별도 namespace로 실행했다. O 식별자는 `I193_BEFORE_20260716_O / I193_FIXTURE_20260716_O / EXEC193_BEFORE_20260716_O`, source는 `origin/develop 6796ed146244d8f3f5b5dd7048ebe16865084a97`이다.

- Fixture: ACTIVE member 1,000명, account 5개, charge 35,000개.
- Correctness: pagination, 1개월 archive cutoff, includeArchived, #200 duty ownership, #206 tie ordering 통과.
- Workload: 16 cases × 484, HTTP 7,744건, checks 23,232건, failure 0.
- 성능: throughput `42.483669 req/s`, case p50 `109.60~251.62ms`, p95 `208.54~423.45ms`, worst max `1293.83ms`.
- Window: `2026-07-16T07:27:07.498Z~07:30:10.197Z`.
- Resource: 93 samples valid. App peak CPU `286.51%`/RAM `756MiB`, PostgreSQL `241.69%`/`277MiB`, Redis `21.93%`/`19.56MiB`.
- Integrity: external activity 0, planner/table maintenance stable, pgss unavailable continuity, runtime/DB/postmaster/target binding exact.
- Security: users update exact `+2`, 임시 ADMIN USER 복구, rejection artifact 없음, credential-pattern report hit 없음.

Runner classification은 `conditional-shared-stack`, `automaticAdoption=false`를 유지했다. PM이 다른 세션이 없는 exclusive window를 독립 확인해 O를 유효 before baseline으로 수동 채택했다. 따라서 자동 채택 정책은 완화하지 않으며, after는 PM integration branch에서 동일 조건으로만 수집한다.

## Production optimization

Commit `93bbe64`에서 승인된 두 관리자 캠퍼스 집계 endpoint를 전용 DB projection read port로 전환했다. 기존 ACTIVE membership 순회 + 멤버별 User 조회와 조건에 맞는 전체 `ChargeItem` entity materialization/JVM 집계를 제거하고, summary 1회 + member aggregate/page 1회 + distinct count 1회의 고정 query로 변경했다.

PM 리뷰에서 세 statement가 기본 `READ_COMMITTED`의 서로 다른 snapshot을 볼 수 있는 P1을 찾았다. 2-transaction/latch integration RED에서 summary 뒤 concurrent charge commit 시 member/page가 새 행을 보는 불일치를 재현했고, 두 public endpoint에만 read-only `REPEATABLE_READ`를 적용해 같은 snapshot을 보장했다. 다른 query 경로의 isolation은 변경하지 않았다.

Focused 23/23과 현재 전체 test XML tests 561/failures 0/errors 0/skipped 3을 확인했다. PM 독립 build는 `BUILD SUCCESSFUL in 3m16s`, asciidoctor는 `BUILD SUCCESSFUL in 17s`였고, issue-local Node 36/36, JS/MJS check, Bash check, k6 static inspect와 diff check가 통과했다. API/Flyway/dependency/index 변경은 없다. After는 아직 실행하지 않았으므로 O 대비 개선률은 PM integration branch 측정 전까지 성과로 기록하지 않는다.

#194에는 `charge_items`의 campus/account/category/status/user filter-group 축과 `campus_members(campus_id,status,user_id)`를 PostgreSQL EXPLAIN/index 후보로 전달한다.

## 관련 이슈

- #193
