---
project: FaithLog
type: troubleshooting
created: 2026-06-22
tags:
  - FaithLog
  - troubleshooting
  - security
  - docker
---

# #76 tokenVersion Docker/Security QA 이슈

## 문제 상황

Issue #76 Docker API QA 중 로컬 컨테이너에서 회원가입 API가 401로 막혔고, 기존 Postgres volume이 있는 상태에서 `users.token_version` 추가 시 앱 시작이 실패했다.

## 에러 메시지

- `POST /api/v1/auth/signup` 응답: `401 AUTH_UNAUTHORIZED`
- Postgres schema update: `column "token_version" of relation "users" contains null values`

## 원인 분석

- Security public endpoint matcher가 local Docker profile의 Spring Security path matching과 맞지 않아 공개 auth endpoint가 permitAll로 처리되지 않았다.
- 기존 users row가 있는 DB에 nullable=false column을 추가하면서 기본값이 없어 Postgres가 NOT NULL 제약을 만족할 수 없었다.

## 해결 방법

- `SecurityConfig`에서 `PathPatternRequestMatcher.withDefaults()`를 사용해 health/auth/swagger 공개 경로를 명시 matcher로 등록했다.
- `User.tokenVersion` column definition을 `bigint default 0`으로 지정해 기존 row schema update에서도 기본값이 채워지도록 했다.

## 재발 방지

- Docker API QA에 signup/login을 포함해 public endpoint regression을 확인한다.
- schema migration 정리 전까지 local `ddl-auto=update` 환경에서 기존 row가 있는 volume도 검증한다.

## 관련 이슈

- #76
