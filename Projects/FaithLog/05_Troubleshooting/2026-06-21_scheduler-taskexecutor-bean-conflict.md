---
project: FaithLog
type: troubleshooting
created: 2026-06-21
tags:
  - FaithLog
  - troubleshooting
  - spring-boot
  - scheduler
---

# Scheduler 활성화 시 TaskExecutor Bean 충돌

## 문제 상황

#24 PM 보강 후 Docker compose로 `postgres`, `redis`, `app`을 올렸을 때 app 컨테이너가 시작 직후 종료됐다.

## 에러 메시지

`AsyncNotificationDispatchAdapter` 생성자 parameter 1의 `TaskExecutor` 후보가 `applicationTaskExecutor`, `taskScheduler` 두 개라 단일 bean을 결정할 수 없다는 startup failure가 발생했다.

## 원인 분석

#24에서 `@EnableScheduling`을 활성화하면서 Spring Boot가 `taskScheduler` bean을 추가했다. 이 bean도 `TaskExecutor` 후보로 잡혀, 기존 async notification dispatch adapter의 qualifier 없는 `TaskExecutor` 주입이 모호해졌다.

## 해결 방법

`AsyncNotificationDispatchAdapter` 생성자에 `@Qualifier("applicationTaskExecutor")`를 추가해 FCM dispatch는 Boot 기본 application task executor를 사용하도록 고정했다. 또한 `faithlog.scheduler.enabled=true` 조건으로 context를 띄우는 `FaithLogSchedulerConfigTest`를 추가해 회귀를 막았다.

## 재발 방지

- scheduler-enabled context test 유지
- Docker compose health를 PR 전 검증 게이트로 유지
- scheduler 관련 bean을 추가할 때 executor/scheduler 타입 충돌 여부를 확인

## 관련 이슈

- #24
