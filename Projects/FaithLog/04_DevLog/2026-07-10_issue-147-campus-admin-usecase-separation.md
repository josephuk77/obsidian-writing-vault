---
project: FaithLog
type: devlog
issue: "#147"
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - refactoring
---

# #147 Campus와 Admin 유스케이스 책임 분리

## 1. 작업 배경

#145의 DDD 내부 MVC 패키지 구조를 유지하면서 `CampusService`, `AdminManagementService`, `AdminDashboardService`의 과도한 Application 책임을 기능 동작 변경 없이 유스케이스 단위로 나눴다.

## 2. 최종 설계 기준

- Campus: 생성, 가입/재가입, 조회, 수정, 멤버 관리, 커피 담당자 관리의 6개 Service.
- Admin: 서비스 사용자 관리, 서비스 캠퍼스 관리, 캠퍼스 관리자 대시보드 조회의 3개 Service.
- 기존 3개 Service는 repository/transaction을 소유하지 않는 호환 façade로 유지.
- 기존 command/query/result/policy/port, API, DB, 권한, 트랜잭션 의미 유지.

## 3. 구현 내용

- Service:
  - `CampusCreationService`: 캠퍼스 생성과 초대코드 유일성, 생성 side effect.
  - `CampusJoinService`: 초대코드 가입과 INACTIVE 멤버 재가입.
  - `CampusQueryService`: 내 캠퍼스 목록과 상세.
  - `CampusUpdateService`: 캠퍼스 정보 수정.
  - `CampusMemberManagementService`: 멤버 조회/삭제/role 변경과 tokenVersion 증가.
  - `CampusDutyAssignmentService`: 담당자 조회/지정/해제와 campus row lock.
  - `AdminUserManagementService`: 서비스 ADMIN 사용자 목록/상세/role 변경.
  - `AdminCampusManagementService`: 서비스 ADMIN 캠퍼스 목록/멤버 직접 추가.
  - `AdminDashboardQueryService`: dashboard summary read-only 집계.
- Policy: 공통 Campus 활성 사용자와 캠퍼스 관리자 검증을 `CampusAccessPolicy`로 모으고 기존 `CampusRolePolicy`와 `AdminAccessPolicy` 의미를 유지.
- Result: 대시보드 결과를 `admin/service/result/AdminDashboardSummaryResult`로 이동.
- Controller: 기존 endpoint mapping은 그대로 두고 각 유스케이스 Service를 직접 호출.
- Test: 구조 경계 테스트 4건과 캠퍼스 수정 characterization test 1건 추가.

## 4. TDD 기록

1. 실패 테스트 작성: 새 책임 Service 파일/메서드와 repository-free façade를 요구하는 구조 테스트를 추가했다.
2. 실패 확인: 구조 테스트 4 tests / 4 failed.
3. 최소 구현: 기존 메서드 몸체와 검증 순서를 9개 유스케이스 Service로 이동했다.
4. 테스트 통과: admin/campus focused 47 tests 및 전체 320 tests 성공.
5. 리팩토링: Controller를 새 Service 경계에 연결하고 기존 Service는 호환 위임만 남겼다.

## 5. 테스트 결과

- `./gradlew test --tests 'com.faithlog.campus.*' --tests 'com.faithlog.admin.*'`: 47 tests 성공.
- `./gradlew test`: 320 tests / 0 failures / 0 errors / 1 skipped, `BUILD SUCCESSFUL`.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- 격리 Docker: PostgreSQL/Redis healthy, `/api/v1/health` `data.status=UP`, compose down 성공.

## 6. 고민한 부분

다른 도메인 통합 테스트가 `CampusService`를 fixture helper로 사용하므로 기능 파일을 삭제하지 않았다. 대신 façade에는 repository와 transaction을 두지 않고 새 Service proxy로 위임해 기존 내부 호출 호환과 실제 책임 분리를 함께 유지했다.

## 7. 트러블슈팅

- 문제: `pm-dev`의 `dev_gate.py`가 실행되지 않음.
- 원인: `python` 명령 부재 후 `python3`로 재실행했으나 저장소에 필수 harness 파일이 없음.
- 해결: 도구 게이트 실패를 숨기지 않고 코드 TDD/Gradle/Docker 검증과 분리해 기록. `score_code.py`는 `passed=false`, `review_gate.py`는 quality/TDD harness 부재 실패로 확인했다.
- 재발 방지: harness 도입 전에는 PM 보고에서 게이트 실패와 실제 코드 검증 결과를 별도로 표시.

## 8. 다음 작업

- [ ] PM 세션에서 커밋과 API/권한/트랜잭션 무변경 증거 재검증.
- [ ] GitHub 인증 복구 후 Project 카드를 Code Review로 이동.
- [ ] PM 승인 후 develop 대상 PR 생성.

## 9. Velog 글감

- 대형 Spring Application Service를 transaction/authorization 의미 변경 없이 유스케이스 Service로 분리한 방법.
