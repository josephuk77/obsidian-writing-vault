---
project: FaithLog
type: devlog
issue: "#150"
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - refactoring
---

# #150 Devotion 유스케이스 책임 분리

## 1. 작업 배경

`DevotionService`가 일별 저장, 주간 draft/최종 제출, 본인 주간 조회, 관리자 미제출 조회, 벌금 계산과 Billing port orchestration을 함께 소유하고 있었다. `PenaltyRuleService`도 목록 조회와 관리자 생성/수정 책임을 함께 소유해 Issue #145의 새 패키지 구조 안에서 유스케이스 경계가 드러나지 않았다.

## 2. 최종 설계 기준

- API path, request/response JSON, HTTP status, ErrorCode와 사용자 메시지를 변경하지 않는다.
- Entity, repository query 의미, DB/Flyway, 인증·인가, 7일 row, 1회 제출, 0원 청구 미생성, 월간 집계 정책을 변경하지 않는다.
- 각 이동 public 유스케이스가 기존 write 또는 read-only transaction 경계를 직접 소유한다.
- Controller는 전용 유스케이스 서비스를 직접 호출한다.
- 기존 `DevotionService`와 `PenaltyRuleService`는 repository/transaction/업무 규칙 없는 호환 delegate로만 남긴다.
- 주간 최종 제출의 벌금 계산과 `DevotionPenaltyChargePort` 호출은 하나의 write transaction 안에 유지한다.

## 3. 구현 내용

- Command Service:
  - `DailyDevotionCommandService`: `updateDailyCheck`
  - `WeeklyDevotionCommandService`: `updateWeeklyCheck`, 벌금 계산과 Billing port orchestration
  - `PenaltyRuleCommandService`: `createPenaltyRule`, `updatePenaltyRule`
- Query Service:
  - `MyWeeklyDevotionQueryService`: `getMyWeeklyCheck`
  - `MissingDevotionMemberQueryService`: `getMissingMembers`
  - `DevotionMonthlySummaryQueryService`: 기존 월간 조회 경계 유지
  - `PenaltyRuleQueryService`: `listPenaltyRules`
- Controller:
  - 네 Devotion/PenaltyRule Controller를 전용 서비스에 직접 연결했다.
- 호환 facade:
  - `DevotionService`는 325줄에서 48줄 delegate로 축소했다.
  - `PenaltyRuleService`는 130줄에서 34줄 delegate로 축소했다.
- Repository/Entity/API/DTO/ErrorCode/Flyway: 변경 없음.

## 4. TDD 기록

1. 기존 Devotion focused characterization을 실행해 현재 동작이 GREEN임을 확인했다.
2. 전용 서비스 책임, 직접 transaction, Controller 연결, 얇은 facade, 순환 의존 금지를 고정하는 구조 테스트 5건을 production 수정 전에 추가했다.
3. 전용 파일 부재와 기존 Controller/facade 결합으로 5 tests / 5 failures RED를 확인했다.
4. 기존 메서드 본문과 private helper를 유스케이스별 서비스로 이동하고 Controller를 직접 연결해 구조 테스트를 GREEN으로 만들었다.
5. 기존 focused 동작 테스트, #165 4-domain 조합, 전체 테스트로 정책 무변경을 회귀 검증했다.

## 5. 테스트 결과

- Devotion focused service/Controller/REST Docs/구조 테스트: `BUILD SUCCESSFUL`
- Billing/Devotion/Poll/Batch 4-domain 조합: `BUILD SUCCESSFUL`
- `./gradlew test`: 338 tests / 0 failures / 0 errors / 1 skipped, `BUILD SUCCESSFUL`
- `./gradlew build`: `BUILD SUCCESSFUL`
- `./gradlew asciidoctor`: `BUILD SUCCESSFUL`
- `git diff --check`: 성공
- 격리 Docker QA `faithlog-qa-150-devotion`: image build, PostgreSQL/Redis healthy, `/api/v1/health` `data.status=UP`, compose down 성공
- Docker 정리: `docker builder prune -f`로 build cache 699.6MB 정리. volume/image/system prune 미실행.

## 6. 고민한 부분

공통 access/helper 서비스를 새로 만들면 중복은 줄지만 새 서비스 간 의존과 정책 추상화 결정이 생긴다. 이번 이슈는 동작 무변경 리팩터링이므로 각 유스케이스가 기존 private helper와 검증 순서를 직접 소유하도록 두고 공통 helper 서비스는 추가하지 않았다.

주간 최종 제출에서는 `submittedAt` 기록, active penalty rules 조회, 벌금 계산, 0원 early return, 양수 Billing port 호출이 한 트랜잭션으로 묶여야 한다. 이 흐름을 별도 서비스 체인으로 나누지 않고 `WeeklyDevotionCommandService` 안에 응집시켜 기존 all-or-nothing 경계를 유지했다.

## 7. 트러블슈팅

- GitHub Project: Issue #150의 project item이 비어 있었고 token에 `read:project` scope가 없어 카드 연결/`In Progress` 전환을 수행하지 못했다.
- PM harness: 비활성 보관된 `pm-dev` 원문에 따라 `dev_gate.py`를 실행했지만 `harness.yaml`, `.harness` 기획/정책, custom agent 설정이 없어 실패했다. `score_code.py`는 critical/security finding 0건을 기록했지만 specialist/overall score 부재로 `passed=false`였고, `review_gate.py`도 quality/TDD harness와 evidence 파일 부재로 실패했다. #150 범위 밖 harness 파일은 생성하지 않았으며 생성된 `.harness/reports/`는 커밋하거나 삭제하지 않고 보존했다.
- Gradle: `asciidoctor` 첫 실행은 Gradle wrapper lock의 sandbox 권한으로 실패했고 동일 명령의 승인 실행에서 성공했다.
- Docker: 첫 격리 QA 실행은 Docker socket sandbox 권한으로 실패했고 승인 실행에서 성공했다.

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정
- [ ] GitHub Project scope가 준비되면 #150 카드 상태 반영

## 9. Velog 글감

- 거대 Application Service를 transaction-safe 유스케이스 서비스로 분리하는 구조 테스트 전략
- 호환 facade를 남기면서 production caller를 전용 서비스로 전환하는 점진적 리팩터링
