---
project: FaithLog
type: devlog
issue: "#188"
status: review
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - excel
  - rest-docs
---

# #188 관리자 주차별 사용자 경건과 벌금 조회 및 Excel 다운로드

## 1. 작업 배경

관리자가 캠퍼스 ACTIVE 멤버의 주차별 경건 제출 현황과 실제 저장된 벌금을 한 화면에서 조회하고 같은 기준의 XLSX를 내려받도록 구현했다. 과거 벌금을 현재 규칙으로 재계산하지 않고 `charge_items`의 실제 청구를 사용한다.

## 2. 최종 설계 기준

- JSON: `GET /api/v1/admin/campuses/{campusId}/devotions/weeks/{weekStartDate}/members`
- Excel: `GET /api/v1/admin/campuses/{campusId}/devotions/weeks/{weekStartDate}/export`
- service `ADMIN` 또는 해당 캠퍼스 ACTIVE `MINISTER`, `ELDER`, `CAMPUS_LEADER`만 허용
- `weekStartDate`는 월요일만 허용
- 현재 ACTIVE 멤버만 포함하고 캠퍼스 간 데이터를 섞지 않음
- 제출자와 미제출자를 분리하고 미제출자를 하단에 배치
- 실제 `PENALTY` charge id/amount/status 표시
- 사용자 확정: `totalPenaltyAmount = PAID + UNPAID`; `WAIVED/CANCELED`는 행에는 보이되 합계 제외
- JSON과 Excel은 동일 query result 사용
- Entity/DB/Flyway/ErrorCode/기존 경건 제출·벌금 생성·납부·정산 계약 변경 없음

## 3. 구현 내용

- Query service: read-only transaction에서 권한과 campus scope를 검증한 뒤 ACTIVE members, users, weekly records, daily checks, charges를 bulk 조회
- Repository: `PENALTY + DEVOTION_RECORD + sourceId IN` bulk query 추가
- Response: 제출자의 주간 count, 토요일 지각, 제출 시각, 실제 charge, 월~일 7일 체크와 별도 미제출 목록
- Excel renderer: `주간 요약`, `일별 상세` 두 시트. 제출자 우선, 미제출자 하단 별도 구역
- HTTP: XLSX MIME과 `faithlog-devotion-{campusId}-{weekStartDate}.xlsx` filename 고정
- Dependency: direct `org.apache.poi:poi-ooxml:5.5.1` 1개 추가
- REST Docs: JSON 전체 fields, Excel response headers, index include와 include 회귀 테스트

## 4. TDD 기록

1. JSON controller test 선작성: endpoint 부재로 3 tests가 expected 200/actual 404
2. 최소 query/API 구현 후 JSON·bulk·structure focused GREEN
3. Excel workbook 계약 test 선작성: export endpoint 부재로 404
4. renderer/controller/POI 추가 후 2 sheets/header/order/value/MIME/filename GREEN
5. REST Docs index test 선작성: 신규 include 누락 assertion failure
6. JSON/Excel snippets와 `index.adoc` 연결 후 GREEN

## 5. 테스트 결과

- Devotion/Billing/Admin focused: 82 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 420 tests / 0 failures / 0 errors / 3 skipped
- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- `git diff --check`: 성공
- test source: 81개
- REST Docs snippet groups: 126개

## 6. 쿼리와 회귀 방지

멤버 수와 무관하게 ACTIVE members, user profiles, weekly records, daily checks, charges를 각각 bulk 호출한다. 단위 테스트가 주요 repository/port 호출을 각 1회로 고정하고 개별 멤버 조회가 생기지 않도록 회귀를 막는다. 일별 row가 없는 제출자는 월요일부터 일요일까지 false 기본값 7개를 응답에서만 합성한다.

## 7. Docker 이관과 관찰 기록

최신 사용자 결정으로 feature 세션에서는 Docker build/up/API QA를 실행하지 않는다. #188/#189/#190 finding 0 이후 최신 `origin/develop`에서 만든 `integration/188-190-devotion-meal-billing`에서 PostgreSQL/Redis/backend와 세 기능 연결 QA를 한 번 수행한다.

결정 전 시도에서는 공개 image pull과 Docker 내부 `bootJar` 4분 38초 성공 뒤 overlay2/containerd `input/output error`가 발생했고 host available space가 561MiB였다. 이 관찰은 사실로 남기되 #188 feature 완료 blocker로 보지 않는다. 임의 파일 삭제, Docker 데이터 삭제, `down -v`, named volume 삭제, system/image/volume prune은 수행하지 않았다.

## 8. 트러블슈팅

- 문제: Gradle workspace metadata/daemon registry read 오류 1회와 Excel autosize 실행 지연
- 해결: cache 삭제 없이 daemon stop/retry, Excel fixed column width 사용
- 문제: Docker Desktop overlay2/containerd I/O 오류와 low disk
- 처리: 파괴적 복구 없이 중단하고 Docker QA를 승인된 integration 단계로 이관

## 9. 다음 작업

- [ ] PM `origin/develop...HEAD` 독립 코드리뷰 finding 0 확인
- [ ] #188/#189/#190 승인 후 integration branch 병합
- [ ] integration branch에서 Docker health와 세 기능 실제 API 연결 QA
- [ ] integration compose down 후 마지막 Docker 명령 `docker builder prune -f`

## 10. 이력서 문장 후보

관리자 주차별 경건·실제 벌금 조회와 2-sheet XLSX export를 동일 bulk query model로 구현해 campus 격리와 N+1 회귀를 고정하고, 82개 focused·420개 전체 테스트와 REST Docs 126개 스니펫 기준으로 권한·집계·파일 계약을 검증했다.

## 11. PM 1차 finding 대응

- 벌금 합계 정책은 개발 세션에서 사용자가 “각자 주차별이 페이드랑 언페이드랑 합산할게”라고 직접 답해 `UNPAID + PAID`를 승인한 근거를 재확인했다. 기능 코드는 유지하고 저장소 decision log에 이 명시적 근거를 추가했다.
- `AGENTS.md`와 Codex Hook에 일회성 #188/#189/#190 번호, 통합 브랜치명, Docker 순서를 하드코딩했던 범위를 수정했다. 전역 문서에는 PM 전체 diff 리뷰와 finding 재검증이라는 일반 완료 게이트만 두고, 이번 통합 절차는 저장소 decision log에만 유지했다.
