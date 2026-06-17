---
project: FaithLog
type: velog-draft
created: 2026-06-17
tags:
  - FaithLog
  - backend
  - spring-boot
  - jwt
  - tdd
---

# 모바일 MVP에서 JWT 인증을 TDD로 세운 기록

## 글로 풀어볼 문제

모바일 앱에서 로그인 성공 시 토큰을 어떻게 전달하고, 서버는 어떤 claim과 검증 흐름을 가져가야 하는가.

## 내가 고민한 지점

- HttpOnly Cookie 대신 JSON response body token transport를 선택한 이유
- Refresh Token rotation과 logout blacklist를 후속 이슈로 분리하면서도 #27에서 hook을 남기는 방법
- Controller slice 테스트와 실제 Security filter 통합 테스트의 책임 분리

## 최종 선택

- 로그인 응답 body에 `accessToken`, `refreshToken`, 만료 정보를 반환한다.
- API 호출은 `Authorization: Bearer {accessToken}`를 사용한다.
- Access Token에는 `jti`, `userId`, `role`, `sessionId`를 넣는다.
- Refresh/logout 저장소 구현은 #28로 분리하고 #27에서는 blacklist checker interface만 둔다.

## 코드 또는 설계 예시

- `JwtProvider.issueTokens(User user)`
- `JwtAuthenticationFilter`
- `AuthControllerTest`, `AuthServiceTest`, `UserMeControllerTest`

## 배운 점

TDD로 인증을 구현할 때 Controller mapping, Service/JWT claim, Security filter integration을 나누면 실패 원인이 선명해진다.

## 글 전개 순서

1. 모바일 인증에서 token transport 결정
2. 먼저 실패시킨 테스트 세트
3. JWT claim 설계와 Security filter 구현
4. 테스트 context 실패 트러블슈팅
5. #28 refresh/logout으로 남긴 경계
