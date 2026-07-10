---
project: FaithLog
type: devlog
issue: "#148"
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

# #148 Billing 계좌와 청구 명령 책임 분리

## 1. 작업 배경

#145의 DDD 내부 MVC 구조와 #147의 유스케이스 Service 분리 원칙을 Billing에 적용했다. 하나의 BillingService가 계좌 명령, PENALTY/COFFEE 청구 생성, 청구 상태 변경, 일부 조회까지 소유하던 구조를 기능 동작 변경 없이 분리했다.

## 2. 최종 설계 기준

- PaymentAccountCommandService: 계좌 생성, 비활성화, PENALTY 활성화, soft delete.
- ChargeCreationService: PENALTY 청구 생성/갱신, COFFEE 청구 생성/갱신.
- ChargeStatusCommandService: 본인 납부 완료, 관리자 상태 변경.
- 이동된 8개 public 명령은 각각 기존 write Transactional 경계를 직접 소유.
- BillingService는 repository, transaction, business rule을 소유하지 않는 호환 facade.
- 사용자는 #149 조회 재설계 없이 기존 계좌 조회 3개 surface만 BillingQueryService로 1:1 기계 이동하는 최소 호환 연결을 최종 승인했다.

## 3. 구현 내용

- Service:
  - PaymentAccountCommandService가 campus pessimistic lock, owner 권한, active 교체, flush, 미납 PENALTY 청구 재연결을 소유한다.
  - ChargeCreationService가 계좌 snapshot과 PENALTY/COFFEE source별 upsert 및 terminal 정책을 소유한다.
  - ChargeStatusCommandService가 본인 납부와 관리자 상태 전이 권한을 소유한다.
  - BillingQueryService는 listPaymentAccounts, listAdminPaymentAccounts, requireActivePenaltyAccount의 기존 구현과 read-only transaction을 그대로 받았다.
- Controller:
  - AdminBillingController는 계좌 명령과 관리자 상태 변경을 전용 Service에 직접 보낸다.
  - BillingController는 본인 납부 완료를 ChargeStatusCommandService에 직접 보낸다.
- Adapter:
  - BillingDevotionPenaltyChargeAdapter와 BillingCoffeePollChargeAdapter는 ChargeCreationService를 직접 사용한다.
  - Devotion의 활성 PENALTY 계좌 확인은 BillingQueryService에 연결했다.
- Facade:
  - BillingService는 3개 명령 Service와 BillingQueryService delegate만 남겼다.
- Test:
  - 구조 테스트 4건과 rollback/COFFEE upsert characterization 테스트 2건을 추가했다.

## 4. TDD 기록

1. 실패 테스트 작성: 전용 Service와 직접 Transactional, production caller wiring, repository-free facade를 요구하는 구조 테스트를 먼저 추가했다.
2. 실패 확인: BillingCommandUseCaseServiceStructureTest 3 tests / 3 failed.
3. 동작 고정: 신규 계좌 insert 실패 시 기존 active PENALTY 계좌 deactivate + flush rollback과 COFFEE UNPAID 갱신/terminal 보존 테스트는 기존 코드에서 GREEN이었다.
4. 최소 구현: 기존 메서드 본문, 검증 순서, ErrorCode, repository 호출 순서를 3개 명령 Service로 이동했다.
5. PM 리뷰 RED: 신규 `NOT_SUPPORTED` rollback 테스트가 커밋 fixture context를 정리하는지 검사하는 구조 테스트를 먼저 추가해 1 test / 1 failure를 확인했다.
6. 격리 보강: 해당 테스트에만 `DirtiesContext(AFTER_METHOD)`를 적용해 #148 신규 오염을 제거했다. develop에도 동일하게 존재하는 기존 Devotion/Poll 순서 의존 실패 10건은 이번 범위에서 수정하거나 성과로 집계하지 않았다.
7. 테스트 통과: 구조 테스트, Billing focused, 분리 실행한 Devotion/Poll settlement/Batch 연결 테스트와 전체 326 tests가 성공했다.

## 5. 테스트 결과

- Billing 전체 + Devotion/Poll settlement/Batch focused 테스트: 성공.
- ./gradlew test: 326 tests / 0 failures / 0 errors / 1 skipped, BUILD SUCCESSFUL.
- ./gradlew build: 성공.
- ./gradlew asciidoctor: PM 세션의 post-fix 독립 재실행까지 성공.
- git diff --check: 성공.
- 정적 검사: Swagger 문서 annotation과 Controller Entity 직접 반환 모두 0건.
- 격리 Docker: PostgreSQL/Redis healthy, /api/v1/health data.status=UP, compose down 성공.
- Docker cache 정리: 정리 전후 active container 0개를 확인했다. buildx builder는 명시적으로 사용하지 않았고 docker builder prune -f로 미사용 cache 2.084GB를 회수했다. Build Cache는 28개/2.477GB/회수 가능 2.084GB에서 9개/393.3MB/회수 가능 0B가 됐다. 기존 중지 컨테이너 3개와 named volume 15개는 보존했고 system/volume/image prune은 실행하지 않았다.
- PM baseline 대조: Billing/Devotion/Poll/Batch 광범위 묶음은 #148에서 180 tests / 10 failures, 깨끗한 origin/develop에서 175 tests / 동일 10 failures였다. 동일한 기존 context 오염이므로 #148 production 회귀가 아님을 확인했다.
- PM production 리뷰: API mapping/DTO/ErrorCode/Entity/Flyway, 권한, campus lock, flush, rollback, snapshot, terminal 정책에서 finding 없음.

## 6. 고민한 부분

BillingService를 완전한 얇은 facade로 만들려면 기존 조회 메서드도 delegate해야 하지만 #149 범위를 선행하면 안 됐다. 새 조회 구조나 최적화를 추가하지 않고 이미 존재하는 BillingQueryService에 기존 구현, 검증 순서, repository 호출, ErrorCode, message, read-only transaction을 1:1 이동하는 최소 호환 연결로 제한했고, 사용자가 PM 최종 결정에서 이 권장안을 승인했다.

## 7. 트러블슈팅

- 문제: asciidoctor 첫 실행과 Docker QA 첫 실행이 sandbox의 Gradle cache lock 및 Docker socket 접근 제한으로 실패했다.
- 원인: workspace 외부 Gradle cache와 Docker daemon socket에 대한 관리형 sandbox 권한 제한.
- 해결: 동일 명령을 승인된 권한 경로로 재실행해 asciidoctor와 격리 Docker health를 모두 성공시켰다.
- 재발 방지: 기존 Gradle sandbox lock 및 PM harness 누락 troubleshooting 문서를 재사용하고, 코드 실패와 환경 권한 실패를 분리해 보고한다.
- PM gate: score_code.py는 review-score JSON/Markdown을 생성했지만 저장소에 harness.yaml specialist 설정이 없어 overall 누락과 passed=false를 기록했다. review_gate.py는 harness policy와 TDD evidence 파일 부재로 실패했다. critical/security finding은 0건이며 생성된 .harness 보고서는 untracked로 보존했다.
- 테스트 격리: 신규 rollback characterization은 test transaction을 끄고 fixture를 커밋하므로 해당 메서드 종료 후 Spring context를 폐기하도록 고정했다. 기존 광범위 실패 10건은 develop baseline에도 동일해 별도 후속 범위로 분리했다.

## 8. 다음 작업

- [x] PM 세션에서 커밋, API/DB/권한/트랜잭션 무변경 증거를 코드리뷰하고 최소 호환 조회 이동 승인.
- [ ] GitHub Project scope 복구 후 #148 카드를 Code Review 상태로 이동.
- [ ] 사용자 지시 후 develop 대상 PR 생성.
- [ ] #149 Billing 조회 책임 분리는 별도 이슈에서 수행.

## 9. Velog 글감

- Spring Billing Application Service를 계좌, 청구 생성, 상태 변경 유스케이스로 분리하면서 기존 transaction propagation과 DB unique 순서를 보존한 방법.
