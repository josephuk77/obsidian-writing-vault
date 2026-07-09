---
project: FaithLog
type: troubleshooting
created: 2026-06-20
tags:
  - FaithLog
  - troubleshooting
  - spring-boot
  - test-context
---

# Notification concurrency test bean 후보 중복

## 문제 상황

#41 Redis 알림 dedup/lock 구현 후 `./gradlew test --tests 'com.faithlog.notification.*'` 실행 시 여러 SpringBootTest context가 시작하지 못했다.

## 에러 메시지

`NoUniqueBeanDefinitionException`이 발생했고, NotificationLockPort 또는 NotificationDeduplicationPort 주입 대상 bean 후보가 둘 이상으로 잡혔다.

## 원인 분석

테스트 프로파일용 `InMemoryNotificationConcurrencyPort`를 concrete bean으로 등록하면서, 같은 인스턴스를 반환하는 `NotificationDeduplicationPort`, `NotificationLockPort` bean도 별도로 등록했다. concrete class가 두 interface를 구현하므로 Spring 입장에서는 같은 port 타입 후보가 중복된 셈이었다.

## 해결 방법

별도 interface-returning bean 두 개를 제거하고, `InMemoryNotificationConcurrencyPort` concrete bean 하나만 등록했다. 이 bean이 두 port interface를 직접 구현하므로 application service 주입과 테스트 autowire가 모두 단일 후보로 해결됐다.

## 재발 방지

테스트 지원용 in-memory adapter가 여러 port interface를 구현할 때는 concrete bean 하나만 등록한다. 별도 interface bean을 추가해야 한다면 `@Primary` 또는 qualifier 정책을 먼저 명확히 정한다.

## 관련 이슈

- #41
