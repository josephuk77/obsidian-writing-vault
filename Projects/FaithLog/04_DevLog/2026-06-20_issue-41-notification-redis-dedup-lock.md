---
project: FaithLog
type: devlog
issue: #41
status: done
created: 2026-06-20
tags:
  - FaithLog
  - backend
  - spring-boot
  - redis
  - notification
  - tdd
---

# #41 Redis 알림 중복 방지와 알림 락 구현

## 1. 작업 배경

#40에서 구현된 FCM 토큰 등록, 관리자 알림 요청, notification_logs, 비동기 FCM 발송, transient retry 흐름 위에 Redis 기반 dedup/lock을 추가했다. 새 알림 API를 만들지 않고 기존 관리자 알림 API와 worker 흐름을 보강하는 작업이었다.

## 2. 최종 설계 기준

- FCM 토큰 source of truth는 user_fcm_tokens이다.
- 알림 이력 source of truth는 notification_logs이다.
- Redis는 중복 실행 방지와 동시 실행 방지에만 사용한다.
- 자동 알림 dedup key는 notificationType + campusId + scopeId + targetUserId + businessDate 기준이다.
- 일 단위 TTL은 25시간, 주차 단위 TTL은 8일이다.
- lock key는 notification:lock:{jobName}:{campusId}:{scopeId}이고 기본 TTL은 10분이다.
- 자동/스케줄 알림은 Redis 장애 시 fail-closed, 수동 관리자 알림은 API 실패로 처리한다.
- 수동 관리자 알림은 자동 business dedup으로 막지 않는다.

## 3. 구현 내용

- Application: NotificationDeduplicationService, NotificationLockService, key/lease/command value object 추가.
- Port: NotificationDeduplicationPort, NotificationLockPort, NotificationRedisOperationException 추가.
- Redis Adapter: RedisNotificationDeduplicationAdapter, RedisNotificationLockAdapter 추가.
- Existing flow: NotificationService 수동 관리자 알림 요청에 짧은 실행 lock 연결. NotificationDeliveryWorker request dispatch에 requestId 기준 lock 연결.
- ErrorCode: NOTIFICATION_REDIS_UNAVAILABLE, NOTIFICATION_LOCK_ALREADY_RUNNING 추가.
- Test: dedup TTL, lock TTL, custom TTL, Redis 장애 fail-closed, 수동 API Redis 장애 실패, 수동/자동 dedup 분리, worker lock 실패 시 dispatch 차단 검증.

## 4. TDD 기록

1. 실패 테스트 작성: NotificationDeduplicationServiceTest, NotificationLockServiceTest, RedisNotificationConcurrencyAdapterTest를 먼저 추가했다.
2. 실패 확인: 신규 port/service/adapter와 NOTIFICATION_REDIS_UNAVAILABLE 부재로 compileTestJava 52 errors 실패를 확인했다.
3. 최소 구현: application port/service와 Redis adapter를 추가했다.
4. 테스트 통과: 신규 #41 테스트 묶음 성공 후 notification 전체 테스트와 전체 테스트를 통과시켰다.
5. 리팩토링: test profile의 in-memory notification concurrency port를 단일 bean으로 정리해 Spring context 후보 중복을 제거했다.

## 5. 테스트 결과

명령:

`./gradlew test --tests com.faithlog.notification.application.NotificationDeduplicationServiceTest --tests com.faithlog.notification.application.NotificationLockServiceTest --tests com.faithlog.notification.infrastructure.redis.RedisNotificationConcurrencyAdapterTest`

결과:

구현 전 `compileTestJava` 52 errors 실패, 구현 후 BUILD SUCCESSFUL.

명령:

`./gradlew test --tests 'com.faithlog.notification.*'`

결과:

37 tests / 0 failures.

명령:

`./gradlew test`

결과:

198 tests / 0 failures / 0 errors / 0 skipped.

명령:

`./gradlew build`

결과:

BUILD SUCCESSFUL.

명령:

`./gradlew asciidoctor`

결과:

최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행은 BUILD SUCCESSFUL.

Docker/API QA:

`docker compose up -d --build postgres redis app` 성공. postgres/redis healthy, backend started, 컨테이너 내부와 호스트 health 모두 `{"status":"UP"}` 확인. 실제 API QA에서 관리자 CUSTOM 알림 2회 발송 모두 `202 Accepted`, `queuedCount=1`, 서로 다른 `notificationRequestId`, 첫 요청 로그 `SENT` 확인. `docker compose down` 성공.

## 6. 고민한 부분

수동 관리자 알림은 관리자의 의도적 발송이므로 자동 business dedup을 적용하지 않았다. 다만 Redis 장애 시 수동 API가 조용히 발송되면 중복 방지 정책을 우회하게 되므로, 짧은 실행 lock을 요청 시작 시 획득하도록 했다.

## 7. 트러블슈팅

- 문제: test profile에서 notification concurrency port 후보가 중복되어 Spring context가 실패했다.
- 원인: concrete in-memory bean과 interface-returning bean이 같은 port 타입 후보로 동시에 등록됐다.
- 해결: concrete in-memory bean 하나만 등록하고 해당 bean이 두 port interface를 직접 구현하게 정리했다.
- 재발 방지: 테스트 지원 bean이 interface를 구현할 때 별도 wrapper bean을 추가하지 않는다.

## 8. 다음 작업

- [ ] #24 Scheduler/Batch에서 자동 알림 작업이 NotificationDeduplicationService와 NotificationLockService를 호출하도록 연결한다.
- [ ] 오래 남은 PENDING notification_logs 재처리는 #24 또는 후속 이슈에서 다룬다.

## 9. Velog 글감

- Redis setIfAbsent 기반 dedup/lock을 application port로 숨기고, 자동 알림과 수동 알림의 정책을 분리한 과정.
