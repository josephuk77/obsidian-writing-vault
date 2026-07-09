---
project: FaithLog
type: velog-draft
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
---

# JWT stateless 구조에서 role 변경 즉시 무효화하기

## 글로 풀어볼 문제

Access Token이 stateless JWT라면 role 변경 후에도 이미 발급된 token의 claim은 만료 전까지 남는다. 운영 서비스에서는 이 시간 차이가 권한 회수 지연으로 이어질 수 있다.

## 내가 고민한 지점

- Redis blacklist/session allowlist를 확장할지
- token version을 DB에 두고 JWT claim과 비교할지
- refresh/logout rotation 정책과 충돌하지 않게 어디에서 검증할지
- campus role처럼 token claim에 직접 들어가지 않는 권한 변경도 무효화할지

## 최종 선택

`users.token_version`을 두고 Access Token에 `tokenVersion` claim을 포함했다. 인증 필터에서 `userId/tokenVersion`을 DB 현재 값과 비교하고, service role 또는 campus role이 바뀌면 대상 user의 version을 증가시킨다.

## 코드 또는 설계 예시

- `JwtProvider`: access token claim에 `tokenVersion` 추가
- `JwtAuthenticationFilter`: claim 누락 또는 DB version mismatch 시 인증 미설정
- `User.changeRole`: 실제 role 변경 시 tokenVersion 증가
- `CampusService.changeCampusRole`: 실제 campus role 변경 시 대상 user tokenVersion 증가

## 배운 점

- stateless JWT도 작은 server-side version state를 결합하면 권한 회수 지연을 줄일 수 있다.
- Docker API QA는 테스트 환경이 못 잡는 Security matcher/schema update 문제를 잘 드러낸다.

## 글 전개 순서

1. 문제 상황: role claim과 권한 회수 지연
2. 대안 비교: TTL 단축, Redis blacklist/session, tokenVersion
3. FaithLog 구현 구조
4. refresh/logout 정책과의 충돌 방지
5. 테스트와 Docker QA로 확인한 것
