---
project: FaithLog
type: devlog
issue: "#176"
status: done
created: 2026-07-12
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - redis
  - tdd
---

# #176 Refresh Token Rotation 원자성 및 동시 재사용 차단

## 1. 작업 배경

#158 감사에서 refresh current JTI 확인과 교체가 Redis GET→SET으로 분리돼 동일 old refresh의 병렬 요청이 모두 성공하는 race가 확인됐다. 목표는 공개 API와 token TTL을 유지하면서 승자를 정확히 하나로 제한하고, reuse가 감지된 session의 access와 refresh를 함께 폐기하는 것이다.

## 2. 최종 설계 기준

- expected JTI 비교와 new JTI+TTL 교체는 Redis Lua CAS 한 번으로 수행한다.
- loser/reuse는 `401 AUTH_UNAUTHORIZED`이며 해당 `userId + sessionId`만 폐기한다.
- `auth:session:revoked:{userId}:{sessionId}`에는 고정 marker만 저장한다.
- marker TTL은 configured refresh validity 1,209,600초 + 안전 여유 60초다.
- 다른 session과 다른 user는 영향받지 않고, UUID 새 session으로 재로그인할 수 있다.
- normal logout 의미는 session marker 폐기로 확대하지 않는다.

## 3. 구현 내용

- Port: rotation/revocation TTL을 함께 받는 `RefreshTokenStore.rotate`, `RefreshTokenRotationResult`, 필터 read 전용 `SessionRevocationChecker`
- Service: candidate token 생성 후 CAS 승자만 반환하고 loser는 reuse session revoke 수행
- Production adapter: match rotation과 mismatch refresh 삭제+marker 저장을 모두 처리하는 단일 Lua
- Test adapter: synchronized CAS/revoke로 production 상태 전이 재현
- Filter: access blacklist, session revoked marker, tokenVersion 순으로 확인하며 Redis 오류 시 principal 미생성
- API/DTO/DB/Flyway: 변경 없음

## 4. TDD 기록

1. 실패 테스트 작성: 같은 old refresh를 두 thread/barrier로 동시에 호출
2. RED: 실제 `[200, 200]`, 기대 `[200, 401]`, 1 test / 1 failure
3. 최소 구현: 원자 rotate result 계약과 in-memory synchronized CAS
4. Production: 단일 Redis rotate-or-revoke Lua와 filter marker checker
5. GREEN: 동시 success 1/401 1과 session 격리·fail-closed 회귀 통과

## 5. 테스트 결과

- PM review RED: 수동 revoke를 제거한 실제 Redis test에서 refresh key가 남아 `expected false, actual true`로 실패
- `./gradlew test`: 380 tests / 0 failures / 0 errors / 2 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- 실제 Redis integration: `ROTATED 1 / REJECTED 1`, revoke marker TTL과 후속 거절 확인
- Docker HTTP QA: PostgreSQL/Redis healthy, backend health UP, 병렬 refresh 200 1건/401 1건

## 6. 고민한 부분

CAS loser가 이미 winner에게 access를 응답한 뒤 발견될 수 있으므로 refresh key만 삭제해서는 부족했다. 또한 mismatch 판정과 별도 revoke Lua 사이에도 경합 창이 생기므로 단일 Lua가 match면 rotate, mismatch면 refresh 삭제+marker 저장을 완료하게 했다. marker가 이미 있으면 TTL을 연장하지 않고 reject하며, filter는 read-only checker로 winner access를 거절한다.

## 7. 트러블슈팅

- Docker Hub credential helper가 base-image metadata 조회에서 정체됐다.
- 로컬 검증 runtime image에 현재 bootJar를 read-only mount하는 임시 compose override로 production Redis adapter HTTP QA를 완료했다.
- PM 수정 후 격리 project `faithlog-qa-176-fix`를 volume 삭제 없이 compose down했고 마지막 Docker 명령 `docker builder prune -f`의 회수 대상 build cache는 0B였다.

## 8. 다음 작업

- [ ] PM 코드 리뷰와 검증 후에만 push/PR 진행

## 9. Velog 글감

- GET→SET refresh race를 Redis Lua CAS와 session-scoped denylist로 닫는 과정
