---
project: FaithLog
type: devlog
issue: #24
status: done
created: 2026-06-21
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - scheduler
---

# #24 Batch/Scheduler PM Reinforcement

## 1. 작업 배경

PM 검증에서 #24 초기 구현이 Poll 자동 생성/커피 마감/FCM cleanup 일부에 머물러 자동 알림 3종, PENDING notification_logs 재처리, scheduler trigger 노출, Docker 실기동 검증이 부족하다고 확인됐다.

## 2. 최종 설계 기준

- 새 사용자-facing API는 추가하지 않는다.
- Scheduler/Batch는 Controller 없이 application service를 호출한다.
- 자동 알림은 `notification_logs`를 source of truth로 남기고, FCM token은 `user_fcm_tokens`를 source of truth로 사용한다.
- #41 Redis scheduled lock과 business dedup을 사용하며 Redis 장애 시 자동 알림은 fail-closed 처리한다.
- 기준 시간대는 `Asia/Seoul`이다.

## 3. 구현 내용

- Service: `AutomaticNotificationService`, `PendingNotificationRecoveryService`
- Scheduler: `FaithLogScheduledJobs`에 경건생활 미제출, 투표 미응답, 미납, PENDING 재처리 job 추가
- Repository: active campus 조회, poll due window 조회, 오래된 PENDING log 조회 메서드 추가
- Config: `application.yml`에 #24 scheduler 설정값 노출
- Test: 자동 알림 dedup/fail-closed/수동 dedup 분리, PENDING 10분 기준/1회 재처리/FAILED 정책, scheduler-enabled context 회귀 테스트

## 4. TDD 기록

1. 실패 테스트 작성: `AutomaticNotificationServiceTest`, `PendingNotificationRecoveryServiceTest`
2. 실패 확인: 구현 전 `AutomaticNotificationService`, `PendingNotificationRecoveryService` 부재로 `compileTestJava` 실패
3. 최소 구현: 자동 알림 service와 PENDING 재처리 service 추가
4. 테스트 통과: 신규 batch application 테스트 및 `com.faithlog.batch.*` 통과
5. 리팩토링: Docker 실기동에서 발견한 `TaskExecutor` 주입 충돌을 qualifier와 scheduler context test로 고정

## 5. 테스트 결과

- `./gradlew test`: 214 tests / 0 failures / 0 errors / 0 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check origin/develop...HEAD`: 성공
- Docker compose: 내부 `/actuator/health` `{"status":"UP"}`

## 6. 고민한 부분

- 투표 미응답 알림은 1분 fixed-delay scan에서 누락을 줄이기 위해 1분 lookback window를 두고, poll + offset scope를 dedup key에 포함했다.
- 수동 버튼 알림은 관리자 요청 흐름과 lock만 사용하고, 자동 business dedup key와 섞이지 않도록 별도 테스트로 보존했다.
- PENDING 재처리는 별도 retry count schema를 추가하지 않고 10분 이상 PENDING request를 1회 worker로 재처리한 뒤 남은 PENDING을 FAILED로 닫는 방식으로 #24 범위 안에서 처리했다.

## 7. 트러블슈팅

- 문제: Docker에서 scheduler 활성화 후 `TaskExecutor` 후보가 2개가 되어 app startup 실패
- 원인: `@EnableScheduling`이 `taskScheduler` bean을 추가했고 `AsyncNotificationDispatchAdapter`가 qualifier 없는 `TaskExecutor`를 요구함
- 해결: `@Qualifier("applicationTaskExecutor")`를 추가하고 scheduler-enabled context test를 추가
- 재발 방지: Docker health와 `FaithLogSchedulerConfigTest`로 확인

## 8. 다음 작업

- [ ] PM 세션 재검증 요청
- [ ] PM 검증 후 PR 생성

## 9. Velog 글감

- Spring Scheduler와 Redis lock/dedup으로 안전한 자동 알림 배치를 구현한 과정
- Docker 실기동이 잡아낸 TaskExecutor bean ambiguity
