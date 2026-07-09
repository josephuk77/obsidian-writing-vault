# 2026-06-21 Issue #45 조별 기도제목 조회와 입력

## 작업 범위

- 브랜치: `feat/45-prayer-group-weekly-board`
- 활성 캠퍼스, ACTIVE 기도 시즌, 활성 기도조, 활성 조원, ACTIVE 캠퍼스 멤버 기준의 조별 기도제목 조회/저장 구현.
- 저장 단위는 페이지 blob이 아니라 조원별 `prayer_submissions` row.
- `content` nullable 저장, 저장 시 실제 `submittedAt` 유지, GET은 row 미생성.
- 일반 ACTIVE 멤버는 자기 활성 기도조만 저장, 캠퍼스 관리자 권한은 전체 조 저장.
- ACTIVE 시즌 중복 생성 방지, 기도조 멤버 PUT 전체 교체와 inactive/reactivate 구현.

## TDD 실패 Evidence

- `./gradlew test --tests com.faithlog.prayer.application.PrayerServiceTest`
  - 구현 전 prayer domain/service/repository 부재로 `compileTestJava` 63 errors 실패.
- `./gradlew test --tests com.faithlog.prayer.presentation.PrayerApiRestDocsTest`
  - 컨트롤러 구현 전 첫 `POST /api/v1/admin/campuses/{campusId}/prayer-seasons` route 부재로 assertion 실패.

## 검증 결과

- `./gradlew test --tests com.faithlog.prayer.application.PrayerServiceTest` 성공.
- `./gradlew test --tests com.faithlog.prayer.presentation.PrayerApiRestDocsTest` 성공.
- `./gradlew test` 성공: 223 tests / 0 failures / 0 errors / 0 skipped.
- `./gradlew build` 성공.
- `./gradlew asciidoctor` 성공.
- Docker: `docker compose up -d --build app` 성공, `GET /api/v1/health` 200/`UP`, `docker compose down` 완료.

## 실제 API QA

- MANAGER 테스트 계정 생성 후 캠퍼스 준비, 일반 멤버 3명 invite join.
- 시즌 생성, 중복 ACTIVE 시즌 409/`PRAYER_ACTIVE_SEASON_ALREADY_EXISTS` 확인.
- 기도조 2개 생성, 조원 배정, 전체 교체 inactive/reactivate 확인.
- 일반 ACTIVE 멤버 전체 조별 조회 성공.
- GET 전후 `prayer_weeks`/`prayer_submissions` row count `1/2 -> 1/2`로 row 미생성 확인.
- 일반 멤버 자기 조 저장 성공, PUT 후 row count `2/4`로 필요한 row 생성 확인.
- 일반 멤버 다른 조 저장 403/`PRAYER_SUBMISSION_FORBIDDEN` 확인.
- 관리자 전체 조 저장 성공.
- version 충돌 409/`PRAYER_SUBMISSION_CONFLICT`; batch rollback으로 submission count `4 -> 4`, 충돌 batch의 다른 멤버 row `0` 확인.
- 화요일 weekStartDate 400/`PRAYER_INVALID_WEEK_START_DATE` 확인.
- 다음 월요일 `2026-06-29` 사전 저장 성공.

## 수치

- Java sources: 415
- Test files: 49
- REST Docs snippet groups: 94

## 메모

- `NO_MEETING`은 신규 source/test에 추가하지 않음.
- `content: null`로 명시 저장된 submission row는 작성완료 집계에 포함한다.
- Swagger 문서화 annotation은 추가하지 않고 Spring REST Docs 테스트로 API 계약을 문서화했다.

## PM 코드 리뷰 보강 - 실제 optimistic locking

- 리뷰 문제: 기존 구현은 저장 전 request version과 entity version을 비교한 뒤 `PrayerSubmission.update()`에서 수동으로 `version += 1`을 수행해, 두 트랜잭션이 같은 version을 읽으면 lost update 가능성이 있었다.
- 수정: 기존 row 업데이트를 `UPDATE ... WHERE id = :id AND version = :expectedVersion` 조건부 update로 변경하고, affected row가 0이면 `PRAYER_SUBMISSION_CONFLICT`로 처리한다.
- TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.prayer.application.PrayerSubmissionConcurrencyTest`가 `updateContentIfVersionMatches` repository method 부재로 `compileTestJava` 실패.
- 동시성 검증: 두 트랜잭션이 같은 version 1을 읽고 동시에 update를 시도할 때 1건만 성공하고 1건은 `PRAYER_SUBMISSION_CONFLICT`로 처리됨을 테스트로 검증.
- 회귀 검증: `PrayerServiceTest`, `PrayerApiRestDocsTest`, `./gradlew test`(224 tests / 0 failures), `./gradlew build`, `./gradlew asciidoctor`, `git diff --check origin/develop...HEAD` 성공.
- Docker/API QA: `docker compose up -d --build app`, `/api/v1/health` 200/UP, 실제 API stale version update 409/`PRAYER_SUBMISSION_CONFLICT`, 최종 content/version `second`/`2`, `docker compose down` 성공.
- PM 확인 필요: CLOSED 시즌 group 생성/수정/member 교체 차단 정책은 승인 전이라 구현하지 않음.

## PM 재검증 보강 - 테스트 격리

- 실패 원인: `PrayerSubmissionConcurrencyTest`가 실제 H2 DB에 `prayer_weeks`/`prayer_submissions` row를 남겼고, `PrayerApiRestDocsTest`가 전체 repository count 0을 가정해 build 순서에서 실패했다.
- 수정: REST Docs 테스트의 GET row 미생성 검증을 전체 count 0이 아니라 GET 전후 baseline count 불변 검증으로 변경했다.
- 수정: 동시성 테스트는 자신이 만든 prayer week/submission row만 `@AfterEach`에서 명시적으로 정리한다.
- 재검증: 지정 #45 테스트 묶음 성공, `./gradlew test` 성공(224 tests / 0 failures), `./gradlew build` 성공, `git diff --check origin/develop...HEAD` 성공, `./gradlew asciidoctor` 성공.
