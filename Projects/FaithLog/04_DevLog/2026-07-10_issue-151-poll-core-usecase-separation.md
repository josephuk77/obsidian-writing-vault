---
project: FaithLog
type: devlog
issue: #151
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #151 Poll 핵심 유스케이스 책임 분리

## 1. 작업 배경

`PollService` 578줄이 생성, 시간 상태 동기화, 관리자 종료와 커피 정산, 응답, 목록/상세/결과/미응답자, 댓글, 사용자 선택지 추가를 함께 소유해 유스케이스 경계가 불분명했다. 기능 계약을 바꾸지 않고 책임과 트랜잭션 소유자를 분리했다.

## 2. 최종 설계 기준

- 13개 public 유스케이스를 8개 전용 Service로 분리한다.
- 각 moved public method가 기존 `@Transactional` 또는 `@Transactional(readOnly = true)`를 직접 소유한다.
- Controller는 전용 Service를 직접 호출한다.
- `PollService`는 repository, transaction, 예외, 업무 규칙이 없는 호환 delegate로만 유지한다.
- PollTemplate, Coffee settlement, Scheduler/Batch 책임은 재설계하지 않는다.

## 3. 구현 내용

- Command: `PollCreationCommandService`, `PollStatusCommandService`, `PollResponseCommandService`, `PollCommentCommandService`, `PollUserOptionCommandService`
- Query: `PollQueryService`, `PollResultQueryService`, `PollCommentQueryService`
- 공통 helper: `PollStatusSynchronizer`, `PollLookupSupport`, `PollResultAssembler`
- Controller: `PollController`, `AdminPollController`를 전용 Service에 직접 연결
- 호환 facade: `PollService`를 578줄에서 103줄 delegate로 축소
- Test: `PollUseCaseServiceStructureTest` 5건 추가

## 4. TDD 기록

1. 실패 테스트 작성: 전용 책임, 직접 transaction, Controller 연결, 얇은 facade, 전용 서비스 간 의존 금지 구조 검사
2. 실패 확인: 5 tests / 5 failures
3. 최소 구현: 기존 public/private 코드를 검증·repository 호출 순서 그대로 전용 Service와 package-private helper로 이동
4. 테스트 통과: 구조 테스트와 Poll focused service/REST Docs/Batch GREEN
5. 리팩토링: 전체 구조 검사에서 `PollLookupPolicy` 이름의 책임 패키지 위반 1건을 확인해 `PollLookupSupport`로 이름만 수정

## 5. 테스트 결과

- Poll focused service/Controller/REST Docs/Batch: BUILD SUCCESSFUL
- #165 원본 Billing/Devotion/Poll/Batch 조합: 197 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 343 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- 격리 Docker QA: image build 성공, PostgreSQL/Redis healthy, backend `data.status=UP`, volume 삭제 없는 compose down 성공
- Docker build cache 정리: `docker builder prune -f`, 696.1MB

## 6. 고민한 부분

시간 기준 OPEN 동기화와 공개 기간은 목록, 상세, 결과, 댓글 조회와 여러 write 경계가 실제로 공유한다. 전용 Service끼리 의존시키면 결합 방향이 복잡해지므로 package-private helper로 분리하되, transaction은 public 유스케이스 Service에 유지했다.

## 7. 트러블슈팅

- 문제: 첫 전체 테스트에서 `DomainPackageStructureTest` 1건 실패
- 원인: `PollLookupPolicy`가 `service/policy`가 아닌 `service`에 있어 기존 파일명 책임 규칙 위반
- 해결: 업무 동작을 바꾸지 않고 helper 이름을 `PollLookupSupport`로 변경
- 재발 방지: 전체 구조 테스트와 Poll 구조 테스트를 함께 실행

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정

## 9. Velog 글감

- 거대 Spring Application Service를 transaction과 호출 순서 변경 없이 유스케이스별로 분리하는 방법
