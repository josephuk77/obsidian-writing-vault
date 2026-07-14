---
project: FaithLog
type: devlog
issue: 156
status: done
created: 2026-07-12
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - auth
---

# #156 User와 Auth 유스케이스 책임 분리

## 1. 작업 배경

`AuthService`와 `UserAccountService`가 인증·사용자 공개 유스케이스와 token/campus/withdrawal 세부 책임을 함께 소유하고 있었다. API·DB·보안 동작을 바꾸지 않고 각 transaction 경계를 전용 application service로 이동했다.

## 2. 최종 설계 기준

- signup, login, refresh rotation, logout, users/me, withdrawal을 6개 public service로 분리한다.
- token 발급/allowlist, ACTIVE campus 결과, session revocation, soft-delete는 package-private support로 응집한다.
- Controller는 전용 service를 직접 호출하고 기존 두 Service는 얇은 compatibility facade로 둔다.
- logout current-device FCM port를 유지하고 withdrawal 전체 FCM 비활성화도 application port로 연결한다.

## 3. 구현 내용

- Public: `SignupCommandService`, `LoginCommandService`, `RefreshTokenRotationService`, `LogoutCommandService`, `UserMeQueryService`, `AccountWithdrawalCommandService`.
- Support: `AuthTokenIssuanceSupport`, `CampusMembershipQuerySupport`, `UserSessionRevocationSupport`, `AccountSoftDeletionSupport`.
- Facade: `AuthService` 188→55줄(-70.7%), `UserAccountService` 103→19줄(-81.6%).

## 4. TDD 기록

1. 변경 전 auth/user·role invalidation·FCM focused baseline 성공.
2. 6개 전용 transaction, Controller 직접 연결, thin facade, support/port, cycle/SDK 누출 금지 구조 테스트 추가.
3. `6 tests / 5 failures` RED 확인.
4. 기존 검증·예외·호출 순서와 transaction을 전용 경계로 이동.
5. 구조 및 동작 회귀 GREEN 확인.

## 5. 테스트 결과

- Focused auth/user/role invalidation/FCM: 성공.
- 전체: 374 tests / 0 failures / 0 errors / 1 skipped.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- `git diff --check`: 성공.
- 격리 Docker: PostgreSQL/Redis healthy, app health `200 + UP`.
- API QA: signup/login/me/refresh/reuse 401/logout/access 401/refresh 401 및 별도 계정 탈퇴/access 401/relogin 401 전체 성공.

## 6. 고민한 부분

기존 withdrawal flow에는 마지막 active service ADMIN 보호가 없었다. 리팩터링 동작 변경 금지에 따라 추가하지 않고 후속 보안 감사 MEDIUM 항목으로 기록했다. 영향은 마지막 ADMIN 탈퇴 시 관리자 기능 운영 잠금 가능성이다.

## 7. 트러블슈팅

- 활성 `pm-dev`/`.harness`가 없어 임의 생성 없이 FaithLog TDD gate를 적용했다.
- Docker daemon 미실행 상태를 확인하고 Docker Desktop을 시작한 뒤 `faithlog-qa-156-user-auth-20260712` 고유 project로 QA했다.
- 첫 image build는 stale Alpine cache의 `xargs: echo: Exec format error`로 실패했다. 허용된 builder cache 1.877MB만 정리하고 한 번 재시도해 build와 QA에 성공했다.
- 시작 Build Cache 1.617GB(회수 가능 367B), 최종 prune 회수 696.5MB, 정리 후 Build Cache 1.748GB/회수 가능 0B, 마지막 `docker builder prune -f` 회수 0B를 기록했다.
- 동일 project를 volume 삭제 없이 down했다. system/image/volume prune, `down -v`, named volume 삭제는 실행하지 않았다.

## 8. 다음 작업

- [x] PM 코드리뷰 blocking finding 0건.
- [ ] 별도 승인 후 push/PR 및 원격 CI.

## 9. Velog 글감

- JWT/Redis/FCM 계약을 유지하며 인증 application service를 유스케이스 단위로 분리하는 방법.
