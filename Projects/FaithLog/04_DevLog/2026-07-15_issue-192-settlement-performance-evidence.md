---
project: FaithLog
type: devlog
issue: "#192"
status: in-progress
created: 2026-07-15
tags:
  - FaithLog
  - backend
  - performance
  - tdd
---

# #192 정산 성능 before baseline evidence 계약

## 작업 배경

최신 `origin/develop`의 #200 COFFEE ownership/duty 계약과 #201 page-size/archive 계약에 맞춰 정산 fixture/API 시나리오 drift를 보정했다. 실제 baseline 측정 전 PM 리뷰에서 발견한 runtime, DB, resource, metric, pg_stat_statements, correctness evidence false-green 경로를 fail-closed 계약으로 고정했다.

## 구현 내용

- app/PostgreSQL/Redis full ID, image, StartedAt, Compose service/config hash, port 및 DB/postmaster/Redis run ID exact continuity
- canonical decimal string/BigInt DB counter delta, exact table/planner/maintenance/idle activity schema
- pg_stat_statements global reset 제거 및 strict cumulative composite identity delta
- Docker full ID/name one-to-one resource sample, interval/max-gap/window/CPU/RAM 검증
- warmup/login을 measured DB/resource window 전에 별도 k6 process로 격리하고 fresh JWT를 사전 검증
- measured throughput을 exact request count와 earliest-start/latest-finish window로 계산
- DB-derived exact charge identity/API page/order correctness 및 conditional boundary-only summary gate

## TDD 기록

- 1차 RED: 14개 중 9 pass / 5 fail
- 추가 RED: warmup/token boundary와 clean evidence의 `accepted:true` 모순 재현
- maintenance quiet gate RED: focused 20개 중 10개 실패로 5/30/180 exact binding, 30초/29초 경계, worker/drift reset, timeout, strict collector/schema, runner 순서, summary metadata와 missing-evidence false-green 재현
- PM false-green RED: overall 30초지만 `resetCount=6`인 위조 passed evidence 채택, 마지막 quiet 29/30초 provenance, 5초 미만 synthetic poll을 focused 16개 중 13 pass/3 fail로 재현
- 승인 preflight RED: initial capture 뒤 post-lock snapshot이 continuity의 initial-only phase 검사에 잘못 들어가 안전 중단됨
- 두 번째 승인 preflight RED: `docker exec`에 `-i`가 없어 stdin SQL이 PostgreSQL collector로 전달되지 않고 exit 0/empty stdout이 발생함
- 세 번째 승인 runner 감사 RED: `prepare-measured-token.mjs`의 TTL gate가 실패해도 `if ! run_mode` 조건식에서 Bash `set -e`가 함수 본문에 적용되지 않아 DB-before/resource/measured k6/db-after가 계속됨
- 최소 수정: 임의 명시 phase의 strict schema/target 자체 검증을 `validateRuntimeSnapshot`으로 분리하고 initial-only 규칙은 continuity에 유지
- 최소 수정: DB collector를 immutable PostgreSQL ID의 `docker exec -i`로 연결하고 empty stdout을 SQL·stderr 원문 노출 없이 명시적으로 거부
- 최소 수정: `run_mode`의 runtime-before/warmup/token과 DB/resource/runtime evidence critical step에 명시적 실패 반환을 적용해 조건식 문맥과 무관하게 fail-fast를 보장하고 기존 final runtime/rejected cleanup 경계를 유지
- GREEN: `quietStartedAt`과 최소 poll interval 보강 후 전체 static/fake 계약 49/49 pass, `bash -n`, 전체 Node syntax, working/branch `git diff --check` 통과

## 측정 상태

승인된 첫 두 preflight는 fixture/DB write/k6 load 전에 안전 중단되었다. 거부된 `EXEC192_BEFORE_20260716_A`와 `PERFORMANCE_192_BEFORE_20260716_B` / `BEFORE_..._B` / `EXEC..._B`는 재사용하지 않고 보존한다.

세 번째 승인 runner `_C`는 fresh seed(1,000 users/34 polls/34,000 responses)를 완료한 뒤 coffee-sequential warmup 1회를 실행했다. PM의 read-only DB 감사 결과 campusId 3, ACTIVE memberships 1,000, polls 34, CLOSED COFFEE 1/OPEN 16, COFFEE charges 1,000, MEAL charges 0이다. measured token TTL gate에서 중단되어 measured settlement k6 요청은 0건이지만 warmup coffee settlement 1회가 1,000 charges를 생성했으므로 `_C` fixture/report는 partial-write rejected run으로 보존하고 절대 재사용하지 않는다. 수치 summary가 생성되더라도 continuous observer 부재를 명시해 `measurementStatus=conditional-boundary-only`, `automaticAdoption=false`, `accepted=false`로 분류한다.

승인 runner `_D`는 fresh fixture campusId 4, ACTIVE 1,000명, polls 34에서 COFFEE sequential warmup 1회와 measured 10회를 HTTP/check/failure 0으로 완료했다. 관찰된 measured latency는 avg 1,758.608ms, p50 1,579.446ms, p95 3,070.672ms, p99 3,819.714ms, max 4,006.974ms, count 10이다. DB 감사는 CLOSED COFFEE 11/OPEN COFFEE 6, COFFEE charges 11,000, MEAL 0이다. 그러나 resource timestamps `22:50:50.459`, `53.601`, `56.731`, `59.858`, `22:51:03.000`, `05.106` 사이 gap이 약 3.1초로 approved maxGap 3초를 넘었고 runtime-after/db-after/status가 생성되지 않았다. 따라서 이 latency는 불완전 evidence의 관찰값일 뿐 baseline 또는 성과로 채택하지 않으며 `_D` fixture/report는 rejected로 보존하고 절대 재사용하지 않는다.

`_D` root cause는 blocking `docker stats --no-stream` capture 약 2.1초 뒤 unconditional sleep 1초가 더해진 cadence와 marker 제거 시 while body가 status 1을 반환한 것이다. initial synchronous sample 뒤 marker 동안 blocking capture를 back-to-back 실행하고 marker 종료 뒤 explicit 0, capture 실패 시 non-zero를 반환하도록 보정했다. approved maxGap 3초는 완화하지 않는다.

승인 runner `_E`는 COFFEE sequential warmup 1회와 measured 10회를 모두 성공했고 failure는 0이다. 관찰 latency는 avg 857.750ms, p50 834.618ms, p95 992.683ms, p99 1,090.164ms, max 1,114.534ms이며 measured window는 `22:58:20.396Z`~`22:58:28.976Z`다. resource samples는 `20.332`, `22.334`, `24.351`, `26.356`, `28.368`, `30.395`, `32.428`로 consecutive gap 2,002~2,033ms가 모두 maxGap 3초 이내다. nearest pre-start sample은 64ms 전, earliest post-end sample은 1,419ms 후라 경계를 충족하지만 별도 final sample이 end보다 3,452ms 늦다는 이유로 false reject되었다. 따라서 `_E`는 rejected로 보존하고 절대 재사용하지 않으며 관찰 latency를 baseline 또는 성과로 채택하지 않는다.

resource boundary coverage는 전체 first/last 대신 `latest(sample <= start)`와 `earliest(sample >= end)`를 선택해 각각 maxGap 이내인지 검증한다. extra pre/post sample도 strict schema/identity, timestamp unique/monotonic, consecutive maxGap을 모두 통과해야 한다. mode validator 실패는 sanitized stage와 `resource-boundary-coverage` 같은 reason을 machine-readable rejected adoption에 기록하고, runner는 future mode가 없는 상태에서 full summarizer를 실행하지 않아 최초 원인을 보존한다. 실제 재실행은 PM만 fresh `_F` IDs로 수행한다.

승인 runner `_F`는 COFFEE sequential warmup 1회와 measured 10회를 모두 성공했고 failure는 0이다. 관찰 latency는 avg 1,085.800ms, p50 1,019.432ms, p95 1,394.072ms, p99 1,525.923ms, max 1,558.886ms다. initial synchronous resource sample은 성공했지만 첫 background `docker stats` row가 `resource memory percent consistency`로 거부되어 after evidence가 없다. Docker가 independently rounded `MemUsage` used/limit와 `MemPerc`를 출력하는데, 기존 validator가 used/limit 대표 byte ratio와 percentage 표시 정밀도만 비교한 것이 false reject 원인이다. `_F`는 rejected로 보존하고 절대 재사용하지 않으며 관찰 latency를 baseline 또는 성과로 채택하지 않는다.

collector와 evidence validator는 used, limit, memory percentage 각 표시값의 unit·decimal precision에서 half-display-unit 구간을 만들고, 가능한 used/limit ratio 구간과 percentage 구간의 inclusive overlap을 하나의 BigInt 계약으로 검증한다. canonical safe-integer byte/display binding, memory percentage 100 상한, multi-core CPU 100 초과 허용은 양 경계에서 동일하다. background capture/parser 실패는 최초 stage `coffee-sequential-resource-sampler`와 reason `resource-capture-failed`를 비밀·raw Docker row·stderr 없이 기록하고 후속 capture 또는 generic cleanup이 덮지 못한다. 실제 재실행은 PM만 fresh `_G` IDs로 수행한다.

승인 runner `_G`는 fresh seed와 COFFEE sequential을 통과한 뒤 MEAL sequential DB pair에서 `users` maintenance drift를 감지해 fail-closed했다. `autovacuum_count`는 `1 -> 2`, `lastAutovacuum`은 `22:50:57Z -> 23:34:59Z`로 바뀌었다. accepted/validated adoption은 생성되지 않았으며 `_G`는 rejected로 보존하고 절대 재사용하지 않는다.

승인 runner `_H`는 fresh seed 직후 COFFEE sequential DB pair에서 `poll_responses` maintenance drift를 감지해 fail-closed했다. `autovacuum_count`는 `3 -> 4`, `lastAutovacuum`은 `23:07:58Z -> 23:37:59Z`로 바뀌었고, 같은 시각 `poll_response_options.autovacuum_count=4`였다. 후속 감사 시 active autovacuum worker는 0이었다. accepted/validated adoption은 생성되지 않았으며 `_H`도 rejected 보존·재사용 금지다.

두 run은 대량 seed와 `ANALYZE` 뒤 최대 약 17초 후 시작한 autovacuum이 measured DB window에 진입한 사례다. 기존 validator는 maintenance 오염을 의도대로 차단했다.

사용자는 post-seed maintenance quiet gate를 poll 5초, 연속 quiet 30초, timeout 180초로 승인했다. runner는 fresh fixture seed와 기존 `ANALYZE`를 완료한 뒤, 첫 warmup과 모든 DB/resource measurement boundary 전에 gate를 실행한다. 각 read-only poll은 instance-wide `backend_type='autovacuum worker'` active count와 12개 evidence table의 `last_analyze`, `last_autoanalyze`, `last_vacuum`, `last_autovacuum`, `analyze_count`, `autoanalyze_count`, `vacuum_count`, `autovacuum_count` exact snapshot을 수집한다. worker가 하나라도 active이거나 필드 하나라도 drift하면 quiet clock을 즉시 reset하며, 29초는 통과하지 않고 30초 경계는 통과한다. 180초 내 충족하지 못하거나 schema/collector가 실패하면 warmup 전에 fail-closed한다.

5/30/180은 암묵 default 없는 runtime-required target/report identity다. machine evidence에는 case, 승인 입력, gate start, 마지막 `quietStartedAt`, 종료, poll/reset count, final status, sanitized reason만 기록하고 raw SQL, stderr, path, credential/token은 넣지 않는다. passed evidence는 마지막 quiet start부터 종료까지 최소 30초, 전체 gate 최대 180초를 독립 검증한다. reset 0이면 quiet start는 gate start와 같고 reset 1회 이상이면 더 늦어야 한다. synthetic observation은 consecutive gap 최소 5초이며 collector overhead에 따른 더 긴 gap만 허용한다. 추가 `VACUUM`/`ANALYZE`, autovacuum/config 변경, statistics reset, extension 변경은 없다. `_G`, `_H`와 모든 prior rejected ID는 계속 재사용 금지다.

PM-only fresh `_I`는 quiet gate `00:27:43.472Z~00:28:14.226Z`, `quietStartedAt=start`, 7 polls/reset 0, exact 5/30/180을 통과했다. COFFEE sequential과 MEAL sequential measured가 success/failure 0으로 끝났고 COFFEE concurrent도 5 requests/failure 0까지 실행됐다. 그러나 concurrent measured window `00:28:56.165Z~00:29:02.504Z`의 마지막 약 0.6초에 `charge_items` natural autovacuum `00:29:01.911Z`와 autoanalyze `00:29:02.139Z`가 겹쳤다. before `autoanalyze_count=4/autovacuum_count=2`, after `5/3` drift를 validator가 감지해 runner는 fail-closed했고 accepted/validated summary는 생성하지 않았다. `_I`는 rejected 보존·재사용 금지다.

관찰 latency avg/p50/p95/p99/max는 COFFEE sequential `949.660/936.207/1069.439/1087.285/1091.746ms`, MEAL sequential `980.010/960.980/1088.337/1095.499/1097.290ms`, COFFEE concurrent `3745.826/3811.780/6127.945/6295.797/6337.760ms`다. 모두 rejected 관찰값이며 baseline 또는 성과로 채택하지 않는다.

post-seed quiet만으로는 앞선 mode의 누적 write가 `n_mod_since_analyze`를 올리고 다음 mode 예상 write와 합쳐 natural autoanalyze threshold를 넘는 상황을 차단하지 못했다. 관찰 설정은 analyze threshold 50, scale factor 0.1, naptime 1min이고 `_I` 후 `charge_items.reltuples=162011`, `n_mod_since_analyze=2000`이다.

사용자는 각 mode warmup 직전 readiness gate를 승인했다. 실행 순서는 seed+기존 fixture `ANALYZE` 뒤 COFFEE sequential readiness/warmup/measured, MEAL sequential readiness/warmup/measured, COFFEE concurrent readiness/warmup/measured, MEAL concurrent readiness/warmup/measured다. exact expected writes는 순서대로 11,000/11,000/6,000/6,000이고, `n_mod_since_analyze + expectedWrites < triggerAt`과 worker0/12-table maintenance stable 30초를 함께 만족해야 quiet clock이 진행된다. 부족하면 자연 maintenance를 최대 180초 기다리고 worker/maintenance/headroom 변화는 quiet clock을 reset한다.

effective threshold/scale은 table reloption이 있으면 해당 값, 없으면 global current setting을 사용한다. trigger/projection은 JavaScript `Number` 없이 canonical decimal/BigInt와 reduced rational로 계산한다. mode evidence는 nMod, reltuples, effective base/scale, triggerAt, expected/projected writes, sufficient, 5/30/180, timestamps/polls/resets를 lossless exact schema로 보존하고 네 mode 모두 strict valid해야 conditional summary를 만든다. disabled autoanalyze, unknown/negative stats, malformed/unsafe 값, missing/mismatch/forgery는 fail-closed다. test-only RED 17/26에서 focused GREEN 27/27, 전체 static/fake 60/60을 확인했다. 수동 `VACUUM`/`ANALYZE`, config/reloption/reset/extension, Docker lifecycle, production/Flyway/dependency 변경은 없다. 다음 actual은 PM만 fresh `_J` ID로 실행한다.

PM-only fresh `_J`는 COFFEE sequential warmup 1회와 measured 10회 뒤 첫 DB pair에서 `activity drift`로 fail-closed했다. db-initial과 before에는 동일 semantic identity의 idle Hikari pool PID `33948`, `34291`, `34496`, `34906`, `35061`이 있었고, after에는 `33948` 대신 PID `35476` / backend start `01:00:03.539781Z`가 생겼다. semantic identity와 multiplicity 5는 유지된 정상 connection rotation이다. accepted/validated summary는 0이며 `_J`는 rejected 보존·재사용 금지, 모든 관찰값은 baseline/성과 채택 금지다.

snapshot별 exact row schema, unique PID, RFC3339 backend start, idle state와 raw PID/start provenance는 유지한다. initial/mode pair/inter-mode continuity는 PID와 backend start만 제외한 database/user/applicationName/clientAddress/state sorted multiset을 exact 비교한다. multiplicity/count, identity, state, null/malformed, duplicate PID drift는 계속 fail-closed한다. DB-pair validator는 최초 sanitized stage `coffee-sequential-db-pair-validator`와 reason `activity-drift`를 보존하고 raw path/stderr/credential/secret은 기록하지 않는다. test-only RED 21/26에서 최소 GREEN 26/26을 확인했으며 다음 actual은 PM fresh `_K`만 허용한다.

PM-only fresh `_K` IDs는 `PERFORMANCE_192_BEFORE_20260716_K` / `BEFORE_20260716_K` / `EXEC192_BEFORE_20260716_K`다. campusId 11, ACTIVE 1,000, fresh polls 34/responses 34,000에서 COFFEE sequential readiness가 `01:10:57.982Z~01:11:39.051Z`, quiet start `01:11:08.215Z`, poll/reset `9/1`, `nMod=0`, `reltuples=174011`, `triggerAt=17452`, expected/projected `11000/11000` sufficient로 통과했다. warmup 1회와 measured 10회는 failure 0/status 0이었다. rejected 관찰 avg/p50/p95/p99/max는 `877.7962/833.7495/1027.62265/1051.42693/1057.378ms`, count 10, rate `1.138697967/s`이며 baseline/성과가 아니다.

MEAL sequential readiness는 `01:11:55.984Z~01:15:01.008Z`, quiet start null, poll/reset `37/37`, `nMod=11000`, `reltuples=174011`, `triggerAt=17452`, expected/projected `11000/22000` insufficient로 `maintenance-readiness-timeout` 됐다. current nMod가 자연 trigger보다 낮아 last autoanalyze `00:29:02.139845Z`/count 5에서 멈춰 있지만 다음 mode projected 값은 trigger를 넘는다. 이 workload에서 승인된 natural-maintenance wait-only gate가 mode 사이에 진행 불가능함이 실제로 확인됐다. partial state는 COFFEE CLOSED/OPEN `11/6`, MEAL `17/0`, COFFEE/MEAL charges `11000/0`이다. baseline adoption은 rejected, accepted/validated 0이고 `_K`는 보존·재사용 금지다. exit 뒤 다른 k6/runner는 없었고 production/Flyway/dependency change는 0이다. 사용자 새 정책 결정 전 actual 재실행과 runner/test/production 변경은 금지다.

## Fresh single-mode 프로토콜

사용자는 `_K`에서 확인된 mode 사이 wait-only deadlock을 제거하기 위해 네 mode를 서로 다른 fresh dataset/fixture/execution으로 분리하는 정책을 승인했다. runner는 `coffee-sequential`, `meal-sequential`, `coffee-concurrent`, `meal-concurrent` 중 exact `MODE` 하나만 받고 default/alias/all을 거부한다. 각 실행은 full 1,000 ACTIVE/34 polls/34,000 responses create-only seed와 기존 fixture `ANALYZE` 뒤 selected readiness, warmup 1회, measured, selected correctness, final continuity, conditional summary만 수행하며 비선택 artifact/write는 0이어야 한다. 실제 네 부하는 PM이 한 서버에서 이 순서로 하나씩만 실행하고 integration after도 동일 프로토콜을 사용한다.

per-mode summary는 `conditional-boundary-only`, `accepted=false`, `automaticAdoption=false`다. strict bundle은 exact four modes, distinct dataset/fixture/execution IDs, 동일 source commit/target role/workload, contained regular JSON/no symlink, SHA-256 continuity, parsed target/fixture identity, conditional status를 검증한다. mode별 metric은 그대로 보존하고 단일 latency로 평균하지 않는다.

TDD는 single-mode/bundle focused RED 18개 중 9 pass/9 fail, 실제 `EXEC192_...` 경로와 parsed target/fixture 결속 RED 7개 중 3 pass/4 fail을 거쳐 focused 18/18, bundle 7/7, 전체 issue-local static/fake 77/77 GREEN으로 종료했다. 모든 issue-local Node syntax, Bash syntax, diff-check도 통과했다. production Java/API/DB, Flyway, dependency diff와 개발 세션 actual Docker/DB/fixture/k6 실행은 모두 0이다.

PM-only 첫 split attempt `_L`은 `PERFORMANCE_192_BEFORE_CS_L` / `BEFORE_CS_L` / `EXEC192_BEFORE_CS_L`, `MODE=coffee-sequential`로 시작했지만 preflight Node test가 parent MODE를 global DB collector fake child에 상속해 global evidence gate에서 실패했다. Docker/fixture/DB/k6 전 안전 중단됐고 mutable write는 예상되지 않지만 PM artifact audit 대상으로 보류하며 IDs는 재사용하지 않는다. production collector의 global/mode strict boundary는 그대로 두고 global test child에서 상속된 parent MODE만 제거했다. 같은 parent MODE에서 focused RED 0/2→GREEN 2/2, 전체 77/77을 확인했으며 개발 세션 actual 실행은 0이다.

PM-only retry `_CS_M`은 `PERFORMANCE_192_BEFORE_CS_M` / `BEFORE_CS_M` / `EXEC192_BEFORE_CS_M`로 preflight 77/77을 통과했지만 initial global DB capture에서 exported runtime MODE가 production collector child에 전달되어 fail-closed했다. partial report는 보존하며 fixture seed/write와 k6 load는 0으로 예상하고 IDs는 재사용하지 않는다. actual runner의 `capture_db` global/mode 분기를 추출한 harness가 global capture/validation의 MODE 누출과 mode scope의 exact selected MODE를 RED 3/4로 재현했다. global 두 child에만 `env -u MODE`를 적용한 뒤 focused 6/6과 parent-MODE 전체 77/77을 통과했다. collector schema와 mode evidence 계약, production/Flyway/dependency는 변경하지 않았고 개발 세션 actual 실행은 0이다.

PM-only fresh `_CS_N`은 origin/source commit `355f79d`, preflight 77/77 뒤 ACTIVE 1,000, polls 34, responses 34,000 fresh fixture seed를 완료했다. 그러나 `run_mode` 첫 local statement가 `mode` 할당과 mode-dependent path 확장을 동시에 수행해 `set -u mode: unbound variable`로 중단됐다. warmup/measured k6 artifact는 0이고 seed-report charge before/after 변화도 0이다. `_CS_N`은 fixture-write partial rejected로 보존하고 절대 재사용하지 않는다.

actual `run_mode` 함수 추출 harness에서 global lowercase mode fallback 없이 exact 인자를 전달했을 때 같은 nounset과 status 0/adoption null을 RED 1/4로 재현했다. `local mode="$1"`과 path locals를 다음 statement로 분리한 뒤 GREEN 4/4, parent-MODE 전체 77/77을 통과했다. 의도된 pre-measured failure는 status 1과 rejected adoption을 남겨 별도 trap 수정은 하지 않았다. production/Flyway/dependency와 개발 세션 actual 실행은 0이다.

## Valid current-develop before

PM은 `build/reports/k6/poll-settlement/bundles/EXEC192_BEFORE_BUNDLE_O`에서 source `355f79df5b2e47636b7d1a17dea029da6c93c62d`, target SHA `8a35ba2b2be146c40d89c00670fe16a62548e9a0e7d4501e347d7e05dee2ca80`, protocol `faithlog-192-single-mode-v1` bundle을 완료했다. `_CS_O/_MS_O/_CC_O/_MC_O`는 각각 fresh ACTIVE 1,000/polls 34/responses 34,000과 SHA continuity를 통과했다. 모든 failure rate는 0이고 evidence는 validated지만 `conditional-boundary-only`, `accepted=false`, `automaticAdoption=false`를 유지한다.

- COFFEE sequential: count 10, p50/p95/p99/max `890.6895/1117.2471/1168.37502/1181.157ms`, throughput `1.0649627`
- MEAL sequential: count 10, p50/p95/p99/max `1146.035/1294.67735/1303.83467/1306.124ms`, throughput `0.8567512`
- COFFEE concurrent: count 5, p50/p95/p99/max `2732.844/4330.2564/4474.45768/4510.508ms`, throughput `1.1084017`
- MEAL concurrent: count 5, p50/p95/p99/max `3019.871/6293.2634/6762.88068/6880.285ms`, throughput `0.7265330`

`pg_stat_statements`는 unavailable이고 DB/table counters와 resource evidence는 supporting data다. 이 bundle은 production 최적화 진입을 승인하는 current-develop before reference이며 자동 채택 성과가 아니다. actual after는 최종 integration에서만 수행한다.

## Production 정산 batch 개선

before supporting counter는 COFFEE/MEAL sequential에서 `payment_accounts.seq_scan=9009/10020`, `charge_items.idx_scan=9000/10000`, `users.idx_scan=9020/10032`, concurrent에서 COFFEE `4004/4000/4011`, MEAL `5010/5000/5017`이었다. 이는 기존 per-response 계좌/charge 조회 구조와 일치하지만 pg_stat_statements가 unavailable이므로 statement별 귀속 근거로 과장하지 않는다.

정산 서비스는 command collection 하나를 billing으로 전달하고, billing은 collection당 account를 한 번 검증한 뒤 source ID set으로 기존 charge를 한 번 잠금 조회한다. 기존 COFFEE UNPAID만 갱신하고 terminal 상태는 유지하며, MEAL 기존 charge는 동일하게 duplicate로 거부한다. 신규 entity는 repository collection-save boundary로 전달하지만 `ChargeItem` identity ID와 필수 row insert가 남으므로 JDBC insert batching을 주장하지 않는다.

API/controller/DTO, 인가, #200 creator/duty/account ownership, 정산 금액, duplicate prevention, transaction rollback, #201 archive paging은 변경하지 않았다. 신규 batch 계약은 production 수정 전 missing symbol 8건으로 RED였고, 최소 GREEN 뒤 신규 4/4, 확대 focused 134/134, 전체 Gradle 556 tests / failure 0 / error 0 / skipped 3, build, asciidoctor, issue-local static/fake 77/77을 통과했다. Docker/DB/k6/after는 실행하지 않았으며 개선률은 아직 없다.

#194 전달 후보는 locked bulk query `EXPLAIN (ANALYZE, BUFFERS)`와 `charge_items(campus_id,payment_category,source_type,source_id)`, 그리고 실제 plan 확인을 전제로 한 `poll_options(poll_id,sort_order)`다. `payment_accounts`는 PK가 이미 있으므로 fixture small-table seq scan만으로 새 index를 제안하지 않는다. #192에서 index/Flyway/dependency 변경은 0이다.

## 남은 작업

JWT issued lifetime 1,800초, sequential maxDuration 27분(1,620초), safety 120초, concurrent maxDuration 14분(840초) 계약으로 fresh single-mode before 네 건과 strict bundle 검증을 완료했다. 다음 성능 측정은 PM 최종 integration branch에서 동일 split protocol로 after를 순차 실행하는 단계다. index/Flyway 후보는 #194로 이관하며 #192 개별 브랜치에서는 after, Docker build, index/Flyway를 실행하지 않는다.

## 2026-07-17 current-develop R baseline 및 batch 구현

최신 authoritative before는 `EXEC192_BEFORE_CURRENT_BUNDLE_R`이다. source는 `6796ed146244d8f3f5b5dd7048ebe16865084a97`, target SHA-256은 `7e7dd3a430666112f5139cf3950f2b859dc49034c5306cee0b770cfe80b8cb62`다. 네 mode 모두 correctness와 HTTP/check failure 0을 통과했고, continuous exclusivity와 숫자 유효성을 분리하기 위해 `conditional-boundary-only`, `accepted=false`, `automaticAdoption=false`를 유지한다.

before p50/p95/p99/max는 COFFEE sequential `2932.822/6231.9487/6504.08494/6572.119ms`, MEAL sequential `1317.1715/1450.967/1514.9534/1530.95ms`, COFFEE concurrent VUS5 `3705.763/5941.3596/6143.80952/6194.422ms`, MEAL concurrent VUS5 `3892.11/6154.0946/6357.64532/6408.533ms`다. 성능 개선 전 authoritative evidence이며 성과 수치가 아니다.

COFFEE sequential의 `payment_accounts.seq_scan=10010`, `seq_tup_read=1241250`, `charge_items.idx_scan=10000`과 MEAL sequential의 `10020/1272540/10000`은 inspected call graph의 per-response account/charge lookup과 일치한다. `pg_stat_statements`가 없으므로 statement별 귀속으로 과장하지 않는다.

TDD RED는 batch service/repository 계약 부재 8개 compile error였다. 최소 GREEN은 COFFEE/MEAL command collection을 한 번 전달하고, account validation 1회, source ID set 기존 charge 잠금 조회 1회, repository collection-save 1회로 바꿨다. 기존 COFFEE UNPAID update와 terminal 보존, MEAL duplicate 409/final flush/rollback, #200 ownership/lock, amount/source/snapshot, scalar API는 유지한다. `saveAll`은 collection boundary일 뿐 Hibernate JDBC insert batching을 뜻하지 않으며 필수 charge row insert 수 감소를 주장하지 않는다.

자체 리뷰에서 batch `saveAll` 단계의 unique 충돌이 기존 MEAL duplicate 409 매핑을 우회하는 1/1 RED를 추가로 재현했고, save와 final flush를 같은 매핑 경계에 둬 수정했다. 검증은 신규 batch focused 5/5, 관련 billing/poll/#200/#201 113/113, 전체 Gradle 560 tests 중 failure/error 0, skipped 3, build와 asciidoctor GREEN이다. API/DTO/ErrorCode/frontend, Flyway/index/dependency는 변경하지 않았고 개발 세션은 Docker/after/load를 실행하지 않았다. bulk lookup index 후보는 #194에서 실행계획을 검증한다.

## 2026-07-16 latest-develop scenario compatibility

valid before bundle과 production 최적화 commit은 그대로 보존하고, `origin/develop` `6796ed146244d8f3f5b5dd7048ebe16865084a97` 기준 test/scenario만 별도 branch에서 보정했다. #206 stable charge paging에 맞춰 correctness expected page를 `created_at DESC, id DESC`로 고정했고, #202 RLS와 무관한 direct JDBC observer는 runtime target의 DB user/name만 사용하며 Supabase Data API credential을 사용하지 않는다.

runner의 `TARGET_CONTRACT`는 default 없는 runtime-required 입력이다. checked-in target JSON은 과거 before target의 immutable reference일 뿐 integration-after에 자동 재사용하지 않는다. before/after comparator는 같은 target role/workload, 서로 다른 source commit/target identity, exact four modes와 conditional evidence를 요구하며 mode별 지표를 분리 보존한다.

초기 drift 검증은 test-only RED `10/13`, focused GREEN `15/15`였다. 공통 무결성 전체 감사에서 source/Flyway/runtime/workload target이 mutable setup 전에 한 번에 검증되지 않는 gap과 실제 k6 v2 wrapper의 Counter/Rate/Trend metadata 및 Counter-rate/Rate passes-fails 수학 gap 3건을 RED `18/21`로 고정했다. 최소 GREEN 뒤 focused `21/21`, full issue-local static/fake `85/85`, Node syntax `31/31`, Bash syntax, JSON parse, diff-check GREEN이다. authoritative before O 네 mode의 measured/warmup evidence도 강화 validator를 read-only로 통과했다. 최신 develop 상태는 **scenario-ready / not measured**이며 Docker/DB/HTTP/fixture/k6/EXPLAIN과 production/Flyway/dependency 변경은 0이다. 여러 performance issue의 test code는 병렬 보정할 수 있지만 실제 부하는 PM이 한 서버에서 하나씩만 순차 실행한다.
