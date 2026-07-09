---
project: FaithLog
type: devlog
issue: "#57"
status: done
created: 2026-06-19
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #57 내 월간 경건생활 통계 조회 구현

## 1. 작업 배경

Notion 10.5 기준의 내 월간 경건생활 통계 조회 API를 #57 범위로 분리해 구현했다. #31의 하루 체크/주간 제출, #32의 벌금 규칙/계산, #33의 벌금 청구 자동 생성은 변경하지 않았다.

## 2. 최종 설계 기준

- API: `GET /api/v1/campuses/{campusId}/devotions/me/monthly-summary?year={year}&month={month}`
- 현재 로그인한 사용자 본인 데이터만 조회한다.
- 조회 전 해당 캠퍼스의 ACTIVE 멤버십을 검증한다.
- 신규 월간 통계 테이블은 만들지 않는다.
- 월간 합계는 선택 월의 첫날부터 마지막 날까지 `devotion_daily_checks.record_date` 기준으로 계산한다.
- 월 경계 주차는 선택 월에 포함되는 날짜만 부분 집계한다.
- `SATURDAY_LATE` 지각 시간은 해당 주차의 토요일 날짜가 선택 월에 포함될 때만 월 통계에 포함한다.

## 3. 구현 내용

- Entity: 기존 `WeeklyDevotionRecord`, `DevotionDailyCheck`, `Campus`, `CampusMember`, `User` 구조 사용.
- Query: `GetMyMonthlyDevotionSummaryQuery`.
- Service: `DevotionMonthlySummaryQueryService`를 읽기 전용 query service로 추가.
- Repository: 월과 겹치는 weekly record 조회, 선택 월 안의 daily check 조회 query method 추가.
- Controller: `DevotionController`에 `/monthly-summary` GET endpoint 추가.
- DTO: `MyMonthlyDevotionSummaryResult`, `MyMonthlyDevotionSummaryResponse`.
- Test: 서비스, 컨트롤러, REST Docs 테스트에 월 경계 부분 집계와 오류 계약 검증 추가.

## 4. TDD 기록

1. 실패 테스트 작성: 월 경계 주차 부분 집계, 토요일 지각 월 귀속, 본인 데이터 조회, ACTIVE 멤버십 검증, `year/month` 검증, REST Docs 계약 테스트를 먼저 작성.
2. 실패 확인: 구현 전 대상 테스트 묶음이 `DevotionMonthlySummaryQueryService`, `GetMyMonthlyDevotionSummaryQuery`, `MyMonthlyDevotionSummaryResult`, `DEVOTION_INVALID_YEAR_MONTH` 부재로 `compileTestJava` 실패.
3. 최소 구현: query service/result/response DTO, repository query method, controller endpoint, devotion domain error code를 추가.
4. 테스트 통과: #57 대상 테스트 묶음 성공.
5. 리팩토링: 월간 집계 책임을 Controller가 아닌 query service에 유지해 응답 변환과 계산 책임을 분리했다.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 130 tests / 0 failures / 0 errors / 0 skipped

추가 확인:

- `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`
- `./gradlew build`
- `./gradlew asciidoctor`
- `docker compose up -d --build postgres redis app`
- 앱 컨테이너 내부 `GET /api/v1/health` 응답 `status=UP`
- `docker compose down`

## 6. 고민한 부분

월간 통계는 저장 테이블을 새로 만들지 않고 기존 weekly/daily 원본을 읽어 계산했다. 토요일 지각 시간은 daily row 날짜 기준이 아니라 weekly record의 토요일 날짜 기준이므로, 일별 체크 카운트 계산과 별도 함수로 분리했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor` 첫 실행이 Gradle wrapper lock 파일 권한 문제로 실패했다.
- 원인: 샌드박스가 `~/.gradle/wrapper/dists/...zip.lck` 접근을 막았다.
- 해결: 동일 명령을 권한 승인으로 재실행해 성공시켰다.
- 재발 방지: asciidoctor 검증에서 같은 lock 권한 오류가 나오면 샌드박스 이슈로 기록하고 같은 명령을 승인 경로로 재실행한다.

## 8. 다음 작업

- [ ] PM 세션에서 #57 검증 후 PR 생성 여부를 결정한다.

## 9. Velog 글감

- 월 경계 주간 데이터를 날짜 기준으로 부분 집계하는 API 설계
- Controller를 얇게 유지하면서 Spring REST Docs로 계약을 고정하는 TDD 흐름
