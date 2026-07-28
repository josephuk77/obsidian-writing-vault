---
project: FaithLog
type: devlog
issue: "#192"
status: baseline
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - performance
  - k6
  - before
---

# #192 커피·밥 투표 정산 1,000명 before baseline

## 1. 작업 배경

COFFEE close/settlement와 MEAL post-settlement는 응답자별 계좌/기존 청구 조회와 개별 저장을 반복한다. production 성능 코드를 바꾸기 전에 ACTIVE member 1,000명에서 재현 가능한 개선 전 기준선을 측정했다.

## 2. 최신 실행 환경 결정

- shared `faithlog-latest` keep-running
- backend `127.0.0.1:28080`
- PostgreSQL 17 `127.0.0.1:25432`
- Redis 7 `127.0.0.1:26379`
- 기존 frontend QA fixture(users 7/campuses 1/members 7/polls 3/responses 7/charges 5) 삭제·수정 0
- container stop/rebuild/down/prune 0, 측정 후 health 200/UP
- 다른 baseline/frontend/부하 테스트와 병렬 실행하지 않음

## 3. Fixture

`PERFORMANCE_192_BEFORE_20260714_A`, seed `192000`을 사용했다.

- 별도 PERFORMANCE campus와 ACTIVE member 1,000명
- COFFEE/MEAL 각각 17 poll
  - sequential warmup 1(통계 제외)
  - sequential measured 10(VUS 1)
  - concurrent warmup 1(통계 제외)
  - concurrent measured 5(VUS 5)
- poll당 option 4, final responses 1,000, response options 1,000
- 전체 polls 34, responses 34,000, response options 34,000
- option별 250명 결정적 분배
- MEAL option: PER_MEMBER 5,000/6,000원, GROUP_TOTAL 10,001/20,003원

actor 한 명만 실제 signup API를 사용하고, 999명 × 34 poll의 대량 row는 setup 비용이 settlement latency에 섞이지 않도록 additive DB seed로 생성했다. 기존 row는 UPDATE/DELETE/TRUNCATE하지 않고 seed 전 ID 범위 checksum을 저장했다.

## 4. TDD 기록

1. shared lifecycle 불변, fixture count/seed, custom Trend, VUS5, 통계 수집, DB 무결성을 검사하는 Node 계약 테스트를 먼저 작성했다.
2. 구현 파일이 없어 `5 tests / 5 failures` RED를 확인했다.
3. seed/manifest, k6, runner, verifier, summarizer, README를 구현했다.
4. `5 tests / 0 failures` GREEN과 Node/Bash 문법 검증을 통과했다.
5. k6 raw summary 구조가 예상한 `metric.values`가 아니라 metric 직접 값이어서 summary 단계만 실패했다. raw 측정과 DB verification은 보존됐고 파서를 실제 구조와 호환하도록 수정해 재측정 없이 summary를 복구했다.

## 5. Baseline 결과

| mode | p50 | p95 | max | failure |
| --- | ---: | ---: | ---: | ---: |
| COFFEE sequential | 1,532.245ms | 2,027.062ms | 2,161.118ms | 0.00% |
| MEAL sequential | 1,803.806ms | 2,122.883ms | 2,146.442ms | 0.00% |
| COFFEE VUS5 | 2,630.567ms | 2,779.701ms | 2,808.399ms | 0.00% |
| MEAL VUS5 | 1,827.121ms | 1,940.715ms | 1,963.340ms | 0.00% |

Docker peak sample:

- COFFEE sequential: app 186.13% CPU/543.1MiB, PostgreSQL 27.49%/114.6MiB, Redis 1.73%/9.63MiB
- MEAL sequential: app 136.09%/532.8MiB, PostgreSQL 22.14%/119.2MiB, Redis 0.79%/9.63MiB
- COFFEE VUS5: app 364.33%/535.7MiB, PostgreSQL 39.14%/125.4MiB, Redis 0.51%/9.63MiB
- MEAL VUS5: app 88.97%/590.9MiB, PostgreSQL 15.26%/130.0MiB, Redis 0.72%/9.63MiB

## 6. PostgreSQL 관찰

`pg_stat_statements`는 available하지만 installed=false였다. shared PostgreSQL의 preload/restart가 필요하므로 변경하지 않았고 SQL calls/total execution time 상위 query는 `shared Docker 제약으로 미측정`이다.

대체 `pg_stat_user_tables` delta에서 warmup 포함 순차 11 poll 기준:

- COFFEE: `payment_accounts` index scan 11,011, `charge_items` index scan 11,000, insert 11,000
- MEAL: `payment_accounts` index scan 11,022, `charge_items` index scan 11,000, insert 11,000

응답자별 계좌 검증, source charge lookup, 개별 save 반복이 명확한 개선 후보다. COFFEE response-option 조회의 scan 형태와 인덱스 필요성도 후보지만 DB/Flyway 변경은 사용자 승인 후에만 판단한다.

## 7. DB 무결성

- COFFEE charges 17,000
- MEAL charges 17,000
- meal settlements 17, charge groups 68
- source unique duplicate 0
- poll별 responses/options 1,000
- COFFEE option snapshot amount와 charge 일치
- MEAL group amount와 charge 일치
- GROUP_TOTAL exact ceiling/actual/rounding 및 settlement totals 일치
- 기존 fixture users/campuses/members/polls/responses/charges count/checksum 불변

## 8. 결과 경로와 다음 단계

ignored report: `build/reports/k6/poll-settlement/runs/20260714T022829Z/`

최종 검증은 baseline Node 계약 5/5, Node/Bash 문법, k6 inspect VUS5/5 iterations, 전체 449 tests/0 failures/0 errors/3 skipped, Gradle build, asciidoctor, REST Docs snippet group 151개와 렌더된 index, diff check를 통과했다.

이 수치는 개선 성과가 아니라 `before` 기준선이다. PM baseline 승인 전 production 성능 코드 변경, push, PR은 하지 않았다. 다음 단계는 PM이 동일 fixture/seed 조건을 승인한 뒤 bulk account/source charge 조회와 batch save 후보를 TDD로 검토하는 것이다.
