---
project: FaithLog
type: devlog
issue: "#224"
status: review
created: 2026-07-29
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - tdd
---

# #224 회원가입 이메일 인증 및 비밀번호 재설정

## 1. 작업 배경

회원가입 전에 이메일 소유권을 확인하고, 임시 비밀번호 없이 인증번호 확인 직후 사용자가 새 비밀번호를 직접 설정하도록 backend core를 추가했다.

## 2. 최종 설계 기준

- 이메일은 trim한 원래 대소문자를 저장하고 인증/중복 비교는 canonical lowercase로 통일한다.
- V13은 `lower(email)` 중복을 자동 수정하지 않고 실패하며, 정상 데이터에는 unique index를 만든다.
- Redis challenge/code/grant key는 독립 HMAC secret의 fingerprint만 사용한다.
- password reset 존재/부재 요청은 같은 durable Cloud Tasks 경로를 사용한다.
- Task에는 opaque dispatch token만 저장하고 recipient/code는 AES-256-GCM Redis payload에만 둔다.
- 비밀번호 변경은 user row lock, grant 1회 소비, BCrypt, tokenVersion 증가, Refresh Session 전체 삭제를 보장한다.
- 운영 발송은 Brevo SMTP `smtp-relay.brevo.com:587`과 required STARTTLS를 사용하며, Cloud Tasks 재시도 경계는 exactly-once가 아닌 at-least-once로 기록한다.

## 3. 구현 내용

- API: signup 인증 request/confirm, password reset request/confirm/complete 5개 공개 endpoint.
- Redis: 발급/시도/확인/소비 Lua 원자 연산과 encrypted dispatch payload/lease/ack 경계.
- Worker: Google issuer, exact audience/service account, `email_verified=true` OIDC 검증.
- Session: Access/Refresh Token 모두 DB tokenVersion과 대조하고 reset 전 token을 거부한다.
- Email: provider-independent sender port 뒤에 Spring JavaMail 기반 Brevo SMTP adapter를 구현했다. signup/password-reset별 한국어 plaintext+HTML, 6자리 code/TTL, 승인된 CID logo를 전송한다.
- Config: provider flag가 true일 때만 Brevo adapter를 만들며 exact host/port/login, SMTP AUTH, STARTTLS enable/required, positive timeout, runtime SMTP key, sender identity, logo checksum을 fail-fast 검증한다.
- Asset: `mail/faithlog-logo.png`, 112x112, 14,996 bytes, SHA-256 `6059e8f38377cfe485752cdf2fa37a014e01586246de5fd4ff26a40446d1b748`.

## 4. TDD 기록

1. 이메일 canonical/legacy duplicate, timing enumeration, grant 조기 소비, 약한 HMAC을 RED로 고정했다.
2. V13/lower lookup, Cloud Tasks, non-consuming resolve, strict Base64 32-byte secret으로 GREEN 처리했다.
3. 리뷰에서 dispatch lease 유실, provider idempotency, test-profile 운영 adapter 충돌을 추가 RED로 재현했다.
4. in-progress retry, stable delivery ID, 운영 adapter `!test` 경계로 GREEN 처리했다.
5. JavaMail multipart/CID/trace header/provider exception 계약을 RED로 고정하고 Brevo adapter를 GREEN 처리했다.
6. sender/recipient/code/TTL/logo hash와 SMTP AUTH/STARTTLS/timeout/provider bean 분리를 추가 RED로 고정하고 fail-closed 설정으로 GREEN 처리했다.

## 5. 테스트 결과

- `./gradlew test build asciidoctor`: BUILD SUCCESSFUL.
- 전체 656 tests, failures 0, errors 0, skipped 9.
- 실제 Redis 원자성 5 tests GREEN. UUID 임시 key는 종료 시 정리했다.
- 전용 임시 PostgreSQL에서 V1~V13, lower(email) unique, legacy duplicate fail-closed 3 tests GREEN. 임시 DB는 삭제했다.
- Brevo focused/config/worker/OIDC/encrypted-store 회귀 GREEN. 실제 Brevo network 발송은 수행하지 않았다.

## 6. 보안/장애 경계

- reset request는 계정 존재 여부와 무관하게 provider latency 밖의 동일 enqueue 경로를 사용한다.
- 같은 비밀번호 400은 grant를 보존하지만 새 비밀번호 성공은 동시성에서도 정확히 1회다.
- worker 재시도는 stable 64-hex delivery ID를 사용하고 SMTP adapter는 이를 CRLF-safe `X-FaithLog-Delivery-Id` trace header에 보존한다. Brevo SMTP는 provider-side idempotency를 보장하지 않아 send 성공 뒤 Redis ack 실패 시 같은 code가 드물게 중복 발송될 수 있다.
- raw email/code/password/JWT/Authorization/provider body를 로그, task body, Redis key, report에 남기지 않는다.
- 이메일 본문에는 remote image, tracker, deep link, JWT, grant, recipient address, user content를 넣지 않는다.

## 7. 다음 작업

- [ ] PM 전체 diff 재리뷰
- [ ] Cloud Tasks queue/IAM/Secret Manager 설정 후 worker smoke
- [ ] PM Docker app-only rebuild/recreate 뒤 실제 Brevo signup/reset 수신 smoke와 로그 민감정보 감사
- [ ] SMTP 전달/중복 관측 지표와 alert threshold 결정
- [ ] iOS/Android 강제 업데이트 이후 `FAITHLOG_AUTH_EMAIL_VERIFICATION_REQUIRED=true` 전환

## 8. 배포 경계

기본 provider/dispatch flags가 false인 local/Docker에서는 app startup/health가 가능하다. 준비된 Cloud Run 계약은 tasks+worker+Brevo를 함께 true로 두고 HMAC/AES/SMTP password를 Secret Manager에서 주입하며 signup-required는 mobile rollout 전 false를 유지한다. V13 배포 전 운영 DB의 `lower(email)` 중복을 감사해야 하며, 중복이 있으면 migration이 데이터를 건드리지 않고 실패한다. QA 컨테이너 lifecycle, 실제 SMTP 발송, push/PR/merge는 수행하지 않았다.
