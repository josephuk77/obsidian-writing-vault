---
project: FaithLog
type: devlog
issue: #30
status: done
created: 2026-06-18
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #30 캠퍼스 멤버 역할과 커피 담당자 관리

## 1. 작업 배경

캠퍼스 관리자가 멤버의 캠퍼스 역할을 변경하고, 커피 담당자를 `CampusRole`이 아닌 `CampusDutyAssignment + DutyType.COFFEE`로 관리할 수 있게 한다.

## 2. 최종 설계 기준

- 역할 위계: `MINISTER > ELDER > CAMPUS_LEADER > MEMBER`.
- 관리자는 자기 역할과 같은 단계까지 target user에게 부여할 수 있고, 자기보다 높은 역할은 변경하거나 부여할 수 없다.
- 전역 `ADMIN`은 모든 캠퍼스 역할을 변경할 수 있다.
- 전역 `MANAGER`만으로는 역할 변경 또는 커피 담당자 관리 권한이 생기지 않는다.
- 커피 담당자 관리는 전역 `ADMIN` 또는 active campus member 중 `MEMBER`가 아닌 역할이 수행한다.
- 캠퍼스당 활성 `DutyType.COFFEE` 담당자는 1명만 유지한다.

## 3. 구현 내용

- Entity: `CampusDutyAssignment`, `DutyType.COFFEE`, `CampusMember.changeCampusRole()`.
- Command: `ChangeCampusRoleCommand`, `AssignCoffeeDutyCommand`.
- Service: `CampusService`에 역할 변경, 관리자 멤버 목록, 커피 담당자 목록/지정/해제 유스케이스 추가.
- 동시성: `assignCoffeeDuty()`에서 캠퍼스 row를 `PESSIMISTIC_WRITE`로 잠근 뒤 기존 active `DutyType.COFFEE` 배정을 revoke하고 새 배정을 저장해, 캠퍼스별 active coffee assignment 1개를 유지한다.
- Repository: `CampusDutyAssignmentRepositoryPort`, `CampusDutyAssignmentRepository`, 캠퍼스 멤버 목록 조회 메서드.
- Controller: `AdminCampusController`.
- Test: `CampusServiceTest`, `CampusControllerTest`, `CampusApiRestDocsTest`.

## 4. TDD 기록

1. 실패 테스트 작성: 역할 위계 same-level assignment, 상위 역할 변경/부여 거부, `ADMIN`/`MANAGER` 권한, 커피 담당자 교체/해제 테스트를 먼저 추가.
2. 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.campus.application.CampusServiceTest --tests com.faithlog.campus.presentation.CampusControllerTest --tests com.faithlog.campus.presentation.CampusApiRestDocsTest`가 `DutyType`, command/result, service method 부재로 `compileTestJava` 실패.
3. 최소 구현: 도메인 권한 비교, application use case, JPA repository, DTO/controller 추가.
4. 테스트 통과: 동일 집중 테스트 통과 후 전체 테스트로 확대.
5. 리팩토링: REST Docs index와 decision log, resume metrics 정리.
6. 동시성 실패 테스트 보강: concurrent coffee assignment 테스트가 lock 구현 전 `NonUniqueResultException`으로 실패하는 것을 확인.
7. 동시성 구현: campus row pessimistic lock 적용 후 동일 테스트와 전체 검증 통과.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`, 47 tests / 0 failures / 0 errors / 0 skipped.

추가 검증:

- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공. 샌드박스에서 Gradle wrapper lock 접근 실패 후 권한 상승 재실행으로 성공.
- REST Docs snippet groups: 22.
- Admin campus snippets: 5.
- `./gradlew test --tests com.faithlog.campus.application.CampusDutyAssignmentConcurrencyTest`: 구현 전 active row 중복으로 `NonUniqueResultException` 실패 확인, lock 적용 후 성공.
- `docker compose build app`: 성공.
- `docker compose up -d postgres redis app`: 성공. postgres/redis healthy, app container started.
- `GET /api/v1/health`: `status=UP` 확인.
- 문서 동기화: `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/backend-implementation-policy.md`, GitHub Issue #30, Notion 역할/커피/API 문서를 same-level assignment 기준으로 갱신.

## 6. 고민한 부분

역할 변경 문구가 기존에는 아래 역할만 변경하는 것으로 해석될 수 있었지만, 최신 사용자 결정에 따라 같은 단계 부여를 허용했다. 커피 담당자 권한도 `MEMBER`가 아닌 캠퍼스 역할과 전역 `ADMIN` 기준으로 분리했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor`가 샌드박스에서 `~/.gradle/wrapper` lock 파일 접근 권한으로 실패.
- 원인: Gradle wrapper cache lock 파일이 작업트리 밖에 있음.
- 해결: 같은 명령을 권한 상승으로 재실행.
- 재발 방지: Gradle wrapper lock 실패 시 동일 검증 명령을 권한 상승으로 재시도한다.

## 8. 다음 작업

- [x] Docker 환경 검증 수행.
- [ ] 최종 Flyway migration consolidation 시 `campus_duty_assignments` 스키마 포함.

## 9. Velog 글감

- 캠퍼스 역할 위계를 코드로 모델링하고 API 권한 테스트로 고정하기.
