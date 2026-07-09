---
project: FaithLog
type: devlog
issue: #142
status: done
created: 2026-07-09
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - poll
---

# #142 [Fix] 투표 조회 상태 시간 동기화

## 1. 작업 배경

운영 API에서 `starts_at <= now < ends_at`인 투표가 DB에는 존재하지만 `status = SCHEDULED`로 남아 있어 사용자 투표 목록, 상세, 응답 저장 전 open 검증에서 숨겨지거나 거부되는 문제가 있었다.

## 2. 최종 설계 기준

- DB `timestamptz`/UTC 저장은 정상이며 KST 저장 방식으로 바꾸지 않는다.
- 비교는 `Instant`/UTC 기준으로 처리한다.
- `SCHEDULED && startsAt <= now < endsAt`인 투표만 조회/응답 경계에서 `OPEN`으로 동기화한다.
- path `campusId` 범위 안의 투표만 동기화한다.
- 종료된 투표를 조회 시점에 `CLOSED`로 저장하지 않고, 커피 정산/알림 같은 close side effect를 호출하지 않는다.

## 3. 구현 내용

- Entity: `Poll.open()` 기존 도메인 메서드만 사용.
- Command: 변경 없음.
- Service: `PollService`에 현재 기간 예약 투표를 여는 동기화 메서드를 추가하고 목록/상세/결과/댓글 목록 조회 및 응답/댓글/사용자 옵션 open 검증 전에 적용.
- Repository: 변경 없음.
- Controller: 변경 없음.
- Test: `PollServiceTest.current_scheduled_poll_opens_on_member_list_detail_and_response_with_campus_scope` 추가.

## 4. TDD 기록

1. 실패 테스트 작성: 현재 기간 `SCHEDULED` poll, 시작 전 예약 poll, 3일 이내 종료 poll, 다른 캠퍼스 current poll을 함께 구성.
2. 실패 확인: `./gradlew test --tests com.faithlog.poll.application.PollServiceTest`가 새 목록 assertion에서 실패.
3. 최소 구현: campus scope로 읽은 poll에 대해서만 `SCHEDULED && startsAt <= now < endsAt`이면 `poll.open()` 수행.
4. 테스트 통과: focused PollService 테스트 성공.
5. 리팩토링: stream `peek` side effect를 명시적 `forEach` 동기화로 정리.

## 5. 테스트 결과

명령:

`./gradlew test --tests com.faithlog.poll.application.PollServiceTest`

결과:

`BUILD SUCCESSFUL`

추가 명령:

`./gradlew test --tests com.faithlog.poll.presentation.PollApiRestDocsTest`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

- 조회 메서드는 기존에 `readOnly = true`였기 때문에 동기화 mutation이 유실되지 않도록 write transaction으로 바꿨다.
- `now == endsAt`은 요구사항의 `now < endsAt`에 맞춰 open 가능 시간에서 제외했다.
- 자동 `CLOSED` 저장은 커피 정산 경계를 깨뜨릴 수 있어 추가하지 않았다.

## 7. 트러블슈팅

- 문제: 현재 기간 `SCHEDULED` poll이 목록에 포함되지 않았다.
- 원인: `isVisibleInWindow`와 `requireOpenPoll`이 상태 `OPEN`을 먼저 요구했다.
- 해결: campus-scoped lookup 뒤 현재 기간 예약 poll만 `OPEN`으로 동기화.
- 재발 방지: 목록/상세/응답/캠퍼스 scope/미래 예약/마감 응답 거부를 한 테스트에서 회귀 검증.

## 8. 다음 작업

- [ ] PM 검증 후 전체 테스트/build/Docker QA 결과를 최종 확인한다.

## 9. Velog 글감

- 조회 경계에서 side effect 없는 상태 동기화와 도메인 이벤트/정산 경계 분리
