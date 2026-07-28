---
project: FaithLog
type: devlog
issue: "#206"
status: done
created: 2026-07-16
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #206 청구 항목 페이징 동률 정렬 안정화

## 1. 작업 배경

#193 current-develop before preflight에서 동일 `created_at`을 가진 청구가 안정적인 ID 순서 없이 반환됐다. offset paging 경계에서 중복 또는 누락이 발생할 수 있어 성능 측정을 중단하고 별도 이슈로 분리했다.

## 2. 최종 설계 기준

- 내 청구 목록과 관리자 회원별 청구 상세에만 적용한다.
- 기존 primary sort를 유지하고 같은 방향의 `id` secondary sort를 자동 추가한다.
- API path, query 형식, DTO, ErrorCode, Flyway, dependency는 변경하지 않는다.
- 관리자 회원 집계의 기존 정렬은 변경하지 않는다.

## 3. 구현 내용

- `BillingPageRequests.chargeItems()`가 검증된 primary order 뒤에 같은 방향의 `id` order를 추가한다.
- 모든 허용 primary property의 ASC/DESC를 단위 테스트로 고정했다.
- 동일 timestamp 두 행을 `size=1`로 조회해 두 공개 API의 페이지 순서와 무중복을 통합 테스트로 검증했다.
- REST Docs에 서버 내부 tie-break 동작을 명시했다.

## 4. TDD 기록

1. 실패 테스트 작성: 단위 계약과 동일 timestamp 페이지 경계 통합 계약을 추가했다.
2. 실패 확인: 신규 3 tests 중 1 pass / 2 failures. 기존 응답은 낮은 ID를 첫 페이지에 반환했다.
3. 최소 구현: primary sort 뒤 같은 방향의 `id` sort만 추가했다.
4. 테스트 통과: focused 및 전체 테스트가 통과했다.
5. 리팩토링: 공통 validator와 관리자 집계는 건드리지 않았다.

## 5. 테스트 결과

- `./gradlew test`: 88 suites / 555 tests / 0 failures / 0 errors / 3 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- REST Docs: 170 snippet groups, HTML 생성 확인

## 6. 프론트 영향

API path, query parameter, response shape가 유지되므로 production frontend API client/type/UI 수정은 없다. 다만 integration mock의 `getMockAdminMemberChargeState`, `getMockMemberChargeList`는 primary 방향과 무관하게 ID ASC tie-break를 사용하므로 DESC 계약에 맞춘 mock과 관련 테스트의 별도 최소 수정이 필요하다. 이 backend 세션에서는 frontend 파일을 편집하지 않았다.

## 7. 다음 작업

- [ ] PM 독립 리뷰 후 통합 브랜치에 반영
- [ ] 최신 develop 서버에서 #193 fresh before 측정 재개
