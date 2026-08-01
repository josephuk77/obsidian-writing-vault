# 2026-07-28 Issue #7 Supabase JWT 인증·인가 개발 일지

---
title: "2026-07-28 Issue #7 Supabase JWT 인증·인가 기반 구현"
created: "2026-07-28"
tags:
  - type/project
  - status/active
  - area/backend
  - area/security
  - area/supabase
---

## 목표

Supabase Auth access token을 Spring Security OAuth2 Resource Server에서 검증하고 `/api/v1/**`를 보호했다. 회원가입·로그인 API나 프로필 API는 만들지 않고 공통 인증·인가 기반만 구현했다.

## 구현 내용

- `/api/v1/**` 인증 필수, Actuator health/info 공개, 비활성 springdoc 경로와 그 밖의 경로 기본 거부
- stateless session, Bearer token 전용 요청과 CSRF 비활성화 근거, 명시적 CORS Origin allowlist
- ES256/RS256 JWKS decoder와 `local-hs256` 전용 legacy shared-secret decoder 전략 분리
- signature, `exp`, `nbf`, `iss`, `aud=authenticated`, `role=authenticated`, UUID `sub`와 선택적 UUID `session_id` 검증
- `anon`, `service_role`, 잘못된 issuer/audience/sub와 중복 Authorization 헤더 거부
- Spring `Jwt`가 도메인에 누출되지 않는 불변 `CurrentUser`와 작은 `CurrentUserAccessor` 계약
- `401 AUTH_TOKEN_INVALID`, `403 AUTH_ACCESS_DENIED`와 한국어 message·traceId JSON 응답
- OpenAPI 전역 `bearerAuth` scheme과 security requirement
- JaCoCo 전체 라인 커버리지 하한을 0%에서 90%로 상향

## 공식 문서와 실제 token 결정

- Supabase 공식 JWT/JWKS·claim 문서와 Auth changelog를 다시 확인했다.
- 2026년 7월 self-hosted `API_EXTERNAL_URL`이 `/auth/v1`을 포함하도록 바뀐 내용을 issuer 문서에 반영했다.
- Supabase CLI 2.110.0으로 가짜 사용자를 signup해 실제 access token을 확인한 결과 `alg=ES256`, `aud=authenticated`, `role=authenticated`, UUID `sub`였다.
- 최신 로컬 CLI도 JWKS를 기본으로 사용하고 HS256은 `local-hs256` profile에서만 허용하기로 결정했다.
- JWKS decoder가 시작 시 네트워크 조회를 하지 않고, 조회한 같은 `kid`는 endpoint 일시 장애 중에도 cache에서 검증하는 테스트를 추가했다.

## Red → Green → Refactor

### Red

- 운영 구현 전 보안 단위·통합 테스트를 추가했다.
- `./gradlew test --tests ...` 실행에서 `SupabaseJwtValidator`, 현재 사용자 변환, decoder factory, 접근 제어 클래스 24개 symbol 부재로 `compileTestJava`가 실패했다.

### Green

- Spring Security와 OAuth2 Resource Server 의존성, 최소 decoder·validator·filter chain·오류 handler를 추가했다.
- 정상, 누락, malformed, 서명 변조, 만료, 미래 `nbf`, issuer/audience/role/sub 오류, 401/403, CORS, 공개/보호 경로, OpenAPI 테스트가 성공했다.

### Refactor

- JWKS와 HS256을 `JwtDecoderStrategy` 구현으로 분리하고 공통 검증 완료 계약은 factory가 적용했다.
- Security 설정, decoder 전략, claim 검증·변환, 오류 응답, CORS 책임을 별도 클래스로 나눴다.
- CORS Origin을 trim·빈 값 제거·중복 제거하고 wildcard를 fail-fast로 거부했다.
- 실제 CLI 결과가 ES256임을 확인한 뒤 로컬 기본을 JWKS로 바로잡았다.

## 검증 결과

| 검증 | 결과 |
| --- | --- |
| `cd services/spring-api && ./gradlew clean check` | 성공 |
| 단위·Slice·통합·Architecture·OpenAPI | 성공 |
| JaCoCo 라인 커버리지 | 314/327, 약 96.0%, 하한 90% 통과 |
| `./scripts/quality-gate.sh` | 성공 |
| pre-push 전체 품질 게이트 | 성공 |
| Supabase CLI 2.110.0 실제 Auth smoke | ES256 JWKS→Spring 200, 변조 token 401, 미허용 경로 403 성공 |
| `./scripts/docker-smoke-test.sh` | Health·PostGIS·스키마·fixture 성공 |
| 비밀정보 검사·`git diff --check` | 성공 |
| 임시 사용자·token 파일·CLI 파일 | 삭제 완료 |
| 이번 검증 Docker/Supabase 컨테이너·네트워크·volume·image | 모두 0건 |

## SOLID 적용

- SRP: Security 설정, CORS, decoder 전략, claim validator/converter, 오류 응답 분리
- OCP: `JwtDecoderStrategy` 목록으로 JWKS와 HS256 교체·확장
- LSP: 모든 decoder가 동일한 timestamp·issuer·Supabase claim validator 계약을 통과
- ISP: `CurrentUserAccessor` 하나의 작은 현재 사용자 추상화
- DIP: 도메인 사용자는 Spring `Jwt`가 아니라 `CurrentUser` 계약에 의존

## 커밋과 원격 반영

| SHA | 작업 단위 |
| --- | --- |
| `7bec138` | Supabase JWT 인증 기반과 테스트·smoke 구현 |
| `90170d2` | 인증 환경과 운영 경계 한국어 문서화 |
| `3157554` | Reviewer 지적 JWT 보안 경계 검증 강화 |
| `c0e5944` | exp·profile matrix·현재 사용자 계약·CORS·장애 분류·Jackson 3 보완 |
| `9d833e1` | JWKS provider fault 세분화와 CORS 기본 port canonicalization |
| `b882ac9` | 비정규 CORS 숫자형 host startup fail-fast |

- 브랜치: `feat/7-supabase-jwt-security`
- 로컬 HEAD: `b882ac992d383adecd7d8dd88de3b00b15418550`
- 원격 HEAD: `b882ac992d383adecd7d8dd88de3b00b15418550`
- PR은 만들지 않았다. 최신 `develop...HEAD`를 별도 Reviewer 작업에서 검토해야 한다.

## Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa819-cd64-76a3-b212-2321f0dc4b95`의 HEAD `90170d2` 판정을 받아 다음을 테스트 우선으로 보완했다.

### Red

- claim 경계·HTTPS·CORS·JWKS rotation 테스트를 먼저 추가하고 관련 테스트 명령을 실행했다.
- `aud` 누락 시 `SupabaseJwtValidator` NPE가 filter chain 밖으로 전파됐다.
- JWKS endpoint 503의 unknown `kid`에서 `AuthenticationServiceException`이 전파됐다.
- 기본/운영 HTTP issuer·JWKS와 넓은 사설망 HTTP, 빈 CORS allowlist가 허용돼 6개 테스트가 실패했다.
- 정확한 로컬 profile resolver 테스트는 구현 전 `cannot find symbol` 9건으로 `compileTestJava`가 실패했다.

### Green과 Refactor

- claim 원시 타입을 검사해 `aud`, `role`, `sub`, `session_id`를 fail-closed 처리하고 존재하는 빈 `session_id`와 non-canonical UUID를 거부했다.
- `SecurityRuntimeEnvironment`와 `JwtEndpointPolicy`로 decoder mode와 실행 환경을 분리했다. 기본/운영은 issuer·JWKS HTTPS를 강제하고 정확한 `local`/`local-hs256`만 loopback·`host.docker.internal` HTTP를 허용한다.
- Spring Security failure handler가 JWKS 조회 장애를 `401 AUTH_TOKEN_INVALID + traceId`로 변환하도록 구성했다.
- CORS 목록이 정규화 후 비면 startup fail-fast하고 trim·dedup·wildcard 금지·credentials=false를 유지했다.
- Nimbus JWKS cache에 `Cache-Control: max-age=300`을 적용한 테스트 서버로 old→old+new unknown `kid` 재조회 요청 수 1→2와 장애 중 cached old 성공, unseen `kid` 401을 확인했다.
- 관련 경계 테스트, startup context, 전체 `clean check`, 품질 게이트, Docker와 실제 Supabase ES256 smoke가 모두 성공했다.

### 원본 TDD 증거

- 원본 task: `019fa7f3-012b-7e91-9844-ab1ec6e88e15`
- Issue 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5102897485
- 기존 세션의 2026-07-28 18:05 KST `compileTestJava` 24개 symbol 실패와 같은 명령의 Green·Refactor 출력을 옮겼으며, 사후 가짜 Red나 커밋 재작성은 하지 않았다.

## 두 번째 Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa852-7200-7e20-809f-59bfe4de74af`의 HEAD `3157554` 판정 6건을 동일 브랜치에서 테스트 우선으로 보완했다.

### Finding별 수정

- `exp`: filter chain에서 누락 token이 200으로 통과하는 Red를 확인했다. 변환 완료 claim이 `Instant`가 아니면 fail-closed하고, null·문자열·객체 변환 실패·과거·epoch를 모두 `401 AUTH_TOKEN_INVALID + traceId`로 고정했다.
- profile×mode: 실행 환경과 허용 decoder mode를 `SecurityRuntimePolicy`의 별도 값으로 유지했다. 정확한 `local`은 JWKS, 정확한 `local-hs256`은 HS256만 허용하고 혼합·유사·대소문자·공백 profile은 fail-fast한다. `test` 같은 비보안 단일 profile은 운영 JWKS 정책을 적용한다.
- 현재 사용자 계약: `CurrentUser`, `CurrentUserAccessor`, `AuthenticatedRole`을 Spring 비의존 `application.security` 경계로 이동했다. `global.security` adapter만 `Jwt`와 `SecurityContext`를 사용하며 production-neutral domain fixture와 ArchUnit으로 누출 금지를 검증한다.
- CORS: http/https scheme, host, 선택적 1~65535 port만 허용하고 scheme·host 소문자 normalization 후 dedup한다. userinfo/path/query/fragment/encoded 우회/상대 URI/host 없음/wildcard/invalid port는 startup fail-fast한다.
- 장애 분류: known unknown kid와 원격 `RemoteKeySourceException`은 401을 유지한다. 그 밖의 예상 못한 provider 장애는 raw message 없이 `500 AUTH_INTERNAL_ERROR`와 traceId만 반환하고 committed response에는 중복 기록하지 않는다.
- Jackson 3: 보안 오류 writer가 Boot 4.1의 `tools.jackson.databind.ObjectMapper` bean을 주입받는다. `SecurityConfig`의 직접 생성과 보안 코드의 Jackson 2 의존을 제거하고 ArchUnit으로 고정했다.

### Red

- `./gradlew --no-daemon test --tests '*SecurityIntegrationTest.exp*'`: 2개 중 1개 실패, exp 누락 token이 401 대신 200.
- resolver/startup matrix: 11개 중 4개 실패, local mode override·혼합·유사 profile 허용.
- domain contract `compileTestJava`: application 계약 부재 `cannot find symbol` 3건.
- CORS property/preflight: 5개 중 2개 실패, normalization과 URI 문법 차단 부재.
- 내부 decoder fault/JWKS rotation: 2개 중 1개 실패, 예상 장애가 500 대신 401.
- Jackson 3/비활성 문서: 4개 중 2개 실패, Jackson 2 ArchUnit 위반 4건과 constructor 타입 불일치.

### Green과 Refactor

- 관련 52개 테스트: `BUILD SUCCESSFUL in 17s`.
- `spotlessApply` 후 관련 suite: `BUILD SUCCESSFUL in 18s`.
- `./gradlew --no-daemon clean check`: `BUILD SUCCESSFUL in 34s`.
- 전체 테스트 64개, 실패·오류 0, 실제 Auth 조건부 1개는 기본 검사에서 skip하고 Supabase smoke에서 별도 성공했다.
- JaCoCo line 314/327, 약 96.0%로 90% 하한을 통과했다.

### 통합·보안 검증

- 공식 Supabase Claims Reference에서 `exp`·`iat` required, `nbf` optional을 확인했다. 이번 범위는 `exp` 존재·타입·만료를 강제하고 `nbf`는 존재 시 검사하며 `iat` 정책 확장은 하지 않았다.
- Supabase CLI 2.110.0의 일반/start/db reset/status/stop 도움말을 먼저 확인했다.
- start, db reset 2회, 가짜 signup, 실제 ES256 access token의 Spring 200·변조 401·인가 403이 성공했다.
- 품질 게이트, 별도 Docker smoke, pre-push 품질 게이트가 성공했다.
- all-files 비밀정보 검사와 `git diff --check`를 통과했다.
- 이번 작업 container/network/volume/생성 smoke image/임시 CLI·token 파일은 0건이며 기존 사용자 Docker 자원은 보존했다.

### 증거와 인계

- 이번 TDD 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5103595039
- 원본 최초 TDD 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5102897485
- 새 commit/로컬·원격 HEAD: `c0e5944cd68c55df6ad531bc95cace0ed2541adc`
- PR은 만들지 않았다. PM은 고정 base `93eeae4...c0e5944`를 새 독립 Reviewer 작업에서 검토해야 한다.

## 세 번째 Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa885-7a6a-7951-9f30-8d85bff2db46`의 HEAD `c0e5944` 판정 중 재현 가능한 두 건만 범위로 고정해 테스트 우선으로 보완했다.

### Finding별 수정

- JWKS 장애 분류: 기존에는 cause chain에 `RemoteKeySourceException`만 있으면 모두 401로 처리해 HTTP 200 malformed JWKS body도 token 오류로 숨겼다. 최소 `RemoteJwksFailureClassifier`를 추가해 실제 I/O·resource access·HTTP 5xx 가용성 실패만 401로 유지하고, `ParseException` 기반 payload/protocol fault와 예상 못한 decoder/service fault는 고정 한국어 message의 `500 AUTH_INTERNAL_ERROR + traceId`로 처리했다. 예외 message 문자열은 분류에 쓰지 않았다.
- CORS 기본 port: URI의 scheme·host·port를 구조적으로 재조립해 `http:80`과 `https:443`을 브라우저 Origin 직렬화와 같은 portless 형태로 바꾸고 중복 제거했다. 비기본 port와 IPv6 bracket, 기존 문법 fail-fast, credentials=false를 유지했다.

### Red

- JWKS filter-chain 명령: `./gradlew --no-daemon test --tests '*JwksRotationSecurityIntegrationTest' --tests '*MalformedJwksSecurityIntegrationTest' --tests '*UnexpectedJwtDecoderFailureIntegrationTest'`
- 결과: 4개 중 1개 실패. malformed HTTP 200에서 `Status expected:<500> but was:<401>`을 재현했다. cached old 200, unseen kid+503의 401, 예상 못한 fault 500은 유지됐다.
- CORS 명령: `./gradlew --no-daemon test --tests '*AppCorsPropertiesTest' --tests '*SecurityIntegrationTest.허용한_CORS_origin만_preflight를_통과한다'`
- 결과: 6개 중 3개 실패. `:80`/`:443`가 보존되고 portless preflight의 allow-origin header가 없음을 재현했다.

### Green과 Refactor

- JWKS 3-way matrix: cached old kid 200, unseen kid+503 `401 AUTH_TOKEN_INVALID + traceId`, malformed HTTP 200 `500 AUTH_INTERNAL_ERROR + 고정 한국어 message + traceId`가 모두 통과했다.
- CORS matrix: domain/localhost/IPv4/IPv6의 기본 port 생략·dedup, 비기본 port 보존, IPv6 bracket 보존과 실제 preflight 허용/거부 경계가 통과했다.
- `spotlessApply` 후 두 finding targeted suite가 `BUILD SUCCESSFUL in 17s`, 보안 패키지와 Architecture 회귀 suite가 `BUILD SUCCESSFUL in 20s`로 성공했다.
- 응답과 로그에 raw 예외 message, JWKS body, URL query, kid/key, token, payload, email/PII를 추가하지 않았다. committed response 중복 write 테스트도 유지했다.

### 전체 검증과 증거

- `./gradlew --no-daemon clean check`: `BUILD SUCCESSFUL in 38s`
- JaCoCo line 322/335, 약 96.1%, 하한 90% 통과
- `GITHUB_HEAD_REF=feat/7-supabase-jwt-security ./scripts/quality-gate.sh`: 전체 성공
- 별도 Docker smoke와 pre-push Docker smoke: health·PostGIS·schema·fixture 성공
- 공식 Supabase CLI 2.110.0 `--help`, start, db reset 2회, fake signup, 실제 ES256 token Spring 200·변조 401·인가 403 성공
- all-files 비밀정보 검사와 `git diff --check` 성공
- 이번 작업 임시 파일·Supabase stack·smoke container/network/volume/image는 0건으로 정리했고 기존 사용자 Docker 자원은 보존했다.
- TDD Issue 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5104084223
- Green 중간 실패·테스트 보정 추가 증거: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5104147178
- 새 commit/로컬·원격 HEAD: `9d833e10f8f0bc03027e72a631304a35ed265c24`
- 새 환경변수와 사용자 입력 변경은 없다. PR·merge·Reviewer 역할·force push·승인 파일 조작은 하지 않았다.

## 네 번째 Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa8b5-5430-7d11-9ebe-df79844cfb66`의 HEAD `9d833e1` 판정 중 남은 CORS 숫자형 host canonicalization 한 건만 테스트 우선으로 보완했다.

### 정책과 구현

- canonicalize 대신 안전한 startup fail-fast를 선택했다.
- IPv4는 정확히 4개 dotted-decimal octet, 각 0~255, `0` 외 leading zero가 없는 경우만 숫자형 주소로 허용한다.
- IPv6는 DNS를 사용하지 않는 순수 parser로 8개 그룹을 만든 뒤 lowercase·leading-zero 제거·가장 긴 첫 zero run 압축 결과와 입력이 같은 canonical 표기만 허용한다.
- DNS-like hostname은 숫자와 dot만으로 이루어진 후보가 아니면 기존 hostname 경계로 처리한다.
- WHATWG URL parser 전체나 DNS 조회, 문자열 치환은 추가하지 않았다.

### Red

- 명령: `./gradlew --no-daemon test --tests '*AppCorsPropertiesTest' --tests '*SecurityIntegrationTest.허용한_CORS_origin만_preflight를_통과한다'`
- 결과: 8개 중 1개 실패.
- `브라우저와_다르게_직렬화되는_비정규_numeric_host는_시작_설정이_실패한다`에서 `Expecting code to raise a throwable.`로 실패했다.
- 첫 입력 `HTTP://[0:0:0:0:0:0:0:1]:80`이 예외 없이 허용되는 기존 결함을 확인했다.
- 같은 테스트 목록에 `0177.0.0.1`, `127.1`, `2130706433`, leading-zero/range 초과 IPv4와 noncanonical IPv6 기대를 운영 코드보다 먼저 작성했다.

### Green과 Refactor

- 초기 Green targeted suite가 `BUILD SUCCESSFUL in 12s`로 통과했다.
- IPv4 0/255 경계, canonical IPv6의 대소문자·semantic dedup, DNS-like hostname을 보강했다.
- `spotlessApply` 후 단위·startup context·실제 preflight suite가 `BUILD SUCCESSFUL in 13s`로 통과했다.
- canonical `127.0.0.1`, `[::1]`, domain/localhost와 기본 port 제거·비기본 port 보존을 유지했다.
- 실제 cross-origin `http://127.0.0.1`, `http://[::1]` preflight가 성공하고 다른 Origin/method/header와 credentials=false 경계도 유지됐다.

### 전체 검증과 증거

- 보안 패키지 전체와 Architecture 회귀: `BUILD SUCCESSFUL in 18s`
- `./gradlew --no-daemon clean check`: `BUILD SUCCESSFUL in 31s`
- 최종 test task 69개, 실패 0
- JaCoCo line 397/418, 약 95.0%, 하한 90% 통과
- 전체 quality gate와 pre-push quality gate 성공
- 별도 Docker smoke와 gate Docker smoke의 health·PostGIS·schema·fixture 성공
- 공식 Supabase CLI 2.110.0 `--help`, start, db reset 2회, fake signup, 실제 ES256 Spring 200·변조 401·인가 403 성공
- all-files 비밀정보 검사와 `git diff --check` 성공
- 이번 작업 임시 파일·Supabase stack·smoke container/network/volume/image는 0건이며 기존 사용자 자원은 보존했다.
- TDD Issue 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5104507714
- 새 commit/로컬·원격 HEAD: `b882ac992d383adecd7d8dd88de3b00b15418550`
- 새 환경변수·사용자 입력은 없다. PR·merge·Reviewer 역할·force push·승인 파일 조작은 하지 않았다.

## 다섯 번째 Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa8d9-93e6-7070-838b-e9670b5b8e66`의 HEAD `b882ac9` 판정 중 남은 16진 numeric IPv4 host 한 건만 테스트 우선으로 보완했다.

### 정책과 구현

- DNS 조회와 WHATWG URL parser 재구현 없이 lexical fail-fast를 선택했다.
- host의 모든 label이 비어 있지 않은 ASCII decimal component 또는 `0x` 뒤에 유효 ASCII hex digit이 하나 이상인 component로만 구성됐는데 canonical dotted-decimal IPv4가 아니면 startup에서 거부한다.
- 단일 `0x7f000001`·대문자 변형, dotted hex/decimal 혼합, 기존 축약·leading-zero numeric IPv4가 이 경계에 포함된다.
- `0x.example.com`, `api-0x7f.example.com`, `deadbeef.example`, `x7f000001.example`, `0xg.example.com`처럼 numeric component만으로 구성되지 않은 DNS-like hostname은 허용한다.

### Red

- 명령: `./gradlew --no-daemon test --tests '*AppCorsPropertiesTest' --tests '*SecurityStartupValidationTest.문법에_맞지_않는_CORS_origin은_context가_실패한다'`
- sandbox의 Gradle cache lock 권한 실패 후 같은 명령을 정식 권한으로 재실행했다.
- 22개 중 3개 실패했다.
- `http://0x7f000001`과 `http://0X7F000001`이 예외 없이 허용돼 각각 `Expecting code to raise a throwable.`로 실패했다.
- 실제 configuration context도 `http://0x7f000001` 설정에서 시작에 성공해 실패했다.

### Green과 Refactor

- 작은 `isWhatwgNumericIpv4Candidate`와 numeric component 판별만 추가한 동일 targeted 명령이 `BUILD SUCCESSFUL in 9s`로 통과했다.
- Node WHATWG `URL`로 단일·혼합 16진 입력은 `127.0.0.1`로 직렬화되고 DNS-like 입력은 원문 host를 유지함을 대조했다.
- IPv4/IPv6 ASCII hex digit helper를 공유하고 인증 문서에 `0x` component 거부를 명시했다.
- `spotlessApply` 후 단위·startup·실제 preflight suite가 `BUILD SUCCESSFUL in 15s`로 통과했다.
- canonical `127.0.0.1`, canonical IPv6, 기본 port 제거·semantic dedup·비기본 port, 실제 canonical IPv4 preflight 계약을 유지했다.

### 전체 검증과 증거

- 보안 패키지 전체와 Architecture 회귀: `BUILD SUCCESSFUL in 18s`
- 최종 `./gradlew --no-daemon clean check`: `BUILD SUCCESSFUL in 33s`
- test task 83개, 실패·오류 0, 조건부 로컬 Supabase 1개 skip
- JaCoCo line 401/423, 약 94.8%, 하한 90% 통과
- 전체 quality gate와 별도 Docker smoke 성공
- 공식 Supabase CLI 2.110.0 `--help`, start, db reset 2회, fake signup, 실제 ES256 Spring 200·변조 401·인가 403 성공
- all-files 비밀정보 검사와 `git diff --check` 성공
- TDD Issue 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5104944110
- 새 commit/로컬·원격 HEAD: `4a24207888167378ebaf2e989afbd623cb393c7e`
- 이번 작업 container/network/volume/image/temp는 0건이며 기존 사용자 Docker 자원은 보존했다.
- 새 환경변수·사용자 입력은 없다. PR·merge·Reviewer 역할·force push·승인 파일 조작은 하지 않았다.

## 여섯 번째 Reviewer CHANGES_REQUESTED 보완

Reviewer 작업 `019fa8ff-463f-7453-9b8f-cedc137230ff`의 HEAD `4a24207` 판정 중 trailing-dot/bare-`0x` numeric host 한 건만 테스트 우선으로 보완했다.

### 정책과 구현

- numeric 후보 판별용으로 optional trailing root dot을 한 번 제거한다.
- 정확한 `0x`/`0X` component는 WHATWG zero numeric component 후보로 처리한다.
- numeric trailing dot은 browser가 제거해 다른 IPv4 Origin이 되므로 startup fail-fast한다.
- 정상 DNS host의 trailing dot은 Node WHATWG Origin과 동일하게 보존한다.
- DNS 조회와 WHATWG parser 전체 구현은 추가하지 않았다.

### Red

- 명령: `./gradlew --no-daemon test --tests '*AppCorsPropertiesTest' --tests '*SecurityStartupValidationTest.문법에_맞지_않는_CORS_origin은_context가_실패한다'`
- 30개 중 7개 실패했다.
- `0x7f000001.`, 대문자 변형, bare `0x`/`0X`와 trailing-dot 변형 6개가 각각 `Expecting code to raise a throwable.`로 실패했다.
- startup context도 `http://0x7f000001.` 설정에서 실패하지 않고 정상 시작했다.

### Green과 Refactor

- trailing root dot 제거와 bare `0x` zero component 판별만 추가한 동일 명령이 `BUILD SUCCESSFUL in 7s`로 통과했다.
- dotted bare-`0x` 혼합, 정상 DNS trailing-dot 보존과 실제 Spring preflight를 보강했다.
- targeted Refactor suite가 `BUILD SUCCESSFUL in 10s`, 전체 security/Architecture/OpenAPI 회귀가 `BUILD SUCCESSFUL in 14s`로 통과했다.
- 인증 문서에 bare `0x`, numeric trailing-dot fail-fast와 정상 DNS trailing-dot 보존을 반영했다.

### 전체 검증과 증거

- `./gradlew --no-daemon clean check`: `BUILD SUCCESSFUL in 21s`
- test task 94개, 실패·오류 0, 조건부 로컬 Supabase 1개 skip
- JaCoCo line 405/427, 약 94.8%, 하한 90% 통과
- 전체 quality gate와 별도 Docker smoke, pre-push quality gate 성공
- 공식 Supabase CLI 2.110.0 `--help`, start, db reset 2회, fake signup, 실제 ES256 Spring 200·변조 401·인가 403 성공
- all-files 비밀정보 검사와 `git diff --check` 성공
- TDD Issue 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/7#issuecomment-5105533068
- 새 commit/로컬·원격 HEAD: `30acec1ad6878a8bbe02c151632d5f8eedc24e07`
- 이번 작업 container/network/volume/image/temp 0건이며 기존 사용자 Docker 자원은 보존했다.
- 새 환경변수·사용자 입력은 없다. PR·merge·Reviewer·force push·승인 파일 조작은 하지 않았다.

## 남은 위험

- 운영 Supabase 프로젝트 연결과 실제 운영 signing-key rotation은 범위 밖이라 실행하지 않았다.
- 새 `kid` 최초 조회 시 JWKS endpoint가 장애면 해당 token은 거부된다.
- ARM Mac에서 기존 PostGIS amd64 이미지 에뮬레이션 경고가 있지만 모든 Docker 계약은 통과했다.
