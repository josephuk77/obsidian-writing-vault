---
project: FaithLog
type: devlog
issue: "#189"
status: done
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - billing
---

# #189 밥 담당과 투표 항목 그룹별 후청구

## 1. 작업 배경

COFFEE와 분리된 다수 MEAL duty, 담당자별 본인 MEAL 계좌, 즉시 시작하는 SINGLE MEAL poll, CLOSED poll의 option group별 후청구가 필요했다.

## 2. 최종 설계 기준

- ACTIVE MEAL duty 수 제한 없음, role 변경 없음.
- service ADMIN/캠퍼스 관리자도 ACTIVE MEAL duty가 아니면 운영 API 403.
- 계좌는 본인 소유만 관리하고 settlement 시 poll 전체 공통 계좌 하나를 선택.
- 생성 시 `startsAt/createdAt`은 같은 서버 Clock Instant, 즉시 OPEN, 미래 endsAt만 입력.
- 사용자 option 추가와 기존 `optionIds`/`poll_response_options` 계약 유지.
- close 시 settlement/charge 0건.
- PER_MEMBER 또는 GROUP_TOTAL 정수 ceiling 계산. requested/actual/rounding 분리.
- poll row lock + settlement unique + charge source unique, 전체 단일 transaction.
- 다른 담당자 settlement의 account ID/상세 비노출.

## 3. 구현 내용

- Entity: `MealPollSettlement`, `MealPollChargeGroup`, MEAL enum 확장.
- Command: poll 생성, settlement/group, MEAL charge command.
- Service: 공통 MEAL duty access, 본인 계좌, poll create/manage/close, exact calculator, settlement, 본인 계좌 charge 집계.
- Repository: ACTIVE MEAL duty/account partial unique, poll pessimistic lock, settlement/group repositories.
- Controller: duty, account, management poll, close, batch charges, my-account charges.
- Test: duty/account isolation, immediate OPEN, forbidden fields, user-added option, close 0 rows, 10,000÷3 rounding, rollback, overflow, retry 409, account redaction, REST Docs.

## 4. TDD 기록

1. 실패 테스트 작성: enum/V8, account API, poll server time, poll charges, exact calculator.
2. 실패 확인: enum/V8 2 failures, account endpoint failure, missing `createdAt` compile failure, charges 404, calculator compile failure.
3. 최소 구현: enum/schema → duty → account → poll → settlement 순서.
4. 테스트 통과: 책임 단위 focused GREEN 확인.
5. 리팩토링: exact calculator 추출, generic admin MEAL 비노출, Clock 주입, DB race unique 보강.
6. 코드리뷰 RED: 일반 관리자 MEAL 우회·dashboard 노출·공용 poll lock·null list 요소는 82 tests 중 6 failures, 정산 poll 보존 삭제는 FK failure로 재현.
7. 코드리뷰 GREEN: 공용 pessimistic poll lookup, MEAL 404/dashboard 제외, V8 cascade, Bean Validation 보강 후 회귀 90 tests 통과.
8. 재리뷰 RED/GREEN: 수동 close의 `endsAt` 변경을 1 failure로 재현해 상태만 CLOSED로 바꿨고, 실제 write 후 rollback·전용 close 404·role 불변·PER_MEMBER/snapshot·7일 초과·30일 retention 범위 내 CLOSED 목록을 보강.
9. 최종 DB 리뷰 GREEN: settlement 응답 option ID 정렬을 구조 테스트 RED 후 고정해 첫 charge INSERT 이후 rollback 증명을 결정적으로 만듦.
10. PM 리뷰 RED/GREEN: persisted 비-COFFEE template에 MEAL request body를 보낸 권한 없는 coffee duty가 기대 403 대신 400을 받는 인가 순서 회귀를 unit/HTTP 2건으로 재현했다. persisted target 인가를 unsupported validation보다 먼저 수행해 권한 없는 요청은 403, 권한 있는 manager 요청은 기존 400을 유지하고 template/options 불변을 검증했다.
11. PM retention 정정: 35일 CLOSED 조회 false-green을 8일 CLOSED로 바꿔 관리자 7일 제한 초과와 기존 30일 retention을 동시에 만족시켰다. 31일 settled MEAL graph cascade 삭제 테스트는 유지했다.

## 5. 테스트 결과

- focused Duty/Poll/Billing/Flyway/REST Docs: 188 tests / 0 failures / 0 errors / 2 skipped.
- full: 429 tests / 0 failures / 0 errors / 3 skipped.
- `./gradlew build`, `./gradlew asciidoctor`, `git diff --check`: 성공.
- REST Docs: 전체 147개 snippet group, MEAL 관련 23개, 렌더된 `index.html` 확인.
- Docker QA: 사용자 최신 결정으로 #188/#189/#190 통합 브랜치에서 수행하도록 deferred.

## 6. 고민한 부분

GROUP_TOTAL을 부동소수점 없이 quotient/remainder로 계산하고, client count를 신뢰하지 않고 최종 response tables를 다시 집계했다. 다른 duty도 정산 여부는 확인해야 하지만 계좌 정보는 보면 안 되므로 계산 snapshot과 account ID 노출을 분리했다.

## 7. 트러블슈팅

- 문제: GitHub Project 조회 실패.
- 원인: token에 `read:project` scope 없음.
- 해결: issue body는 최신 원문을 확인했지만 Project 카드는 임의 변경하지 않고 완료 보고에 제한을 명시.
- 재발 방지: Project 자동 갱신 세션에는 사전에 `read:project` scope를 준비.

## 8. 다음 작업

- [ ] PM finding 0 확인.
- [ ] 세 feature 승인 후 integration branch에서 PostgreSQL Flyway 및 Docker 연결 HTTP QA.

## 9. Velog 글감

- 정수 exact arithmetic으로 poll group 총액을 동일 금액 청구로 배분하는 방법.
- JPA transaction과 PostgreSQL unique/pessimistic lock을 함께 사용한 one-shot settlement.
