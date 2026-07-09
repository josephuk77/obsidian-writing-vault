---
project: FaithLog
type: devlog
issue: #76
status: done
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - tdd
---

# #76 역할 변경 시 기존 Access Token 무효화 정책 구현

## 1. 작업 배경

역할 변경 후 이미 발급된 Access Token의 role claim이 만료 전까지 유지되는 보안 공백을 줄이기 위해 Issue #76을 구현했다.

## 2. 최종 설계 기준

- PM 승인 후 `users.token_version` 기반으로 구현했다.
- Access Token에는 `tokenVersion` claim을 포함한다.
- 인증 필터는 token의 `userId/tokenVersion`과 DB의 현재 `tokenVersion`을 비교한다.
- service-level role 변경과 campus role 변경은 모두 대상 user의 `tokenVersion`을 증가시킨다.
- tokenVersion 불일치 또는 누락은 기존 `AUTH_UNAUTHORIZED` 정책을 재사용한다.
- refresh 재발급은 Redis allowlist/rotation 정책을 유지하면서 최신 role/tokenVersion으로 새 Access Token을 발급한다.

## 3. 구현 내용

- Entity: `User.tokenVersion`, `increaseTokenVersion()`, 실제 role 변경 시 version 증가
- Service: service-level role 변경은 `User.changeRole()`에서 version 증가, campus role 변경은 변경이 있을 때 `CampusUserTokenVersionPort`로 대상 user version 증가
- Repository: `UserRepository`가 campus token version port를 구현
- Security: `JwtProvider` access token claim 추가, `JwtAuthenticationFilter` tokenVersion 검증, `AccessTokenVersionChecker` port/adapter 추가
- Test: `RoleTokenInvalidationIntegrationTest`로 service role, campus role, logout/refresh 충돌 회귀 테스트 추가
- Docs: decision log, backend policy, Codex hook, resume metrics 갱신

## 4. TDD 기록

1. 실패 테스트 작성: `RoleTokenInvalidationIntegrationTest`
2. 실패 확인: 구현 전 신규 테스트 2건이 Access Token `tokenVersion` claim 부재로 실패
3. 최소 구현: claim 추가, DB tokenVersion 비교, role 변경 시 version 증가
4. 테스트 통과: 신규 테스트와 인증/admin/campus 집중 테스트 통과
5. 리팩토링: Docker QA에서 확인한 공개 endpoint matcher와 기존 Postgres volume schema update 이슈 보강

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`235 tests / 0 failures / 0 errors / 0 skipped`

추가 검증:

- `./gradlew build` 성공
- `./gradlew asciidoctor` 성공
- Docker API QA 성공

## 6. 고민한 부분

- tokenVersion 불일치 전용 ErrorCode를 추가할지 검토했지만, PM 승인 기준에 따라 기존 인증 실패 정책을 재사용했다.
- campus role은 API 권한에 직접 영향을 주므로 service-level role과 동일하게 Access Token 무효화 대상으로 처리했다.
- Redis refresh allowlist/logout blacklist 구조는 변경하지 않고 tokenVersion 검증을 추가했다.

## 7. 트러블슈팅

- Docker local profile에서 public auth endpoint가 401로 막혀 `PathPatternRequestMatcher` 명시 matcher로 수정했다.
- 기존 Postgres volume의 users row 때문에 `token_version not null` column 추가가 실패해 `bigint default 0` column definition을 보강했다.

## 8. 다음 작업

- [ ] PM 검증 후 PR 생성

## 9. Velog 글감

- JWT stateless 구조에서 role 변경 즉시 무효화를 token version으로 구현하는 방법
