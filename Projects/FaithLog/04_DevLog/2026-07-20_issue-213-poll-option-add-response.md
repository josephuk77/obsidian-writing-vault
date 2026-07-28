---
project: FaithLog
type: devlog
issue: "#213"
status: done
created: 2026-07-20
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #213 투표 조회 응답에 사용자 항목 추가 허용 여부 노출

## 1. 작업 배경

투표에는 `allowUserOptionAdd` 설정이 저장되고 생성 응답에도 포함됐지만, 일반 투표 목록과 상세 조회 응답에서는 누락되어 프론트가 사용자 선택지 추가 UI를 제어할 수 없었다.

## 2. 최종 설계 기준

- 목록의 각 투표와 상세 응답에 저장된 `allowUserOptionAdd` boolean을 필수로 반환한다.
- 누락값을 프론트가 추론하지 않는다.
- 기존 ACTIVE 멤버, OPEN 상태, 활성 시간 구간 검증은 서버가 유지한다.
- API 경로, 요청 DTO, 권한, ErrorCode, Entity, DB/Flyway는 변경하지 않는다.

## 3. 구현 내용

- `PollListItemResult`에 엔티티 설정값을 전달했다.
- `PollListResponse`와 `PollDetailResponse`에 `allowUserOptionAdd`를 추가했다.
- REST Docs 목록·상세 응답 필드와 API 설명을 갱신했다.

## 4. TDD 기록

1. 기본 `false` 투표와 명시적 `true` 투표의 목록·상세 HTTP 응답 계약을 먼저 추가했다.
2. 필드 누락으로 focused 2/2 실패를 확인했다.
3. 결과/DTO 매핑만 최소 구현했다.
4. focused 테스트와 전체 회귀 테스트를 통과했다.

## 5. 테스트 결과

- Focused: 2/2 PASS
- 전체: 574 tests, failures/errors 0
- `./gradlew test build asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: PASS

## 6. 영향 범위

- 프론트는 조회 응답의 `allowUserOptionAdd`를 사용해 선택지 추가 UI를 제어할 수 있다.
- Flyway, DB schema, 권한, 투표 상태 변경 로직에는 영향이 없다.

