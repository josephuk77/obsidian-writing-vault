---
project: FaithLog
type: security-audit
issue: 158
status: done
created: 2026-07-12
tags:
  - FaithLog
  - security
  - jwt
  - session
  - redis
  - OWASP
---

# #158 JWT와 세션 수명주기 보안 감사

## 1. 감사 배경

#157과 #156이 반영된 `origin/develop` `634d19c7` 기준으로 JWT, Redis session,
`tokenVersion`, logout/회원탈퇴/FCM cleanup을 보안 동작 변경 없이 읽기 전용으로 감사했다.

## 2. 감사 범위

- production/config/schema 47개 파일, focused test 8개 파일
- 인증·role 변경·FCM API 10개
- Redis 인증 흐름 5개, key type 2개
- JWT signature/algorithm/key 입력/type/expiration/JTI/issuer/audience
- access blacklist, refresh allowlist/rotation/reuse, sessionId, `tokenVersion`
- login/refresh/logout/회원탈퇴/service role/campus role/FCM ownership 전이
- Redis 장애 fail behavior, 401/403, log/error/REST Docs credential 노출

## 3. token/session 기준

- Access Token: 기본 1,800초
- Refresh Token: 기본 1,209,600초(14일)
- `auth:access:blacklist:{jti}`: access 남은 수명 + 60초
- `auth:refresh:{userId}:{sessionId}`: refresh 만료까지, value는 current `refreshJti`
- role 변경: service/campus 모두 target `tokenVersion++`, 기존 access 즉시 401
- 회원탈퇴: active=false/version 증가, refresh 전체 삭제, 현재 access blacklist,
  FCM/membership 전체 비활성화

## 4. 감사 결과

- Confirmed: Critical 0 / High 0 / Medium 1 / Low 0
- F-158-01: refresh current JTI의 GET 비교와 새 JTI SET이 원자적이지 않아 같은 old refresh의
  동시 요청이 모두 성공하고 서로 다른 access token이 기본 최대 1,800초 유효할 수 있다. 공격자
  SET이 마지막이면 공격자 refresh가 current JTI와 14일 TTL로 남고, 차단 전 성공적인 후속 회전마다
  TTL이 다시 14일로 설정돼 원래 refresh 만료를 넘어 sliding session persistence를 연장할 수도 있다.
- Severity Medium, confidence 10/10, 독립 코드 검증 완료
- CWE-362, 보조 CWE-294, OWASP API2:2023 Broken Authentication
- ASVS 5.0.0 `7.2.4`, `7.4.1`, OAuth refresh control intent `10.4.5`

구체적 실행 순서는 `A GET(old) → B GET(old) → A SET(newA) → B SET(newB)`다. 마지막 refresh
하나만 allowlist에 남지만 두 access token은 blacklist/version 변경이 없어 만료까지 쓸 수 있다.
마지막 SET이 공격자 요청이면 공격자가 current refresh를 보유한다. 다만 정상 client가 loser refresh를
다시 제출하면 mismatch 처리로 session key가 삭제된다. 해당 session logout과 회원탈퇴도 종료
조건이며, `tokenVersion` 변경은 기존 access를 무효화하지만 refresh session 자체는 삭제하지 않는다.

## 5. 정책/false positive/운영 확인

- logout은 승인 문서대로 제시 access JTI 하나와 current refresh session만 폐기한다. refresh 전후
  access가 겹칠 때 과거 access가 남는 동작은 현재 구현 결함이 아니라 PM 정책 재확인 항목이다.
- JJWT 0.12.6의 `alg=none`/RSA·EC confusion과 access/refresh type confusion은 거절된다.
- Redis 인증 장애는 principal/성공 응답을 만들지 않아 fail-closed다.
- Redis에는 raw token이 아닌 current `refreshJti`만 저장된다.
- JWT secret 최소 entropy/startup validation, issuer/audience, 환경 간 key 재사용, Upstash 운영 설정,
  Cloud Run log redaction, 모바일 secure storage는 운영 미확인으로 분리했다.
- Auth REST Docs snippet의 token/password 패턴은 test profile dummy/test JWT이며 ignored `build/`
  산출물이다. production leak finding은 아니지만 masking hardening 후보로 남겼다.
- #157 F-157-01은 중복 finding으로 만들지 않고 탈퇴 후 session cleanup만 참조했다.

## 6. 검증과 기록

- 2개 Gradle 명령, 8 classes, 33 tests / 0 failures / 0 errors / 0 skipped
- `git diff --check` 확인
- production/test/config/DB/Flyway 변경 0건
- 실제 secret/token/개인정보 값 출력·기록 0건
- Docker, push, PR, 수정 Issue 생성 0건
- 저장소 문서:
  - `docs/security/158-jwt-session-lifecycle.md`
  - `docs/security/158-audit-findings.md`
  - `docs/resume-metrics.md`

## 7. 후속 후보

- [ ] PM 승인 후 Redis CAS/Lua 기반 refresh 비교·교체 원자화와 동시성 회귀 테스트
- [ ] PM이 logout을 현재 session 전체 폐기로 정의할지 결정
- [ ] JWT key/audience와 Upstash/Cloud Run/mobile 운영 체크리스트 확인

이 감사는 AI 보조 정적 감사이며 전문 보안 감사나 침투 테스트를 대체하지 않는다.
