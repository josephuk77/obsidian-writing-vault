---
project: FaithLog
type: devlog
issue: "#79"
status: done
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - performance
---

# #79 [Perf] 투표 목록 조회 응답 여부 N+1 쿼리 개선

## 1. 작업 배경

`PollService.listPolls`가 투표 목록 조회 후 각 poll마다 현재 사용자의 응답 여부를 `findByPollIdAndUserId`로 개별 조회해 poll 수에 비례한 추가 repository 호출이 발생할 수 있었다.

## 2. 최종 설계 기준

- API 경로, request/response 계약, 권한 정책은 변경하지 않는다.
- 진행 중/지난 투표 노출 정책과 일반 사용자 3일, 관리자 7일 공개 기간 정책을 유지한다.
- 현재 로그인 사용자의 응답 여부만 bulk 조회로 계산한다.

## 3. 구현 내용

- Repository: `PollResponseRepository.findByPollIdInAndUserId(Collection<Long> pollIds, Long userId)` 추가.
- Service: visible poll ID 목록으로 현재 사용자 응답을 1회 조회하고 `respondedPollIds` set으로 `PollListItemResult.responded` 계산.
- Test: 여러 poll 목록에서 응답 여부 정확도와 기존 per-poll `findByPollIdAndUserId` 미호출을 검증.

## 4. TDD 기록

1. 실패 테스트 작성: `poll_list_marks_current_user_responses_without_per_poll_response_lookup`
2. 실패 확인: 구현 전 `NeverWantedButInvoked`로 기존 단건 조회 호출 확인
3. 최소 구현: pollIds 기반 bulk 조회 메서드와 set 매핑 추가
4. 테스트 통과: 신규 단일 테스트와 poll 패키지 테스트 통과
5. 리팩토링: 새 테스트 spy annotation을 `@MockitoSpyBean`으로 조정해 신규 deprecation warning 방지

## 5. 테스트 결과

- `./gradlew test --tests 'com.faithlog.poll.application.PollServiceTest.poll_list_marks_current_user_responses_without_per_poll_response_lookup'`: 성공
- `./gradlew test --tests 'com.faithlog.poll.*'`: 성공
- `./gradlew test`: 성공, 236 tests / 0 failures / 0 errors / 0 skipped
- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- `docker compose up -d --build postgres redis app`: 성공
- 컨테이너 내부 `GET /api/v1/health`: `status=UP`
- `docker compose down`: 성공

## 6. 고민한 부분

Hibernate statistics 기반 query count 테스트 대신 기존 `@SpringBootTest` 구조에 맞춰 repository spy 호출 수 검증을 사용했다. 이슈에서 허용한 두 방식 중 코드베이스에 더 작은 변경으로 맞는 방식이었다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor` 첫 실행이 `~/.gradle` wrapper lock 권한 때문에 실패.
- 원인: Codex sandbox가 workspace 외부 Gradle lock 파일 쓰기를 차단.
- 해결: 권한 상승으로 동일 명령 재실행해 성공.
- 재발 방지: wrapper lock 접근이 필요한 Gradle 명령은 동일 증상 발생 시 권한 상승 재실행한다.

## 8. 다음 작업

- [ ] 운영 환경에서 실제 poll 목록 크기 기준 query/time 계측이 필요하면 별도 성능 측정 이슈로 분리한다.

## 9. Velog 글감

- Spring Data JPA 목록 API에서 boolean flag 계산 N+1을 bulk lookup과 set mapping으로 줄이는 방법.
