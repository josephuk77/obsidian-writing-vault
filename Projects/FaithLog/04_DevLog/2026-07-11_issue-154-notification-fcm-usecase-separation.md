---
project: FaithLog
type: devlog
issue: #154
status: done
created: 2026-07-11
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #154 Notification 발송과 FCM 책임 분리

## 1. 작업 배경

#145~#153의 도메인별 책임 분리 이후에도 `FcmTokenService`는 token upsert, 사용자 비활성화, logout port 구현을 함께 소유했고, `NotificationService`는 관리자 권한·대상 계산·로그 생성·dispatch·manual lock을 함께 소유했다. `AutomaticNotificationService`에도 같은 PENDING/SKIPPED 생성과 dispatch 연결이 중복돼 있었다.

## 2. 최종 설계 기준

- `FcmTokenCommandService`가 등록/upsert, 사용자 비활성화, logout current-device port, stale cleanup transaction을 직접 소유한다.
- `NotificationRequestCommandService`가 관리자/자동 요청, PENDING/SKIPPED log 생성, manual lock/business dedup, after-commit dispatch transaction을 직접 소유한다.
- delivery worker, log query, Redis dedup/lock port-adapter는 기존 전용 경계를 유지한다.
- Controller와 automatic/cleanup batch는 전용 command 서비스를 직접 호출한다.
- 기존 `FcmTokenService`와 `NotificationService`는 repository/transaction/`BusinessException`/업무 규칙 없는 호환 delegate다.

## 3. 구현 내용

- Token command: `FcmTokenCommandService`
- Notification request command: `NotificationRequestCommandService`
- Automatic request DTO: `AutomaticNotificationRequestCommand`
- Compatibility facade: `FcmTokenService`, `NotificationService`
- Direct callers: `FcmTokenController`, `AdminNotificationController`, `AutomaticNotificationService`, `FcmTokenCleanupService`
- Unchanged boundaries: `NotificationDeliveryWorker`, `NotificationLogQueryService`, `NotificationDeduplicationService`, `NotificationLockService`, Redis/FCM adapters

## 4. TDD 기록

1. 기존 notification/controller/adapter/batch/logout focused 기준선 GREEN 확인
2. 구조 테스트 작성: 최초 6 tests 중 5 failures RED
3. 최소 구현: validation, repository 호출 순서, transaction, lock/dedup, dispatch 순서를 유지한 책임 이동
4. 구조 테스트 7건과 focused 동작 테스트 GREEN
5. thin facade, direct caller, service cycle, SDK 누출 정적 검증

## 5. 테스트 결과

- 전체 `./gradlew test`: 362 tests / 0 failures / 0 errors / 1 skipped, 실행된 테스트 통과율 100%
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: 성공
- API mapping/DTO/Entity/Flyway/ErrorCode/config 변경: 0건
- Swagger annotation, Controller Entity 반환, service Redis/Firebase SDK 누출, 서비스 순환 의존: 각 0건
- GitHub CI: PR/push 금지 지시로 미실행

## 6. 고민한 부분

- automatic request의 DB transaction 안에서 Redis dedup 예약과 log 생성을 유지하고, dispatch adapter가 commit 이후 worker를 실행하는 기존 순서를 보존했다.
- pending recovery는 worker를 동기 호출한 뒤 여전히 PENDING인 row만 FAILED로 바꾸므로 worker 자체에 `@Async`를 추가하지 않고 기존 after-commit adapter 경계를 유지했다.
- delivery worker의 transient retry 3회, `1s -> 5s -> 30s`, permanent invalid-token 비활성화와 token별 failure 기록은 이동하지 않았다.

## 7. 트러블슈팅

- `pm-dev` 원문은 비활성 보관 경로에만 있고 저장소 Harness 자료와 활성 canonical script가 없어 임의 생성 없이 FaithLog TDD gate를 적용했다.
- Gradle wrapper lock이 sandbox에서 한 차례 막혀 승인된 동일 명령으로 재실행해 성공했다.
- 호스트 Data 볼륨이 99% 사용되고 가용 공간이 2.1GiB여서 격리 Docker build/health QA를 실행하지 않았다. 금지된 system/image/volume prune, named volume 삭제, 파일 삭제로 우회하지 않았다.

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정
- [ ] 원격 Docker CI 또는 디스크 여유가 있는 환경에서 image build/health 검증

## 9. Velog 글감

- after-commit async와 recovery 동기 호출을 보존하며 Notification command 경계를 분리하는 방법

## 10. 이력서 후보

`Notification의 FCM token command와 관리자·자동 요청 command를 분리해 105줄/205줄 통합 Service를 33줄/20줄 호환 facade로 각각 68.6%/90.2% 축소하고, 7개 구조 회귀 테스트·362개 전체 테스트로 API·DB·권한·retry·Redis fail-closed 정책 무변경을 보장했다.`
