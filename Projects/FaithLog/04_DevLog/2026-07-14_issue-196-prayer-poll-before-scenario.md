---
project: FaithLog
type: devlog
issue: "#196"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - tdd
---

# #196 기도조·투표 목록 before 시나리오

## 1. 작업 배경

기도 current season/groups/assignable/weekly board와 Poll member/admin 목록·상세·결과 관련 read flow의 production N+1 수정 전 계약을 준비했다. 이번 단계는 `scenario-ready / not-measured`이며 실제 baseline과 개선 수치는 없다.

## 2. fixture 계약

- stable `datasetId`: `issue-196-prayer-poll-list-v2`
- 실행마다 lowercase 새 immutable `fixtureRunId` 사용
- primary: campus creator 1명 + generated member 999명 = ACTIVE 1,000명
- isolation: campus creator 1명 + generated member 49명 = ACTIVE 50명
- Prayer: 40조 × 25명, 제출 800명 / 미제출 200명
- Poll: option 5개, 응답 800명 / 미응답 200명, comments 200개
- Poll templates: 40개 × option 8개
- visibility: OPEN, 종료 2일, 종료 5일, 종료 8일, future SCHEDULED
- current-develop duty: COFFEE creator/다른 COFFEE duty/MEAL duty와 current COFFEE/current MEAL/91일 archived MEAL Poll

기존 row와 다른 fixture run의 row는 수정·삭제하지 않는다. 현재 run의 여덟 Poll(5 CUSTOM + current COFFEE + current/archived MEAL)은 exact ID/campus와 run ID에서 파생한 title을 확인한 한 SQL statement로만 시각을 보정하며, 일부 불일치와 0600 attempt receipt 이후 재-shaping은 거부한다. credential/token/inviteCode는 manifest에 기록하지 않는다.

## 3. 측정 흐름과 correctness

- runner는 명시한 mode만 실행하며 explicit `all`일 때 endpoint별 k6 프로세스를 하나씩 `prayer → poll-member → poll-admin → poll-duty` 순서로 실행한다.
- Prayer current season/groups/assignable/admin board/member board를 각각 분리한다.
- Poll member/admin list/detail/results/comments, admin missing-members/templates, cross-campus 404를 각각 분리한다.
- 개수·정렬·`editable`·`myGroupId`·campus isolation(외부 ID 404와 직접 campus 403)과 Poll 3일/7일 visibility, exact time window, result count/anonymous identity를 응답마다 검증한다.
- endpoint마다 Trend p50/p95/p99/max, Counter throughput, Rate failure, CPU/RAM, SQL query count/queriesPerRequest/repeated SQL, table estimated row/scan/fetch/write counter, 실제 image tag/immutable image ID, published target port와 Compose label을 기록한다.
- endpoint마다 별도 warmup을 끝낸 뒤 measured DB/log/resource/activity window를 열고, measured 직전 재발급 token의 JWT `exp` 여유를 raw token 저장·출력 없이 확인한다.
- exact required table/field schema, 8개 non-empty planner key, database/address/port/postmaster identity, analyze/autoanalyze/vacuum/autovacuum count와 null-or-valid timestamp 불변을 요구한다. PostgreSQL counter는 decimal string으로 수집해 BigInt exact delta를 기록하며 cumulative monotonic과 table별 write delta 개별 0을 검증한다.
- latest develop의 generic Poll 비페이지 배열/ID 내림차순, MEAL PageResponse explicit `id,desc`/90일 archive, #200 `manageableByMe`, #202 27-table RLS/JDBC owner 무영향을 검증한다.
- app/DB/Redis full container ID·image ID·StartedAt과 PostgreSQL/Redis process identity를 lock 전후, warmup 전, measured 직전·직후, 최종 report 전에 재검증한다. runtime/resource sampling interval과 max gap은 기본값 없는 runtime 승인 입력이며 boundary/gap/minimum count evidence만 준비한다.
- seed/shape/run은 lock 전 immutable app/DB/Compose/published endpoint/PostgreSQL snapshot과 lock 직후 identity를 exact 비교한다. `BASE_URL`은 explicit numeric loopback만 허용하고 address-family-compatible published binding exact 1개를 공통 검증한다. RAM은 strict bytes used/limit와 `0..100%` reported 값을 검증해 canonical bytes/percent를 기록한다.

## 4. TDD 기록

1. production 변경 전에 scenario contract 7개를 작성했다.
2. 필수 fixture/scenario/runner/evidence 파일 부재로 `7 tests / 7 failures` RED를 확인하고 별도 커밋했다.
3. create-only fixture, 현재-run Poll shaper, endpoint별 k6 시나리오, project-scoped canonical-lock runner, SQL/table/resource/activity summarizer, README를 구현했다.
4. 1차 구현 뒤 contract `8 tests / 0 failures` GREEN을 확인했다.
5. PM review의 lock 호환성, warmup 분리, token 수명, DB counter reset/상쇄, 외부 activity/autoanalyze, k6 direct metric shape, report overwrite, explicit mode, credential 상속 finding을 fake orchestration/evidence로 추가해 test-only `10 tests / 7 failures` RED를 별도 커밋했다.
6. 최소 도구 변경과 warmup 실패/stale token·child credential scope/다른 k6 PID/reversed percentile/exclusive report fake evidence 보강 뒤 contract `12 tests / 0 failures` GREEN과 Node/Bash 정적 검증을 수행했다.
7. PM 2차 review의 identical missing planner/analyze schema, 10분 1표본/긴 sampling gap, same-name container runtime 교체, vacuum/autovacuum drift를 test-only `12 tests / 9 pass / 3 fail` RED로 고정했다.
8. exact schema/maintenance gate, sample timeline coverage, 네 시점 runtime continuity, operator exclusive-window 선언을 최소 도구 변경으로 반영하고 같은 이름 container ID 교체 시 login/k6 0건을 포함해 contract `12 tests / 0 failures` GREEN을 확인했다.
9. PM 3차 review의 미승인 자동 채택, `Number.MAX_SAFE_INTEGER` counter 정밀도, target identity 기본값을 test-only `13 tests / 10 pass / 3 fail` RED로 고정했다.
10. sampling/target identity를 runtime 승인 입력으로 분리하고 clean evidence도 `automaticAdoption=false`/`conditional-not-adoptable`로 막았다. SQL decimal string과 BigInt delta, missing target의 inspect/login 0건을 포함해 contract `13 tests / 0 failures` GREEN을 확인했다.
11. PM 후속 review의 seed/shape/direct k6 target fallback, summarizer의 1초/2초 상수, negative/foreign resource 허용을 test-only `14 tests / 11 pass / 3 fail` RED로 고정했다.
12. 모든 entrypoint의 target을 runtime 필수로 통일하고 arbitrary approved sampling 값을 coverage에 결속했으며 app/DB exact 2-container와 finite/nonnegative resource gate를 추가해 contract `14 tests / 0 failures` GREEN을 확인했다.
13. PM 5차 review의 lock 대기 중 runtime 교체, published binding host/address-family 불일치, malformed/impossible RAM evidence를 test-only `16 tests / 11 pass / 5 fail` RED로 고정했다.
14. lock 전후 runtime/PostgreSQL exact continuity, shared numeric-loopback binding validator, strict memory byte/percent parser를 최소 도구 변경으로 반영해 contract `16 tests / 0 failures` GREEN을 확인했다.
15. 최신 develop drift를 `962e0e3`에서 `18 tests / 16 pass / 2 fail`, 공통 source/DB/Redis/pgss/resource 감사 gap을 `6ecd59b` test-only RED로 고정했다.
16. dataset v2, pagination/archive/#200/#202 ordering, app/DB/Redis continuity, pgss stable available/unavailable, k6 v2 두 metric shape, decimal-string/BigInt, full-ID resource cadence, immutable namespace와 최초 rejection 보존을 최소 보정해 `21 tests / 0 failures` GREEN을 확인했다.
17. current-develop handoff에서 conditional endpoint 순차 수집을 보정하고, 실행형 fake orchestration으로 prayer 5 endpoint 완료 후 exit 2, rejected/malformed/missing report와 k6/resource/integrity/runtime failure의 최초 중단을 고정했다. 첫 focused RED는 `23 tests / 22 skipped / 1 fail`, timeout 반례 전체 RED는 `23 tests / 22 pass / 1 fail(status=null)`이었다. operational status가 모두 0일 때만 continuation을 기록하고 optional `PERF_REPORT_ROOT` temp base로 artifact를 격리한다. 각 fake subcase는 timeout/error/signal 없음과 exact exit status·15초 미만을 요구하며 최종 계약은 `23 tests / 0 failures`다.

## 5. 안전 경계

- Docker/DB/seed/k6를 실행하지 않았다.
- production Java/API/권한/응답/오류/트랜잭션/Entity/DB/Flyway/dependency를 변경하지 않았다.
- runner는 Docker lifecycle을 바꾸지 않고 app/DB/Redis 실제 label 확인 뒤 `/tmp/faithlog-performance-{composeProject}.lock`과 다른 k6 부재를 요구한다.
- report는 새 runtime 필수 `executionRunId`의 ignored `build/reports/k6/issue-196/{fixtureRunId}/{executionRunId}` 아래에 생성한다. Optional `PERF_REPORT_ROOT`를 쓰더라도 그 아래 fixture/execution ID를 붙이며 기존 경로를 덮어쓰지 않는다.
- warmup/measured VUS와 duration 및 mode는 승인된 측정 세션의 runtime 필수 입력으로 남겼다.
- sampling만으로 짧은 transient activity의 절대 부재를 증명할 수 없고 cadence/max-gap/exclusive-window 방식도 사용자 미승인이다. 별도 승인 전에는 clean sampled evidence도 `adoption-policy-pending-user-approval`로 non-zero 종료하며 baseline 채택이 불가능하다.
- `BASE_URL`, app/DB/Redis container, expected service/image tag/immutable ID, source/Flyway/Redis identity, credential/workload도 기본값 없는 runtime 승인 입력이며 seed/shape/run은 누락 시 API/Docker/DB 전에, direct k6는 request 전에 실패한다. Resource evidence는 exact app/DB/Redis 3-container name/full-ID와 finite/nonnegative CPU, strict RAM bytes/percent만 허용한다.
- `localhost`는 승인된 해석 규칙이 없어 거부하고 explicit `127.0.0.1`/`[::1]`만 허용한다. 같은 address family의 exact/wildcard published binding이 requested port에 exact 1개여야 하며 lock 전후 immutable identity가 달라지면 login/API write/Poll UPDATE/k6는 0건이다. RAM used/limit는 strict unit의 safe bytes, positive limit, `used <= limit`, reported percent `0..100`을 모두 만족해야 한다.
- credential은 shell-only로 내리고 login/DB child에만 inline 전달한다. k6에는 token만 전달하며 metadata/summarizer/Docker inspection child에는 credential을 상속하지 않는다.
- correctness failure는 0건만 허용한다. 각 endpoint 직전·직후 다섯 Poll time window를 재검증하고 warmup/k6/resource/activity sampler/window/log/after-DB-snapshot 실패, 필수 latency/throughput/table/resource/activity evidence 누락·오형식, counter reset/상쇄/write delta는 reason과 함께 rejected로 보존한 뒤 runner를 실패시켜 baseline으로 인정하지 않는다.
- 최초 machine-readable rejection은 `primaryRejectionReason`으로 보존하고 기존 report를 덮어쓰지 않는다. clean evidence도 `automaticAdoption=false`, `conditional-not-adoptable`이다. 여러 성능 이슈의 test-code 보정은 병렬 가능하지만 shared-stack actual load는 PM exclusive window에서 순차 실행한다.

## 6. 다음 작업

- [ ] PM이 시나리오 전체 diff와 correctness/evidence 계약을 리뷰한다.
- [ ] 승인된 단독 측정 세션에서 사용자가 지정한 exact app image와 실제 Compose label을 확인한다.
- [ ] seed → 현재-run Poll shaping → endpoint 순차 baseline을 실행한다.
- [ ] 실제 raw/report evidence를 검토한 뒤에만 production N+1 수정 범위를 결정한다.

## 7. 이력서 지표 상태

`scenario-ready / not-measured`. 실제 baseline, 개선율, 성과 문장은 기록하지 않는다.
