---
project: FaithLog
type: devlog
issue: #109
status: done
created: 2026-06-30
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #109 경건생활 벌금 0원 청구 생성 방지

## 1. 작업 배경

주간 경건생활 최종 제출에서 계산된 벌금 총액이 0원이어도 `charge_items`에 `PENALTY` 청구가 생성되거나, 활성 `PENALTY` 계좌가 없다는 이유로 제출이 실패할 수 있었다.

## 2. 최종 설계 기준

- `submit = true` 제출 후 계산된 벌금 총액이 0원이면 `PENALTY` 청구를 생성하지 않는다.
- 0원 제출은 활성 `PENALTY` 계좌가 없어도 성공한다.
- 1원 이상 벌금은 기존처럼 활성 `PENALTY` 계좌를 확인하고 `PENALTY` 청구를 생성한다.
- 기존 API response 계약과 DB schema는 변경하지 않는다.

## 3. 구현 내용

- Service: `DevotionService.createPenaltyCharge(...)`에서 `calculation.totalAmount() == 0`이면 billing port 호출 전 반환하도록 변경했다.
- Test: 0원 벌금 제출 시 charge 미생성, 활성 계좌 없이 0원 제출 성공, 1원 이상 벌금/계좌 없음 실패 회귀를 검증했다.
- Docs: decision log, backend policy, Codex hook, resume metrics를 #109 정책으로 보강했다.

## 4. TDD 기록

1. 실패 테스트 작성: `DevotionServiceTest`에 0원 벌금 charge 미생성 및 활성 계좌 없는 0원 제출 성공 테스트 추가.
2. 실패 확인: `./gradlew test --tests 'com.faithlog.devotion.application.DevotionServiceTest'`가 19 tests 중 2 failures로 실패.
3. 최소 구현: 0원 계산 결과에서 billing port 호출을 건너뛰도록 service 분기 추가.
4. 테스트 통과: focused service/docs 테스트와 전체 테스트 통과.
5. 리팩토링: REST Docs missing-account fixture를 양수 벌금 조건으로 보정.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` (269 tests / 0 failures / 0 errors / 1 skipped)

명령:

`./gradlew build`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

기존 missing-account 테스트가 계좌 선확인 구조에 기대고 있어, #109 이후에는 계산 결과가 양수인 fixture에서만 missing-account 실패를 검증하도록 보정했다.

## 7. 트러블슈팅

- 문제: 기존 REST Docs missing-account fixture가 penalty rule 없이 0원으로 계산되어 성공 응답이 되었다.
- 원인: #109 변경으로 계좌 확인이 계산 이후로 이동하면서, 실제 양수 벌금 조건이 필요해졌다.
- 해결: 계좌는 만들지 않고 penalty rule만 생성해 양수 벌금 missing-account 실패를 문서화했다.
- 재발 방지: 0원/양수 벌금 조건을 각각 별도 테스트로 고정했다.

## 8. 다음 작업

- [ ] PM 검증 후 커밋/PR 진행

## 9. Velog 글감

- 0원 청구 row를 만들지 않는 결제 도메인 경계 설계
