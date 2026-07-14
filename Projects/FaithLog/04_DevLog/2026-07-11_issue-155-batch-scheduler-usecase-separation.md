---
project: FaithLog
type: devlog
issue: 155
status: done
created: 2026-07-11
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - batch
  - scheduler
---

# #155 Batch와 Scheduler 책임 분리

## 1. 작업 배경

Issue #152와 #154 이후에도 Poll 자동화와 세 자동 알림이 각각 하나의 Service에 함께 남아 있었다. 공개 API와 DB 동작을 바꾸지 않고 scheduler trigger와 application use case의 책임을 분리했다.

## 2. 최종 설계 기준

- Scheduler는 기존 cron/fixedDelay trigger, `Instant.now()`, 결과 로깅만 소유한다.
- Poll 자동 생성과 due coffee close/settlement는 서로 다른 use case가 소유한다.
- 경건생활 미제출, 투표 미응답, 미납 알림은 각각 독립 use case가 소유한다.
- stale FCM cleanup은 사용자 토큰 command와 분리해 cleanup transaction을 직접 소유한다.
- retention과 PENDING recovery는 기존 전용 TransactionTemplate 경계를 유지한다.

## 3. 구현 내용

- Poll: `ScheduledPollCreationService`, `DueCoffeePollClosureService`.
- Notification: `DevotionMissingNotificationService`, `PollMissingNotificationService`, `PaymentUnpaidNotificationService`.
- Cleanup: `FcmTokenCleanupService`가 90일 cutoff와 repository transaction 직접 소유.
- Facade: `PollAutomationService` 121→29줄, `AutomaticNotificationService` 296→34줄.
- Scheduler: 8개 기존 trigger에서 전용 job service 직접 호출.

## 4. TDD 기록

1. 기존 Batch focused GREEN 확인.
2. 전용 경계, transaction, thin facade, scheduler direct call, SDK 누출/순환 의존 금지 구조 테스트 5건 추가.
3. `5 tests / 5 failures` RED 확인.
4. 기존 상수·락 키·repository 호출·TransactionTemplate 코드를 전용 Service로 이동.
5. 구조 GREEN, scheduler disabled와 coffee settlement exactly-once characterization 보강.

## 5. 테스트 결과

- Batch focused: 성공.
- Batch/Notification/Poll/Billing/Devotion/User: 283/283 성공.
- 전체: 368 tests / 0 failures / 0 errors / 1 skipped.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- `git diff --check`: 성공.

## 6. 정책 보존

Asia/Seoul, scheduler property/cron/fixedDelay와 enable flag, template/week 중복 방지와 snapshot, OPEN 생성, CLOSED 후 coffee settlement, Redis dedup/lock/fail-closed, CUSTOM 포함 5/3/2/1시간 알림, 90일 stale FCM, 10분 PENDING recovery, retention 기간·2월 1일·삭제 순서를 유지했다. API/DTO/HTTP/ErrorCode/auth, Entity/DB/Flyway/repository query, TTL/retry/dependency 변경은 없다.

## 7. 환경 제약

- GitHub token에 `read:project` scope가 없어 Project 카드 확인/이동 불가.
- 현재 파일시스템에 `pm-dev/SKILL.md`, 저장소 `.harness`, `harness.yaml` 없음. 임의 생성 없이 FaithLog TDD gate 적용.
- 호스트 Data 볼륨 100%·가용 1.8GiB와 Docker socket 접근 거부로 삭제/prune 없이 Docker QA 생략. 원격 Docker CI 필요.
- PM 코드리뷰 전 push/PR 금지에 따라 로컬 커밋까지만 수행.

## 8. 다음 작업

- [ ] PM 코드리뷰.
- [ ] 승인 후 원격 CI/Docker image build 검증.

## 9. Velog 글감

- Scheduler를 얇게 유지하면서 transaction과 lock을 use case로 이동하는 리팩터링.
