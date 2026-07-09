---
project: FaithLog
type: devlog
issue: '#106'
status: done
created: 2026-06-30
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #106 기도 운영 기간과 기도조 관리 조회 API 보강

## 1. 작업 배경

기도제목 운영 기간과 기도조 관리 화면에 필요한 현재 운영 기간, 시즌별 조 목록, 배정 가능 멤버, 본인 기도제목 저장 API를 보강했다.

## 2. 최종 설계 기준

- 현재 운영 기간은 `status = ACTIVE`와 `endDate = null`을 함께 만족해야 한다.
- 닫힌 season은 active 조회와 주간 board에서 제외한다.
- 같은 season 안에서 한 userId는 하나의 active prayer group에만 배정 가능하다.
- 일반 ACTIVE 멤버의 editable은 본인 현재 조의 본인 항목만 true다.
- `/me` 저장은 본인 submission만 생성/수정하고 보강된 weekly board 응답을 반환한다.

## 3. 구현 내용

- Service: current season, season groups, assignable members, duplicate active group assignment validation, enhanced weekly board, save-my-submission use case 추가.
- Controller: admin current/groups/assignable endpoints와 member `/me` endpoint 추가.
- DTO/Result: currentSeason, myGroupId, group seasonId, submitted, editable, member email, assignable member response 추가.
- ErrorCode: `PRAYER_GROUP_MEMBER_ALREADY_ASSIGNED`, `PRAYER_GROUP_ASSIGNMENT_REQUIRED` 추가.
- REST Docs: 신규 snippets와 `src/docs/asciidoc/index.adoc` Prayer 섹션 갱신.

## 4. TDD 기록

1. 실패 테스트 작성: `PrayerServiceTest`에 current season, groups, assignable members, duplicate assignment, weekly board, `/me` save 테스트를 먼저 추가.
2. 실패 확인: `./gradlew test --tests com.faithlog.prayer.application.PrayerServiceTest`에서 신규 메서드/result/command/ErrorCode 부재로 `compileTestJava` 27 errors 확인.
3. 최소 구현: service/repository/result/controller/DTO/ErrorCode 추가.
4. 테스트 통과: focused service/docs 테스트와 prayer package 테스트 통과.
5. 리팩토링: 기존 replace-members 테스트를 새 중복 배정 정책에 맞게 조정하고 문서 필드를 보강.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 267 tests / 0 failures / 0 errors / 1 skipped

추가 검증:

- `./gradlew build` 성공
- `./gradlew asciidoctor` 성공
- `git diff --check` 성공

## 6. 고민한 부분

`/me` 저장 요청은 사용자 승인 계약대로 `content`만 받도록 구현했다. 기존 submission row의 `version`은 weekly board 응답에 유지하되, `/me` 저장 요청에는 version을 요구하지 않았다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor` 최초 실행이 `~/.gradle` lock 파일 접근 권한 때문에 실패.
- 원인: workspace sandbox 밖의 Gradle wrapper cache lock 파일 접근 제한.
- 해결: 동일 명령을 승인 요청으로 재실행해 성공.
- 재발 방지: Gradle wrapper가 홈 디렉터리 cache/lock을 접근하는 문서 빌드 명령은 sandbox 실패 시 승인 후 재실행한다.

## 8. 다음 작업

- [ ] PM 검증 후 PR 생성
- [ ] 필요 시 Docker/API QA 수행

## 9. Velog 글감

- 운영 기간 기반 그룹 board API에서 현재 상태와 편집 권한을 서버가 계산한 사례
