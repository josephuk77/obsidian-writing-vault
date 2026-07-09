---
project: FaithLog
type: devlog
issue: #31
status: done
created: 2026-06-19
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #31 주간 경건생활 제출과 일별 체크 구현

## 1. 작업 배경

사용자가 캠퍼스별 하루 경건생활을 체크하고, 주간 화면에서 저장/제출한 뒤 본인 주간 기록과 관리자 미제출자 목록을 조회할 수 있도록 구현했다.

## 2. 최종 설계 기준

- 경건생활 원본은 `devotion_daily_checks`.
- `weekly_devotion_records`는 제출 여부, 주간 요약, 이후 벌금 계산 기준.
- 하루 체크는 daily row와 weekly row를 생성/수정하지만 `submittedAt`과 청구를 변경하지 않는다.
- 주간 PUT은 월요일부터 일요일까지 7일치 daily row를 생성/수정하고, 요청 누락 날짜는 false로 채운다.
- #31에서 월간 통계는 제외한다. 월간 통계는 #57 범위다.
- #31에서 실제 `PENALTY charge_items` 생성/갱신은 제외한다. 실제 연결은 #33 범위다.

## 3. 구현 내용

- Entity: `WeeklyDevotionRecord`, `DevotionDailyCheck`
- Command/Result: 일별/주간 update command, 본인 조회 query, 관리자 미제출자 query, response result records
- Service: `DevotionService`
- Repository: `WeeklyDevotionRecordRepository`, `DevotionDailyCheckRepository`
- Controller: `DevotionController`, `AdminDevotionController`
- Test: `DevotionServiceTest`, `DevotionControllerTest`, `DevotionApiRestDocsTest`

## 4. TDD 기록

1. 실패 테스트 작성: 일별 체크, 주간 제출, 본인 조회, 관리자 미제출자 조회, 권한/월요일 검증 테스트 추가.
2. 실패 확인: `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest`가 devotion 클래스 부재로 `compileTestJava` 실패.
3. 최소 구현: devotion Entity, Repository, Application Service, Controller, DTO 추가.
4. 테스트 통과: #31 서비스/컨트롤러/REST Docs 테스트 통과.
5. 리팩토링: REST Docs descriptor와 Asciidoc index를 보강해 문서 렌더 검증까지 통과.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`, 92 tests / 0 failures / 0 errors / 0 skipped

추가 명령:

`./gradlew asciidoctor`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

- Notion 일부 상세 문서에는 주간 제출 시 `PENALTY` 청구 생성까지 포함되어 있었지만, 최신 사용자 결정과 `docs/decision-log.md` 기준으로 #31에서는 실제 청구 생성을 제외했다.
- 관리자 미제출자 조회 기준은 daily row가 아니라 `weekly_devotion_records.submitted_at`으로 고정했다.

## 7. 트러블슈팅

- 문제: `asciidoctor` 최초 실행이 Gradle wrapper lock 권한 문제로 실패.
- 원인: sandbox가 사용자 홈 디렉터리의 `.gradle` lock 파일 생성을 제한.
- 해결: 권한 상승으로 같은 명령을 재실행해 성공.
- 재발 방지: Gradle wrapper가 홈 디렉터리 cache/lock을 쓰는 명령은 같은 증상이 반복될 수 있음을 최종 보고에 남긴다.

## 8. 다음 작업

- [ ] #33에서 주간 제출 결과를 실제 `PENALTY charge_items` 생성/갱신 흐름과 연결
- [ ] #57에서 월간 경건생활 통계 API 별도 구현

## 9. Velog 글감

- 주간 제출과 일별 체크를 분리하면서 제출 기준을 `submittedAt`으로 안정화한 TDD 사례
