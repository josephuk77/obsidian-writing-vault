# 2026-06-19 Issue #61 서비스 ADMIN 유저와 캠퍼스 관리

## Scope

- GitHub Issue: #61
- Branch: `feat/61-service-admin-user-campus-management`
- Goal: 서비스 전역 `ADMIN` 전용 유저/캠퍼스 관리 API 구현.

## Decisions

- 캠퍼스 운영 상태는 새 enum/컬럼 없이 `campuses.is_active`에서 계산한다.
  - `true` -> `ACTIVE`
  - `false` -> `PAUSED`
- `INVITED` 캠퍼스 상태와 audit log 저장/조회는 이번 범위에서 제외한다.
- 마지막 서비스 ADMIN 보호 기준은 활성 사용자 중 `users.role = ADMIN`인 계정 수다.
- 서비스 ADMIN 직접 멤버 추가에서 이미 ACTIVE 멤버십이 있으면 `CAMPUS_ALREADY_JOINED` 400으로 실패한다.
- 기존 INACTIVE 멤버십은 새 row를 만들지 않고 `ACTIVE + MEMBER`로 재활성화한다.

## TDD Evidence

- 구현 전 실패:
  - `./gradlew test --tests com.faithlog.admin.presentation.AdminManagementControllerTest`
  - 결과: 4 tests / 4 failed
  - 원인: `/api/v1/admin/users`, `/api/v1/admin/users/{userId}/role`, `/api/v1/admin/campuses`, 직접 멤버 추가 endpoint 미구현.

## Implementation

- `admin` application/presentation 패키지를 추가했다.
- `AdminAccessPolicy`로 서비스 ADMIN 접근 정책을 분리했다.
- 사용자/캠퍼스 검색 criteria, result DTO, repository port를 추가해 Controller/Service에 조회 조립을 몰아넣지 않았다.
- Controller는 Entity를 반환하지 않고 request/response DTO와 `PageResponse`를 반환한다.
- `users.role` 변경은 role 필드만 수정하며, 마지막 활성 ADMIN 강등은 차단한다.
- 서비스 ADMIN은 캠퍼스 멤버십 없이 전체 유저/캠퍼스를 조회하고 수정할 수 있다.
- `PATCH /api/v1/campuses/{campusId}`를 추가해 기존 캠퍼스 수정 정책을 재사용하고 서비스 ADMIN 권한을 검증했다.

## Validation

- `./gradlew test --tests com.faithlog.admin.application.AdminManagementServiceTest --tests com.faithlog.admin.presentation.AdminManagementControllerTest`
- `./gradlew test --tests com.faithlog.admin.presentation.AdminManagementApiRestDocsTest`
- `./gradlew test`
  - 138 tests / 0 failures / 0 errors / 0 skipped
- `./gradlew build`
- `./gradlew asciidoctor`
  - 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
- REST Docs snippet group: 57개
- Docker:
  - `docker compose build app` 2회 모두 베이스 이미지 metadata 조회 단계에서 `DeadlineExceeded: context deadline exceeded` 실패.
  - 컨테이너는 시작되지 않았고 `docker ps` 기준 running container 0개.

## Compliance

- Swagger 문서화 어노테이션 추가 없음.
- Controller Entity 직접 반환 없음.
- 신규 DB schema/enum 추가 없음.
- audit log 저장/조회 구현 없음.
- `INVITED` 상태 저장/조회 구현 없음.

## Notes

- PM harness `dev_gate.py`는 저장소에 `harness.yaml`, `.harness/*`, `.codex/agents/*`가 없어 실패했다. 기능 구현 검증은 Gradle 테스트, build, REST Docs, 정적 검색으로 대체 기록했다.
