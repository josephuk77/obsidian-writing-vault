---
project: FaithLog
type: troubleshooting
created: 2026-07-10
tags:
  - FaithLog
  - troubleshooting
  - spring-test
  - test-isolation
---

# 패키지 이동 후 전체 테스트 순서 의존 실패

## 문제 상황

도메인별 focused 테스트는 통과했지만 package 이동 후 전체 `./gradlew test`에서 `AdminManagementServiceTest` 1건과 `BillingServiceTest` 4건이 실패했다.

## 에러 메시지

- 마지막 ADMIN 강등 예외가 발생하지 않음
- `chargeItemRepository.count()` 기대 0/1, 실제 25/26

## 원인 분석

기존 FQCN은 `application` 테스트가 `presentation` 테스트보다 먼저 정렬됐다. 새 FQCN에서는 `controller` 테스트가 `service` 테스트보다 먼저 실행됐다. 일부 controller 통합 테스트가 남긴 H2 데이터가 전역 ADMIN/charge count를 검증하는 service 테스트보다 먼저 생성되면서 테스트가 실행 순서에 의존하게 됐다. 실패한 두 class만 격리 재실행하면 모두 통과해 생산 로직 회귀가 아님을 확인했다.

## 해결 방법

`AdminManagementServiceTest`와 `BillingServiceTest`에 `@DirtiesContext(classMode = BEFORE_CLASS)`를 적용해 class 시작 전에 Spring context와 test schema를 재생성했다. 생산 코드는 변경하지 않았다.

## 재발 방지

- package/class 이름 변경 후 focused 테스트뿐 아니라 전체 suite를 실행한다.
- 전역 count나 마지막 관리자 같은 전체 DB 상태 전제 테스트는 독립된 context 또는 명시적 baseline으로 격리한다.
- source-tree 구조 테스트와 전체 integration suite를 모두 품질 게이트로 유지한다.

## 관련 이슈

- #145
