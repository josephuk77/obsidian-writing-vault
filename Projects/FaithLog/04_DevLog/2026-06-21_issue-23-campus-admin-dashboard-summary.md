---
project: FaithLog
type: devlog
issue: "#23"
status: done
created: 2026-06-21
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #23 캠퍼스 관리자 대시보드 통합 조회 API

## 1. 작업 배경

캠퍼스 내부 관리자 홈에서 구성원, 경건생활, 미납 청구, 투표 상태를 한 번에 조회하는 요약 API가 필요했다. #23은 서비스 전역 ADMIN 유저/캠퍼스 관리 API가 아니라 캠퍼스 내부 관리자 대시보드 API로 범위를 분리했다.

## 2. 최종 설계 기준

- API: `GET /api/v1/admin/campuses/{campusId}/dashboard/summary`
- `weekStartDate`는 선택 query parameter이며, 생략 시 서버가 `Asia/Seoul` 기준 현재 주 월요일을 계산한다.
- 권한은 `users.role = MANAGER`가 아니라 `campus_members.campus_role` 기준이다.
- 서비스 전역 `ADMIN`은 모든 캠퍼스 접근 가능, 캠퍼스 `ACTIVE + MINISTER/ELDER/CAMPUS_LEADER`는 자기 캠퍼스 접근 가능, `MEMBER`/다른 캠퍼스 관리자/전역 `MANAGER` 단독은 접근 불가다.
- 상세 목록 API는 #31/#36/#38/#40 범위로 두고 #23은 숫자 요약만 반환한다.

## 3. 구현 내용

- Entity: 새 Entity 없음
- Command: query parameter `weekStartDate` 직접 사용
- Service: `AdminDashboardService`
- Repository: 기존 JPA repository에 대시보드 집계용 조회 method 추가
- Controller: `AdminDashboardController`
- Test: `AdminDashboardControllerTest`, `AdminDashboardApiRestDocsTest`

## 4. TDD 기록

1. 실패 테스트 작성: 권한 matrix, weekStartDate 기본/성공/실패, 전체 집계 응답 테스트를 먼저 작성했다.
2. 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.admin.presentation.AdminDashboardControllerTest`가 신규 endpoint 부재로 3 tests failed.
3. 최소 구현: 대시보드 전용 service/controller/response DTO와 repository method를 추가했다.
4. 테스트 통과: dashboard controller/REST Docs 테스트 통과.
5. 리팩토링: ACTIVE 멤버가 0명일 때 poll response `IN ()` 쿼리 의존이 생기지 않도록 방어했다.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 228 tests / 0 failures / 0 errors / 0 skipped

추가 검증:

- `./gradlew build` 성공
- `./gradlew asciidoctor` 성공
- `docker compose up -d --build postgres redis app` 성공
- Docker `GET /actuator/health` 200 / `{"status":"UP"}` 확인
- 실제 API QA로 summary 집계, service ADMIN 200, MEMBER/다른 캠퍼스 관리자/전역 MANAGER 단독 403, non-Monday 400 확인

## 6. 고민한 부분

대시보드 집계는 기존 상세 API를 재구현하지 않고, 화면 첫 진입에 필요한 숫자만 반환하도록 제한했다. `charges.byCategory`는 클라이언트가 두 카테고리를 안정적으로 렌더링할 수 있게 `PENALTY`, `COFFEE`를 항상 순서대로 반환한다.

## 7. 트러블슈팅

- 문제: Docker QA 첫 fixture 스크립트에서 SQL 블록이 적용되지 않아 summary assertion이 실패했다.
- 원인: API로 만든 기본 캠퍼스/멤버십은 존재했지만, 집계용 weekly/charge/poll fixture가 DB에 반영되지 않았다.
- 해결: SQL fixture 적용을 별도 `docker exec -i faithlog-postgres psql` 명령으로 분리해 반영하고 응답을 재검증했다.
- 재발 방지: Docker QA에서 fixture 적용 후 row count 또는 실제 응답을 먼저 출력/확인한다.

## 8. 다음 작업

- [ ] PM 검증 후 PR 생성

## 9. Velog 글감

- 캠퍼스 내부 권한과 서비스 전역 권한을 분리한 관리자 대시보드 API 설계
