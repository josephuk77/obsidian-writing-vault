---
project: FaithLog
type: devlog
issue: "#55"
status: done
created: 2026-06-19
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #55 공통 에러 코드와 요청 검증 구조 정리

## 1. 작업 배경

#36 청구 조회 구현 이후 broad error code와 요청 검증 로직이 여러 계층에 흩어져 있어, `HTTP status + 세부 code`를 고정 API 계약으로 삼는 리팩토링을 진행했다.

## 2. 최종 설계 기준

- 글로벌 `ErrorCode` enum 하나를 유지하되 `AUTH_*`, `CAMPUS_*`, `BILLING_*`, `GLOBAL_*` prefix로 세분화한다.
- `page`, `size`, `sort`는 잘못된 값이면 자동 보정하지 않고 `400`을 반환한다.
- Bean Validation 실패는 `GLOBAL_VALIDATION_FAILED`로 응답한다.
- 정렬/페이지 파싱은 공통 요청 검증 컴포넌트로 분리한다.
- 비즈니스 규칙은 정책 클래스로 분리한다.

## 3. 구현 내용

- Global: 세부 `ErrorCode`, `GlobalExceptionHandler`, `RestAuthenticationEntryPoint` 정리
- Request validation: `PageSortRequestValidator` 추가
- Policy: `CampusRolePolicy`, `BillingAccessPolicy`, `ChargeStatusPolicy` 추가
- Billing/Campus/Auth: broad code와 하드코딩 예외 호출부 정리
- Git hook: `.githooks/commit-msg` 추가 및 커밋 메시지 형식 검증
- REST Docs: 대표 에러 응답 snippet 추가

## 4. TDD 기록

1. 실패 테스트 작성: 세부 code, page/size/sort 400, Bean Validation, 도메인 예외, REST Docs 에러 응답 테스트 추가
2. 실패 확인: 대상 테스트 묶음 28 tests / 12 failed
3. 최소 구현: ErrorCode 세분화, 공통 validator, 정책 클래스 분리
4. 테스트 통과: 수정된 테스트 묶음 44 tests 성공
5. 리팩토링: 서비스 예외 호출부와 문서 기대값 정리

## 5. 테스트 결과

- `./gradlew test`: BUILD SUCCESSFUL, 79 tests / 0 failures
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- hook 수동 검증: 잘못된 메시지 실패, 올바른 메시지 성공

## 6. 고민한 부분

- 기존 청구 조회 권한 예외에 전용 세부 code가 없어 사용자 확인 후 `BILLING_CHARGE_LIST_FORBIDDEN`을 추가했다.
- Bean Validation 기본 메시지가 영어로 내려와 사용자 표시용 메시지 기준에 맞춰 DTO 검증 메시지를 한국어로 명시했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor` 최초 실행이 Gradle wrapper lock 파일 권한 문제로 실패
- 원인: sandbox 밖 Gradle wrapper lock 접근 제한
- 해결: 동일 명령을 권한 상승으로 재실행해 성공
- 재발 방지: Gradle wrapper lock 권한 실패 시 같은 검증 명령을 승인 기반으로 재실행

## 8. 다음 작업

- [ ] PM 세션에서 브랜치 커밋 목록과 테스트 결과 리뷰

## 9. Velog 글감

- Spring Boot에서 에러 code를 안정 API 계약으로 관리하는 리팩토링
