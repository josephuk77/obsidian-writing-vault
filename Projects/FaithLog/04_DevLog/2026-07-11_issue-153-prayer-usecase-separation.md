---
project: FaithLog
type: devlog
issue: #153
status: done
created: 2026-07-11
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #153 Prayer 유스케이스 책임 분리

## 1. 작업 배경

#145~#152의 도메인별 책임 분리 이후에도 606줄 `PrayerService`는 시즌, 조, 주간 보드, 조별 다중 제출, 본인 제출, 권한, 대상 조원 조회, 결과 조립을 함께 소유했다. 공개 API와 DB 동작을 바꾸지 않고 유스케이스와 transaction 경계를 분리했다.

## 2. 최종 설계 기준

- 11개 public 유스케이스가 7개 전용 Service에서 기존 write/read-only transaction을 직접 소유한다.
- 두 Prayer Controller는 전용 Service를 직접 호출한다.
- 공통 권한, 활성 조·조원 조회, 보드 조립만 package-private support로 응집한다.
- `PrayerService`는 repository/transaction/`BusinessException`/업무 규칙이 없는 호환 delegate로만 유지한다.
- API/DTO/ErrorCode, 권한, 시즌·조·주차·제출, optimistic locking, all-or-nothing, Entity/DB/Flyway/repository 정책은 변경하지 않는다.

## 3. 구현 내용

- Season: `PrayerSeasonCommandService`, `PrayerSeasonQueryService`
- Group: `PrayerGroupCommandService`, `PrayerGroupQueryService`
- Board: `PrayerWeekBoardQueryService`
- Submission: `PrayerGroupSubmissionCommandService`, `MyPrayerSubmissionCommandService`
- Support: `PrayerAccessSupport`, `PrayerTargetMemberSupport`, `PrayerBoardAssembler`
- Compatibility facade: `PrayerService`
- Controller: `AdminPrayerController`, `PrayerController`를 전용 Service에 직접 연결

## 4. TDD 기록

1. 실패 테스트 작성: 직접 transaction, Controller 전용 Service 연결, thin facade, 서비스 간 의존 금지 구조 테스트 5건
2. 실패 확인: 5 tests / 5 failures
3. 최소 구현: 기존 public/private 로직을 validation·repository 호출 순서 그대로 이동
4. 테스트 통과: 구조 테스트 5건과 Prayer service/동시성/REST Docs GREEN
5. 리팩토링: 권한·대상 조원·보드 조립을 실제 공유 경계로 정리하고 호환 facade를 delegate로 축소
6. PM 리뷰: 다중 제출 Service를 `PrayerGroupSubmissionCommandService` 기준으로 구조 테스트부터 변경해 5/5 RED 확인 후 production 이름만 변경해 GREEN

## 5. 테스트 결과

- Prayer focused service/동시성/REST Docs/구조: 성공
- Campus + Billing/Devotion/Poll/Prayer/Batch: 260 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 355 tests / 0 failures / 0 errors / 1 skipped, 실행된 테스트 통과율 100%
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: 성공
- GitHub CI: PR/push 금지 지시로 미실행
- Docker QA: 1차 BuildKit metadata DB I/O 오류, daemon 복구 후 2차 호스트 가용 공간 116MiB·100% 사용 상태의 no-space 오류로 image/health 확인 미완료. volume 삭제 없는 project down 수행

## 6. 고민한 부분

- 조원 전체 교체는 중복 ID, ACTIVE 캠퍼스 멤버, 타 조 중복 배정, 기존 row 재활성/비활성, 신규 row 저장 순서를 바꾸지 않았다.
- 조별 다중 제출은 일반 ACTIVE 멤버의 자기 활성 조 다중 입력과 관리자 전체 조 입력 권한을 유지하며, 모든 version을 쓰기 전에 검증하고 조건부 update 실패 시 같은 transaction 전체를 rollback하는 경계를 유지했다.
- 보드 GET은 `prayer_week`/`prayer_submission`을 만들지 않고, 저장 command만 필요한 row를 생성한다.
- `PrayerService`는 기존 내부 호출과 테스트 호환을 위해 남기되 606→90줄(-85.1%)의 순수 delegate로 제한했다.

## 7. 트러블슈팅

- `pm-dev`가 비활성 보관 경로에만 있고 저장소 Harness 파일과 활성 gate가 없어, 누락 파일을 만들거나 품질 기준을 완화하지 않고 FaithLog TDD/검증 기준을 사용했다.
- Asciidoctor 첫 실행은 sandbox Gradle wrapper lock 권한으로 실패했고 승인 경로의 동일 명령으로 성공했다.
- Docker QA는 BuildKit `metadata_v2.db`/`snapshots.db` I/O 오류와 호스트 디스크 부족으로 중단돼 별도 troubleshooting 문서에 기록했다. Android Emulator, 기존 volume/image는 건드리지 않았다.

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정
- [ ] 사용자가 호스트 디스크 공간을 확보한 뒤 격리 Docker health QA 재실행

## 9. Velog 글감

- transaction과 repository 호출 순서를 보존하면서 Spring Application Service 책임을 분리하는 구조 테스트 설계

## 10. 이력서 후보

`Prayer의 11개 유스케이스를 조별 다중 제출을 포함한 7개 응집 Service와 3개 package-private support로 분리해 606줄 통합 Service를 90줄 호환 facade로 85.1% 축소하고, 5개 구조 회귀 테스트·355개 전체 테스트·260개 연관 도메인 테스트로 API·DB·권한·optimistic locking·all-or-nothing 동작 무변경을 보장했다.`
