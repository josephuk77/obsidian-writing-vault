---
project: FaithLog
type: devlog
issue: "#190"
status: review
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - billing
  - devotion
  - rest-docs
---

# #190 벌금 취소 후 경건 재제출과 관리자 납부 완료

## 1. 작업 배경

관리자가 잘못 제출된 경건 벌금을 취소해도 주간 제출이 닫힌 채 남았고, 취소된 unique-source 청구 때문에 사용자가 다시 제출할 때 양수 벌금을 갱신할 수 없었다. 또한 기존 관리자 청구 상태 API는 `PAID` 전환을 금지했다.

## 2. 최종 설계 기준

- 기존 `PATCH /api/v1/admin/charges/{chargeItemId}/status` 확장
- 기존 권한 범위의 `UNPAID -> PAID` 허용, `paidAt`은 서버 현재 시각
- terminal 상태에서 `PAID` 전환은 기존 409 conflict
- `UNPAID PENALTY + DEVOTION_RECORD -> CANCELED`이면 같은 transaction에서 source weekly `submittedAt`만 null
- daily checks 보존, `WAIVED/COFFEE/POLL_RESPONSE` 미영향
- 재제출은 현재 활성 벌금 규칙 적용
- 양수는 기존 CANCELED charge row를 같은 ID로 `UNPAID` 재사용하고 계좌 snapshot까지 갱신
- 0원은 기존 CANCELED row 유지, 새 row 생성 금지
- Billing Entity와 Devotion Entity는 직접 참조하지 않고 application port/adapter 사용
- DB/Flyway/dependency 변경 없음

## 3. 구현 내용

- Entity: `ChargeItem.reactivateCanceledCharge`와 `WeeklyDevotionRecord.reopenForResubmission`으로 상태 불변식을 각 aggregate에 유지
- Command: 관리자 PAID는 기존 policy에서 `markPaid`를 사용하고 terminal conflict는 기존 ErrorCode 재사용
- Orchestration: Billing 소유 transaction에서 `DevotionChargeReopenPort` 호출, Devotion adapter가 source/campus/user 검증
- Reuse: `ChargeCreationService`가 unique source의 CANCELED row를 새 row 없이 재활성화
- Controller/DTO: 기존 mapping과 request/response DTO 유지, Entity 직접 반환과 Swagger annotation 추가 없음
- REST Docs: 관리자 PAID와 PENALTY cancel/reopen 계약을 기존 Billing 문서에 추가

## 4. TDD 기록

1. production 수정 전 7개 통합 시나리오와 domain/controller/REST Docs 회귀를 작성했다.
2. 최초 실행은 `7 tests / 6 failures / 0 errors / 0 skipped`였고 영향 제외 경로 1건만 통과했다.
3. 관리자 PAID, cancel/reopen port, 동일 row 재사용을 작업 단위별 최소 구현했다.
4. focused `148 tests / 0 failures`, 전체 `425 tests / 0 failures / 0 errors / 3 skipped`를 확인했다.
5. 실패 테스트·관리자 PAID·경건 재오픈·재제출 row reuse·문서를 5개 커밋으로 분리했다.
6. PM 리뷰에서 관리자 취소와 사용자 납부가 동시에 모두 성공하는 lost update를 latch 통합 테스트로 RED 재현하고, 양쪽 상태 쓰기가 동일 row의 `PESSIMISTIC_WRITE` 잠금을 사용해 후행 요청이 커밋 상태를 다시 읽고 기존 상태별 전이를 수행하도록 GREEN 전환했다. ADMIN·ELDER·CAMPUS_LEADER PAID, 만료 토큰 401, 다른 캠퍼스 관리자 403, terminal-to-PAID 409 REST Docs도 보강했다.
7. PM 재검토에서 양수 재제출의 source-key 조회가 row를 잠그지 않아 동시 납부 PAID를 stale UNPAID로 덮을 수 있는 경로를 repository 진입 latch 테스트로 RED 재현했다. PENALTY/COFFEE 기존 source charge 조회를 `PESSIMISTIC_WRITE`로 바꾸고 두 동시성 테스트 모두 실제 잠금 조회 호출 전·완료 후 latch를 분리해 선행 transaction 해제 전에는 조회가 완료되지 않음을 검증하도록 보강했다.

## 5. 테스트 결과

- Billing·Devotion·관리자 Controller·REST Docs: `148 tests / 0 failures / 0 errors / 0 skipped`
- 전체 `./gradlew test`: `425 tests / 0 failures / 0 errors / 3 skipped`
- `./gradlew build`: 성공
- REST Docs snippet groups: 126개
- `./gradlew asciidoctor`: 성공
- `git diff --check`: 성공

## 6. 트랜잭션과 회귀 방지

charge cancellation과 weekly reopen은 Billing command transaction 하나로 묶었다. source record가 없거나 campus/user가 다르면 기존 Devotion not-found 오류를 내고 charge cancellation도 rollback한다. 재제출 중 계좌 조회나 charge update가 실패해도 weekly/daily/charge 전체가 rollback된다. 사용자·관리자 상태 변경과 PENALTY/COFFEE 기존 source charge 갱신·재활성화는 동일 charge row write lock으로 직렬화해 뒤 요청이 커밋된 상태를 다시 읽고 기존 상태별 전이를 수행한다. 사용자 본인 납부 완료, 401/403 구분, COFFEE/POLL_RESPONSE terminal 정책은 유지했다.

## 7. Docker QA 이관

최신 사용자 결정으로 feature 세션에서는 Docker build/up/API QA를 더 실행하지 않는다. #188/#189/#190 승인 후 `integration/188-190-devotion-meal-billing`에서 세 기능 연결 QA를 한 번 수행한다. 결정 전 격리 compose build/up 뒤 Docker Desktop daemon이 중단되어 실제 HTTP QA는 수행하지 못했다. destructive cleanup, `down -v`, named volume 삭제, system/image/volume prune은 실행하지 않았다.

## 8. 다음 작업

- [ ] PM `origin/develop...HEAD` 코드리뷰 finding 0 확인
- [ ] #188/#189/#190 승인 후 integration branch 병합 대기
- [ ] integration branch에서 제출→PENALTY→cancel/reopen→재제출 양수/0원→관리자 PAID와 401/403/409 실제 HTTP QA
- [ ] 안전하게 가능할 때 기존 #190 격리 compose project만 volume 보존 down

## 9. 이력서 문장 후보

벌금 취소와 경건 재제출을 application port 기반 단일 transaction으로 연결하고 상태 전이와 source charge 재활성화를 row lock으로 직렬화해 daily 기록 보존·rollback·terminal conflict를 보장했으며, 148개 focused·425개 전체 테스트와 REST Docs로 검증했다.
