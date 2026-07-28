---
project: FaithLog
type: devlog
issue: "#194"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - postgresql
  - explain
  - tdd
---

# #194 PostgreSQL 실행계획 기반 복합·부분 인덱스 before 시나리오

## 1. 작업 배경

#192/#193/#195/#196/#197/#198/#199는 공통 1,000명 fixture에서 정산, 관리자 목록/집계, 기도/투표 연관 조회, 경건/cleanup, 알림, 대시보드 병목을 각각 측정한다. #194는 추측으로 production index를 추가하지 않고, 이 핵심 SQL의 PostgreSQL 실행계획 before 증거를 같은 identity와 metric 계약으로 수집할 준비만 담당한다.

## 2. 현재 상태

`scenario-ready / not-measured`

- Docker/PostgreSQL/EXPLAIN/ANALYZE 실행 0건
- 실제 baseline 수치, plan hash, 성능 개선율 0건
- Flyway/index/HypoPG/DB extension 변경 0건
- production Java/API/권한/응답/ErrorCode/트랜잭션/Entity/의존성 변경 0건
- 기존 row 수정/삭제 0건

## 3. 시나리오 계약

- 이슈별 핵심 read SQL 24개를 inventory로 연결했다.
- logical `datasetId`와 구체적 `fixtureRunId`를 분리하고, 7개 원 이슈 report 경로와 SQL anchor를 가진 cross-issue report를 입력받는다.
- runtime-only `PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD`를 사용하며 credential 값은 report에 저장하지 않는다.
- issue-local ignored report를 사용하고, 실제 PostgreSQL container를 read-only `docker inspect`한 뒤 actual Compose project의 canonical `/tmp/faithlog-performance-{project}.lock`을 원자 획득한다. 획득 당시 device/inode가 유지된 빈 lock directory만 비재귀 해제하며 다른 k6/fixture/DB 측정과 병렬 실행하지 않는다.
- Compose project/service/config/working-dir label, container ID/name, image ID/reference, start time과 network identity를 기록한다. pre-lock identity를 canonical lock 직후 확인하고 DB identity psql 뒤 재-inspect해 시작 binding을 양쪽에서 고정한다. planner/schema/DB after-state 뒤 마지막 inspect로 종료 binding도 고정하며, inspect `POSTGRES_DB`와 psql server address/port/database/postmaster 시작 시각이 모두 일치해야만 채택한다. lifecycle 변경 명령은 runner에 없다.
- `WARM_RUNS`와 observer `ACTIVITY_SAMPLE_INTERVAL_MS`는 승인된 값을 runtime에 반드시 입력하고 숨은 기본값은 두지 않는다. sampling interval은 실행 창별 사용자 승인 pending이다.
- 현재 #193은 `conditional-shared-stack`, #196/#199는 `conditional-not-adoptable` artifact만 생성하므로 별도 사용자 승인 bridge 계약 전까지 cross-issue gate는 EXPLAIN 0회로 fail closed한다. 존재하지 않는 성공 status나 일반 `approved` 필드는 허용하지 않는다.

## 4. 실행계획/상태 계약

향후 승인된 측정 창에서만 모든 SQL을 `BEGIN READ ONLY`와 `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`로 순차 실행한다.

- `cold_like_observation`: 첫 관찰 1회. cache reset이 없으므로 true cold cache가 아니다.
- `warm_cache`: 첫 관찰 이후 동일 SQL 반복. 두 구간 모두 `cacheResetPerformed=false`다.
- 전후 planner settings와 table별 analyze/autoanalyze/vacuum/autovacuum/visibility 통계, schema/index fingerprint, PostgreSQL instance 전체 database의 외부 client backend를 기록한다. observer 자신과 exact 등록 measured backend만 제외하며 다른 database activity는 별도 reason으로 남긴다. 타 role visibility 제한으로 `state=NULL`인 client backend도 idle이 아닌 오염으로 처리한다. 시작 snapshot이 불완전하거나 외부 activity가 있으면 EXPLAIN 전에 중단한다. 실행 중 상태·source/artifact/schema/DB/Compose identity 변화 또는 transient activity는 report를 `invalid/pending`으로 기록하고 non-zero로 종료해 채택을 차단한다. SIGTERM은 큰 승인 sampling interval의 pending delay를 즉시 깨우며, observer 전용 5초 grace가 진행 중 최대 2초 sample과 final sample을 포괄해 report를 보존한다.
- 각 실행의 capturedAt을 EXPLAIN ANALYZE 시각으로 남기며 수동 ANALYZE는 실행하지 않는다.

plan structure는 literal을 placeholder로 정규화하고 재귀 parent-child topology를 보존해 SHA-256 `planHash`를 만든다. timing/actual row/loop/buffer는 hash에서 제외하므로 runtime metric만 다른 동일 topology는 같은 hash, topology만 다른 plan은 다른 hash가 된다. 별도 metric으로 Seq/Index/Index Only/Bitmap scan, estimated/actual rows, loops, shared hit/read, rows removed, sort method/space, planning/execution time을 기록한다.

## 5. 후보와 정확성

inventory는 predicate/order/join column과 후보 방향을 기록하지만 DDL 결정이나 개선 성과로 취급하지 않는다.

각 SQL은 `exact-current-production`, `reconstructed-current-query`, `synthetic-candidate` 중 하나로 분류한다. 현재 24개는 production source 대조 결과 reconstructed 2개, synthetic 22개, exact 0개이며 전부 `productionBeforeEligible=false`다. report contract도 production-before activation을 비활성화했으며 captured Hibernate SQL artifact와 실행 shape를 1:1 검증하는 별도 사용자 승인 계약 전에는 켤 수 없다. 특히 i193 admin charge filter/page, i197 cleanup predicate count surrogate, i199 dashboard summary는 synthetic candidate이므로 hypothetical evidence로만 유지한다.

#193 finding-zero branch `01faf929c24746e3a300e40d11171fc7d473954d`의 새 `AdminChargeAggregationQueryRepository`는 한 read-only `REPEATABLE_READ` API 호출에서 동일 criteria로 `summary`, 회원 aggregate/page, `count(distinct user_id)` 세 SQL을 실행한다. #194는 이 source revision과 production source SHA-256, 동적 predicate/order shape, 16개 API case별 3-statement 비교 matrix를 별도 handoff로 고정했다. 현재 develop 미통합·runtime SQL 미capture 상태이므로 `exact-production-branch-candidate-not-measured`, `productionBeforeEligible=false`, `automaticAdoption=false`이고 기존 24개 실행 inventory에는 자동 편입하지 않는다.

- `charge_items(campus_id,payment_category,status,user_id)`: V1 `uk_charge_items_source(campus_id,user_id,payment_category,source_type,source_id)`와 prefix/column 중복 및 summary/page/count별 적용성을 따로 비교한다.
- `charge_items(campus_id,payment_account_id,payment_category,status,user_id)`: account-scoped case와 account predicate 없는 admin case를 분리하고, 가장 넓은 후보의 insert/status-update 비용을 함께 본다.
- `campus_members(campus_id,status,user_id)`: V1 `uk_campus_members_campus_user(campus_id,user_id)`가 이미 join probe를 제공하므로 actual plan의 status 이득과 write cost를 증명할 때만 유지하는 conditional 후보다.
- leading-wildcard keyword는 extension/index 별도 승인 전까지 후보 채택 금지다.

- polls status/ends/id 및 COFFEE OPEN partial 방향
- weekly devotion campus/week/user
- charge campus/status/account/user/source 방향
- notification status/time/id
- meal charge group settlement/id
- prayer/poll/member/FCM/cleanup join·time predicate

각 SQL에는 campus isolation, stable order/page, terminal status, MEAL rounding, active/stale token, UNPAID cleanup 제외, dashboard MEAL 제외 같은 correctness check를 연결했다. API-level 정확성은 원 이슈 report가 소유하며 #194 EXPLAIN runner만으로 새로 증명했다고 보고하지 않는다.

## 6. TDD 기록

1. inventory, runner safety, plan normalization, cache/planner state, ignored report 계약 테스트를 production 변경 전에 작성했다.
2. 구현 파일이 없어 `5 tests / 5 failures` RED를 확인하고 test-only 커밋으로 남겼다.
3. read-only SQL inventory, runner, normalizer, report contract, README를 구현했다.
4. `5 tests / 0 failures` GREEN을 확인했다.
5. PM finding을 canonical project lock, 필수 `WARM_RUNS`, DB identity, planner integrity, evidence classification, plan topology 계약으로 먼저 추가해 `11 tests / 5 pass / 6 fail` RED를 확인하고 test-only 커밋으로 남겼다.
6. 최소 수정 뒤 `11 tests / 11 pass` GREEN을 확인했다.
7. PM 2차 finding 8건을 test-only RED로 고정하고 artifact/anchor/source/schema/activity/vacuum/rejected-report/date 계약과 child-reap 경계를 보강해 `23/23` GREEN을 확인했다.
8. PM 3차 finding 4건은 `4 tests / 4 failures` RED 커밋 뒤 conditional cross-issue fail-closed, instance-wide activity, lock 직후/종료 Compose continuity, runtime-required sampling interval을 최소 구현해 전체 `27/27` GREEN을 확인했다.
9. 전체 diff 독립 리뷰의 NULL-state visibility, DB identity inspect bracket, long-interval SIGTERM 3건은 `7 tests / 4 pass / 3 fail` RED 커밋 뒤 최소 수정해 전체 `30/30` GREEN을 확인했다.
10. 후속 shutdown-bound finding은 `8 tests / 7 pass / 1 fail` RED 뒤 느린 fake sample 두 번을 observer 전용 grace가 포괄하도록 수정해 전체 `31/31` GREEN을 확인했다.
11. 최신 `origin/develop` `6796ed146244d8f3f5b5dd7048ebe16865084a97`의 #200/#201/#202/#206 drift는 신규 계약 `6/6 RED`로 먼저 고정했다. 공통 무결성 감사 확장에서는 10개 중 6개 RED를 확인한 뒤 #200 COFFEE ownership, #201 archive cutoff, #202 V11 RLS/JDBC role, #206 stable ordering, runtime-only target/image, PostgreSQL decimal-string bigint와 `pg_stat_statements` continuity, 50개 source hash와 최초 0600 rejection을 scenario-only로 보정해 전체 `41/41` GREEN을 확인했다.
12. 자체 전체-diff 리뷰에서 live/dead tuple 누적 counter 변화가 채택 gate에 연결되지 않은 gap을 `10 tests / 9 pass / 1 fail` RED로 재현했다. 모든 누적 counter를 BigInt로 비교하고 변화별 machine-readable reason을 중복 없이 남기도록 최소 수정해 `10/10`, 전체 `41/41` GREEN으로 전환했다.
13. #193 finding-zero production SQL source hash/shape와 16-case 3-query matrix가 없는 상태를 신규 Node 계약 `3/3 RED`로 고정했다. source-derived builder, immutable handoff manifest, 기존 unique index 중복/쓰기비용/partial 판단과 leading-wildcard 금지 계약을 최소 구현해 신규 계약 `3/3 GREEN`으로 전환했다.

## 7. 검증과 다음 작업

최신 develop 보정의 Node contract는 `41 tests / 41 pass`다. #192/#193/#195/#196/#197/#198/#199 현재 artifact는 모두 별도 사용자·PM approval evidence schema가 없어 pending이고 `automaticAdoption=false`다. 관련 Node syntax, Bash syntax, JSON 24-query parse, 50개 source hash, SQL read-only safety와 `git diff --check`만 수행하며 production Java/Flyway/dependency는 변경하지 않았다. 실제 DB/Docker/HTTP/k6/psql/EXPLAIN/ANALYZE baseline은 실행하지 않았고 상태는 계속 `scenario-ready / not-measured`다.

다음 단계는 7개 원 이슈가 실제 측정·채택된 뒤 정확한 per-issue artifact schema와 별도 사용자/PM 승인 증거를 #194에 연결하고, 실제 Hibernate SQL을 capture해 exact-current-production inventory를 별도 승인하는 것이다. 이후 승인된 1,000명 fixtureRunId, Compose target/image, `WARM_RUNS`, `ACTIVITY_SAMPLE_INTERVAL_MS`가 준비되고 다른 부하가 없는 PM 순차 측정 창에서 before plan만 수집한다. index/Flyway 구현과 성과 문장은 exact production 실행계획 evidence를 PM에 보고하고 별도 승인을 받은 이후에만 진행한다.
