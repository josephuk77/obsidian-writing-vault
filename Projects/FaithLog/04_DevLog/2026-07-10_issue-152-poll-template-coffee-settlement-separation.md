---
project: FaithLog
type: devlog
issue: #152
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #152 Poll 템플릿과 커피 정산 책임 분리

## 1. 작업 배경

#151 이후에도 `PollTemplateService`는 template command/query, 권한·계좌 검증, option snapshot 저장과 결과 조립을 함께 소유했다. `PollAutomationService`는 schedule/lock/transaction 외에 template→Poll/PollOption 복사를, `CoffeePollSettlementService`는 eligibility·응답/선택지 조회·Billing port 호출을 함께 소유해 책임 경계를 분리했다.

## 2. 최종 설계 기준

- template command 3개와 query 2개가 전용 Service에서 기존 transaction을 직접 소유한다.
- template option snapshot resolve/save/replace/result 조립은 package-private support에 응집한다.
- 자동 생성 service는 due 탐색, Asia/Seoul window, Redis lock, transaction orchestration을 유지하고 복사 책임을 factory에 위임한다.
- coffee settlement command가 all-or-nothing transaction과 Billing port 호출을 소유하고 support가 eligibility와 response/option 조립을 담당한다.
- API/DB/권한/scheduler/멱등성/terminal/rollback 정책은 변경하지 않는다.

## 3. 구현 내용

- Command: `PollTemplateCommandService`, `CoffeePollSettlementCommandService`
- Query: `PollTemplateQueryService`
- Support: `PollTemplateOptionSupport`, `CoffeePollSettlementSupport`
- Batch: `ScheduledPollFactory`, `ScheduledPollWindow`
- Compatibility facade: `PollTemplateService`, `CoffeePollSettlementService`
- Controller: `AdminPollTemplateController`를 전용 command/query service에 직접 연결
- 유지: 이미 응집된 `CoffeeCatalogService`, scheduler API/설정, repository/port 계약

## 4. TDD 기록

1. 실패 테스트 작성: 직접 transaction, Controller 전용 service 연결, thin facade, option support, scheduled factory 위임, settlement command/support, 순환 의존 금지 구조 테스트 6건
2. 실패 확인: 6 tests / 6 failures
3. 최소 구현: 기존 검증·repository·Billing port 호출 순서를 보존한 책임 이동
4. 테스트 통과: 구조 테스트 6건과 기존 Poll/REST Docs/Batch/4-domain/전체 테스트 GREEN
5. 리팩토링: 자동 생성의 전체 Poll/PollOption snapshot 필드와 비활성 auto template 제외 characterization 보강

## 5. 테스트 결과

- Poll/template/catalog/settlement/REST Docs/Batch focused: 62 tests / 0 failures
- Billing/Devotion/Poll/Batch 4-domain: 204 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 350 tests / 0 failures / 0 errors / 1 skipped, 실행된 테스트 통과율 100%
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: 성공
- GitHub CI: PR/push 금지 지시로 미실행
- 격리 Docker QA: image build 성공, PostgreSQL/Redis healthy, backend `data.status=UP`, volume 삭제 없는 compose down 성공
- Docker build cache: `docker builder prune -f`로 696.2MB 정리

## 6. 정량 변화와 이력서 근거

- `PollTemplateService`: 218→42줄(-176, -80.7%)
- `PollAutomationService`: 207→121줄(-86, -41.5%)
- `CoffeePollSettlementService`: 130→17줄(-113, -86.9%)
- template public use case: 5개를 2개 전용 Service로 분리
- 신규 구조 테스트: 6개
- 전체 Java source/test: 548개, test source: 69개
- 위 줄 수는 facade/orchestrator 축소 수치이며 추출 class를 포함한 전체 코드 감소를 의미하지 않는다.

이력서 후보:

`Poll template의 5개 command/query와 자동 생성·커피 정산 책임을 전용 Service/Support/Factory로 분리해 기존 통합 Service를 최대 86.9% 축소하고, 6개 구조 회귀 테스트·350개 전체 테스트·204개 4-domain 테스트·격리 Docker health 검증으로 API·DB·권한·스케줄·정산 동작 무변경을 보장했다.`

## 7. 트러블슈팅

- `pm-dev` gate는 저장소에 Harness 기획/정책 파일이 없어 실패했다. PM 승인에 따라 누락 파일을 생성하거나 품질 기준을 완화하지 않고 FaithLog TDD·focused/full/build/asciidoctor/Docker QA를 실제 gate로 사용했다.
- Asciidoctor 첫 실행은 sandbox Gradle wrapper lock 권한으로 실패했고 승인 경로의 동일 명령에서 성공했다.
- `.harness/reports`는 untracked로 보존하고 커밋·삭제하지 않았다.

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정

## 9. Velog 글감

- transaction과 repository 호출 순서를 바꾸지 않고 Spring Application Service 책임을 분리하는 구조 테스트 설계
