---
project: FaithLog
type: devlog
issue: "#199"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - before
---

# #199 관리자 대시보드 집계 before 시나리오

## 1. 작업 배경

관리자 대시보드 summary는 멤버 상태, 주간 경건 제출, 미납 벌금·커피 청구, 투표와 응답 누락을 한 응답으로 집계한다. production 집계 쿼리를 변경하기 전에 공통 1,000명 데이터셋에서 재현 가능한 before 증거를 수집할 시나리오만 준비했다.

## 2. 현재 상태

`scenario-ready / not-measured`

baseline 채택 상태는 `conditional-not-adoptable`이다. 현재 승인된 공유 stack evidence는 measured 전후 `pg_stat_activity` 경계 snapshot뿐이어서 그 사이에 시작·종료한 짧은 외부 요청을 완전히 검출한다고 주장하지 않는다. 승인된 continuous provenance 또는 격리 방식 전에는 runner가 evidence를 수집한 뒤 non-zero로 종료한다.

- seed/k6/Docker/DB 실행 0건
- 실제 latency, throughput, failure, CPU/RAM, DB baseline 수치 0건
- production Java/API/권한/응답/ErrorCode/트랜잭션/Entity/DB/Flyway/의존성 변경 0건
- 공통 fixture 생성·수정·삭제 0건
- push/PR/merge 0건

## 3. 실제 API와 프론트 진입 계약

- `GET /api/v1/admin/campuses/{campusId}/dashboard/summary`
- 선택 query `weekStartDate=YYYY-MM-DD`; 명시 시 월요일만 허용
- service `ADMIN` 또는 대상 캠퍼스 ACTIVE `MINISTER`/`ELDER`/`CAMPUS_LEADER` 허용
- 일반 MEMBER, 다른 캠퍼스 관리자, global MANAGER-only는 `403 ADMIN_DASHBOARD_ACCESS_FORBIDDEN`

프론트 `develop` `aba1ab07bcb54c1df85ecf53238f4cb0484c2df3`의 초기 진입은 login 뒤 `users/me`와 `campuses/me`를 병렬 호출하고, 관리자 화면에서 dashboard·members·duty assignments·prayer board·invite code 요청을 시작한다. #199 k6 setup은 세션 진입까지만 재현하고 measured 구간은 dashboard summary 하나로 격리한다.

## 4. Fixture와 실행 안전 계약

- 공통 데이터셋 `datasetId`와 #199 mode별 `fixtureRunId`를 분리한다.
- `empty`, `small`, ACTIVE member 정확히 1,000명인 `thousand` 중 사용자가 runtime에 명시한 중복 없는 mode만 선택 순서대로 실행한다. default 선택은 없다.
- `thousand`는 devotion/penalty/coffee/meal/poll/prayer 공통 fixture manifest의 `fixtureRunId`를 참조하며 #199가 seed를 중복 수행하지 않는다.
- credential은 runtime environment에서만 받고 manifest/report/git에 저장하지 않는다.
- app/PostgreSQL/Redis의 실제 Compose project/service label을 credential bootstrap 전에 읽고, project가 모두 같을 때만 `/tmp/faithlog-performance-${project}.lock`을 원자 획득한다. 같은 project의 다른 성능 이슈가 lock을 보유하면 시작하지 않는다.
- `BASE_URL`, `APP_CONTAINER`, `POSTGRES_CONTAINER`, `REDIS_CONTAINER`는 default 없는 runtime 필수 승인 target이다. 선택에 쓰이지 않는 `CONTAINER_ALIAS`는 optional evidence-only다.
- manifest의 승인 app/PostgreSQL/Redis service label과 app container port를 실제 inspect 결과와 exact 비교한다. `BASE_URL`은 `localhost`가 아니라 numeric loopback을 사용하고 선택 address family와 호환되는 published binding이 정확히 하나이며 port가 일치할 때만 실행한다. 정상 IPv4/IPv6 dual-stack pair는 선택 family별 하나이면 허용한다.
- 공통 lock 획득 후 최초 immutable identity에서 endpoint port/address family와 project/service를 다시 검증한다. 각 mode measured 전후에는 세 container의 ID/image ID/ref/StartedAt/Compose config hash, app published ports와 PostgreSQL postmaster identity를 최초 값과 exact 비교한다.
- shared Docker lifecycle `up/build/restart/down/rm/prune`은 runner 범위에 없다.
- 각 mode 시작 시 warmup token을 발급해 DB/API context 전에 warmup duration+승인 safety를 덮는지 검사하고, warmup 종료 뒤 measured 직전에 fresh JWT를 다시 발급해 measured duration+safety를 검사한다. token 값은 저장·출력하지 않고 mode 종료 즉시 비운다.
- 기존 mode report directory가 있으면 stale 파일을 삭제·덮어쓰지 않고 fail closed한다.

## 5. 측정·정확성 계약

mode별 warmup과 measured를 분리하고 p50/p95/p99/max, throughput, failure rate를 기록한다. cache reset을 하지 않으므로 첫 관찰을 cold-cache 결과로 부르지 않는다.

응답은 member active/inactive/admin count, devotion submitted/missing/rate, `UNPAID` PENALTY/COFFEE amount·member total, non-MEAL OPEN/recently CLOSED poll count, OPEN poll별 response count와 aggregate missing count를 exact match로 검증한다. campus-scoped manager가 isolation campus 조회 시 403인지도 확인한다.

warmup과 measured 모두 failure rate 0, request count 양의 safe integer, throughput 양의 finite, latency finite/non-negative와 `p50 <= p95 <= p99 <= max`를 채택 게이트로 강제하되 사용자 미승인 latency threshold는 만들지 않는다.

Docker CPU/RAM 전후 snapshot과 PostgreSQL database/table counter, row count, exact aggregate, optional `pg_stat_statements`, planner settings, analyze/autoanalyze/vacuum/autovacuum 상태를 read-only evidence로 수집한다. Docker resource gate는 before/after mode와 boundary, app/PostgreSQL/Redis full container ID/name, exact component set을 검사한다. CPU는 multi-core의 100% 초과를 허용하면서 finite/non-negative를, RAM은 safe numeric range와 positive limit, `used <= limit`, `0 <= percent <= 100`을 강제하며 malformed/mixed/모순 evidence를 contaminated로 차단한다. 값은 경계 snapshot일 뿐 continuous/peak로 해석하지 않는다. correctness/context SQL과 login/session/isolation traffic은 pure pre/post counter 구간 밖에서만 실행하고, measured k6 setup은 HTTP 0건으로 고정한다. DB machine-readable evidence의 OPEN poll별 실제 `pollId/responseCount` 집합과 aggregate missing을 manifest와 exact 비교한다. external activity와 실제 Compose label도 환경 보고서에 남긴다.

DB window gate는 `EXTERNAL_ACTIVITY=none`, 현재 observer PID를 제외한 non-idle `pg_stat_activity` 0, required table/planner set exact, capturedAt 순서, stats reset 없음, counter monotonic/table delta, planner와 analyze/autoanalyze 불변을 강제한다. 같은 observer application name의 다른 session도 외부로 집계한다. database identity, 모든 counter, table stability field, planner setting/source/context는 엄격한 schema로 검사해 null/빈 문자열/누락을 0 또는 동일값으로 허용하지 않는다. counter는 decimal string/BigInt로 delta를 계산해 큰 누적값의 정밀도를 보존한다. planner evidence는 observer psql session 범위이며 measured app-session planner state를 증명한다고 해석하지 않는다. 누락·역행·reset·외부 활동이면 contaminated이고, 깨끗한 경계 snapshot도 중간 활동을 완전 증명하지 못하므로 conditional/non-adoptable이다.

`pg_stat_database` database-wide delta에는 observer snapshot 자체의 read-only transaction/tuple overhead가 포함될 수 있으므로 exact dashboard query count로 해석하지 않는다. `pg_stat_user_tables` app-table delta는 snapshot이 application table을 직접 읽지 않는다는 별도 경계로 해석하며, 이 세 가지 정책을 counter JSON의 `observerOverhead` metadata로 남긴다.

## 6. TDD 기록

1. production controller/authorization, 실제 프론트 순서, mode/fixture, metric/correctness, runner lock/Compose label, read-only DB evidence, ignored report 계약 테스트를 먼저 작성했다.
2. 구현 파일이 없어 `8 tests / 8 failures` RED를 확인하고 test-only commit으로 남겼다.
3. issue-local manifest, k6, exact verifier, sequential runner, DB evidence, README를 구현했다.
4. 초기 Node contract `8 tests / 0 failures`, Node/Bash syntax, JSON parse, SQL read-only 정적 검사와 `git diff --check` GREEN을 확인했다.
5. PM 독립 리뷰에서 실패 요청 채택 가능성, measured DB counter에 사전 검증/setup traffic 혼입, OPEN poll별 DB count 미대조 3건을 찾았다.
6. 신규 실행형 계약은 기존 8건을 유지한 채 `11 tests / 3 failures` RED였다. runtime token bootstrap, k6 summary 채택 validator, pure DB counter 분리, machine-readable DB correctness exact validator를 적용한 뒤 `11 tests / 0 failures` GREEN으로 고정했다.
7. PM 재리뷰에서 cross-issue lock 불일치, 세 mode 단일 토큰의 1,800초 만료 위험, DB-wide counter observer overhead 해석 누락을 재현했다. 기존 11건을 포함한 계약은 `14 tests / 5 failures` RED였고, 같은 Compose project 검증/공통 project lock, 30분 초과 fake orchestration의 mode별 토큰 발급, DB-wide/app-table 해석 metadata 적용 후 `14 tests / 0 failures` GREEN이 됐다.
8. 다음 PM 재리뷰의 endpoint 결속, JWT 수명, activity/planner/analyze, counter delta, stale report, mode default 6건은 전체 `21 tests / 10 failures`와 activity control targeted `1 failure` RED로 재현했다. published-port/service identity, measured fresh JWT exp, machine DB window gate, 신규 report directory, runtime 필수 mode 적용 후 `21 tests / 0 failures` GREEN으로 고정했다.
9. 4차 PM 재리뷰의 measured 중간 외부 요청 blind spot, malformed DB evidence false-green, runtime identity replacement 3건은 targeted `6 selected / 5 failures` RED로 재현했다. same-name session 집계, strict DB schema, immutable container/PostgreSQL continuity를 추가했다. 완전한 외부 provenance는 현재 승인 범위에 없으므로 baseline adoption은 의도적으로 conditional/non-adoptable로 유지한다.
10. 전체 diff 자체 리뷰에서 JSON `null` 응답, localhost/wildcard address-family false binding, lock 전 target identity TOCTOU, bigint counter 정밀도, Docker CLI password argv, observer planner 범위 과장, conditional 상태 메시지와 독립 회귀 계약을 `7 failures` RED로 추가 확인했다. numeric loopback/post-lock immutable target 재검증, runtime-only environment 전달, decimal string/BigInt delta와 observer-session planner context로 보강했고 최신 전체 계약은 `27 tests / 0 failures` GREEN이다.
11. 5차 PM 재리뷰의 fractional request count/역전 percentile, vacuum/autovacuum drift, raw Docker CPU/RAM evidence, warmup JWT TTL 4건은 targeted `6 tests / 6 failures` RED였다. safe integer/percentile order, vacuum strict stability, exact resource identity/mode/boundary gate, warmup duration+safety TTL gate 적용 후 전체 `31 tests / 0 failures` GREEN으로 고정했다.
12. 6차 PM 재리뷰의 dual-stack published port false rejection, 모순된 RAM evidence, PostgreSQL/Redis 암묵 target 3건은 targeted `3 tests / 3 failures` RED였다. address-family-compatible binding exact 선택, RAM 일관성/safe range, 세 container runtime-required target을 적용한 뒤 전체 `33 tests / 0 failures` GREEN으로 고정했다.

## 7. 다음 작업

- PM이 공통 fixture 준비 상태, 다른 활동 중지, 부하 강도·시간과 continuous provenance/격리 방식을 승인한 뒤에만 adoptable Docker/DB/k6 baseline을 실행한다.
- before 결과와 query/table evidence를 검토하기 전 production 집계 쿼리를 변경하지 않는다.
- 실제 baseline은 local Docker before 관찰값으로만 기록하고 개선 성과로 해석하지 않는다.
