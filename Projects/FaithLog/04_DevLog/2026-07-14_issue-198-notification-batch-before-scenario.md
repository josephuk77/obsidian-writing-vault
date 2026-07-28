---
project: FaithLog
type: devlog
issue: "#198"
status: scenario-ready-not-measured
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - notification
  - tdd
---

# #198 알림 생성·전송 before 시나리오

## 1. 작업 배경

현재 알림 생성·전송이 1,000명 대상에서 수행하는 token 조회, notification log 생성·상태 저장, 실패 token 비활성화 비용을 production 최적화 전에 측정할 수 있도록 before harness를 준비했다. 이번 단계는 `scenario-ready / not-measured`이며 실제 fixture, notification job, Docker, 성능 DB, Firebase 전송과 baseline 측정은 실행하지 않았다.

## 2. 측정 경계

- scheduler가 target user ID를 계산한 뒤 호출하는 `NotificationRequestCommandService.requestAutomaticNotification`부터 측정한다.
- 생성 단계의 사용자별 Redis daily dedupe, active sendable token 조회, PENDING/SKIPPED log 저장을 포함한다.
- captured request ID를 실제 `NotificationDeliveryWorker.processRequest`에 전달해 token 재조회, production `1s → 5s → 30s` retry backoff, SENT/FAILED/SKIPPED 저장, permanent failure token 비활성화를 포함한다.
- cron cadence와 upstream target discovery duration은 제외한다.
- 현재 key인 `notificationType + campusId + scopeId + targetUserId + businessDate`, 전달된 target을 request service가 다시 campus membership 검증하지 않는 경계, 사용자별 partial failure continuation을 characterization한다.

## 3. 안전 계약

- `PERF_FCM_ADAPTER=fake`, local test harness, Firebase credential 부재를 모두 강제한다.
- `test|docker|prod`와 기타 profile, 사용자 승인 project와 다른 actual Compose label, label 누락, manifest의 Compose project/database 불일치, inherited DB/Redis endpoint, dirty worktree, `faithlog-latest` shared stack을 즉시 거부한다.
- Spring context 시작 전 datasource/Redis endpoint를 고정하고 `ComposeCoffeeCatalogSeedRunner`를 test mock으로 대체해 dummy token/log 밖의 seed mutation을 막는다.
- Spring endpoint는 inspected dedicated container의 published host port로 강제하고 Java harness에서 URL/host/port/DB와 `ddl-auto=validate`를 다시 검증한다.
- test-only deterministic fake sender가 success, transient-then-success, permanent failure만 재현하며 실제 Firebase class나 credential을 사용하지 않는다.
- `PERFORMANCE_198_DUMMY:` token과 fixtureRunId marker log만 허용한다. non-dummy active token이 있으면 fixture 준비가 fail closed하며 fixture 외 token은 수정하지 않는다.
- fixture와 runner가 #198 global lock과 actual Compose project 이름의 canonical lock을 함께 획득한다. same-project lock이 이미 있으면 fixture SQL과 Gradle을 시작하지 않는다.
- initial/before/after/final container ID·image·StartedAt·Compose service/config hash, PostgreSQL database/endpoint/postmaster start, Redis run ID/port/uptime가 연속적인지 verifier 전에 확인한다.
- Docker lifecycle 명령은 runner에 포함하지 않는다.

## 4. Fixture와 correctness

- 기존 PERFORMANCE campus의 ACTIVE member 정확히 1,000명을 재사용하고 user/campus/member를 만들거나 수정하지 않는다.
- `datasetId`와 sample별 `fixtureRunId`, `warmup|measured`를 분리한다.
- success/transient/permanent/inactive/no-token count는 모두 양수이며 합계 1,000인 runtime 필수 입력이다. 승인되지 않은 비율과 반복 횟수는 기본값으로 정하지 않는다.
- 생성 log 1,000개, PENDING/SKIPPED 분포, 최종 SENT/FAILED/SKIPPED 분포, permanent dummy token 비활성화를 exact count로 검증한다.
- 동일 dedupe replay log 0, request ID의 다른 campus/user log 0, fixture 외 token mutation 0, permanent failure 뒤 나머지 SENT 지속을 검증한다.
- success+permanent token을 함께 가진 sentinel 사용자의 log가 SENT이고 permanent dummy token만 inactive가 되는 사용자 내부 partial failure도 검증한다.

## 5. 지표 계약

- creation/delivery duration과 throughput의 p50/p95/p99/max
- Hibernate prepared statements와 1,000명 기준 per-user DB calls
- Gradle/Spring startup과 correctness replay/postflight를 포함하는 harness-lifecycle PostgreSQL table/database counter 및 Redis commandstats delta. exact schema/stats reset/captured ordering과 strict numeric monotonicity를 요구하고, 다른 부하가 없는 전제에서 notification log/token physical write와 Redis SET의 logical write 대비 under/over-count를 모두 거부한다.
- approved cadence로 immutable PostgreSQL+Redis identity 두 row가 있는 Docker sample instant를 최소 2개 수집하고 workload 전후를 덮는다. missing/null/string/mixed-container/one-sample evidence는 실패한다.
- Java process CPU duration/heap delta 및 PostgreSQL/Redis container raw CPU/RAM
- notification log/token insert/update count
- permanent fake send failure/attempt 기준 provider failure rate, final FAILED/PENDING log rate와 exact correctness 결과

실제 sample을 실행하지 않았으므로 위 항목은 모두 `not measured`다. 개선 수치나 이력서 성과로 해석하지 않는다.

현재 sample은 매번 새 test JVM을 띄우는 cold-JVM 모델이고 warmup은 외부 PostgreSQL/Redis cache만 대상으로 한다. additive fixture가 dummy token/log/dedupe history를 sample마다 늘리므로 summarizer는 runtime approved exact warmup/measured count와 unique fixtureRunId를 검증한 뒤에도 fail-closed disabled 상태다. `snapshot-restore|fixture-only-cleanup` 중 하나와 cold-JVM 또는 same-JVM 반복 모델을 사용자가 승인하고 구현이 pre-run equivalence를 증명하기 전에는 summary/percentile을 만들지 않는다.

## 6. TDD와 검증

1. 구현 파일 전에 scenario guard, fixture, runner, harness, metric/correctness 계약 테스트 5건을 작성했다.
2. 파일 부재로 `5 tests / 5 failures` RED를 확인하고 별도 커밋했다.
3. fixture SQL/shell, guarded runner, Java test harness, verifier, summarizer, README를 최소 구현했다.
4. PM 리뷰에서 endpoint/Compose binding, cross-worktree lock, production retry backoff, partial failure 순서, evidence 파싱과 workload fingerprint를 보강했다.
5. PM 전체 diff finding 5건을 approved sample count 부재, cumulative-state 충돌, canonical lock 불일치, runtime continuity 부재, strict evidence 부재의 `5 tests / 5 failures` RED로 재현하고 별도 커밋했다.
6. exact count gate, fail-closed cumulative enum, fake same-project lock, fake same-name runtime replacement, strict PostgreSQL/Redis/Docker evidence를 구현했다.
7. 최종 독립 리뷰에서 post-lock endpoint race, SQL `_` wildcard prefix, transient Docker replacement, Redis SET evidence default, signal cleanup, 임의 cadence tolerance와 음성 계약 부족을 RED로 고정했다.
8. locked/initial/before/after/final identity, exact dummy prefix, immutable-ID stats, missing command fail-closed, HUP/INT/TERM cleanup, runtime-approved maximum gap을 구현했다.
9. runtime 재리뷰에서 workload 직전 continuity 지연, inherited final phase 축소, fixture signal cleanup, mutable-name SQL/snapshot을 RED로 고정하고 pre-workload exact check, immutable-ID exec, lock ownership cleanup으로 보강해 전체 Node 계약 `14 tests / 0 failures` GREEN을 확인했다.
10. 기존 전체 `450 tests / 0 failures / 4 skipped`, Gradle build, asciidoctor 이력은 유지한다. production Java/Gradle은 변경하지 않았다.

## 7. 변경 제외 범위

- production Java/API/권한/응답/오류/트랜잭션/Entity/DB/Flyway/의존성 변경 0건
- batch size, bulk token query, log batch insert/update, Redis pipeline/Lua 적용 0건
- notification job/fixture/seed/Docker/성능 DB/Firebase 실행 0건
- 실제 credential/token 값 기록 0건
- push/PR/merge 0건

## 8. 다음 작업

- [ ] PM이 dedicated non-shared Compose project와 fixture 분포를 승인한다.
- [ ] PM이 warmup/measured 반복 횟수를 승인한다.
- [ ] PM이 Docker stats cadence와 maximum gap을 승인한다.
- [ ] PM이 cold-JVM 또는 same-JVM 반복 실행 모델을 승인한다.
- [ ] PM이 동일 DB/Redis snapshot 복원 또는 fixture-only cleanup 정책을 승인한다.
- [ ] 승인한 cumulative-state 전략을 구현하고 각 sample의 동일 pre-run fingerprint를 증명한 뒤 summarizer gate를 연다.
- [ ] 다른 부하가 없는 상태에서 fixture와 before sample을 실행한다.
- [ ] raw evidence와 correctness report를 검토한 뒤 production batch 후보 적용 여부를 별도로 결정한다.

## 9. Velog 글감

- 외부 FCM을 완전히 차단하면서 실제 notification service/worker 경로를 측정하는 characterization harness 설계

## 10. 2026-07-16 current-develop 공통 무결성 보정

- latest develop `6796ed146244d8f3f5b5dd7048ebe16865084a97`의 Flyway V1-V11과 #200 reminder/FCM/dedupe/stale-token production source identity를 고정했다.
- delivery는 current #200 request-wide bulk token snapshot 1회와 request log ID ascending ordering을 before 동작으로 보존한다. pagination/archive 및 #206 charge ordering은 이 notification direct-service workload에 적용되지 않는다.
- target Compose project, full PostgreSQL/Redis container ID, Compose service, image ID, PostgreSQL credential과 Redis auth mode는 fallback 없는 runtime 필수값이다.
- locked/initial/before/after/final container·PostgreSQL·Redis continuity, canonical decimal-string/BigInt cumulative counters, pg_stat_statements available/unavailable continuity, exact PostgreSQL+Redis CPU/RAM bytes-percent/cadence-window를 fail-closed 검증한다.
- fixtureRunId token과 notification-log namespace freshness를 모두 확인한다. 모든 prepared/verified/failed 결과는 `accepted=false`, `automaticAdoption=false`이며 최초 machine-readable rejection은 덮어쓰지 않는다.
- k6 v2 Counter/Rate/Trend는 Java direct-service harness에 적용되지 않는다. exact scenario failure 0과 creation → dedupe-replay → delivery 순서를 기록하며 p50/p95/p99/max는 승인된 multi-sample 전략 전까지 생성하지 않는다.
- 공통 감사 RED는 `7 tests / 7 failures`, 최소 GREEN 후 감사 계약은 `7 tests / 0 failures`였다. 실제 Docker/DB/HTTP/k6/fixture/cleanup은 실행하지 않았고 상태는 계속 `scenario-ready / not-measured`다.

## 11. 2026-07-17 fresh-05 conditional isolated before

- project/batch/report: `faithlog-perf-198-20260717-05` / `before-20260717-05` / `/private/tmp/faithlog-perf-198-reports/20260717-05`
- snapshot restore 11회, warmup 1회, measured 10회, final summary가 exit 0으로 완료됐다.
- 상태는 `conditional-isolated-snapshot-restored`, `accepted=false`, `automaticAdoption=false`, fake/local, cold-JVM이며 `externalFcmUsed=false`다.
- report 467개 파일의 read-only inventory SHA-256은 size/mtime 목록 `943cacc98f80c2c1cb8db45427f7fbc473d9ed10143706337862d8e8c17d6036`, per-file SHA 목록 `254ab5f3130278fac876323c96e9bd2478ea4134456e583e5e87e90e22e60597`다.
- creation duration p50/p95/p99/max는 `4374.0778125 / 4587.04813545 / 4616.35986069 / 4623.687792 ms`, throughput은 `228.62278901445 / 235.99378014695 / 238.75170402809 / 239.44118499837 /s`, prepared statements `2000`, per-user `2`다.
- delivery duration은 `104736.676979 / 105108.45254375 / 105224.59380875 / 105253.629125 ms`, throughput은 `7.63820300717 / 7.64814053088 / 7.64826889765 / 7.64830098934 /s`, prepared statements `1805`, per-user `1.805`다.
- end-to-end duration은 `109151.666791 / 109580.61548765 / 109694.45399753 / 109722.913625 ms`, throughput은 `9.16156855108 / 9.18092293976 / 9.18241306935 / 9.18278560175 /s`다.
- totals는 targets/log inserts `10000`, SENT `7000`, FAILED `1000`, SKIPPED `2000`, creation-stage PENDING `8000`, log updates `8000`, token updates `1010`, fake attempts `9010`, permanent failures `1010`이다. provider fake failure rate는 `0.1120976692563818`, final log failure rate는 `0.125`다.

위 수치는 conditional isolated before이고 자동 resume claim이나 운영 SLO가 아니다. Creation의 prepared statements `2000`은 사용자별 token select `1000` + identity log insert `1000`으로 확인했다. TDD RED로 dedupe/campus/user/order/PENDING-SKIPPED/dispatch를 고정한 뒤 manual/automatic request token 조회를 request-wide bulk 1회로 변경했다. 예상 creation prepared statements는 약 `1001`이지만 actual after와 개선율은 PM의 별도 after load 전까지 미측정이다. Delivery의 `1805`는 partial failure 내구성을 위한 per-log/per-token 독립 transaction을 유지해 이번 변경 범위에서 제외했다.
