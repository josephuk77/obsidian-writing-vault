---
project: FaithLog
type: devlog
issue: "#195"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - before
---

# #195 관리자·캠퍼스 멤버 목록 bulk 전 before 시나리오

## 1. 작업 배경

서비스 관리자 사용자·캠퍼스 목록과 캠퍼스 멤버·담당 배정 목록은 사용자, 멤버십, 캠퍼스를 반복 조회한다. production bulk 최적화 전에 공통 1,000명 데이터셋에서 endpoint별 독립 before 증거를 수집할 시나리오만 준비했다.

## 2. 현재 상태

`scenario-ready / not-measured`

- seed/k6/Docker/DB 실행 0건
- baseline/개선 수치 0건
- production Java/API/권한/응답/ErrorCode/트랜잭션/Entity/DB/Flyway/의존성 변경 0건
- 기존 1,000명 및 QA row 수정·삭제 0건
- push/PR/merge 0건

## 3. API inventory

- `GET /api/v1/admin/users`: `name`, `email`, `userId`, `role`, `page`, `size`, `sort`
- `GET /api/v1/admin/campuses`: `name`, `region`, `status`, `page`, `size`, `sort`
- `GET /api/v1/admin/campuses/{campusId}/members`: query 없음, ACTIVE, membership ID 오름차순
- `GET /api/v1/admin/campuses/{campusId}/duty-assignments`: optional `staleOnly`, baseline은 `staleOnly=false`, ACTIVE assignment + ACTIVE membership, assignment ID 오름차순

앞의 두 pageable API는 기본 `size=20`, 최대 `size=100`을 first/middle/large case로 분리하고 role/status/search를 별도 k6 process로 실행한다. 뒤의 두 API에는 존재하지 않는 pagination을 만들지 않고 1,000 ACTIVE member와 101 active duty full-list를 각각 측정한다. #201의 `includeArchived`는 billing/poll 목록 전용이며 #195 네 endpoint에서는 지원하지 않으므로 보내지 않는다.

### Current develop drift 대조 (2026-07-16)

- 최신 base `origin/develop@6796ed1`, 작업 branch `fix/195-member-list-baseline-current-develop`에서 scenario-only로 재작성했다. 기존 `perf/195-member-list-bulk-baseline`은 읽기 전용 대조로 보존했다.
- #200 이후 duty list user lookup은 이미 bulk이고 campus member list는 per-member lookup이다. 이 current-develop 비대칭을 측정 대상으로 기록하며 duty의 pristine pre-bulk 수치를 주장하지 않는다.
- #202 V11은 RLS를 enable하지만 `FORCE ROW LEVEL SECURITY`는 사용하지 않는다. Owner JDBC 무영향은 정적 경계이고 실제 runtime continuity는 PM 승인 측정 전까지 미검증이다.
- #206의 stable secondary ordering은 billing paging 전용이라 #195에는 적용되지 않는다. #195는 admin의 explicit `id,asc`와 member/duty repository ID ASC만 검증한다.
- #192-#199 test code는 병렬 보정하고 actual fixture/HTTP/DB/Docker/k6는 PM exclusive measurement slot에서만 순차 실행한다.
- 공통 무결성 감사에서 source commit, app/PostgreSQL/Redis approved service·full image/container identity, credential/workload/cardinality/k6 binary/resource cadence를 모두 runtime-required로 고정했다. Redis password가 없는 local Compose 계약에는 임의 credential을 만들지 않는다.
- Fixture mutation은 app/PostgreSQL/Redis를 pre-lock/post-lock/final에 비교하고, measurement는 세 container와 DB endpoint/postmaster identity를 post-lock, case 전후, final에 비교한다. Resource는 세 container의 full ID/name/image/StartedAt, CPU percent, memory bytes와 runtime 승인 boundary maximum gap을 검증한다.
- Counter count는 Rate `passes + fails`와 같아야 하고 `fails=0`, `rate=0`이어야 한다. Fresh report directory를 source/target preflight 전에 만들고 이후 최초 실패는 secret-free `first-rejection.json`을 exclusive create하며 후속 실패가 덮어쓰지 않는다. `automaticAdoption=false`는 유지한다.
- #192 dataset은 999 ACTIVE USER + 1 ADMIN이라 #195의 exact 1,000 ACTIVE USER/admin-excluded 계약에 재사용하지 않는다. Actual provisioning/fixture는 `PERF_1000_20260716_195_A` / `ISSUE195_BEFORE_20260716_A`로 성공했다. Executions A/B/C/D/E는 각각 k6 init, summary shape, resource parsing, psql machine-output, DB-wide transaction attribution blocker로 거부·비재사용이며 다음 fresh execution은 `EXEC195_BEFORE_20260716_F`다. F는 #208 공통 audit 완료 전 실행하지 않는다.
- Provisioning은 signup 1,000건 직후 ADMIN을 다시 로그인하고 JWT `exp`가 runtime `TOKEN_SAFETY_MARGIN_SECONDS` 이상 남았는지 검증한다. Verification의 page/detail 요청마다 다시 확인하고 부족할 때만 fresh login한다. Token/credential/expiry 원문은 저장하지 않고 manifest에는 refresh count만 남긴다.

## 4. Fixture와 실행 안전 계약

- 공통 사용자 데이터 `datasetId`와 관계 fixture `fixtureRunId`를 분리한다.
- 새 `ISSUE195_*` run마다 25개 fixture campus, primary 1,000 ACTIVE membership, isolation sentinel membership, MEAL 100 + COFFEE 1 assignment를 actual API로 추가한다.
- 기존 user/membership/duty/campus/QA row를 PATCH/DELETE하지 않고 role/tokenVersion도 바꾸지 않는다.
- partial fixture는 보존하고 새 run ID로만 재시도한다.
- API/DB credential은 unexported shell variable로만 유지한다. PostgreSQL password는 command-scoped Docker client environment와 값 없는 `docker exec -e PGPASSWORD`로만 전달해 CLI argv/report/log에서 제외하며, k6에는 DB credential을 전달하지 않는다.
- `BASE_URL`은 runtime 필수이며 승인된 app service와 실제 `APP_CONTAINER_ID` published port에 exact 결속한다. Lock 획득 뒤 immutable app/PostgreSQL ID/name/image/start/label/port와 DB identity를 다시 캡처해 original project, 승인 service/database, published endpoint에 재결속한 뒤에만 report evidence/login/warmup을 시작한다.
- dataset/fixture와 별도로 fresh `EXEC195_*` executionRunId를 사용하며 기존 report directory는 덮어쓰거나 append하지 않고 거부한다.
- fixture와 measurement 모두 실제 Compose project label로 만든 `/tmp/faithlog-performance-{composeProject}.lock`을 사용하고 다른 성능 fixture/부하와 병렬 실행하지 않는다.
- 실행 중인 app/PostgreSQL container의 실제 Compose project/service label을 기록하고 project mismatch를 거부한다.
- shared Docker lifecycle `up/down/build/rebuild/prune`은 runner 범위에 없다.

캠퍼스 멤버·담당 목록 권한은 실제 enum 기준 service `ADMIN` 또는 ACTIVE `MINISTER`/`ELDER`/`CAMPUS_LEADER`다. 존재하지 않는 OWNER/MANAGER 명칭은 PM review finding에 따라 정정했다.

## 5. 측정·정확성 계약

No-default runtime input을 받는 warmup과 measured k6 process를 case마다 분리한다. 현재 PM handoff 추천은 warmup `1 VU/30s`, measured `10 VU/2m`, failure `0`, token safety `120s`, resource boundary gap `10s`이며 script default나 측정 성과가 아니다. 각 endpoint/case별로 p50/p95/p99/max, request rate throughput, exact-zero failure gate와 app/PostgreSQL measured 실행 전후 CPU/RAM boundary snapshot을 독립 기록한다. CPU/RAM은 exact case, immutable container ID/name, finite non-negative numeric schema, `before < measured-start <= measured-end < after`, before/after 각 1개를 validator로 검증한 boundary-only 관측이며 continuous/peak 수치로 해석하지 않는다. HTTP 200, success envelope, response shape, strict stable order, page metadata, filter 결과, exact pageable/list cardinality, isolation sentinel 비노출을 검증한다.

인증은 각 case warmup 직전에 fresh token을 발급하고 JWT `exp`가 `warmup + idle control measured duration + measured load duration + runtime safety margin`을 충족하는지 메모리에서 검증한다. 권고값의 최초 요구량은 `30s + 2m + 2m + 120s = 390s`이며 control snapshot/observer write 전에 fail closed한다. measured 직전에는 DB/API 호출 없이 기존 `remaining > measured+margin`을 재검증한다. 그 case의 두 k6 process에만 전달한 뒤 clear하며 token은 파일/report/log에 저장하지 않는다. 각 summary는 direct/v2 shape 모두에서 exact case metric, positive safe-integer request count, positive finite throughput, non-negative finite `p50 <= p95 <= p99 <= max`, zero failure를 검증하되 latency/throughput threshold는 두지 않는다. DB integrity도 request count에 같은 safe-integer 계약을 적용한다.

DB evidence는 각 measured case 직전/직후 필수 table counter와 current-database non-truncated `pg_stat_statements` inventory를 남긴다. 각 phase는 schemaVersion/phase/status/relation exact schema의 availability JSON을 항상 생성한다. before/after가 모두 unavailable이고 두 snapshot이 모두 없을 때만 optional unavailable을 허용하며, availability 변화, malformed/missing marker, available인데 snapshot 누락, unavailable인데 snapshot 공존은 `non-adoptable`이다. 두 phase가 모두 available이면 NDJSON을 line-by-line strict parse하고 observer 제외 뒤 production query row를 최소 1개 요구한다. Empty/observer-only snapshot은 `available-query-snapshot-empty`, JSON parse 오류는 `available-query-snapshot-malformed`로 machine-readable non-adoptable 처리한다. 그 뒤 `(userid,dbid,queryid,toplevel)` 복합 identity를 보존하고 duplicate/malformed/before-after missing/counter regression을 `non-adoptable`로 처리하며, 동일한 non-empty snapshot만 verified zero-call로 구분한다. `calls`/`rows`와 `xact_commit`/`xact_rollback`은 decimal string으로 수집하고 strict `BigInt`로 비교·차감해 `Number.MAX_SAFE_INTEGER` 초과 값도 무손실 기록한다. Runtime-integrity SQL은 stable marker를 붙이고 collector와 delta 양쪽에서 제외해 첫 observer row나 기존 누적 observer row가 production query delta에 섞이지 않게 한다. 자기 backend PID만 activity에서 제외하므로 같은 application_name의 다른 PID도 외부 세션으로 집계한다. Runner evidence case, observer case, measured scenario/case, metricName을 exact 결속한다. Table 기대값과 불변성, required planner/4-table/DB/measured typed schema, 외부 active session, analyze/autoanalyze/vacuum/autovacuum, planner setting 변화를 machine validator로 차단한다. App/PostgreSQL immutable container/image/start identity와 DB TCP endpoint/postmaster epoch를 초기·case 전후·최종에 비교한다. 현재 요청당 tokenVersion 인증 transaction 1 + endpoint service read transaction 1을 코드 근거로 사용해 measured commit delta가 `2 × measured requests + before observer 1`보다 작으면 fail closed한다. DB-wide 초과 commit은 source-unattributed supporting evidence이며 request transaction이나 scheduler에 귀속하지 않는다.

Execution E는 warmup 334/measured 4,200 requests와 zero failure를 완료했지만 DB-wide commit delta 8,427이 request-derived 8,400 + observer 1보다 26 커 old exact-equality gate에서 거부됐다. 모든 latency/throughput은 rejected diagnostic일 뿐 baseline/성과가 아니다. 보정 runner는 measured와 같은 duration의 immediately-before idle control을 strict full runtime schema로 캡처한다. Control case/duration/timestamp와 `controlCommitDelta = backgroundCommitDelta + observer 1`을 measured-before snapshot에 exact bind하고, background를 빼거나 비례 추정하지 않으며 항상 `supporting-only`, `automaticAdoption=false`다. JSON conversion child는 credential-free 최소 environment만 받는다. PM 독립 80/80과 2초 read-only smoke(`control delta 2`, `background 1`, rollback 0, subtraction false)는 GREEN이지만 smoke diagnostic이고 baseline이 아니다. PostgreSQL stats reset이나 설정/extension/lifecycle 변경은 하지 않는다.

개별 evidence validator가 통과해도 boundary 관측과 cooperative lock만으로는 짧은 frontend/QA/CPU-only shared-stack 부하의 부재를 증명할 수 없다. 따라서 최종 `measurement-classification.json`은 `conditional-not-adoptable`, `automaticAdoption=false`로 고정하고 runner는 non-zero로 종료한다. 자동 채택은 사용자가 별도의 exclusive/continuous provenance 계약을 승인하기 전에는 허용하지 않는다.

## 6. TDD 기록

1. production controller inventory, scenario matrix, metric/correctness, additive fixture, runner lock/Compose label, DB read-only evidence, ignored report 계약 테스트를 먼저 작성했다.
2. 구현 파일이 없어 `7 tests / 6 failures` RED를 확인하고 test-only commit으로 남겼다.
3. issue-local manifest, k6, additive fixture prep, sequential runner, DB evidence, README를 구현했다.
4. 첫 GREEN 뒤 PM 독립 review에서 warmup/default, cross-issue lock, case별 DB attribution, campus role 문서 finding 4건을 받았다.
5. finding 재현 계약을 추가해 `8 tests / 2 pass / 6 fail` RED를 커밋한 뒤, runtime login, warmup/measured, 공통 lock, case별 snapshot/query delta, 실제 role enum으로 최소 수정했다.
6. Node contract `8 tests / 0 failures`, Node/Bash syntax, JSON parse, `git diff --check` GREEN을 확인했다.
7. 두 번째 PM review의 case별 token refresh, k6 DB credential 차단, pg_stat snapshot 무결성 finding을 fake 44분/22-phase orchestration과 query delta 계약으로 추가해 test-only RED `8 pass / 5 fail`을 확인했다.
8. case마다 login을 warmup 직전 수행하고 token/credential 환경 범위를 축소했으며 query reset/top-100 소실/음수 counter를 non-adoptable로 처리했다. 최종 Node contract `13 tests / 0 failures`와 정적 검증을 통과했다. fake orchestration만 사용했고 Docker/DB/seed/k6는 실행하지 않았다. 기존 전체 Gradle `449 tests / 0 failures / 0 errors / 3 skipped` 이후 production Java·REST Docs 변경은 없어 별도 build/asciidoctor를 실행하지 않았다.
9. 세 번째 PM review의 target 결속, token case 수명, after-only query, 외부 activity/analyze/planner, summary 필수값, stale report, table counter finding 7건을 실행형 계약으로 추가해 test-only RED `13 pass / 7 fail`을 확인했다.
10. published target/service identity, fake-clock exp, current DB full inventory, summary/DB/table adoption validator와 fresh executionRunId를 최소 구현해 최종 Node contract `20 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline 수치 생성은 계속 0건이다.
11. 네 번째 PM review의 실제 before/after observer 이름 불일치, missing/null evidence 강제 변환, observer SQL query delta 혼입, vacuum/autovacuum 미검증 finding 4건을 추가해 기존 `20 pass`를 유지하면서 신규 `4 fail` RED를 test-only commit으로 남겼다.
12. observer issue/case/phase 구조 검증, strict evidence schema/type gate, stable observer marker 이중 제외, vacuum/autovacuum counter/timestamp 불변성을 최소 구현해 최종 Node contract `24 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
13. 다섯 번째 PM review의 queryId 단독 덮어쓰기, 다른 case adoption 결합, measured 중 container replacement 미감지 finding 3건을 추가해 기존 `24 pass`를 유지하면서 신규 `3 fail` RED를 test-only commit으로 남겼다.
14. pg_stat 복합 identity, runner/observer/measured/metric exact case binding, app/PostgreSQL/DB runtime continuity gate를 최소 구현해 최종 Node contract `27 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
15. 여섯 번째 PM review의 fractional request/reversed percentile, pre-lock/post-lock TOCTOU, Docker argv password, CPU/RAM evidence 미채택 finding 4건을 targeted `4 tests / 4 failures` RED로 test-only commit했다.
16. safe-integer/ordered summary와 DB count, post-lock approved target 재결속, command-scoped password forwarding, strict boundary resource adoption gate를 최소 구현해 전체 Node contract `30 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
17. 일곱 번째 PM review의 same-name 외부 DB 세션 누락, shared-stack 자동 채택, 누적 bigint precision loss finding 3건을 신규 `3 tests / 3 failures` RED로 test-only commit했다.
18. PID-only self exclusion, final conditional classification/non-zero runner, decimal-string/BigInt query·transaction delta를 최소 구현해 전체 Node contract `33 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
19. 여덟 번째 PM review의 before/after pg_stat_statements availability 변화 false-green을 신규 `1 test / 1 failure` RED로 test-only commit했다.
20. phase별 strict machine-readable availability marker와 marker/snapshot continuity gate를 최소 구현해 전체 Node contract `34 tests / 0 failures`로 보강했다. PostgreSQL 설정/extension은 변경하지 않았고 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
21. 아홉 번째 PM review의 available empty inventory false-green과 malformed NDJSON 비구조화 오류를 신규 `1 test / 1 failure` RED로 test-only commit했다.
22. Available phase의 strict NDJSON parse와 production row 최소 1개 gate를 구현해 전체 Node contract `35 tests / 0 failures`로 보강했다. 실제 Docker/DB/seed/k6 실행과 baseline/성과 수치 생성은 계속 0건이다.
23. 최신 develop page/archive/#200 권한·lookup/#202 RLS/#206 ordering drift를 고정하는 신규 계약을 먼저 추가해 targeted `1 test / 1 failure` RED를 커밋했다.
24. `staleOnly=false`, 미지원 `includeArchived`, 현재 bulk/per-member lookup 경계와 ACTIVE/ID ASC correctness를 manifest·fixture·k6·README에 최소 반영해 targeted GREEN과 전체 Node contract `36 tests / 0 failures`를 확인했다. 상태는 계속 `scenario-ready/not-measured`이며 actual Docker/DB/HTTP/k6/seed 실행과 production/Flyway/dependency 변경은 0건이다.
25. PM 공통 무결성 체크리스트를 한 번에 감사해 기존 36개를 유지하면서 source/image/workload 무fallback, Redis continuity, Rate 관측수 수학, full-resource cadence, 최초 machine-readable rejection 5건을 신규 `5 tests / 5 failures` RED로 한 커밋에 고정했다.
26. 승인값을 선택하지 않고 runtime-required 입력과 exact validator만 추가해 신규 5개와 전체 `41 tests / 0 failures` GREEN을 확인했다. 기존 pgss availability/BigInt, DB activity/planner/maintenance, pagination/archive/#200/#206 correctness는 테스트로 재확인하고 중복 구현하지 않았다.
27. Self-review에서 fixture PostgreSQL 연속성 누락과 source-contract preflight 실패의 최초 rejection 미보존을 `2 tests / 2 failures` RED로 추가 재현했다.
28. Fixture 3-container pre/post-lock/final identity와 preflight 이전 atomic report/rejection 경계를 최소 보정해 전체 `43 tests / 0 failures` GREEN을 확인했다. 실제 Docker/DB/HTTP/seed/k6와 성능 수치 생성은 계속 0건이다.
29. 최종 credential self-review에서 source-contract Node가 credential unexport보다 먼저 실행되는 순서 gap을 targeted RED로 확인했다.
30. API/DB credential을 모든 child process 전에 shell-only로 전환하고 전체 `43 tests / 0 failures`를 재확인했다.
31. Fresh dataset provisioner 부재를 namespace/report collision, partial preservation, exact 1,000 ACTIVE USER, ADMIN/inactive/duplicate, credential, 3-container continuity의 test-only RED로 먼저 고정하고 public signup-only 최소 구현으로 targeted `11/11` GREEN을 확인했다.
32. PM finding의 단일 30분 ADMIN JWT 재사용을 fake clock/token으로 `9 pass / 7 fail` RED 재현했다. Signup 직후 mandatory fresh login, runtime 120초 margin, verification 요청별 재검사와 조건부 refresh를 구현해 targeted `16/16`, 전체 issue-local `59/59` GREEN을 확인했다. 실제 provisioning/HTTP/DB/Docker/k6는 0건이다.
33. Relationship fixture의 단일 JWT 재사용, report overwrite, Docker child credential 상속을 test-only RED로 고정하고 모든 authenticated request 직전 JWT margin 검사, exclusive report/first-rejection, secret-free child environment를 최소 구현했다.
34. 후속 absolute report root, numeric loopback, full immutable container identity, child allowlist 계약은 `10 assertions / 7 pass / 3 fail` RED에서 GREEN으로 전환했다. 최종 issue-local은 fixture `10/10`, provisioning `16/16`, scenario `43/43`, 합계 `69/69`이며 상태는 계속 `scenario-ready/not-measured`다. 실제 provisioning/HTTP/DB/Docker/k6와 production/Flyway 변경은 0건이다.
35. Actual handoff 최종 대조에서 measurement runner의 report-root fallback과 provisioner 상대경로 허용을 실행형 RED로 재현했다. 누락/상대경로가 Docker/identity/lock/API/report mutation 전에 거부되도록 provisioning/fixture/execution을 동일한 absolute runtime root 계약으로 통일했고, 최종 issue-local `73/73` GREEN을 확인했다. 실제 load는 0건이다.
36. PM actual slot에서 dataset ACTIVE USER 1,000명 provisioning과 campuses 25/memberships 1,025/duties 101 fixture는 성공했지만, execution A의 첫 warmup은 k6가 `scenario-contract.json`을 JavaScript module로 파싱해 exit `107`로 초기화 실패했다. Warmup/measured HTTP 요청은 모두 0이고 A report는 비재사용이다. 실제 `/opt/homebrew/bin/k6 inspect`로 동일 실패를 RED 고정한 뒤 contract 내용·hash·권한·scenario 의미를 유지한 채 init-context `open()` + `JSON.parse`로 보정했고 전체 issue-local `74/74` GREEN을 확인했다. Dataset/fixture는 보존하며 ADMIN→USER trap 원복 확인 후 fresh execution B만 사용한다.
37. Execution B의 첫 `admin_users/first_page` warmup은 142 HTTP/checks 1,278/1,278/failure 0으로 완료됐지만 실제 k6 v2 Rate가 `{value:0,passes:0,fails:142}`를 내보내 기존 validator가 없는 `rate`를 요구해 거부됐다. Measured HTTP는 0이고 warmup latency는 rejected diagnostic으로만 보존해 baseline/성과에 쓰지 않는다. B summary를 read-only로 직접 검증하고 direct/values, warmup/measured, normalized DB-integrity consumer까지 한 묶음 RED→GREEN했다. Exact math는 `value=0`, `passes=0`, `fails=requestCount`이며 missing/non-finite/string/positive value, positive passes, count mismatch를 모두 거부한다. 전체 issue-local `75/75`, B report 비재사용, PM DB 확인 0 ADMIN/1 USER, 다음은 preserved dataset/fixture + fresh execution C다.
38. Execution C의 첫 `admin_users/first_page` warmup은 530 HTTP/checks 4,770/4,770/failure 0으로 완료됐지만 measured-before DB evidence 뒤 첫 resource snapshot에서 rounded decimal MiB를 integer byte로 요구해 거부됐다. Measured HTTP는 0이고 warmup 수치는 rejected diagnostic으로만 보존해 baseline/성과에 쓰지 않는다. Actual app/PG/Redis 문자열과 `B/kB/KB/KiB/MB/MiB/GB/GiB/TB/TiB`, safe boundary를 nearest whole byte capture→resource adoption으로 RED→GREEN했다. Preserved C raw summary의 historical token-bearing evidence는 수정하지 않고, future setup data에서 token을 제거해 installed-k6 no-HTTP `handleSummary` serialization에 sentinel이 없음을 검증했다. PM 독립 실행까지 전체 issue-local `78/78`, C report 비재사용, broad `perf-195` 임시 계정 0 ADMIN/3 USER, 다음은 preserved dataset/fixture + fresh execution D다.
39. Execution D의 첫 `admin_users/first_page` warmup 542건과 measured 7,197건/checks 64,773/64,773/failure 0은 완료됐지만 after table artifact에 psql `Output format is csv.` status가 섞여 `measured-evidence-after`에서 거부됐다. Latency/throughput을 포함한 모든 D 수치는 rejected diagnostic으로만 보존해 baseline/성과에 쓰지 않는다. Preserved D와 fake psql로 table/runtime/available/unavailable query stdout contamination을 RED 재현하고 collector의 모든 psql invocation을 quiet machine-output mode로 통일했다. SQL/metric/DB window/observer/pgss 의미는 그대로이며 전체 issue-local `79/79`, D report 비재사용, broad `perf-195` 임시 계정 0 ADMIN/4 USER와 cleanup 확인, 다음은 preserved dataset/fixture + fresh execution E다.
40. Execution E는 warmup 334건과 measured 4,200건/checks 37,800/37,800/failure 0을 완료했지만 DB-wide commit excess 26으로 old exact equality에서 거부됐다. Preserved E content/hash/mtime 불변, full-schema same-duration idle control, BigInt observer/background 산식, no-subtraction, control→measured case/duration/timestamp binding, child env 격리, case TTL의 control duration 포함을 RED→GREEN했다. PM 독립 issue-local `80/80`, Node/Bash/JSON/diff-check와 production/Flyway/Gradle diff 0, 2초 read-only supporting-only smoke를 확인했다. E/smoke 수치는 baseline이 아니며 다음 fresh F는 #208 공통 audit 뒤에만 실행한다.

## 7. 다음 작업

- PM은 성공한 dataset/fixture를 다시 만들거나 정리하지 않는다. A/B/C/D/E execution은 모두 보존·비재사용이다. #208 공통 audit 완료 후 fresh `EXEC195_BEFORE_20260716_F`로만 한 서버 한 load를 순차 실행한다. 현재 개발 세션은 실제 DB/HTTP/k6 load를 실행하지 않는다. 자동 채택에는 사용자의 별도 exclusive/continuous provenance 승인이 필요하다.
- endpoint별 before 결과와 query/table evidence를 PM에 보고하기 전 production bulk 최적화를 시작하지 않는다.
- 실제 baseline은 local Docker before로만 기록하고 개선 성과나 이력서 전후 수치로 해석하지 않는다.

## 2026-07-17 G 조건부 actual-before

- `PERF_1000_20260716_195_A` / `ISSUE195_BEFORE_20260716_A` / `EXEC195_BEFORE_20260716_G`에서 11/11 measured adoption과 전 case `failureRate=0`을 완료했다.
- 중간 case rejection은 없고 유일한 first rejection은 예정된 `final-classification` exit `2`다. 최종은 `conditional-not-adoptable`, `automaticAdoption=false`이며 cooperative lock과 boundary evidence가 transient external shared-stack load 부재를 증명하지 못한다.
- G는 명시적 after 비교용 조건부 shared-stack before baseline일 뿐 자동 채택 baseline이나 성능 성과가 아니다. G 실행/report는 재사용하거나 다시 실행하지 않는다.
- 주요 조사 후보는 `admin_users/large_page`(5,068 requests, 42.156241 req/s, p95 339.36645 ms)와 `campus_members/full_list`(5,160 requests, 42.909684 req/s, p95 338.1192 ms)다. 두 current-source 경로의 N+1 제거만 최소 production 제안으로 기록했으며 구현은 사용자 승인 전 금지다.
- 첫 단계는 admin user page bulk membership/campus projection과 campus member bulk user lookup이다. API/frontend/권한/ACTIVE/ID ASC/ErrorCode/transaction/lock은 유지하고 Flyway/index는 추가하지 않는다. after query plan이 필요성을 증명할 때만 `campus_members (user_id, id)` index를 별도 검토한다.
- 검증: issue-local 82/82, Node/Bash/JSON/diff-check GREEN, production/Flyway diff 0, self-review finding 0. Commit `5f6009d166b06f830040c64a91e43951b8416195`.
