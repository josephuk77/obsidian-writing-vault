---
project: FaithLog
type: devlog
issue: #27
status: done
created: 2026-06-17
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - auth
---

# #27 [Feat] 회원가입, 로그인, JWT 인증 구현

## 1. 작업 배경

모바일 MVP에서 사용자가 회원가입과 로그인을 하고, JWT Bearer Access Token으로 인증 API를 호출할 수 있도록 인증 기반을 구현했다.

## 2. 최종 설계 기준

- `users.authProvider`는 구현하지 않는다.
- 로그인 성공 시 `accessToken`, `refreshToken`을 JSON response body로 반환한다.
- 인증 API 호출은 `Authorization: Bearer {accessToken}` 기준이다.
- Access Token 기본 만료시간은 1800초다.
- Access Token에는 `jti`, `userId`, `role`, `sessionId`를 포함한다.
- Refresh Token에는 `userId`, `sessionId`, `refreshJti`를 포함한다.
- Refresh/logout/Redis rotation/blacklist 저장은 #28 범위이고, #27은 blacklist 조회 hook까지만 준비한다.
- Controller는 Entity를 직접 반환하지 않는다.

## 3. 구현 내용

- Entity: `User`, `UserRole(USER, MANAGER, ADMIN)`
- Command: `SignupCommand`, `LoginCommand`
- Service: `AuthService`
- Repository: `UserRepository`
- Controller: `AuthController`, `UserMeController`
- Security: `JwtProvider`, `JwtAuthenticationFilter`, `RestAuthenticationEntryPoint`, `AccessTokenBlacklistChecker`
- Test: `AuthControllerTest`, `AuthServiceTest`, `UserMeControllerTest`

## 4. TDD 기록

1. 실패 테스트 작성: 회원가입 ApiResponse, 로그인 token body, `/api/v1/users/me` Bearer 인증, password hash/JWT claim 테스트 작성
2. 실패 확인: `./gradlew test --tests '*AuthControllerTest' --tests '*UserMeControllerTest' --tests '*AuthServiceTest'`가 미구현 class compile error로 실패
3. 최소 구현: User/Auth/JWT/Security/Controller/DTO 추가
4. 테스트 통과: 대상 테스트와 전체 `./gradlew test` 성공
5. 리팩토링: Service 입력을 Request DTO가 아니라 Command로 받도록 테스트와 구현 정리

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

- 테스트에서 JPA repository를 검증하기 위해 사용자 승인 후 테스트 전용 H2를 추가했다.
- Flyway는 현재 정책대로 추가하지 않았다.
- 캠퍼스 멤버십 도메인이 아직 없으므로 `/users/me`와 로그인 응답의 `campusMemberships`는 빈 배열로 반환한다.

## 7. 트러블슈팅

- 문제: `JwtProvider` 생성자 선택 실패
- 원인: 테스트용 보조 생성자와 운영 생성자가 함께 있어 Spring이 기본 생성자를 찾으려 했다.
- 해결: 운영 생성자에 `@Autowired`를 명시했다.
- 재발 방지: Spring bean에 복수 생성자를 둘 때 주입 생성자를 명시한다.

- 문제: `@WebMvcTest`가 인증 필터 의존성을 찾지 못함
- 원인: MVC slice가 `JwtAuthenticationFilter`는 로드했지만 `JwtProvider`, `AccessTokenBlacklistChecker`는 slice 대상이 아니었다.
- 해결: 컨트롤러 매핑 테스트에서는 해당 의존성을 mock으로 제공했다.
- 재발 방지: 필터 동작 테스트와 Controller slice 테스트의 책임을 분리한다.

## 8. 다음 작업

- [ ] #28에서 refresh/logout, Redis refresh rotation, access token blacklist 저장/삭제 구현
- [ ] 캠퍼스 멤버십 도메인 구현 후 `campusMemberships` 실제 조회 연결

## 9. Velog 글감

- 모바일 앱 JWT 인증에서 Cookie 대신 response body token transport를 선택한 이유
- Spring Security stateless JWT 필터와 TDD로 인증 API를 세우는 과정
