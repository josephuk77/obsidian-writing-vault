---
project: FaithLog
type: devlog
issue: "#32"
status: done
created: 2026-06-19
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #32 경건생활 벌금 규칙과 벌금 계산 구현

## 1. 작업 배경

캠퍼스별 `penalty_rules`를 관리하고, 주간 경건생활 요약값으로 벌금을 계산하는 기반을 구현했다. 실제 `PENALTY charge_items` 생성/갱신 연결은 #33 범위로 남겼다.

## 2. 최종 설계 기준

- API: `GET /api/v1/campuses/{campusId}/penalty-rules`, `POST /api/v1/admin/campuses/{campusId}/penalty-rules`, `PATCH /api/v1/admin/penalty-rules/{ruleId}`
- 타입: `QUIET_TIME`, `PRAYER`, `BIBLE_READING`, `SATURDAY_LATE`
- 계산 타입: `MISSING_COUNT`, `LATE_MINUTE`
- ACTIVE 자동 교체: 같은 캠퍼스와 같은 `ruleType`의 기존 ACTIVE 규칙은 새 ACTIVE 규칙 생성 시 비활성화
- 계산: 부족 일수는 `max(requiredCount - checkedCount, 0)`, 토요 지각은 0분이면 0원, 1분 이상이면 `baseAmount + minutes * amountPerUnit`

## 3. 구현 내용

- Entity: `PenaltyRule`
- Enum: `PenaltyRuleType`, `PenaltyCalculationType`
- Repository: `PenaltyRuleRepository`
- Service: `PenaltyRuleService`
- Domain Service: `DevotionFineCalculator`
- Result: `DevotionFineCalculationInput`, `DevotionFineCalculationItemResult`, `DevotionFineCalculationResult`, `PenaltyRuleResult`
- Controller/DTO: member/admin penalty rule controllers, create/update/response DTO
- Test: domain calculator, application service, Spring REST Docs API 계약 테스트

## 4. TDD 기록

1. 실패 테스트 작성: 계산, 규칙 관리, REST Docs API 테스트를 먼저 추가.
2. 실패 확인: 구현 전 대상 테스트 묶음이 `PenaltyRule`, enum, repository, service, calculator, error code 부재로 `compileTestJava` 실패.
3. 최소 구현: entity/enum/repository/service/controller/calculator를 추가.
4. 테스트 통과: #32 대상 테스트 묶음 성공.
5. 리팩토링: 계산 로직은 domain service에 두고 Controller/Application에는 정책 흐름만 남겼다.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`, 114 tests / 0 failures / 0 errors / 0 skipped

추가 검증:

- `./gradlew build`: 성공
- Docker QA: health 200, #32 POST/GET/PATCH 성공, `docker compose down` 완료
- REST Docs snippets: penalty rule 5개 묶음 생성

## 6. 고민한 부분

- `PATCH isActive=true`도 active rule invariant를 깨지 않도록 같은 campus/ruleType의 다른 ACTIVE 규칙을 비활성화하게 했다.
- 음수 값과 rule/calculation type pairing은 domain entity 검증으로 고정했다.

## 7. 트러블슈팅

- 문제: Docker QA 계정이 기본 `USER`라 캠퍼스 생성에서 403 발생.
- 원인: 캠퍼스 생성은 `MANAGER` 또는 `ADMIN`만 가능.
- 해결: Docker Postgres의 QA 계정 1건만 `MANAGER`로 업데이트하고 API 흐름을 재검증.
- 재발 방지: Docker QA에서 campus 생성이 필요한 경우 테스트 계정 role 설정 단계를 명시한다.

## 8. 다음 작업

- [ ] #33 주간 경건생활 제출 시 계산 결과를 사용해 `PENALTY charge_items` 생성/갱신 연결

## 9. Velog 글감

- 벌금 계산을 Controller가 아닌 domain service로 분리한 TDD 흐름
