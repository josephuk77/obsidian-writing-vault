---
project: FaithLog
type: devlog
issue: "#35"
status: done
created: 2026-06-18
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #35 청구 납부 완료, 면제, 취소 상태 관리

## 1. 작업 배경

사용자가 계좌이체 후 앱에서 `납부했어요`를 누르면 관리자 승인 없이 즉시 `PAID` 처리하고, 관리자는 청구를 `WAIVED`/`CANCELED` 처리하거나 잘못 종료된 청구를 `UNPAID`로 되돌릴 수 있어야 했다.

## 2. 최종 설계 기준

- 사용자 납부 완료 API만 `UNPAID -> PAID` 가능.
- 관리자는 `PAID`로 변경할 수 없음.
- 관리자는 `UNPAID -> WAIVED`, `UNPAID -> CANCELED` 가능.
- 관리자는 `PAID/WAIVED/CANCELED -> UNPAID` 되돌리기 가능.
- `PAID -> UNPAID` 되돌리기 시 `paidAt`은 null로 비움.
- 관리자 상태 변경 사유는 #35에서 저장하지 않음.
- 사용자 납부 완료 API는 body 생략과 빈 JSON을 모두 허용하고, `paidAt`이 없으면 서버 시간을 사용함.
- `paidAt` 요청값은 `2026-06-12T12:30:00Z` 같은 Instant 형식 사용.

## 3. 구현 내용

- Entity: `ChargeItem.markPaid(Instant)`, `waive`, `cancel`, `reopenAsUnpaid`, `paidAt` getter.
- Command: `CompleteChargePaymentCommand`, `ChangeChargeStatusCommand`.
- Service: `BillingService.completeMyChargePayment`, `BillingService.changeChargeStatus`, 본인/ACTIVE 멤버/관리자 권한 검증.
- Repository: `ChargeItemRepositoryPort.findChargeItemById`.
- Controller: `PATCH /api/v1/campuses/{campusId}/charges/me/{chargeItemId}/paid`, `PATCH /api/v1/admin/charges/{chargeItemId}/status`.
- Test: service/controller/REST Docs 테스트 추가.

## 4. TDD 기록

1. 실패 테스트 작성: #35 상태 전이 서비스 테스트, HTTP controller 테스트, REST Docs 테스트 추가.
2. 실패 확인: `./gradlew test --tests 'com.faithlog.billing.*'`가 command/result/domain 메서드 부재로 `compileTestJava` 실패.
3. 최소 구현: 도메인 상태 전이, service 유스케이스, DTO/controller, `CONFLICT` 오류 코드 추가.
4. 테스트 통과: billing 집중 테스트와 전체 테스트 통과.
5. 리팩토링: repository port의 `findById` 충돌을 피하기 위해 `findChargeItemById`로 분리.

## 5. 테스트 결과

명령:

`./gradlew test --tests 'com.faithlog.billing.*'`

결과:

`BUILD SUCCESSFUL`

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 67 tests / 0 failures / 0 errors / 0 skipped

명령:

`./gradlew build`

결과:

`BUILD SUCCESSFUL`

명령:

`./gradlew asciidoctor`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

- `paidAt` optional 계약이 Issue 본문에 미확정으로 남아 있어 사용자 확인 후 body 생략/빈 JSON 허용 및 Instant 형식으로 고정했다.
- 관리자 `PAID` 변경은 enum 파싱 이후 service에서 명시적으로 `400 Bad Request`로 거부했다.
- terminal 상태 전이 오류는 Issue 계약에 맞춰 `409 Conflict`로 분리했다.

## 7. 트러블슈팅

- 문제: 샌드박스에서 `./gradlew asciidoctor`가 Gradle wrapper `.zip.lck` 파일 접근 권한 문제로 즉시 실패.
- 원인: `~/.gradle/wrapper`가 Codex workspace-write sandbox 밖에 있음.
- 해결: 동일 명령을 권한 상승으로 재실행해 성공.
- 재발 방지: Gradle wrapper lock 파일 접근 실패 시 같은 검증 명령을 권한 상승으로 재시도.

## 8. 다음 작업

- [ ] #33 경건생활 자동 청구 연결에서 terminal charge 재제출 정책 재확인.
- [ ] #39 커피 자동 청구 연결에서 상태 전이 정책과 충돌 없는지 확인.

## 9. Velog 글감

- “관리자 승인 없는 납부 완료와 관리자 상태 되돌리기를 도메인 전이로 분리하기”

## 10. PM 리뷰 테스트 보강

- 전역 `ADMIN`이 캠퍼스 멤버십 없이도 관리자 청구 상태를 변경할 수 있음을 서비스 테스트로 고정했다.
- 캠퍼스 관리자 역할 `ELDER`, `CAMPUS_LEADER`가 관리자 청구 상태를 변경할 수 있음을 서비스 테스트로 고정했다.
- 본인 청구라도 캠퍼스 멤버십이 `INACTIVE`이면 납부 완료 API가 `403 Forbidden`을 반환함을 컨트롤러 테스트로 고정했다.
- 재검증: `./gradlew test --tests 'com.faithlog.billing.*'`, `./gradlew test`, `./gradlew build` 모두 성공. 전체 테스트 결과는 70 tests / 0 failures / 0 errors / 0 skipped.
