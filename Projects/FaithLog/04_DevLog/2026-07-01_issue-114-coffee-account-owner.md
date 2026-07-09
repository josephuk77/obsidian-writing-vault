---
project: FaithLog
type: devlog
issue: "#114"
status: done
created: 2026-07-01
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #114 사용자별 커피 계좌와 커피투표 정산 권한 정리

## 1. 작업 배경

#112 이후 COFFEE 계좌가 캠퍼스 단위 active 계좌처럼 동작해 다른 사용자의 커피 계좌를 비활성화하거나 기존 COFFEE 청구가 새 계좌로 재연결될 수 있는 위험을 정리했다.

## 2. 최종 설계 기준

- PENALTY 계좌는 캠퍼스 단위 active 1개를 유지한다.
- COFFEE 계좌는 `campusId + accountType + ownerUserId` 기준으로 active를 유지한다.
- COFFEE 계좌 생성은 requester 본인 소유만 허용한다.
- 캠퍼스 관리자와 active COFFEE 담당자는 COFFEE poll/template을 만들 수 있지만, requester 본인 소유 active COFFEE 계좌가 필수다.
- COFFEE charge는 poll 생성 시 선택한 `paymentAccountId`에 연결하고, 새 COFFEE 계좌 등록으로 기존 미납 COFFEE charge를 재연결하지 않는다.

## 3. 구현 내용

- Entity: 기존 `PaymentAccount.ownerUserId`, `Poll.paymentAccountId`, `ChargeItem.paymentAccountId` 기준 유지
- Command: `CreatePaymentAccountCommand.ownerUserId`는 COFFEE에서 requester 본인 또는 null만 허용
- Service: `BillingService`, `BillingQueryService`, `PollService`, `PollTemplateService`, `PollAccessService` 정책 갱신
- Repository: active COFFEE owner 조회 메서드 추가
- Controller: 기존 API 유지, REST Docs 계약 설명 갱신
- Test: Billing/Poll service, controller, REST Docs 테스트 보강
- DB: `V3__split_active_coffee_payment_account_owner_scope.sql` 추가

## 4. TDD 기록

1. 실패 테스트 작성: 사용자별 COFFEE active 분리, 본인 소유 계좌 제한, 관리자/담당자 COFFEE poll/template 본인 계좌 필수 테스트 추가
2. 실패 확인: focused Billing/Poll service 테스트 4 failures 확인
3. 최소 구현: COFFEE owner scope, poll/template account validation, charge query owner filter 구현
4. 테스트 통과: focused service/controller/REST Docs 테스트 성공
5. 리팩토링: 기존 #112 테스트 기대값과 문서 문구를 #114 정책으로 갱신

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` (280 tests / 0 failures / 0 errors / 1 skipped)

추가 검증:

- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- Docker QA: Docker daemon socket 부재로 수행 불가

## 6. 고민한 부분

- COFFEE `ownerUserId`가 requester와 다른 요청은 추측하지 않고 본인 계좌 원칙에 맞춰 `403 BILLING_PAYMENT_ACCOUNT_OWNER_FORBIDDEN`으로 고정했다.
- 캠퍼스 관리자도 COFFEE 정산 필터에서는 본인 COFFEE 계좌만 조회하도록 제한했고, 전역 ADMIN은 전체 접근 가능하게 했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor` 첫 실행이 `~/.gradle` wrapper lock 파일 접근 제한으로 실패
- 원인: workspace sandbox 밖 Gradle wrapper lock 파일 접근 제한
- 해결: 승인 경로에서 동일 명령 재실행 후 성공
- 재발 방지: sandbox 파일 권한 실패는 코드 실패와 분리해 기록한다.

- 문제: Docker QA 실행 불가
- 원인: `unix:///Users/josephuk77/.docker/run/docker.sock` Docker daemon socket 없음
- 해결: Docker 검증은 수행하지 못했고, Spring Boot 통합 테스트와 REST Docs 계약 테스트로 정책 검증
- 재발 방지: Docker Desktop/daemon 실행 상태 확인 후 재검증 필요
