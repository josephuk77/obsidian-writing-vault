---
project: FaithLog
type: devlog
issue: "#34"
status: done
created: 2026-06-18
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - billing
---

# #34 계좌와 청구 항목 관리 구현

## 1. 작업 배경

경건생활 벌금과 커피 주문 흐름에서 청구 항목이 항상 캠퍼스별 납부 계좌 snapshot을 갖도록 `PaymentAccount`와 `ChargeItem` 기반을 구현했다. 실제 경건생활 제출 연결은 #33, 커피 투표 응답 연결은 #39 범위로 유지했다.

## 2. 최종 설계 기준

- 캠퍼스별 활성 계좌는 `accountType`별 1개만 허용한다.
- 새 활성 계좌 등록 시 기존 활성 계좌는 자동 비활성화한다.
- 모든 ACTIVE 캠퍼스 멤버는 활성 납부 계좌를 조회할 수 있다.
- 일반 멤버 조회 응답은 `ownerUserId`, `isActive`, `createdAt`, `deactivatedAt` 같은 관리용 메타데이터를 노출하지 않는다.
- 새 활성 계좌 등록 시 기존 `UNPAID` 청구는 새 계좌로 재연결하고 snapshot을 갱신한다.
- `PAID`, `WAIVED`, `CANCELED` 청구 snapshot은 과거 기록으로 유지한다.
- 활성 `PENALTY` 계좌가 없으면 `관리자에게 문의하세요`로 실패하고 `charge_items` row를 만들지 않는다.

## 3. 구현 내용

- Entity: `PaymentAccount`, `ChargeItem`
- Enum: `PaymentCategory`, `ChargeSourceType`, `ChargeStatus`
- Service: `BillingService`
- Repository: `PaymentAccountRepository`, `ChargeItemRepository`
- Controller: `BillingController`, `AdminBillingController`
- DTO: 계좌 생성 요청, 관리자 계좌 응답, 멤버 계좌 응답
- REST Docs: 계좌 생성, 조회, 비활성화 snippets 추가

## 4. TDD 기록

1. 실패 테스트 작성: `BillingServiceTest`, `BillingControllerTest`
2. 실패 확인: 구현 전 `./gradlew test --tests 'com.faithlog.billing.*'`가 billing 도메인/서비스/리포지토리 부재로 `compileTestJava` 실패
3. 최소 구현: billing domain/application/infrastructure/presentation 추가
4. 테스트 통과: billing 집중 테스트 성공
5. 리팩토링: terminal 상태 보존 테스트를 `PAID`, `WAIVED`, `CANCELED`로 확장하고 `markWaived`, `markCanceled` 추가

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`

수치:

- 56 tests / 0 failures / 0 errors / 0 skipped
- REST Docs snippet group 25개
- payment account snippets 3개 묶음 생성

명령:

`./gradlew build`

결과:

`BUILD SUCCESSFUL`

명령:

`./gradlew asciidoctor`

결과:

`BUILD SUCCESSFUL`

비고:

- 최초 샌드박스 실행은 Gradle wrapper lock 파일 권한 문제로 실패했고, 권한 상승 재실행으로 성공했다.
- `docker compose build app`은 Docker daemon 응답 `Docker Desktop is unable to start`로 앱 이미지 빌드 전에 중단됐다. Docker Desktop 실행 가능 상태에서 재검증이 필요하다.

## 6. 고민한 부분

- 일반 멤버 계좌 조회 응답에서 계좌번호는 전체 노출하되 관리용 정보는 제외하는 계약을 사용자 확인 후 `docs/decision-log.md`에 기록했다.
- `ChargeItem`은 후속 #33/#39에서 사용할 foundation만 제공하고, 수동 관리자 청구 생성 API는 만들지 않았다.

## 7. 트러블슈팅

- 문제: `PaymentAccountRepositoryPort`와 Spring Data repository 메서드가 테스트에서 타입 해석 충돌을 만들었다.
- 원인: concrete repository 변수에서 port의 `save/findById`와 Spring Data generic 메서드가 함께 후보가 됐다.
- 해결: 테스트에서는 `saveAndFlush`, `getReferenceById`처럼 Spring Data 전용 메서드를 사용했다.
- 재발 방지: port를 상속한 Spring Data repository를 테스트에서 직접 사용할 때는 generic CRUD 메서드와 이름이 겹치는 호출을 피한다.
- 문제: Docker 검증이 `Docker Desktop is unable to start`로 중단됐다.
- 원인: 로컬 Docker Desktop/daemon이 실행 가능한 상태가 아니었다.
- 해결: 이번 세션에서는 Gradle test/build/asciidoctor 검증까지만 완료하고 Docker 재검증 필요 사항으로 남겼다.
- 재발 방지: Docker 검증 전 `docker info` 또는 Docker Desktop 상태를 먼저 확인한다.

## 8. 다음 작업

- [ ] #33 경건생활 제출 흐름에서 `BillingService.createPenaltyCharge` 연결
- [ ] #39 커피 투표 응답 흐름에서 `COFFEE` 청구 생성/갱신 연결
- [ ] #35 `납부했어요` 즉시 PAID 처리 연결

## 9. Velog 글감

- 계좌 snapshot을 청구 항목에 저장하는 이유
- TDD로 결제/청구 기반 도메인 먼저 깔기
