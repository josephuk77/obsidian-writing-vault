# 2026-07-01 Issue #112 계좌 기준 정산 조회와 커피 투표 권한 정책 정리

## 작업 기준

- GitHub Issue #112 `[Fix] 계좌 기준 정산 조회와 커피 투표 권한 정책 정리`
- Branch: `fix/112-billing-account-scope-coffee-poll-policy`
- DB schema 변경 없음

## TDD 기록

구현 전 billing/campus/poll focused 테스트를 먼저 추가했다.

```bash
./gradlew test --tests com.faithlog.billing.application.BillingQueryServiceTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.campus.application.CampusServiceTest --tests com.faithlog.poll.application.PollServiceTest
```

첫 실행은 `AdminCampusChargeListQuery.paymentAccountId`, `BillingService.listAdminPaymentAccounts`, `PaymentAccountResult.createdAt/deactivatedAt` 부재로 `compileTestJava` 실패했다.

## 구현 요약

- `GET /api/v1/admin/campuses/{campusId}/charges`에 optional `paymentAccountId` 필터 추가
- `paymentAccountId`와 `paymentCategory`, `status`, `userId`, `keyword`, pagination 필터 조합 지원
- `GET /api/v1/admin/campuses/{campusId}/charges/my-accounts` 추가
- `GET /api/v1/admin/campuses/{campusId}/payment-accounts` 추가 및 `ownerUserId`, `isActive`, `createdAt`, `deactivatedAt` 메타데이터 반환
- PENALTY 계좌/청구 조회는 캠퍼스 관리자 또는 전역 ADMIN으로 제한
- active COFFEE duty USER는 본인 활성 COFFEE 계좌/청구 범위로 제한
- COFFEE poll 및 COFFEE poll template 생성/수정은 현재 active COFFEE duty만 허용
- 선택 `paymentAccountId`는 요청자가 사용할 수 있는 활성 same-campus COFFEE 계좌로 검증
- 신규 캠퍼스 생성 시 default COFFEE poll template/반복 poll 자동 생성 side effect 제거

## 검증

```bash
./gradlew test
./gradlew build
./gradlew asciidoctor

git diff --check
rg -n 'DEVOTION_FINE|sourceType=COFFEE|BillingType|MANUAL|PAYMENT_REQUESTED|payment-request|requestPayment|poll_responses\.option_id' src docs README.md
rg -n '"optionId"|\boptionId\s*[:=]|\boptionId\s*\(' src docs README.md
```

- `./gradlew test`: 성공, 276 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공. 최초 병렬 실행 중 sandbox가 Gradle wrapper lock 파일 접근을 막아 실패했고, 승인 후 재실행 성공
- `git diff --check`: 성공
- 금지어 검색: 정책 문서의 금지 목록과 기존 내부 변수/도메인 메서드명만 검출. API 요청 계약 회귀 없음
- Spring REST Docs snippet group: 117개

## 남은 확인

Docker compose 실제 API QA는 아직 수행하지 않았다. Spring Boot 통합 테스트와 REST Docs 계약 테스트로 필수 정책은 검증했다.
