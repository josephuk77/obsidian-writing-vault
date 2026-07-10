---
project: FaithLog
type: devlog
issue: "#149"
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - refactoring
  - billing
---

# #149 Billing 조회와 집계 책임 분리

## 1. 작업 배경

#148에서 Billing 명령 책임을 분리한 뒤에도 673줄 `BillingQueryService`가 본인 청구 조회, 관리자 집계, 계좌 조회와 검증을 함께 소유했다. API·DB·권한·집계 결과를 바꾸지 않고 조회 유스케이스별 책임을 분리했다.

## 2. 최종 설계 기준

- `MyChargeQueryService`: `listMyCharges`, `getMyChargeSummary`.
- `AdminChargeQueryService`: `listAdminCampusCharges`, `listAdminCampusChargesForMyAccounts`, `listAdminMemberCharges`.
- `PaymentAccountQueryService`: `listPaymentAccounts`, `listAdminPaymentAccounts` 두 overload, `requireActivePenaltyAccount`.
- 이동된 9개 public 조회 surface는 각각 기존 `@Transactional(readOnly = true)` 경계를 직접 소유한다.
- Controller와 Devotion adapter는 전용 Query Service를 직접 사용한다.
- `BillingQueryService`는 repository, transaction, 예외, 업무 규칙을 소유하지 않는 호환 façade다.
- #148 `BillingService`도 repository/transaction/business-rule-free 상태를 유지한다.

## 3. 구현 내용

- Service:
  - 본인 목록의 status/category/page/size/sort와 월별 paidAt/createdAt 요약 기준을 `MyChargeQueryService`로 이동했다.
  - 관리자 summary/members/detail 조립, `paymentAccountId`, my-accounts PENALTY/COFFEE owner 정책과 정렬을 `AdminChargeQueryService`로 이동했다.
  - 회원/관리자 계좌 목록, active/inactive/soft-delete 필터와 활성 PENALTY 계좌 검증을 `PaymentAccountQueryService`로 이동했다.
  - 새 공통 helper Service나 서비스 간 의존을 만들지 않고 각 유스케이스 Service가 기존 private helper와 repository 호출 순서를 소유한다.
- Controller:
  - `BillingController`는 `MyChargeQueryService`와 `PaymentAccountQueryService`를 직접 사용한다.
  - `AdminBillingController`는 `AdminChargeQueryService`와 `PaymentAccountQueryService`를 직접 사용한다.
- Adapter:
  - `BillingDevotionPenaltyChargeAdapter`는 `PaymentAccountQueryService`로 활성 PENALTY 계좌를 검증한다.
- Facade:
  - `BillingQueryService`는 세 전용 Query Service delegate만 남겼다.
  - `BillingService`의 legacy 계좌 조회도 `PaymentAccountQueryService`에 직접 delegate한다.
- Test:
  - 책임, 직접 read-only transaction, production wiring, façade 무규칙성, 순환 의존 금지를 고정하는 구조 테스트 5건을 추가했다.
  - 본인 목록의 category/status/page/size/sort 조합 characterization을 추가했다.

## 4. TDD 기록

1. 동작 characterization: 본인 목록 필터와 paging/sort 조합 테스트를 기존 구현에서 GREEN으로 확인했다.
2. 실패 테스트 작성: 세 전용 서비스와 직접 transaction, production caller, 얇은 façade, 무순환 의존을 요구하는 구조 테스트를 추가했다.
3. 실패 확인: `BillingQueryUseCaseServiceStructureTest` 5 tests / 5 failures RED.
4. 최소 구현: 기존 public 메서드, private helper, 검증 순서, repository 호출과 ErrorCode/message를 세 서비스로 이동했다.
5. 테스트 통과: 구조/Billing/Controller/REST Docs 및 분리 실행한 Devotion/Poll/Batch 연결 테스트와 전체 332 tests가 성공했다.

## 5. 테스트 결과

- Billing focused와 Controller/REST Docs focused: 성공.
- Devotion/Poll/Batch 연결 테스트 분리 실행: 성공.
- `./gradlew test`: 332 tests / 0 failures / 0 errors / 1 skipped, BUILD SUCCESSFUL.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- `git diff --check`: 성공.
- 정적 검사: API mapping/query parameter/DTO/ErrorCode/DB/Flyway 변경 0건, Swagger 문서 annotation 0건, Controller Entity 직접 반환 0건, 서비스 순환 의존 0건.
- 격리 Docker: `faithlog-qa-149-billing-query`에서 PostgreSQL/Redis healthy, `/api/v1/health`의 `data.status=UP`, 동일 project compose down 성공.
- Docker cache: 마지막 Docker 명령 `docker builder prune -f`로 미사용 build cache 695.8MB를 정리했다. system/volume/image prune과 named volume 삭제는 실행하지 않았다.

## 6. 고민한 부분

공통 access/result helper를 새 Service로 만들면 중복은 줄지만 조회 서비스끼리 새로운 간접 책임과 결합이 생길 수 있다. 이번 이슈는 동작 무변경이 최우선이므로 각 유스케이스의 기존 private helper를 소유 서비스 안에 두고, status 합계처럼 작은 계산 중복은 유지했다. 이 방식으로 메서드와 repository 호출 순서를 추적하기 쉽게 보존했다.

## 7. 트러블슈팅

- 문제: Devotion/Poll/Batch 88-test 묶음에서 `DevotionServiceTest` 10건이 row count 누적으로 실패했다.
- 원인: 깨끗한 `origin/develop=f2b6660`에서도 같은 10건과 같은 실제값이 재현되는 기존 Spring context 순서 오염이었다.
- 해결: #149 브랜치와 clean baseline을 별도 worktree에서 대조했고, `DevotionServiceTest` 단독 성공을 확인했다. #149가 추가한 오염이 아니므로 production/test 코드를 수정하거나 성과로 집계하지 않았다.
- 재발 방지: 대규모 focused 묶음 실패 시 동일 명령을 clean base와 단독 class에서 대조하고 이슈 신규 오염만 최소 격리한다.
- 도구 제약: `pm-dev` dev/review gate는 저장소 공통 harness 파일과 specialist/TDD evidence 부재로 실패했다. score 보고서의 critical/security finding은 0건이었고 `.harness` 보고서는 untracked로 보존했다. GitHub Project는 token의 `read:project` scope 부재로 카드 조회·이동을 수행하지 못했다.

## 8. 다음 작업

- [ ] PM 세션에서 #149 코드리뷰를 진행한다.
- [ ] 리뷰 승인 후 develop 대상 PR을 생성한다.
- [ ] GitHub token scope 복구 후 #149 Project 카드 상태를 갱신한다.

## 9. Velog 글감

- Spring 조회 Service를 본인 조회, 관리자 집계, 계좌 검증으로 분리하면서 transaction과 집계/권한 계약을 보존한 방법.
