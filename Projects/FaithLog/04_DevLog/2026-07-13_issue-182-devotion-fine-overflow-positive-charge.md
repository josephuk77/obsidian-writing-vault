---
project: FaithLog
type: devlog
issue: "#182"
status: done
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - tdd
---

# #182 경건 벌금 overflow와 음수 청구 차단

## 1. 작업 배경

Issue #160 F-160-01에서 상한 없는 `saturdayLateMinutes`와 unchecked `int` 연산이 음수 PENALTY 청구 및 dashboard 합계 왜곡으로 이어지는 경로가 확인됐다.

## 2. 최종 설계 기준

- `saturdayLateMinutes`는 0..1,440분이다.
- 계산은 `long`과 `Math.multiplyExact`/`Math.addExact`를 사용한다.
- overflow와 PostgreSQL `INTEGER` 저장 범위 초과는 `400 DEVOTION_FINE_AMOUNT_OUT_OF_RANGE`로 거부한다.
- Billing create/update는 `amount > 0`만 허용하며 총액 0원은 charge를 만들지 않는다.
- V7 CHECK는 신규 위반을 거부하되 기존 위반 row를 수정하거나 삭제하지 않는다.

## 3. 구현 내용

- Entity: `ChargeItem` 생성 및 미납 갱신 양수 불변식
- Command/DTO: 정상 구조 변경 없음
- Service: 주간 지각 입력 상한 및 exact calculation/storage range guard
- Repository: 변경 없음
- Controller/API mapping: 변경 없음
- Flyway: `V7__enforce_positive_charge_amount.sql`, `ck_charge_items_amount_positive`
- Test: 경계값, 산술/저장 overflow, 전체 rollback, 양수 불변식, clean/legacy PostgreSQL, REST Docs

## 4. TDD 기록

1. 실패 테스트 작성: 1,440/1,441/음수, 규칙 곱셈·합산·저장범위, rollback, ChargeItem, V7 CHECK
2. 실패 확인: 57 tests / 11 failures
3. 최소 구현: 입력 상한, long exact 연산, 범위 오류 변환, 양수 domain invariant, V7 migration
4. 테스트 통과: focused 57 tests GREEN
5. 리팩토링: 계산과 저장 범위 변환을 calculator 내부의 명시적 경계로 유지

## 5. 테스트 결과

- 전체: 396 tests / 0 failures / 0 errors / 3 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- PostgreSQL clean V1→V7 및 legacy V6→V7: 성공
- REST Docs snippet groups: 123

## 6. Docker HTTP QA

- project: `faithlog-qa-182-20260713`
- PostgreSQL/Redis healthy, Flyway 7 migrations, Hibernate validate, health 200
- 1,440 성공; 1,441/음수 400
- 저장범위 초과 400, weekly/daily/charge `0→0`
- 0원 charge `0→0`, 정상 2,500원 charge `0→1`, dashboard unpaid 2,500원
- volume 삭제 없이 down; 마지막 Docker 명령 `docker builder prune -f`, 696.6MB 회수

## 7. 고민한 부분

금액은 `double`이 아니라 정수형을 유지했다. 부동소수점 반올림 오차를 피하면서 중간 계산만 `long` exact arithmetic으로 넓히고 저장 직전에 `INTEGER` 범위를 검증했다. Legacy 0/음수 row가 있으면 migration이 데이터를 바꾸지 않고 CHECK를 미검증 상태로 남기며 신규 위반만 차단한다.

## 8. 트러블슈팅

- 기본 Gradle cache metadata 접근 실패와 sandbox socket 제한은 격리 `GRADLE_USER_HOME` 및 승인된 Gradle 실행으로 해결했다.
- 초기 RED rollback 테스트 fixture가 다른 테스트에 남아 실패 수를 증폭시켜 `@DirtiesContext`로 격리했다.

## 9. 다음 작업

- [ ] PM 코드리뷰 및 독립 검증
- [ ] PM 승인 후 push/PR 결정

## 10. 이력서 문장 후보

경건 벌금 계산을 long exact arithmetic과 INTEGER 범위 검증으로 보강하고 Billing·Flyway 양수 불변식을 3중 적용해 음수 청구와 dashboard 상쇄를 차단했으며, 11개 RED 실패·396개 전체 테스트·clean/legacy PostgreSQL migration·격리 Docker HTTP rollback QA로 검증했다.
