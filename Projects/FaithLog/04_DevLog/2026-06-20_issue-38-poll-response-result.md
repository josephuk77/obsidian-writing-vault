---
project: FaithLog
type: devlog
issue: "#38"
status: done
created: 2026-06-20
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #38 투표 응답과 결과 조회 구현

## 1. 작업 배경

캠퍼스 ACTIVE 멤버가 투표 목록/상세/결과를 조회하고, `optionIds` 기반으로 응답을 생성/수정하며, 관리자가 미참여자를 조회할 수 있게 구현했다. 투표 댓글 CRUD도 MVP 범위로 함께 구현했다.

## 2. 최종 설계 기준

- 투표 응답 요청은 `optionIds` 배열을 사용한다.
- 선택지는 `poll_response_options`에 저장한다.
- 익명 결과는 ADMIN 포함 누구에게도 응답자 식별 정보를 노출하지 않는다.
- 비익명 결과는 선택지별 응답자를 노출한다.
- 일반 사용자는 종료 후 3일, 관리자는 종료 후 7일까지만 지난 투표/상세/결과를 볼 수 있다.
- 댓글 작성/수정/삭제는 OPEN 투표에서만 가능하고, CLOSED 투표는 조회만 가능하다.
- 댓글 삭제는 soft delete로 처리한다.

## 3. 구현 내용

- Entity: `PollResponse`, `PollResponseOption`, `PollComment`
- Command/Result: `RespondToPollCommand`, `PollResponseResult`, `PollResultView`, `PollCommentResult` 등
- Service: `PollService` 응답/결과/목록/상세/미참여자/댓글 흐름 구현
- Repository: `PollResponseRepository`, `PollResponseOptionRepository`, `PollCommentRepository`
- Controller: `PollController`, `AdminPollController` missing-members endpoint
- Test: `PollServiceTest`, `PollApiRestDocsTest`

## 4. TDD 기록

1. 실패 테스트 작성: 응답 저장/수정, 검증 실패, 결과 privacy, visibility window, 미참여자, 댓글 권한/soft delete 테스트 추가.
2. 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.poll.application.PollServiceTest`가 #38 타입/메서드/error code 부재로 `compileTestJava` 실패.
3. 최소 구현: Entity, repository, service command/result, service 메서드, controller/DTO 추가.
4. 테스트 통과: poll service + REST Docs 대상 테스트 성공.
5. 리팩토링: 댓글 조회 visibility window 적용, CLOSED 투표 댓글 수정/삭제 차단 보강.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`, 155 tests / 0 failures / 0 errors / 0 skipped

추가 검증:

- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- `docker compose build app`: 성공
- `docker compose up -d`: 성공
- 컨테이너 내부 `GET /actuator/health`: `{"status":"UP"}`

## 6. 고민한 부분

- 에러 코드는 PM 승인 계약에 맞춰 poll 도메인 prefix 세부 코드로 분리했다.
- 익명 결과는 내부적으로 `poll_responses.user_id`를 저장하되 응답 DTO에서 식별 정보를 완전히 비웠다.
- 댓글은 익명 투표에서도 익명 처리하지 않는 MVP 기준을 따랐다.

## 7. 트러블슈팅

- 문제: 최초 `./gradlew asciidoctor`가 Gradle wrapper lock 파일 권한 문제로 실패.
- 원인: Codex sandbox가 `~/.gradle` lock 파일 접근을 제한.
- 해결: 동일 명령을 승인된 escalation으로 재실행해 성공.
- 재발 방지: asciidoctor 검증에서 wrapper lock 권한 오류가 나오면 동일 명령 escalation 필요.

### PM 검토 후속 수정

- 문제: `RespondToPollRequest.optionIds`의 `@NotEmpty`가 빈 배열을 전역 검증 에러로 처리해 #38 `POLL_RESPONSE_INVALID_SELECTION_COUNT` 계약을 우회할 수 있었다.
- 해결: DTO 검증을 제거하고 service validation에서 빈 배열과 누락값을 처리하도록 수정했다. REST Docs 에러 테스트를 추가했다.
- 문제: `SCHEDULED` 투표가 `endsAt` 전이면 응답/댓글 작성과 목록/상세 노출이 가능했다.
- 해결: write는 `OPEN`이고 `startsAt <= now <= endsAt`인 경우만 허용하고, member list/detail은 진행 중 OPEN 또는 visibility window 안의 지난 투표만 노출하도록 보정했다.
- 문제: 기존 응답을 같은 선택지로 재저장할 때 delete/insert flush 순서에 따라 `(response_id, option_id)` unique 충돌이 발생할 수 있었다.
- 해결: response option 삭제를 JPQL bulk delete로 바꿔 재저장 전 기존 row를 먼저 제거했다.

## 8. 다음 작업

- [ ] #39 커피 투표 응답 시 COFFEE 청구 자동 생성/갱신
- [ ] Flyway 도입 시 #38 테이블/unique 제약 migration 반영

## 9. Velog 글감

- 익명 투표 결과에서 내부 식별자 저장과 API privacy를 분리한 설계
