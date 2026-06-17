---
project: FaithLog
type: troubleshooting
created: 2026-06-17
tags:
  - FaithLog
  - troubleshooting
  - spring-security
  - test
---

# #27 인증 JWT 테스트 context 실패

## 문제 상황

회원가입/로그인/JWT 인증 구현 후 대상 테스트 실행 중 Spring context와 MVC slice 테스트가 실패했다.

## 에러 메시지

- `Failed to instantiate [com.faithlog.global.security.JwtProvider]: No default constructor found`
- `No qualifying bean of type 'com.faithlog.global.security.JwtProvider' available`
- `No qualifying bean of type 'com.faithlog.global.security.AccessTokenBlacklistChecker' available`

## 원인 분석

`JwtProvider`에 운영 생성자와 테스트용 보조 생성자가 함께 있었지만 주입 생성자를 명시하지 않아 Spring이 생성자 선택에 실패했다. 또한 `@WebMvcTest`는 Controller slice와 일부 filter만 로드하므로 JWT provider와 blacklist checker가 자동으로 포함되지 않았다.

## 해결 방법

- `JwtProvider` 운영 생성자에 `@Autowired`를 명시했다.
- `AuthControllerTest`에서 `JwtProvider`, `AccessTokenBlacklistChecker`를 mock bean으로 제공했다.
- 실제 인증 필터 동작은 `UserMeControllerTest`의 `@SpringBootTest` 흐름에서 검증했다.

## 재발 방지

Spring bean에 복수 생성자를 둘 때는 주입 생성자를 명확히 표시한다. Controller slice 테스트에서는 필터 내부 동작까지 검증하지 않고, 필요한 보안 의존성은 mock으로 격리한다.

## 관련 이슈

- #27

## PM 리뷰 후 추가 이슈

### Refresh token Bearer 인증 차단

- 문제: refresh token이 access token parser를 통과해 authenticated endpoint에 사용될 수 있었다.
- 원인: access/refresh token을 구분하는 purpose claim 검증이 없었다.
- 해결: `tokenType` claim을 추가하고 access parser는 `ACCESS`, refresh parser는 `REFRESH`만 허용하게 했다.
- 검증: refresh token으로 `/api/v1/users/me` 호출 시 401 반환.

### Docker app startup 실패

- 문제: Docker image build는 성공했지만 app 컨테이너가 종료됐다.
- 원인: 기존 Postgres volume credential과 compose 기본 credential 불일치로 `FATAL: password authentication failed for user "faithlog"` 발생.
- 해결: volume 삭제/초기화는 파괴적이라 사용자 승인 없이 하지 않았다.
- 다음 조치: Docker volume 초기화 또는 기존 credential 기준 실행 방침 결정 후 헬스체크 재검증.
