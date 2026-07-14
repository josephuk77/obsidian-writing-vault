---
project: FaithLog
type: troubleshooting
created: 2026-07-12
tags:
  - FaithLog
  - troubleshooting
  - redis
  - security
---

# Refresh Token GET→SET race와 Redis Lua CAS

## 문제 상황

같은 old refresh token을 두 요청이 동시에 사용하면 두 요청이 모두 current JTI 비교를 통과하고 각각 token pair를 발급할 수 있었다.

## 에러 메시지

RED 테스트 결과는 actual HTTP status `[200, 200]`, expected `[200, 401]`이었다.

## 원인 분석

`matchesCurrent`의 Redis GET과 새 refresh JTI 저장 SET이 서로 다른 연산이었다. 두 요청이 GET을 먼저 완료하면 single-use rotation 불변조건이 깨졌다. loser를 단순 401 처리하더라도 이미 winner가 받은 access는 refresh allowlist와 독립적으로 유효하므로 session-level access 폐기가 추가로 필요했다.

## 해결 방법

- expected JTI 비교와 new JTI+TTL 저장을 Lua script 한 번으로 수행했다.
- 단일 Lua가 expected JTI match면 new JTI+rotation TTL로 교체하고, mismatch면 같은 실행 안에서 refresh key 삭제와 revoked marker+revocation TTL 저장을 완료한다.
- revoked marker가 이미 있으면 marker TTL을 연장하지 않고 reject한다.
- `JwtAuthenticationFilter`가 marker를 검사하고 Redis 예외 시 인증 principal을 만들지 않게 했다.
- in-memory adapter도 synchronized CAS/revoke로 production 상태 전이를 재현했다.

## 재발 방지

- 동일 credential 동시 요청을 thread/barrier와 실제 Redis integration에서 검증한다.
- 실제 Redis test는 별도 수동 revoke 없이 두 concurrent `rotate()`만으로 refresh 삭제와 marker 생성을 검증한다.
- winner access/refresh 후속 401과 다른 session/user의 200을 함께 검증한다.
- app service가 Redis template, script, key 문자열을 알지 않게 port/adapter 경계를 유지한다.

## 관련 이슈

- #158
- #176
