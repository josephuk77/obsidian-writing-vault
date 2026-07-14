---
project: FaithLog
type: devlog
issue: "#186"
status: done
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - spring-security
  - security
  - tdd
---

# #186 Spring Security 취약 버전 maintenance upgrade

## 1. 작업 배경

Issue #161 F-161-01에서 Spring Boot 3.5.0이 Spring Security 6.5.0을 resolve해 공식 취약 범위 6.5.0-6.5.10에 포함되는 사실이 확인됐다. #186은 개별 Security module override 없이 가장 보수적인 공식 Boot 3.5.x maintenance 경로로 6.5.11 이상을 확보하고 인증·세션·기본 보안 헤더 회귀를 검증한다.

## 2. 승인된 방향

- Spring Boot plugin/BOM: 3.5.0 → 3.5.15
- Spring Security config/core/crypto/web/test: 6.5.0 → 6.5.11
- 개별 Spring Security override 없음
- eager-header workaround 없음
- API/DTO/ErrorCode/status/message, DB/Flyway, SecurityConfig 인가 의미 변경 없음
- Access 1,800초, Refresh 1,209,600초 유지
- #176 Lua rotate-or-revoke와 fail-closed, #76 tokenVersion, logout/withdrawal/FCM lifecycle 유지

## 3. TDD 기록

1. production/build 수정 전에 dependency contract와 200/401/403/404 보안 헤더 테스트 작성
2. RED: 5 tests 중 헤더 4건 통과, Spring Security 6.5.0 때문에 contract 1건 실패
3. test-only commit: `cc0aa8b`
4. Boot plugin 한 줄을 3.5.15로 변경
5. GREEN: Security config/core/crypto/web/test 모두 6.5.11, 취약 범위 잔여 0
6. PM review RED: test-only commit `d5fec90`에서 취약 runtime이 안전 test runtime에 가려지는 false-green과 `6.5.11-RC1` 허용을 `3 tests / 2 failures`로 재현
7. PM review GREEN: `b266272`에서 Gradle 실제 runtime/test resolved artifact manifest를 독립 전달하고 숫자 3-part 정식 release만 허용, contract `10 tests / 0 failures`

최종 manifest:

- runtime: config/core/crypto/web = 6.5.11
- test runtime: config/core/crypto/test/web = 6.5.11
- RC/M/SNAPSHOT/.Final/+build/2-part/4-part: 모두 거부
- PM 독립 구조 리뷰: 이전 false-green 2건 해소, 신규 blocking finding 0

## 4. Resolved Dependency

- runtime 좌표: 208 → 209
- 버전 변경: 81
- 추가: 1
- 제거: 0
- 주요 전이:
  - Spring Framework 6.2.7 → 6.2.19
  - Spring Data 3.5.0 → 3.5.12
  - Hibernate 6.6.15.Final → 6.6.53.Final
  - Jackson BOM 2.19.0 → 2.21.4
  - Lettuce 6.5.5.RELEASE → 6.6.0.RELEASE
  - PostgreSQL JDBC 42.7.5 → 42.7.11
- 전체 81개 좌표 diff: repository `docs/security/186-spring-security-maintenance-upgrade.md`

## 5. 테스트 결과

- 기존 focused 59 범위 + contract 9개 사례: 68 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 413 tests / 0 failures / 0 errors / 3 skipped
- 실제 Redis Lua integration: 1/1
- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- `git diff --check`: 성공
- test source: 78개
- REST Docs snippet groups: 124개

## 6. 보안 헤더와 404 한계

MockMvc는 정상 200, 미인증 401, 권한 부족 403, 미등록 경로 404에서 Cache-Control/Pragma/Expires/X-Content-Type-Options/X-XSS-Protection/X-Frame-Options를 검증했고 secure request의 HSTS도 검증했다.

`SecurityHeaderRegressionTest`는 일반 기본 보안 헤더 회귀 테스트이며 CVE exploit reproducer가 아니다. PM contract 보강에서는 이 테스트와 production 보안 동작을 변경하지 않았다.

다만 MockMvc의 direct handler lookup 404는 실제 servlet ERROR dispatch를 대표하지 않는다. 격리 Docker에서 valid token으로 확인한 결과는 다음과 같다.

- Boot 3.5.0 baseline: `/users/me=200`, unmatched path=`401 AUTH_UNAUTHORIZED`
- Boot 3.5.15: `/users/me=200`, unmatched path=`401 AUTH_UNAUTHORIZED`

따라서 #186 회귀가 아니다. PM A안대로 `DispatcherType.ERROR`/`/error`와 SecurityConfig는 수정하지 않았고 실제 HTTP 404 성공으로 집계하지 않는다. 별도 Issue도 생성하지 않았다. 실제 HTTP 헤더 성과는 200/401/403만 집계한다.

## 7. Docker QA

- compose project: `faithlog-qa-186-20260713`
- PostgreSQL 17/Redis 7 healthy, backend health 200/UP
- signup 201, login 200, Access/Refresh TTL 유지
- 실제 200/401/403 non-HSTS 기본 헤더 PASS
- refresh rotation PASS
- old refresh reuse 후 compromised session access/refresh 401 PASS
- logout 후 current access/refresh 401 PASS
- Redis 동시 Lua: ROTATED 1/REJECTED 1, refresh key 삭제, marker/TTL 경계 PASS
- QA 스크립트는 access/refresh token 값을 출력하거나 문서화하지 않음
- Docker Desktop engine 교착은 데이터 보존 force stop/start로 복구
- baseline 진단 컨테이너와 compose container/network만 제거
- named volume 보존, `down -v`/volume·image·system prune 미실행
- 마지막 Docker 명령 `docker builder prune -f`, 1.4GB 회수
- PM review 보강은 test/build-script만 변경해 Docker를 재실행하지 않음

## 8. 영향 범위

- production Java diff: 0
- API mapping/DTO/ErrorCode/status/message diff: 0
- SecurityConfig/JwtAuthenticationFilter/JwtProvider diff: 0
- Entity/DB/Flyway diff: 0
- Cloud Run/GCP/Supabase/Upstash/Firebase 설정 diff: 0
- wrapper/locking/verification metadata/Docker digest/Action SHA diff: 0
- `docs/decision-log.md` 변경 없음
- push/PR 없음

## 9. 다음 작업

- [ ] PM 최종 코드리뷰 및 독립 검증
- [ ] PM 승인 후 push/PR 결정
- [ ] unmatched-path 실제 HTTP status 정책은 별도 사용자 결정 후보로만 유지

## 10. 이력서 문장 후보

Spring Boot 3.5.0→3.5.15 managed BOM으로 취약 Spring Security 6.5.0을 6.5.11로 교체하고 production/test resolved graph 독립 계약과 정식 release 검증으로 false-green을 차단했으며, 209개 runtime 좌표의 81개 전이·413개 전체 테스트·실제 Redis Lua·격리 Docker 인증/헤더 QA로 회귀를 검증했다.
