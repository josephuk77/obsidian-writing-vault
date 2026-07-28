---
project: FaithLog
type: devlog
issue: "#193"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - tdd
---

# #193 관리자 정산 조회 before 시나리오

## 1. 작업 배경

1,000명 캠퍼스의 관리자 정산 조회 N+1, 전체 ChargeItem 로딩, JVM 집계·정렬·페이지네이션 비용을 측정하기 위한 before 시나리오를 준비했다. 이번 단계는 `scenario-ready, not measured`이며 production 최적화와 실제 성능 측정은 포함하지 않는다.

## 2. 최종 설계 기준

- `/api/v1/admin/campuses/{campusId}/charges`와 `/charges/my-accounts`를 대상으로 한다.
- 프론트 순서인 `PENALTY + UNPAID → paymentCategory → status → userId → keyword → unknown paymentAccountId → pagination`을 따른다. `my-accounts?paymentAccountId`는 현재 서버가 무시하므로 계좌 필터 성과로 집계하지 않는다.
- 공통 `PERF_` 1,000명 dataset은 읽어 재사용하고 승인된 측정 직전에만 `fixtureRunId`별 account/charge row를 additive INSERT한다.
- 기존 사용자/QA/성능/account/charge row는 수정하거나 삭제하지 않는다.
- warmup과 measured run 및 report를 분리한다.
- cross-issue 공통 runner lock, shared-stack activity check, dataset/fixture ID 분리, 실제 Compose label, runtime-only credential을 사용한다.
- Docker lifecycle과 production Java/API/DB/Flyway/dependency를 바꾸지 않는다.

## 3. 구현 내용

- Contract test: 기존 28개에 mutation 전 workload/post-lock target/RAM 정합성 회귀 3개를 더한 계약 31개.
- Fixture: 1,000 ACTIVE user를 재사용하고 PENALTY/owned COFFEE/foreign-owner COFFEE/cross-campus marker row를 fixture marker로 추가한다.
- k6: 16개 조합별 Trend/Counter/Rate를 기록하고 두 summary shape 모두에서 failure=0, 양의 정수 count, 양의 throughput, `0 <= p50 <= p95 <= p99 <= max`를 강제한다.
- Correctness: preflight와 measured가 동일 validator를 사용해 campus/summary와 순서가 고정된 member `userId/name/email/total/status별 금액`을 16-case manifest와 exact 비교한다. supported filter, requester account scope, unknown parameter 무시 mismatch는 failure Rate에 반영한다.
- Identity/TTL: fresh `EXEC193_` report directory와 app/PostgreSQL/DB identity를 고정한다. runtime 필수 safety seconds를 phase duration에 더해 warmup/measured 직전 TTL exact-boundary 이상을 요구한다.
- Docker evidence: runtime 필수 최대 sample gap 아래 exact app/DB ID, ISO timestamp, numeric CPU/RAM, strict monotonic/no-duplicate, first<=measuredStart, last>=measuredEnd를 검증한다.
- Evidence: `pg_stat_database` bigint를 decimal string/`BigInt`로 무손실 처리하고 strict schema로 JSON number/null/coerced counter와 external activity, reset/decrease, statement eviction, planner/n_mod/analyze/vacuum drift를 거부한다. calibration은 exact correction이 아닌 observer-adjusted 근사 자료다. 자동 adoption marker 없이 `conditional-shared-stack`, `automaticAdoption=false`만 기록한다.
- Target: `BASE_URL`은 `127.0.0.1` 또는 `[::1]` numeric loopback만 허용하고 inspected app의 같은 address-family `8080/tcp` binding과 정확히 결속한다. Docker Desktop dual-stack pair는 target family의 한 행만 선택하며 `localhost`는 fail-closed다.
- Pre-mutation gate: 모든 workload count/VUS/duration을 report/container보다 먼저 검증하고 canonical lock 직후 app/PostgreSQL container, DB/postmaster, binding을 pre-lock target과 exact 비교한다.
- RAM evidence: used/limit 계산 percent를 primary로 저장하고 raw MemPerc의 자체 소수 자릿수 반올림과 모순되면 실패한다. agent가 tolerance를 선택하지 않는다.
- Lock: 같은 Compose project를 쓰는 #192/#194/#195 등 다른 성능 runner와 공유하는 `/tmp/faithlog-performance-{composeProject}.lock`을 사용한다.
- Report: `build/reports/k6/issue-193/{datasetId}/{fixtureRunId}/{executionRunId}` fresh 전용 경로.

## 4. TDD 기록

1. 실패 테스트 작성: 필수 시나리오 파일 계약 8개를 먼저 추가했다.
2. 실패 확인: 파일 부재로 `8 tests / 8 failures` RED.
3. 최소 구현: SQL fixture/expectation/evidence, k6, runner, README를 추가했다.
4. 테스트 통과: `8 tests / 0 failures` GREEN.
5. 리팩토링: warmup 뒤 before snapshot, measured 직후 after snapshot, 이후 EXPLAIN 순서로 counter 오염을 제거하고 local-only guard와 lock 정리를 보강했다.
6. PM finding RED: semantic equality, unknown parameter, failure summary, preflight 분리 계약 추가 후 `12 tests / 5 failures`.
7. PM finding GREEN: 공용 scenario definition, Node preflight, failure threshold/validator, synthetic EXPLAIN 명시를 적용해 `12 tests / 0 failures`.
8. PM 재리뷰 RED: direct/wrapped metric, 필수 request/Trend, requester/TTL/fresh auth, fake target binding, 측정 오염·counter 보정, warmup runtime 입력 계약을 추가해 `16 tests / 11 pass / 5 fail`.
9. PM 재리뷰 GREEN: fail-closed target/auth/adoption/integrity validator를 최소 구현해 `16 tests / 16 pass`.
10. 최신 PM RED: stale execution report, malformed/null evidence, 승인 runtime identity, transient read-only 자동 채택, vacuum drift를 추가해 `21 tests / 16 pass / 5 fail`.
11. 최신 PM GREEN: atomic execution, strict schema, runtime stability, conditional classification, maintenance gate를 구현해 `21 tests / 21 pass`.
12. 최종 PM RED: summary 수학, measured body semantics, Docker resource coverage, JWT safety를 추가해 `25 tests / 21 pass / 4 fail`.
13. 최종 PM GREEN: 최소 구현 후 `25 tests / 25 pass`.
14. 추가 PM RED: member row 금액 semantics, 2^53 경계 누적 counter, numeric loopback dual-stack binding을 추가해 `28 tests / 25 pass / 3 fail`.
15. 추가 PM GREEN: 공유 response validator, decimal string/BigInt counter, address-family target binding을 최소 구현해 `28 tests / 28 pass`.
16. post-lock PM RED: mutation 전 workload, lock 직후 complete target, RAM 정합성을 추가해 `31 tests / 28 pass / 3 fail`.
17. post-lock PM GREEN: fail-closed pre-mutation parser/target validator/canonical RAM 계산으로 `31 tests / 31 pass`.

## 5. 테스트 결과

- `node --test performance/k6/admin-charge-query-baseline/scenario-contract.test.mjs`: 31 pass.
- `bash -n performance/k6/admin-charge-query-baseline/run-baseline.sh`: 성공.
- k6 JS/contract test의 `node --check`: 성공.
- `git diff --check`: 성공.
- 전체 `./gradlew test`: 첫 실행은 macOS Byte Buddy 동적 attach 구간에서 4분 이상 진행이 없어 중단(exit 130). 저장소 변경 없이 캐시된 Byte Buddy agent를 실행 시점에 선로딩한 재실행은 `449 tests / 0 failures / 0 errors / 3 skipped`, `BUILD SUCCESSFUL`(5분 7초).
- 전체 테스트는 로컬 H2 기반이며 shared Docker/PostgreSQL을 사용하지 않음.
- PM finding 수정 후 동일 agent 조건 재검증: `BUILD SUCCESSFUL`(5초, tasks up-to-date), XML 기준 `449 tests / 0 failures / 0 errors / 3 skipped`.
- PM 재리뷰 수정 후 최신 전체 재검증: 캐시 Byte Buddy agent 선로딩, `BUILD SUCCESSFUL`(23분 52초), XML 기준 `449 tests / 0 failures / 0 errors / 3 skipped`.
- 최신 21개 계약 수정 뒤 재실행: 6 tasks UP-TO-DATE, `BUILD SUCCESSFUL`(4초), 동일 XML 합계 유지.
- 최종 25개 계약 수정 뒤 재실행: 6 tasks UP-TO-DATE, `BUILD SUCCESSFUL`(35초).
- 추가 28개 계약 수정 뒤 전체 재실행: 6 tasks UP-TO-DATE, `BUILD SUCCESSFUL`(2분 28초), 기존 XML 합계 `449 tests / 0 failures / 0 errors / 3 skipped` 유지.
- 31개 계약 수정 뒤 전체 재실행: 2 tasks executed/4 up-to-date, `BUILD SUCCESSFUL`(3분 32초), XML `449 tests / 0 failures / 0 errors / 3 skipped`.
- seed/k6/Docker/DB 명령: 실행하지 않음.

## 6. 고민한 부분

- warmup 횟수/VUS/max duration, measured VUS/duration, token expiry safety seconds, Docker 최대 sample gap은 승인되지 않아 default를 정하지 않고 runtime 필수 입력으로 남겼다.
- 현재 `my-accounts` Controller/REST Docs는 `paymentAccountId`를 선언하지 않으므로 실제 요청은 unknown parameter 무시 동작으로만 검증한다. production API는 변경하지 않았고 실제 필터 지원은 별도 사용자 결정 대상이다.
- PostgreSQL counter와 Docker stats가 login/correctness/warmup에 오염되지 않도록 initial auth → fixture/correctness → warmup → fresh auth → state/calibration/before → measured → after/state → synthetic EXPLAIN 순서로 분리했다.
- boundary 사이에 완료된 외부 read-only 요청을 production 변경 없이 완전히 귀속할 수 없으므로 실제 실행은 frontend/QA 접근이 중단된 단독 사용 시간으로 제한해야 한다.

## 7. 트러블슈팅

- 문제: 최초 evidence 순서에서는 warmup과 before EXPLAIN이 measured counter delta에 섞일 수 있었다.
- 원인: before snapshot을 warmup 앞에 두고 같은 SQL에서 EXPLAIN까지 실행했다.
- 해결: warmup 후 before snapshot, measured 직후 after snapshot, 그 뒤 EXPLAIN 순서로 변경했다.
- 재발 방지: contract/README에 warmup/measured 분리와 evidence 순서를 명시했다.
- PM finding: JSONB/Jackson key 순서 의존 비교, 지원하지 않는 `my-accounts?paymentAccountId`를 필터로 해석한 false-green, measured 실패 채택 가능성, before 이후 login/correctness 오염, synthetic EXPLAIN의 과도한 증거 해석을 확인했다.
- 해결: semantic deep equality, unknown parameter 전용 case/기대값, failure `rate==0`과 summary validator, report에 저장하지 않는 runtime token preflight, synthetic/production-plan-false metadata와 #194 책임 경계를 적용했다.
- 재발 방지: 위 네 실행 조건을 Node 계약 테스트로 고정하고 EXPLAIN 해석 제한을 README/wiki/decision/resume 기록과 동기화했다.
- PM 재리뷰 finding: k6 direct metric shape, zero/missing request·Trend, 30분 token TTL, 다른 localhost target, measured 중 외부 activity/analyze, fixture 전 credential identity, observer counter overhead, 미승인 warmup VUS/maxDuration을 확인했다.
- 해결: two-shape summary gate, requester/JWT TTL validator와 measured fresh login, inspected published-port fake harness, boundary state/integrity validator, calibration counter correction, warmup runtime 필수 입력을 추가했다.
- 최신 PM finding: report directory 재사용의 stale marker, 최소 malformed/null evidence false-green, 미승인 service/runtime 교체, transient read-only 자동 eligible, vacuum/autovacuum 미감지를 확인했다.
- 해결: fresh execution atomic directory, exact evidence schema, app/PostgreSQL/DB runtime before/after identity, conditional-only classification, vacuum maintenance fields를 추가했다.
- 최종 PM finding: fractional request count와 역전/음수 percentile, measured body 의미 미검증, Docker 한 점/구간 누락/다른 container, TTL safety 미지정을 확인했다.
- 해결: strict metric math, measured case manifest check, Docker resource coverage validator, runtime phase+safety TTL contract를 추가했다.
- 추가 PM finding: 전체 summary가 맞아도 회원별 status 금액이 바뀌는 false-green, JS Number의 2^53 초과 누적 counter 손실, Docker Desktop dual-stack binding 오거부를 확인했다.
- 해결: 기존 DTO 8필드 member row exact 비교를 preflight/measured에서 공유하고, counter JSON을 strict decimal string으로 바꿔 `BigInt`로 계산하며, numeric loopback address family에 맞는 `8080/tcp` binding만 선택한다.
- 재발 방지: 자동 adoption marker를 제거하고 PM 확인 전까지 `conditional-shared-stack`; 실제 측정 전 상태는 `scenario-ready, not measured`로 유지한다.

## 8. 다음 작업

- [ ] PM이 container/service/DB identity, `EXEC193_` ID, `EXTERNAL_ACTIVITY=none`, warmup/measured, token safety, Docker max-gap 입력을 승인한다.
- [ ] shared stack 단독 사용을 확인하고 실제 before baseline을 실행한다.
- [ ] raw report와 correctness/DB/Docker evidence를 PM에 보고한다.
- [ ] 별도 승인 전 production 최적화를 시작하지 않는다.

## 9. Velog 글감

- 공유 Docker stack에서 성능 baseline을 오염시키지 않는 runner lock과 evidence 설계
