---
project: FaithLog
type: devlog
issue: "#197"
status: scenario-ready
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - tdd
---

# #197 경건 제출과 데이터 정리 scheduler baseline 시나리오 준비

## 1. 작업 배경

주간 경건 제출의 7개 daily upsert와 retention cleanup의 무제한 일괄 처리 비용을 측정하기 전에, shared Docker와 운영 데이터에 영향을 주지 않는 실행 계약이 필요했다. 이번 세션 범위는 scenario 작성까지이며 seed, k6, scheduler, Docker, DB 실행과 production 최적화는 금지됐다.

## 2. 최종 설계 기준

- `datasetId`와 `fixtureRunId`를 분리한다.
- 경건 warmup/measured/rollback 사용자와 week를 분리하고 measured는 정확히 1,000명이다.
- runtime Access Token은 ignored report 또는 OS temp에 mode 600으로만 둔다.
- `BASE_URL`, 세 phase의 VUS/MAX_DURATION, TTL safety seconds는 승인 runtime 필수값이며 default를 두지 않는다.
- JWT 원문을 남기지 않고 exp/sub/userId/ACCESS type과 fixture coverage를 검사하며, 전체 승인 duration+safety보다 TTL이 짧으면 write 전에 거부한다.
- 경건 성공은 weekly 1행, daily 7행, expected amount PENALTY charge 1행과 `DEVOTION_RECORD` source uniqueness를 확인한다.
- rollback campus에는 활성 PENALTY 계좌가 없으며 400 이후 weekly/daily/charge가 모두 0행이어야 한다.
- 실행 당일 Asia/Seoul 날짜와 manifest `referenceDate`가 다르면 오래된 fixture로 보고 거부한다.
- retention은 actual Compose label이 `faithlog-perf-197-*`인 isolated 환경만 허용하고 shared/default Docker를 즉시 거부한다.
- retention도 승인 app/DB service label, lock 직후 immutable container identity, candidate SQL 전후 PostgreSQL current database/server/postmaster continuity를 통과해야 한다.
- retention reference instant는 명시적 `Z`/offset이 있는 RFC 3339 값만 허용하며, 연도 경계 weekly/daily FK blocker가 0건이어야 한다.
- 안전한 manual trigger/test path가 없으므로 retention은 expected candidate count의 read-only dry verification까지만 제공한다.
- scheduler는 disabled 상태여야 하고 실제 cleanup/recovery/FCM은 호출하지 않는다.
- actual Compose project/service와 app published port를 먼저 inspect하고, `/tmp/faithlog-performance-<actualComposeProject>.lock`으로 같은 stack의 다른 부하와 충돌시킨다.
- app/DB service 역할은 default 없는 승인 runtime 값과 exact 비교하고 잘못된 same-project service를 lock/DB/k6/write 전에 거부한다.
- warmup 뒤 measured 직전/직후 DB counter/planner/activity window가 오염되면 baseline 채택을 거부한다.
- 세 k6 phase 모두 exact 양의 정수 transaction, 양의 finite throughput, non-negative latency와 `p50 <= p95 <= p99 <= max`를 direct/`metric.values` shape에서 강제한다.
- CPU/RAM은 runtime 승인 interval/max gap, initial immutable app/DB container ID, strict timestamp/numeric sample, measured start/end coverage를 통과해야 한다.
- app/DB container ID/image ID/StartedAt/Compose identity와 PostgreSQL database/address/port/postmaster start를 initial, warmup 전, measured 직전·직후, final에 exact 비교한다.
- 8개 대상 table의 analyze/autoanalyze뿐 아니라 vacuum/autovacuum count와 timestamp도 measured 전후 exact stability를 요구한다.
- PostgreSQL bigint 누적 counter와 승인 signature delta는 decimal string으로 수집해 `BigInt`로 비교하고 external session의 `null`/잘못된 JSON type은 clean 0으로 인정하지 않는다.
- 실제 pgss snapshot은 boolean availability와 available/unavailable별 exact keys, statement inventory, reason/type을 강제하고 malformed truthy 값과 phase drift를 채택하지 않는다.

## 3. 구현 내용

- `performance/k6/issue-197` 독립 디렉터리
- k6 주간 제출 warmup/measured/rollback phase
- actual Compose project-keyed runner lock과 project/service/published port 확인
- app의 docker profile과 Compose-local PostgreSQL URL/username fail-closed 검증
- write 전 전체 cohort active user/membership/campus, fresh weekly/daily/source charge 0행, soft-delete되지 않은 success/rollback 계좌와 네 penalty rule 계산 금액 exact preflight
- runtime workload 범위와 JWT claim/잔여 TTL fail-closed validator
- direct/`metric.values` k6 summary 양쪽의 필수 metric/failure/transaction gate
- measured 직전/직후 PostgreSQL 인스턴스 전체 database counter, 대상 DB table counter, 전체 external session, analyze/autoanalyze/`n_mod_since_analyze`, optional `pg_stat_statements` delta와 contamination gate
- warmup 관측값을 학습하지 않는 사용자 승인 runtime exact signature, mode 0600 고정본/SHA-256, warmup/measured production-shaped table/query/application commit/rollback delta의 독립 attribution gate
- measured phase 전용 app/PostgreSQL CPU/RAM sampling 계약
- immutable app/DB identity와 measured-window coverage를 검증하는 resource evidence non-zero gate
- DB counter window 밖에서 수행하는 4개 runtime continuity checkpoint와 final series gate
- 8개 table의 strict vacuum/autovacuum timestamp/count evidence와 transient drift 거부
- weekly/daily/charge/rollback read-only SQL evidence
- isolated-only retention candidate count SQL과 exact expected count verifier
- scenario manifest schema, runtime credential guard, README
- 저장소 decision log와 resume metrics의 `scenario-ready / not-measured` 기록

production Java/API/권한/응답/오류/트랜잭션/Entity/DB/Flyway/의존성 변경은 없다.

## 4. TDD 기록

1. 실패 테스트 작성: production 변경 전에 scenario 안전·fixture·metric·correctness 정적 계약 8건을 작성했다.
2. 실패 확인: 필요한 Issue #197 scenario 파일 부재로 8건 모두 실패했다.
3. 최소 구현: 경건 write, DB evidence, retention dry verifier, runner와 문서를 추가했다.
4. 테스트 통과: 정적 계약과 fixture validator를 합쳐 13건이 통과했다.
5. 리팩토링: runtime credential mode 600, exact manifest field, shared load lock, scheduler disabled, 고정 report path, 당일 manifest, local DB identity, write 전 계좌/기존 rollback charge preflight, measured-only 자원 수집, retention literal prefix·RFC 3339 instant·annual FK blocker·non-fixture candidate guard를 보강했다.
6. PM finding RED: workload default, project-keyed lock, published-port target, exact fresh cohort preflight, contamination gate, measured DB delta, k6 direct metric shape, JWT TTL/subject coverage를 실행형 계약으로 추가해 `22 tests / 10 pass / 12 fail`을 확인했다.
7. PM finding GREEN: 위 여덟 계약을 최소 수정하고 동일 suite `22 tests / 22 pass`를 확인했다.
8. 독립 재리뷰 RED: production 계좌 lookup의 `deletedAtIsNull` 누락과 경계 사이에서 끝난 외부 read/commit attribution 누락을 회귀로 추가해 `23 tests / 21 pass / 2 fail`을 확인했다.
9. 독립 재리뷰 GREEN: 계좌 preflight에 `deleted_at IS NULL`을 맞추고 pre-warmup signature 대비 measured table/query/commit exact 비례 및 rollback 0 gate를 추가해 `23 tests / 23 pass`를 확인했다.
10. 성능 재리뷰 RED: warmup과 measured 양쪽에 비례 오염이 섞인 경우와 동일 DB 컨테이너의 다른 database 활동을 실행형 회귀로 추가해 대상 suite `11 tests / 9 pass / 2 fail`을 확인했다.
11. 성능 재리뷰 GREEN: runtime 필수 사용자 승인 exact activity signature를 도입해 두 window를 독립 검증하고, 인스턴스 전체 database counter/activity를 수집·거부하도록 보강해 전체 suite `25 tests / 25 pass`를 확인했다.
12. 최종 독립 리뷰 RED: production-shaped weekly/daily update, strict schema runtime validation, signature TOCTOU 고정, target DB normalized query 합산, runner 고정본 wiring을 회귀로 추가해 대상 suite `26 tests / 21 pass / 5 fail`을 확인했다.
13. 최종 독립 리뷰 GREEN: write table update exact 승인값, exact key/type/prefix 검증, mode 0600 freeze와 digest/identity 재검증, target `dbid` + normalized query 합산을 구현해 `26 tests / 26 pass`를 확인했다.
14. digest 결속 RED: 실행 중 고정 signature 파일을 같은 의미의 다른 canonical ordering으로 교체해도 사전 digest와 비교하지 않는 경로를 추가해 `16 tests / 15 pass / 1 fail`을 확인했다.
15. digest 결속 GREEN: freeze 시 SHA-256을 runner 변수/environment evidence에 보존하고 후반 attribution 전에 timing-safe exact 비교하도록 수정했다. 대상 계약 `27 tests / 27 pass`, fixture 포함 전체 `30 tests / 30 pass`를 확인했다.
16. PM 재리뷰 RED: 불가능한 k6 latency, 단일/타 container resource snapshot, runtime 교체, vacuum/autovacuum drift를 실행형 계약으로 추가해 대상 suite `20 tests / 16 pass / 4 fail`을 확인했다.
17. PM 재리뷰 GREEN: 세 phase 수학 gate, runtime 승인 sampling window, immutable app/DB/PostgreSQL identity continuity, 8개 table vacuum/autovacuum stability를 최소 구현해 전체 suite `35 tests / 35 pass`를 확인했다.
18. PM 독립 재리뷰 RED: `2^53` 경계의 DB/activity counter 정밀도 손실, external session `null` false-green, same-project wrong service target을 추가해 대상 suite `25 tests / 21 pass / 4 fail`을 확인했다.
19. PM 독립 재리뷰 GREEN: SQL decimal string 수집과 `BigInt` delta/signature, strict session schema, 승인 app/DB service exact binding을 최소 구현해 전체 suite `39 tests / 39 pass`를 확인했다.
20. retention/pgss 재리뷰 RED: retention wrong service, lock 뒤 container 교체, candidate SQL 뒤 PostgreSQL restart, 문자열 pgss availability를 분리해 대상 suite `29 tests / 25 pass / 4 fail`을 확인했다.
21. retention/pgss 재리뷰 GREEN: retention service/immutable/PostgreSQL continuity와 공통 pgss strict snapshot validator를 구현해 전체 suite `43 tests / 43 pass`를 확인했다.

## 5. 테스트 결과

- PM RED `node --test performance/k6/issue-197/tests/*.test.mjs`: 22 tests / 10 pass / 12 fail
- PM GREEN `node --test performance/k6/issue-197/tests/*.test.mjs`: 22 tests / 22 pass
- 재리뷰 RED: 23 tests / 21 pass / 2 fail
- 재리뷰 GREEN: 23 tests / 23 pass
- 성능 재리뷰 RED: 11 tests / 9 pass / 2 fail
- 최종 GREEN: 25 tests / 25 pass
- 최종 독립 리뷰 RED: 26 tests / 21 pass / 5 fail
- 최종 독립 리뷰 GREEN: 26 tests / 26 pass
- digest 결속 RED: 16 tests / 15 pass / 1 fail
- 최종 대상 GREEN: 27 tests / 27 pass
- 최종 전체 GREEN: 30 tests / 30 pass
- PM 재리뷰 RED: 20 tests / 16 pass / 4 fail
- PM 재리뷰 GREEN: 35 tests / 35 pass
- PM 독립 재리뷰 RED: 25 tests / 21 pass / 4 fail
- PM 독립 재리뷰 GREEN: 39 tests / 39 pass
- retention/pgss 재리뷰 RED: 29 tests / 25 pass / 4 fail
- retention/pgss 재리뷰 GREEN: 43 tests / 43 pass
- Node syntax 14 files: 성공
- Bash syntax 2 files: 성공
- JSON schema parse: 성공
- runner/SQL lifecycle·mutation 금지 패턴: 매칭 0건
- `git diff --check`: 성공
- seed/k6/scheduler/Docker/DB: 실행하지 않음
- Gradle test/build/asciidoctor: production/Gradle/REST Docs 변경이 없어 실행하지 않음

## 6. 고민한 부분

현재 retention service에는 cron을 바꾸지 않고 외부에서 안전하게 호출하여 `DataRetentionCleanupResult`와 timing을 받을 수 있는 경로가 없다. 임시 API나 production hook을 추가하면 이번 승인 범위를 넘으므로 dry verification에서 멈췄다.

DB query delta는 PostgreSQL 설정을 바꾸지 않고 이미 `pg_stat_statements`가 활성화된 경우만 수집한다. unavailable이면 이유를 기록하고 table/database delta는 필수로 남긴다. database-wide counter에는 observer read-only transaction도 포함되므로 exact repository call count로 과장하지 않는다.

## 7. 트러블슈팅

- 문제: retention timing을 지금 수집할 수 없음
- 원인: 승인된 isolated fixture와 safe manual trigger/test path가 없음
- 해결: shared Compose hard reject, dataset prefix, expected candidate count, no-trigger evidence를 먼저 고정
- 재발 방지: trigger가 승인되기 전 p50/p95/p99/max/throughput/failure 값을 만들지 않음

## 8. 다음 작업

- [ ] PM이 경건/retention fixture manifest와 실행 시점을 승인
- [ ] retention isolated fixture seed 승인
- [ ] safe manual trigger/test path 승인 또는 측정 불가 확정
- [ ] 실제 baseline 후에만 병목과 개선 후보 보고

## 9. 이력서 수치 상태

`scenario-ready / not-measured`. 실제 workload와 activity signature는 아직 사용자 승인 전이며, 실제 baseline, 개선률, 성과 문장은 아직 없다.

## 10. 2026-07-16 current-develop drift 보정

- 기준: `origin/develop` exact HEAD `6796ed146244d8f3f5b5dd7048ebe16865084a97`(#200/#201/#202/#206 포함), branch `fix/197-devotion-retention-baseline-current-develop`.
- two-session/one-load 정책에 따라 preparation은 issue-local scenario/test/validator/docs만 수행하고, 실제 Docker/DB/HTTP/k6/cleanup/scheduler는 PM exclusive measurement session까지 실행하지 않는다.
- #201 기본 archive visibility의 최근 1개월 cutoff와 retention의 전년도 `created_at` terminal 후보를 별도 fake/static correctness로 고정했다.
- #200 stale duty와 soft-deleted payment account에 연결된 UNPAID가 retention candidate가 아님을 고정했다.
- #202 V11 RLS를 JDBC correctness 근거로 사용하지 않고 실제 backend endpoint/direct-JDBC evidence가 필요함을 기록했다.
- runtime 승인 revision, image ID, app JAR/API-contract SHA-256과 Compose project/service, numeric loopback, workload/JWT, resource, DB session/maintenance, BigInt/pgss continuity를 fail-closed로 요구한다.
- TDD RED: current-develop drift 대상 7 tests 중 1 pass / 6 fail.
- 최소 GREEN 후 전체 issue-local Node tests: 50 tests / 50 pass.
- Node syntax, Bash syntax 2 files, JSON parse: 성공.
- production backend, Flyway, dependency, Gradle/REST Docs diff와 실제 측정은 0건이다.
- 상태는 계속 `scenario-ready / not-measured`이며 before/after 수치나 독립 개선 기여율을 주장하지 않는다.
- PM 공통 무결성 감사 RED: 7개 항목 중 2 pass / 5 fail. 실제 gap은 Redis runtime/resource continuity, Flyway applied identity, full Docker container ID, 최초 machine-readable rejection 보존이었다. decimal-string 탐색 1건은 테스트 표현 의존 false positive로 판별했다.
- 감사 GREEN: app/DB/Redis exact service·image·full container ID, 승인 DB/Redis port와 app target, PostgreSQL postmaster/Flyway version-script-checksum, Redis run ID/version/port를 pre/post-lock과 final에 연속 검증한다.
- resource evidence는 app/DB/Redis exact 3-role set, CPU percent, RAM bytes, cadence와 measured-window coverage를 요구한다.
- 최초 실패는 fixture-run별 fresh ignored/temp path에 mode 600 JSON으로 한 번만 기록하며 `automaticAdoption=false`; 같은 경로 재사용과 후속 overwrite를 거부한다.
- 기존 k6 v2 direct/values Counter/Rate/Trend 수학, exact count/failure 0/ordered latency, cumulative decimal-string BigInt, pgss availability continuity, fixture freshness 및 #200/#201/#202/#206 관련 경계는 중복 구현 없이 감사 테스트로 재확인했다.
- DB/Redis CLI가 컨테이너 내부 implicit Unix socket/default host를 사용할 수 있는 self-review gap을 RED로 고정하고, runtime-required numeric-loopback `DB_HOST`/`REDIS_HOST`와 exact address/port 검증으로 보정했다.
- devotion lock 전후 app project/service/published port와 DB project/service의 explicit continuity, retention candidate SQL의 `BEGIN TRANSACTION READ ONLY`를 self-review RED→GREEN으로 추가했다.
- 최종 검증: issue-local Node `58 tests / 58 pass`, Node syntax `19 files`, Bash syntax `2 files`, JSON schema parse `3 files`, `git diff --check` 성공. production/Flyway/dependency diff는 0이며 실제 Docker/DB/HTTP/k6/cleanup/scheduler는 실행하지 않았다.

## 11. 2026-07-16 current-develop handoff provenance 보정

- approved source 후보 `/private/tmp/FaithLog-perf-206-deploy`의 clean detached HEAD `6796ed146244d8f3f5b5dd7048ebe16865084a97`, Compose working directory, app image 생성 시각과 API tree digest를 결속했다.
- image OCI revision/API-contract label 부재는 limitation으로 기록하고, newest `%gD` `HEAD@{2026-07-16T13:20:28+09:00}` selector를 실제 checkout 시각으로 사용한다. `%cI` commit 시각과 empty reflog subject는 checkout 증거로 사용하지 않는다.
- credential path는 부모 environment에서 unset하고 validator/k6 child에만 전달한다.
- fixture report root는 exclusive-create를 유지하며 fake/static invocation은 optional `PERF_REPORT_ROOT`로 분리한다. target/workload fallback은 추가하지 않았다.
- devotion 추천 fresh ID와 retention 추천 fresh ID는 서로 다르며 사용자 승인 전 실행값이 아니다. shared `faithlog-frontend-latest`에서는 retention을 즉시 거부한다.
- 상태는 계속 `scenario-ready / not-measured`다. 실제 Docker/DB/HTTP/k6/scheduler/cleanup과 성능 수치 측정은 수행하지 않았다.
- detached reflog와 report-root suite finding까지 보정한 최종 issue-local Node 계약은 `62 tests / 62 pass`다.

## 12. 2026-07-16 #208 공통 harness 호환성 감사 보정

- installed `k6 v2.0.0`의 no-HTTP synthetic summary에서 custom Rate가 direct shape `{passes, fails, value}`이고 Counter가 `{count, rate}`임을 확인해 fixture로 고정했다.
- test-only RED는 Rate의 `passes` 또는 `fails` 누락, rate/value 누락·불일치, Counter와 Rate total 불일치, 음수·소수·unsafe integer를 기존 validator가 충분히 거부하지 못하는 반례를 재현했다.
- GREEN은 warmup/measured/rollback의 phase-specific transaction Counter를 runtime expected total에 exact 결속하고, `passes + fails = Counter total`과 zero-failure의 `rate|value=0`, `passes=0`, `fails=expected total`을 강제한다. direct metric과 `metric.values`, `rate`/`value` one-of를 지원하며 둘 다 있으면 exact 일치해야 한다.
- focused 계약과 issue-local 전체 Node 계약은 `62 tests / 62 pass`다. synthetic은 HTTP 요청 0건이며 실제 devotion/retention 부하, Docker, DB, scheduler, cleanup은 실행하지 않았다.
- production/API/Flyway/Gradle dependency 변경과 성능 수치 주장은 0건이다. 상태는 계속 `scenario-ready / not-measured`다.

## 13. 2026-07-17 devotion actual-before prepare 계층

- 기존 runner는 fresh 1,002명 fixture와 token manifest를 요구하면서 생성 경로가 없었고, fresh run 전에는 알 수 없는 DB-wide commit/query exact activity signature도 요구했다. test-only RED에서 이 두 blocker와 prepare wrapper/module/namespace SQL 부재를 7/7 실패로 고정했다.
- 단일 경로만 추가했다: namespace read-only 0행 확인 → prepare report/secret namespace 배타 예약 → public/admin create-only API seed → 1,002명 최종 login/token manifest → exact devotion preflight → installed k6 inspect. calibration dataset, duplicate workload, cleanup/reuse, warmup 비례 추정은 없다.
- prepare fake full-run은 관리자 login 1, campus 2, PENALTY account 1, penalty rule 4, signup 1,002, service-admin membership 1,002, fixture login 1,002의 exact 3,014 HTTP 호출을 검증한다. raw password/access/refresh token/Authorization은 report/log/argv에 기록하지 않고 credentials만 runtime-only mode 600에 둔다.
- partial failure는 최초 안전한 stage/status/code와 완료 count만 receipt에 남기며 `cleanupAllowed=false`, `reuseAllowed=false`, `automaticAdoption=false`다. app/PG/Redis/source identity와 effective `FAITHLOG_SCHEDULER_ENABLED=false`, common project lock, pre/post-lock/final continuity를 유지한다.
- measured business row와 HTTP/custom Counter는 exact로 유지한다: weekly 1,000, daily 7,000, charge 1,000, rollback persisted 0. DB-wide/table/pgss 누적치는 BigInt monotonic, 대상 insert exact, 나머지 table write 0, rollback 0, external active session 0, planner/maintenance continuity의 supporting evidence로 분리했다. shared-stack 결과는 clean이어도 `conditional-not-adoptable`이다.
- installed `k6 v2.0.0` no-HTTP synthetic에서 Counter `{count:1}`과 Rate `{rate:0,passes:0,fails:1}`을 재확인했다. 최종 issue-local Node 계약은 `71 tests / 71 pass`이며 Node/Bash/JSON/static/diff check가 성공했다.
- production Java/API/Flyway/Gradle dependency 변경과 실제 Docker/DB/HTTP/devotion load/retention trigger/scheduler/cleanup은 0건이다. 상태는 계속 `scenario-ready / not-measured`다.

## 14. 2026-07-17 current API contract digest inventory 보정

- 기존 source provenance는 pre-refactor Java package path 세 개가 revision tree에 없어도 migration tree 하나가 non-empty라 통과했고, 결과적으로 경건 API/service, 알림, scheduler/service drift가 digest에서 빠졌다.
- test-only RED로 required path별 revision-tree 존재와 devotion/notification/batch scheduler/batch service/migration inventory를 고정했다.
- current path 다섯 개를 각각 fail-closed로 확인한 뒤 combined 154-entry inventory를 해시한다. approved revision `6796ed146244d8f3f5b5dd7048ebe16865084a97`의 corrected digest는 `625bc9e8f83561c67f8f8d5bc26c68bdf172c191d57fec01aca4423e7c2b2a9d`이며 기존 migration-only digest는 승인값으로 사용하지 않는다.
- focused provenance 계약 12/12와 issue-local 전체 Node 계약 73/73, Node/Bash/JSON/diff check가 성공했다.
- production/Docker/DB/HTTP/k6 실행과 성능 수치 변경은 0건이다. 상태는 계속 `scenario-ready / not-measured`다.

## 15. 2026-07-17 fresh C PostgreSQL inet preflight 보정

- fresh C는 fixture API write 전 runtime identity에서 PostgreSQL actual `127.0.0.1/32`와 explicit `DB_HOST=127.0.0.1`의 문자열 비교가 달라 rejected됐다. fixture HTTP와 k6 load는 0이고 임시 ADMIN USER는 원복됐다. C evidence는 보존하며 cleanup/reuse하지 않는다.
- test-only RED는 IPv4 `127.0.0.1/32`, IPv6 `::1/128`·expanded loopback과 `/24`·`/64`, 다른 loopback/IP, 외부 주소, CIDR-bearing runtime input 반례를 고정했다.
- evidence actual 문자열은 그대로 저장하고 비교 시에만 IPv4 `/32`, IPv6 `/128` host CIDR과 IPv6 spelling을 canonicalize한다. runtime input은 계속 exact numeric `127.0.0.1|::1`만 허용한다.
- 다음 namespace는 fresh D다. 개발 세션에서는 Docker/DB/API/k6를 실행하지 않고 scenario/test/docs만 수정했다.
- focused runtime identity 계약 13/13과 issue-local 전체 Node 계약 74/74, Node/Bash/JSON/diff check가 성공했다.

## 16. 2026-07-17 fresh D installed k6 v2 inspect 보정

- D (`PERFORMANCE_1000_20260717_DEVOTION_197_D` / `ISSUE197_20260717_DEVOTION_BEFORE_D`)는 runtime/namespace/API seed/DB preflight를 통과했고 preparation receipt는 `prepared`, HTTP 3,014, campus 2/account 1/rule 4/user 1,002/membership 1,002/token 1,002, expected penalty 2,250을 기록했다.
- 마지막 installed k6 inspect는 shell env assignment만으로는 k6 v2 `__ENV`가 채워지지 않아 manifest filename이 비었고 `open()` exit 107로 rejected됐다. measured k6 load는 0이며 임시 ADMIN USER는 원복됐다. D report/fixture는 read-only 보존하고 cleanup/reuse하지 않는다.
- 실행형 RED는 같은 installed k6에서 assignment-only inspect exit 107, explicit `-e` inspect exit 0을 재현했다. no-HTTP synthetic run도 explicit `-e`로 fixture와 credential 파일을 읽되 HTTP metric과 token 원문 출력이 없음을 검증했다.
- prepare inspect와 baseline warmup/measured/rollback 모두 `BASE_URL`, `FIXTURE_MANIFEST`, `CREDENTIALS_FILE`, `PHASE`, `VUS`, `MAX_DURATION`을 explicit `-e`로 전달한다. argv에는 runtime-only file path만 있고 raw password/JWT는 없다. workload, threshold, correctness, rollback, adoption gate는 완화하지 않았다.
- 다음 candidate는 fresh E (`PERFORMANCE_1000_20260717_DEVOTION_197_E` / `ISSUE197_20260717_DEVOTION_BEFORE_E`)다. 개발 세션에서는 E 예약이나 Docker/DB/API/actual load를 실행하지 않는다.
- installed inspect/no-HTTP synthetic을 포함한 issue-local Node 계약은 75/75이며 Node/Bash/JSON/diff check가 성공했다. 상태는 계속 `scenario-ready / not-measured`다.

## 17. 2026-07-17 fresh E resource sampler cadence 보정

- E (`PERFORMANCE_1000_20260717_DEVOTION_197_E` / `ISSUE197_20260717_DEVOTION_BEFORE_E`)는 fixture prepare와 measured 1,000건을 완료했고 HTTP/check/custom failure는 0이었다.
- measured window는 `18:23:31.940Z`~`18:23:34.040Z`였지만 raw resource sample은 6행뿐이었다. 기존 runner가 blocking `docker stats --no-stream`을 app→database→Redis 순서로 따로 호출해 약 2초씩 소비했고, app same-role cadence가 승인 max gap 2초를 넘어 stage `measured`에서 rejected됐다.
- p50 42.58ms, p95 101.28ms, p99 154.74ms, max 196.32ms, throughput 592.299163/s는 non-adoptable E의 diagnostic-only 값이다. baseline이나 성과 수치로 사용하지 않는다.
- E report/fixture는 read-only 보존하고 credentials는 제거됐으며 임시 ADMIN USER는 원복됐다. cleanup/reuse하지 않는다.
- sampler는 pre-window 단일 multi-container no-stream snapshot과 measured 동안 하나의 continuous multi-container stream으로 변경했다. 각 snapshot은 승인된 app/DB/Redis full ID가 정확히 한 번씩 있고 한 timestamp를 공유한다. snapshot 시각은 strictly increasing이며 stop marker 뒤 다음 완전한 snapshot이 measured-end final boundary가 된다.
- ID/row/schema mismatch, incomplete/premature stream end, capture failure, 승인 max gap 이내 snapshot 미도착은 non-zero다. 1초 interval/2초 max gap, boundary 및 correctness/adoption gate는 완화하지 않았다.
- 다음 candidate는 fresh F (`PERFORMANCE_1000_20260717_DEVOTION_197_F` / `ISSUE197_20260717_DEVOTION_BEFORE_F`)이며 개발 세션에서는 예약하거나 실행하지 않는다.
- E-shaped cadence와 multi-container snapshot/stream fake를 포함한 issue-local Node 계약은 77/77이며 Node/Bash/JSON/diff check가 성공했다. 상태는 계속 `scenario-ready / not-measured`다.

## 18. 2026-07-17 fresh F Docker stats ANSI framing 보정

- F (`PERFORMANCE_1000_20260717_DEVOTION_197_F` / `ISSUE197_20260717_DEVOTION_BEFORE_F`)는 fixture prepare와 measured 1,000건을 완료했고 failure는 0이었다.
- installed Docker streaming output은 첫 행 full ID 앞에 CSI cursor-home `ESC[H`, 모든 행 끝에 erase-to-EOL `ESC[K`를 붙였다. no-stream에는 ANSI가 없었다. strict parser는 row 0 full ID를 거부했고 sampler는 measured 종료 전에 non-zero로 끝났다.
- p50 79.56ms, p95 222.09ms, p99 364.84ms, max 537.42ms, throughput 300.159325/s는 non-adoptable F의 diagnostic-only 값이다. baseline이나 성과 수치로 사용하지 않는다.
- F report/fixture는 read-only 보존하고 credentials는 제거됐으며 임시 ADMIN USER는 원복됐다. cleanup/reuse하지 않는다.
- runner identity format은 `.ID`를 명시한다. parser는 snapshot이 완전히 control-free이거나 row 0 시작 `ESC[H` + 세 행 끝 `ESC[K`의 exact framing일 때만 해당 control을 제거한다. unknown/different/malformed CSI, mid-field/control 잔존, mixed framing, 주변 text는 모두 거부하며 그 뒤 full ID/CPU/RAM strict 검증은 유지한다.
- current `faithlog-frontend-latest`의 app/PostgreSQL/Redis를 대상으로 one-snapshot installed Docker read-only smoke를 실행해 exact full IDs 3개, app/database/redis, shared timestamp를 확인했다. lifecycle/DB/API/k6 mutation은 0이다.
- marker/final boundary/stall deadline/orphan cleanup과 1초/2초 cadence, 모든 correctness/adoption threshold는 변경하지 않았다.
- 다음 candidate는 fresh G (`PERFORMANCE_1000_20260717_DEVOTION_197_G` / `ISSUE197_20260717_DEVOTION_BEFORE_G`)이며 PM review 전 실행하지 않는다.
- F ANSI shape와 unknown/mid-field/malformed framing 반례를 포함한 issue-local Node 계약은 78/78이며 Node/Bash/JSON/diff check가 성공했다. 상태는 계속 `scenario-ready / not-measured`다.

## 19. 2026-07-17 fresh G Docker stats recurring display protocol 보정

- G (`PERFORMANCE_1000_20260717_DEVOTION_197_G` / `ISSUE197_20260717_DEVOTION_BEFORE_G`)는 fixture prepare와 measured 1,000건을 완료했고 failure는 0이었다.
- 실제 연속 stream은 initial `ESC[H`와 data-row `ESC[K` suffix뿐 아니라 snapshot 사이 standalone `ESC[K`, recurring first-row `ESC[JESC[H`를 반복했다. 기존 3-physical-line grouping은 separator를 다음 row 0으로 오인해 final boundary 전에 non-zero로 끝났다.
- p50 43.42ms, p95 102.72ms, p99 160.66ms, max 249.91ms, throughput 596.255989/s는 non-adoptable G의 diagnostic-only 값이다. baseline이나 성과 수치로 사용하지 않는다.
- G report/fixture는 read-only 보존하고 credentials는 제거됐으며 임시 ADMIN USER는 원복됐다. cleanup/reuse하지 않는다.
- parser는 exact state machine으로 initial first-row `ESC[H`, 매 data-row `ESC[K`, complete snapshot 사이 standalone `ESC[K` 하나, recurring first-row `ESC[JESC[H`만 허용한다. separator/prefix 누락·중복·순서 변경, `ESC[2J`, unknown/mid-field control, malformed framing은 모두 거부한다.
- current app/PostgreSQL/Redis full ID를 대상으로 installed Docker read-only stream smoke를 실행했다. `stream-samples`가 3 snapshot/9행을 수집하고 두 snapshot 뒤 stop marker, 세 번째 final boundary, 0.497/0.501초 cadence와 exact ID를 strict validator로 확인했다. Docker lifecycle/DB/API/HTTP/k6 mutation은 0이다.
- marker/deadline/maxGap과 1초/2초 cadence, identity/resource/correctness/adoption threshold는 변경하지 않았다.
- exact recurring/malformed framing 반례를 포함한 issue-local Node 계약은 79/79이며 Node/Bash/JSON/diff check가 성공했다. 다음 candidate는 fresh H (`PERFORMANCE_1000_20260717_DEVOTION_197_H` / `ISSUE197_20260717_DEVOTION_BEFORE_H`)이고 이 개발 세션에서는 예약하거나 실행하지 않는다. 상태는 계속 `scenario-ready / not-measured`다.

## 20. 2026-07-17 fresh H direct cardinality와 누적 통계 publication 분리

- H (`PERFORMANCE_1000_20260717_DEVOTION_197_H` / `ISSUE197_20260717_DEVOTION_BEFORE_H`)는 prepare, warmup 1, measured 1,000을 완료했고 HTTP/check/custom failure는 0이었다. 첫 rejection은 stage `measured`, exit 1, `2026-07-16T19:08:52.879Z`이고 rollback은 실행되지 않았다.
- direct read-only join은 campus 82, measured week `2026-07-27`에서 weekly 1,000/distinct users 1,000, weekly source에 연결된 daily 7,000/distinct users 1,000, PENALTY/DEVOTION_RECORD charge 1,000/distinct users 1,000/각 2,250원/합계 2,250,000원을 확인했다. success campus 전체 devotion charge 1,001은 warmup 1 + measured 1,000이다.
- 같은 window의 PostgreSQL cumulative publication은 weekly/daily/charge insert 595/4,165/595와 DB `tup_inserted=5,355`만 보였고 users update 9와 다른 database read delta도 함께 증가했다. 기존 exact/zero gate가 이를 오염으로 처리해 H를 거부했다.
- p50 46.86ms, p95 103.30ms, p99 130.02ms, max 189.19ms, throughput 549.373879/s는 non-adoptable H의 diagnostic-only 값이다. baseline이나 성과 수치로 사용하지 않는다.
- fixture-owned direct SQL을 measured 뒤·rollback 전에 실행해 exact week/user/daily/source/amount/uniqueness/campus cardinality를 검증하고, 같은 SQL을 rollback 뒤 다시 실행해 persisted weekly/daily/charge 0을 검증한다. direct query 전후 app/PostgreSQL/Redis runtime identity도 exact 비교한다.
- `pg_stat_database`/`pg_stat_user_tables`/`pg_stat_statements`는 strict BigInt schema와 monotonicity를 유지하되 양수 delta를 `sourceUnattributedDeltas`로 기록하는 supporting-only evidence다. sleep/tolerance/subtraction/background estimate/publication ratio 추정은 없다. malformed/regression/reset/planner/maintenance/external session/runtime 교체는 계속 fail-closed다.
- H report/fixture는 영구 read-only/non-reusable이고 credentials/runtime secret은 제거됐으며 임시 ADMIN은 USER로 원복됐다. 다음 candidate는 fresh I (`PERFORMANCE_1000_20260717_DEVOTION_197_I` / `ISSUE197_20260717_DEVOTION_BEFORE_I`)다. 이 개발 세션에서는 Docker/DB/API/HTTP/k6를 실행하지 않는다.

## 21. 2026-07-17 fresh I rollback fixture rule ownership 보정

- I (`PERFORMANCE_1000_20260717_DEVOTION_197_I` / `ISSUE197_20260717_DEVOTION_BEFORE_I`)는 prepare, warmup 1, measured 1,000, measured direct cardinality와 runtime continuity를 통과했다. rollback request는 HTTP success-class response를 반환해 expected `400`/`BILLING_REQUIRED_PAYMENT_ACCOUNT_MISSING`/`success=false` check 0/3, custom failure 100%, k6 exit 99로 stage `rollback`에서 rejected됐고 final persisted-row gate는 미도달했다.
- current develop의 `WeeklyDevotionCommandService`는 active-rule 계산 합계가 0이면 charge creation과 active payment-account 조회 전에 성공 반환한다. I prepare는 penalty rule 4개를 success campus에만 만들고 rollback campus에는 계좌와 rule을 모두 만들지 않았으므로, missing-account branch를 기대한 scenario가 stale했다. production 서버 결함이 아니다.
- J부터 동일한 네 rule을 success와 rollback campus에 각각 create-only로 만들고, active PENALTY account는 success 1/rollback 0을 유지한다. preflight는 campus별 rule count 4, rule type/calculation pair 0 invalid, 동일 positive expected amount 2,250을 exact 검증한다.
- unchanged rollback request는 weekly 1행/daily 7행/submit을 같은 transaction 안에서 만든 뒤 positive charge 생성 단계의 missing-account 예외에 도달해야 한다. 응답 400/error code/success=false와 final direct SQL weekly/daily/charge persisted 0을 모두 통과해야 rollback proof가 성립한다. 계약을 완화하지 않았다.
- prepare 예상치는 rule 4/API 3,014에서 rule 8/API 3,018로 바뀐다. I metrics p50 50.14ms, p95 110.04ms, p99 145.10ms, max 187.10ms, throughput 525.637993/s는 diagnostic-only이며 baseline/성과가 아니다. I evidence는 read-only/non-reusable이고 next candidate는 fresh J (`PERFORMANCE_1000_20260717_DEVOTION_197_J` / `ISSUE197_20260717_DEVOTION_BEFORE_J`)다.
- 개발 세션에서는 Docker/DB/API/HTTP/k6를 실행하거나 I를 정리하지 않았다. production/Flyway/dependency 변경도 없다.

## 22. 2026-07-17 fresh J conditional before와 weekly bulk load

- J (`PERFORMANCE_1000_20260717_DEVOTION_197_J` / `ISSUE197_20260717_DEVOTION_BEFORE_J`)는 warmup 1, measured 1,000 failure 0, rollback `400 BILLING_REQUIRED_PAYMENT_ACCOUNT_MISSING`, rollback weekly/daily/charge persisted 0을 모두 통과했다.
- measured direct SQL은 weekly 1,000, daily 7,000, PENALTY/DEVOTION_RECORD charge 1,000, duplicate 0, 각 2,250원/합계 2,250,000원을 exact 확인했다. p50 65.0935ms, p95 145.86005ms, p99 180.06974ms, max 272.145ms, throughput 400.1357260382722/s다.
- app max CPU/RAM은 314.19%/715,548,262 bytes, DB는 163.31%/288,568,115 bytes, Redis는 6.77%/21,820,867 bytes다. cumulative DB/table/pgss는 publication lag가 있는 supporting-only evidence이며 병목 SQL 횟수로 해석하지 않는다.
- shared-stack 분류는 `conditional-not-adoptable`, `automaticAdoption=false`다. J evidence/report는 영구 read-only/non-reusable이며 수정·삭제·cleanup하지 않는다.
- current source call graph는 weekly submit마다 daily 날짜별 조회 7회와 summary 재조회 1회를 수행했다. focused RED에서 이를 재현한 뒤 daily 7행을 한 번 조회해 `recordDate` Map으로 upsert하고 누락 행만 `saveAll` 한 번으로 전달하도록 변경했다.
- static repository daily read 계약은 요청당 8회에서 1회로 줄었지만 identity-backed 7행의 실제 insert/update SQL 감소나 latency/CPU 개선은 주장하지 않는다. API, 권한, weekly lock, transaction/rollback, 벌금 amount/source/account snapshot, daily/weekly correctness는 유지한다.
- frontend/Flyway/index/dependency 변경은 없다. after는 수정 서버를 별도 integration runtime에 올린 뒤 PM 단일 load로 측정하며, index는 #194 EXPLAIN 근거 이후 별도 판단한다.
