---
project: FaithLog
type: devlog
issue: #125
status: done
created: 2026-07-02
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #125 계좌 활성 전환과 정산 API 계약 보강

## 1. 작업 배경

Cloud Run QA에서 active `PENALTY` 계좌가 이미 있는 캠퍼스에 새 `PENALTY` 계좌를 등록할 때 PostgreSQL partial unique index `uk_payment_accounts_active_penalty_type` 충돌이 발생했다. 문서상 기대 동작은 기존 active 계좌를 먼저 inactive로 바꾸고 새 계좌를 active로 저장하는 것이다.

## 2. 최종 설계 기준

- `PENALTY`: 캠퍼스별 active 최대 1개. 교체 등록과 activate 모두 기존 active를 inactive 처리한 뒤 새 active 상태가 DB unique index와 충돌하지 않아야 한다.
- `COFFEE`: active 기준은 `campusId + accountType + ownerUserId`. 같은 owner의 기존 active만 inactive 처리한다.
- 스키마 변경 없이 repository flush 순서를 명시해 해결한다.

## 3. 구현 내용

- Service: `BillingService.createPaymentAccount`에서 기존 active 비활성화 후 `PaymentAccountRepositoryPort.flush()`를 호출한 다음 새 계좌를 저장한다.
- Service: `activatePenaltyPaymentAccount`에서 기존 active `PENALTY`를 inactive 처리하고 flush한 뒤 선택 계좌를 active로 전환한다.
- Repository: `PaymentAccountRepositoryPort`에 `flush()` 계약을 추가했다. JPA 구현체는 `JpaRepository.flush()`를 그대로 사용한다.
- Test: `BillingServiceUnitTest`를 추가해 `deactivate -> flush -> save`와 activate 시 `deactivate -> flush -> activate` 순서를 고정했다.

## 4. TDD 기록

1. 실패 테스트 작성: `BillingServiceUnitTest#createPenaltyPaymentAccount_flushes_deactivation_before_saving_replacement`
2. 실패 확인: 최초 실행은 `PaymentAccountRepositoryPort.flush()` 부재로 `compileTestJava` 실패
3. 최소 구현: repository port에 `flush()` 추가, create/activate 경로에서 기존 active 비활성화 직후 flush
4. 테스트 통과: 단위 테스트, focused billing 테스트, 전체 테스트 통과
5. 리팩토링: helper가 비활성화 여부를 boolean으로 반환하도록 정리해 불필요한 flush를 피함

## 5. 테스트 결과

- `./gradlew test --tests com.faithlog.billing.application.BillingServiceUnitTest`: `BUILD SUCCESSFUL`
- focused billing service/query/controller/REST Docs 테스트: `BUILD SUCCESSFUL`
- `./gradlew test`: `BUILD SUCCESSFUL`, 293 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build`: `BUILD SUCCESSFUL`
- `./gradlew asciidoctor`: `BUILD SUCCESSFUL`
- Docker isolated health QA: `/api/v1/health` 200, `status=UP`
- Docker API QA A-F: PENALTY 등록/activate/delete, COFFEE owner 분리, `charges/my-accounts`, 401/403/409 분리 확인

## 6. 고민한 부분

H2 통합 테스트는 PostgreSQL partial unique index의 flush 순서를 안정적으로 재현하기 어렵다. 그래서 DB별 동작을 억지로 흉내내기보다 서비스 단위 테스트에서 repository 호출 순서를 계약으로 고정했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor`가 sandbox에서 `~/.gradle` wrapper lock 접근 제한으로 실패
- 해결: 승인 경로로 재실행해 성공
- 문제: Docker API QA 보조 DB 상태 출력 SQL의 콜론 quoting 오류
- 해결: API list 응답의 `isActive`, `deactivatedAt`, soft-deleted 제외 결과로 상태를 확인하고, 최종 보고에는 API 응답 기준으로 기록
