---
project: FaithLog
type: devlog
issue: "#33"
status: done
created: 2026-06-19
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #33 경건생활 제출 시 벌금 청구 자동 생성 구현

## 1. 작업 배경

주간 경건생활을 첫 최종 제출할 때 서버가 벌금을 계산하고 `PENALTY` 청구 1건을 자동 생성하도록 연결했다. 관리자가 별도로 벌금 청구를 만드는 API는 MVP 범위에서 제외했다.

## 2. 최종 설계 기준

- 주간 최종 제출은 1회만 가능하다.
- 첫 `submit=true`에서만 `submitted_at` 갱신과 `PENALTY` 청구 생성을 수행한다.
- `submit=false`는 최종 제출 전까지만 가능하고 청구를 만들거나 갱신하지 않는다.
- 활성 PENALTY 계좌가 없으면 `관리자에게 문의하세요`로 전체 요청을 실패시킨다.
- 청구 기준은 `paymentCategory=PENALTY`, `sourceType=DEVOTION_RECORD`, `sourceId=weekly_devotion_records.id`, `status=UNPAID`이다.
- 중복 제출과 제출 후 저장은 `DEVOTION_WEEKLY_ALREADY_SUBMITTED`, HTTP 409, `이미 제출된 주간 경건생활은 수정할 수 없습니다.`로 실패한다.

## 3. 구현 내용

- Entity: 기존 `WeeklyDevotionRecord`, `ChargeItem`, `PaymentAccount`, `PenaltyRule` 구조 사용.
- Command/Port: `DevotionPenaltyChargeCommand`, `DevotionPenaltyChargePort` 추가.
- Service: `DevotionService.updateWeeklyCheck`에서 제출 전 계좌 존재 확인, 제출 후 벌금 계산과 청구 생성 연결, 중복 제출 차단 구현.
- Adapter: `BillingDevotionPenaltyChargeAdapter`가 Devotion port를 기존 `BillingService.createPenaltyCharge`에 연결.
- Controller: 응답 DTO는 기존 주간 경건생활 응답 구조를 유지하고, 청구 생성은 서버 side effect로 처리.
- Test: 서비스, 컨트롤러, REST Docs 테스트에 청구 생성, 계좌 없음, 중복 제출, 제출 후 저장 실패 검증 추가.

## 4. TDD 기록

1. 실패 테스트 작성: 첫 제출 청구 생성, `submit=false` 청구 미생성, 계좌 없음 전체 실패, 중복 제출/제출 후 저장 실패 테스트를 먼저 작성.
2. 실패 확인: `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest`가 12 tests / 2 failed로 실패했고, 중복 제출 테스트는 `DEVOTION_WEEKLY_ALREADY_SUBMITTED` 부재로 `compileTestJava` 실패.
3. 최소 구현: Devotion application port와 Billing adapter를 추가하고, `BillingService.requireActivePenaltyAccount`, `DevotionFineCalculator` Bean 등록, 제출 중복 guard를 구현.
4. 테스트 통과: 서비스 테스트와 컨트롤러/REST Docs 테스트 묶음 통과.
5. 리팩토링: 전체 테스트에서 발견된 절대 count 의존을 delta 검증으로 안정화.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 121 tests / 0 failures / 0 errors / 0 skipped

추가 확인:

- `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest`
- `./gradlew test --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`

## 6. 고민한 부분

Devotion 도메인이 Billing Entity를 직접 의존하지 않도록 application port를 두었다. Billing foundation의 `createPenaltyCharge`가 create-or-update인 정책은 그대로 두고, #33의 one-time submission 정책은 Devotion boundary에서 막았다.

## 7. 트러블슈팅

- 문제: 전체 테스트에서 `ChargeItem` row count가 다른 테스트 데이터 누적으로 예상보다 컸다.
- 원인: 컨트롤러 테스트가 전체 DB 상태에 대한 절대 count를 기대했다.
- 해결: 하루 체크 전 count를 저장하고, 하루 체크는 delta 0, 주간 제출은 delta +1로 검증하게 변경했다.
- 재발 방지: 통합 테스트에서는 전역 count 절대값보다 행위 전후 delta를 우선 사용한다.

## 8. 다음 작업

- [x] PM 검증에서 주간 제출 성공 응답에 청구 요약 필드가 필요한지 최종 결정한다. 기존 `WeeklyDevotionResponse` 구조를 유지하고 `generatedCharges`는 추가하지 않는다.
- [x] Docker compose QA와 최종 `docker compose down` 확인을 완료한다.

## 9. Velog 글감

- 도메인 간 직접 Entity 의존 없이 자동 청구 흐름 연결하기
- TDD로 side effect와 트랜잭션 실패 원자성 검증하기

## 10. PM 리뷰 보강 - 제출 완료 주차 일별 체크 차단

- 배경: 주간 제출 후 `PUT /api/v1/campuses/{campusId}/devotions/me/days/{recordDate}`가 같은 주차 daily row를 수정하면 제출 완료 요약과 생성된 벌금 청구가 불일치할 수 있다.
- 결정: 해당 주차 `weekly_devotion_records.submitted_at`이 있으면 일별 체크 API도 `DEVOTION_WEEKLY_ALREADY_SUBMITTED`, HTTP 409, `이미 제출된 주간 경건생활은 수정할 수 없습니다.`로 실패한다.
- TDD 실패 확인: 구현 전 대상 테스트 묶음이 32 tests / 3 failed로 실패했다. 서비스, 컨트롤러, REST Docs가 제출 완료 주차 일별 체크 차단을 아직 만족하지 못했다.
- 구현: `DevotionService.updateDailyCheck`에서 weekly row를 먼저 조회하고 `submittedAt`을 검사한 뒤, 미제출 주차일 때만 weekly/daily row를 생성 또는 수정하도록 변경했다.
- 검증: 대상 테스트 묶음 성공, `./gradlew cleanTest test --no-parallel --max-workers=1` 성공(124 tests / 0 failures / 0 errors / 0 skipped), `./gradlew test` 성공, `./gradlew build` 성공, `./gradlew asciidoctor` 성공.
- REST Docs: `devotion-daily-check-already-submitted-week` snippet 추가, 전체 snippet group 49개.
