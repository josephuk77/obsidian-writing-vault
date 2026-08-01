# 2026-07-29 Issue #9 Supabase 소셜 로그인

## 목표

Supabase Auth를 중심으로 Google·Kakao built-in OAuth와 Naver `custom:naver` OAuth를 연결한다. Spring은 OAuth 로그인·code 교환·refresh token·provider secret을 소유하지 않고, Naver UserInfo 변환과 공개 provider 카탈로그만 담당한다.

## 구현

- 공개 `GET /api/v1/auth/social/providers`가 고정 순서의 `google`, `kakao`, `custom:naver`와 표시 이름만 반환하도록 구현했다.
- `GET /api/v1/auth/social/naver/userinfo`는 Supabase Auth의 back-channel 요청에 한해 strict Bearer header를 받고, 고정 Naver endpoint `https://openapi.naver.com/v1/nid/me`만 호출한다.
- Naver nested `response.id`, `email`, `name`, `nickname`, `profile_image`를 표준 `sub`, `email`, `email_verified`, `name`, `preferred_username`, `picture`로 변환했다.
- provider access token, 원본 profile, provider error body는 저장·로그·응답에 남기지 않는다.
- Google/Kakao/Naver 콘솔 설정, PKCE·email 필수, callback/redirect allowlist, 환경변수와 프론트엔드 Supabase SDK 흐름을 [[SOCIAL_LOGIN]]에 한국어로 정리했다.

## TDD

### Red

- `./gradlew --no-daemon test --tests 'com.timingjeju.api.domain.auth.*'`를 먼저 실행해 social login 운영 타입이 없어 29개 `cannot find symbol` 오류가 나는 것을 확인했다.
- `SocialLoginIntegrationTest`를 먼저 추가한 뒤 opaque Naver Bearer가 기존 Supabase JWT filter에 의해 401이 되는 4개 실패를 확인했다.

### Green

- social login 전용 공개 SecurityFilterChain과 Naver adapter를 추가한 뒤 domain auth·OpenAPI·Architecture targeted suite가 성공했다.
- upstream 401/403/429/5xx, timeout, malformed body, 64 KiB 초과, email 누락, header/query/form 오류와 redirect allowlist fail-fast를 테스트로 고정했다.

### Refactor

- provider catalog, Naver HTTP gateway, profile 변환, Bearer resolver, 오류 handler, OpenAPI 문서 계약을 책임별로 분리했다.
- 전역 Supabase JWT `bearerAuth`가 공개 social endpoint에 상속되지 않게 OpenApiCustomizer로 operation `security: []`를 명시했다.
- Git hook이 `providerAccessToken = ...`과 테스트 JWT 속성 literal을 비밀정보로 오인해, 실제 값 없이 `naverCredential`과 DynamicPropertySource 테스트 주입으로 바꾼 뒤 hook을 통과했다.

## 검증

- commit: `f4fc12124fa15f076c2e5f14fdf2ee3033dfe5f8` — `feat: #9 Supabase 소셜 로그인 연동`
- `cd services/spring-api && ./gradlew --no-daemon clean check`: 성공, 포맷·컴파일·단위/통합/Architecture·OpenAPI·JaCoCo·bootJar 통과
- `./scripts/quality-gate.sh`: 성공, 자동화 53개와 Spring/Docker 게이트 통과
- `./scripts/docker-smoke-test.sh`: 성공, Health Check·schema/negative constraints·fixture·PostGIS 최근접 정류장 검사 통과
- 공식 Supabase CLI 2.110.0: checksum 확인 후 start, `db reset` 2회, 빈 운영 시드·확장·public 스키마 검증 성공
- 실제 local Auth access token의 `alg=ES256`, `aud=authenticated`, `role=authenticated`, UUID `sub` 및 Spring 보호 API 성공을 확인했다. token 값은 출력하지 않았다.
- `scan-staged-secrets.py --all-files`, `git diff --check` 통과
- smoke 생성 Supabase/Docker 컨테이너·네트워크·볼륨을 정리했고 기존 사용자 Docker 자원은 보존했다.

## 결정과 남은 위험

- Naver custom provider의 실제 콘솔 client id/secret과 공개 HTTPS callback은 외부 계정 권한이 필요한 수동 설정 범위다. Spring 환경변수로 전달하지 않는다.
- `APP_SOCIAL_LOGIN_ENABLED_PROVIDER_IDS`, `APP_SOCIAL_LOGIN_REDIRECT_URLS`만 Spring 설정으로 추가했다.
- 공개 endpoint가 Naver provider token을 받지만, 일반 `/api/v1/**`의 Supabase JWT 정책은 유지된다.
- Reviewer는 fixed upstream URL·redirect allowlist·opaque Bearer JWT 미해석·오류 민감정보 비노출·OpenAPI 공개 security·Naver profile mapping을 집중 검토한다.

## 다음 단계

- PM이 `develop...f4fc12124fa15f076c2e5f14fdf2ee3033dfe5f8`를 독립 Reviewer에 전달한다.
- 승인 뒤에만 `$create-pr`로 develop 대상 PR을 만든다.

## Reviewer 필수 수정 보완

### 지적 사항과 결정

- Spring의 redirect allowlist를 제거하고 `supabase/config.toml`의 `[auth].additional_redirect_urls`만 단일 기준으로 유지했다. 로컬에는 정확한 두 URL만 허용하며 wildcard·query·fragment를 금지했다.
- Google·Kakao·Naver의 미사용 로컬 자격 환경변수를 제거했다. `APP_SOCIAL_LOGIN_PROVIDER_IDS`는 실제 활성 상태가 아니라 Spring이 지원하는 provider 목록만 나타낸다.
- Naver 공식 문서에는 PKCE 사용 계약이 없으므로 지원한다고 단정하지 않았다. 실제 Supabase custom provider 호환성과 identity linking 위험을 격리 환경에서 확인하기 전에는 운영 활성화를 차단하도록 문서화했다.
- Naver UserInfo의 `resultcode=00`, `message=success`를 모두 검증한다. Naver가 이메일 검증 신호를 제공하지 않으므로 `email_verified`를 응답에서 제거했다.
- Naver provider token은 최대 256자와 제한된 문자 집합만 허용하며 중복 header, 쉼표 결합, query/form 전달을 거부한다.
- 공개 경로는 `GET /api/v1/auth/social/providers`, `GET /api/v1/auth/social/naver/userinfo` 두 개만 허용했다. 다른 method와 하위 경로는 Supabase JWT 인증 체인으로 보낸다.
- 인스턴스별 고정 구간 60 req/s 제한과 동시 8개 bulkhead를 추가해 각각 429와 503의 고정 오류 계약으로 변환했다.

### Red

- Naver envelope·이메일 검증 테스트에서 기존 구현이 잘못된 `resultcode/message`를 통과시키고 `email_verified=true`를 반환해 실패했다.
- provider token 경계 테스트에서 257자, 쉼표·콜론·세미콜론 포함 token이 통과해 실패했다.
- 미등록 social 경로가 인증 체인 대신 404가 되어 401 기대 테스트가 실패했다.
- admission control 운영 타입 부재로 `compileTestJava`의 `cannot find symbol` 4건을 확인했다.
- Supabase layout 테스트에서 Spring redirect 이중 기준, 사용되지 않는 provider 환경변수, PKCE 단정 문구, 실제 redirect smoke 부재를 각각 Red로 확인했다.
- 원본 증거: https://github.com/Timing-Jeju/jeju_BE/issues/9#issuecomment-5107047292

### Green과 Refactor

- domain auth·OpenAPI·Architecture 대상 suite, scripts 테스트 56개가 성공했다.
- token resolver, envelope mapper, admission service, exact security matcher를 책임별로 분리했다.
- 문서는 지원 목록과 실제 Supabase 활성 상태, identity linking 위험, Naver PKCE 비보장 경계를 사실대로 구분했다.

### 전체 검증

- commit: `56f7c3ea926b0a0b07a81aa37b11d0f017de3eca` — `fix: #9 소셜 로그인 보안 경계 강화`
- `./gradlew --no-daemon clean check`: 성공, 14개 작업 실행
- `GITHUB_HEAD_REF=feat/9-supabase-social-login ./scripts/quality-gate.sh`: 모든 단계 성공
- `./scripts/docker-smoke-test.sh`: Health·PostGIS·schema·fixture 계약 성공
- 공식 Supabase CLI 2.110.0과 checksum을 확인하고 start, `db reset` 2회, 미등록 redirect 차단, 실제 ES256 token의 Spring 200·변조 401·인가 403을 검증했다.
- JaCoCo line 649/688, 약 94.3%로 90% 기준을 통과했다.
- all-files 비밀정보 검사와 `git diff --check`를 통과했다. token·password·secret은 출력하거나 저장하지 않았다.
- 검증용 Supabase·Docker 자원과 임시 CLI를 정리했고 기존 사용자 volume은 보존했다.

### 다음 단계

- PM은 `develop...56f7c3ea926b0a0b07a81aa37b11d0f017de3eca`를 새 독립 Reviewer에게 전달한다.
- Reviewer 승인 전 PR·merge는 수행하지 않는다.

## 두 번째 Reviewer 필수 수정 보완

### Finding 1 — header 이후 slow body timeout

- 기존 `HttpRequest.timeout`과 `BodyHandlers.ofInputStream()` 조합은 200 header와 첫 byte가 도착하면 body가 5초간 멈춰도 3초 제한을 적용하지 못했다.
- 운영 코드 변경 전에 slow HTTP server로 같은 상황을 재현했고 예외를 기대했지만 정상 반환하여 Red가 되었다.
- Java 표준 `HttpClient.sendAsync`와 64 KiB bounded body subscriber를 사용하고 응답 Future 전체에 3초 deadline을 적용했다.
- timeout과 body 초과 시 subscription 및 response Future를 취소한다. 별도 executor를 소유하지 않아 thread leak이나 shutdown 책임을 만들지 않는다.
- 테스트는 약 3초의 `UPSTREAM_TIMEOUT`, client 연결 종료, token/body/원본 예외 비노출, admission semaphore permit 회복 뒤 정상 재호출을 확인한다.

### Finding 2 — redirect smoke false-positive

- 기존 비활성 Google authorize 요청은 `unsupported_provider` 400과 빈 Location을 반환하는데도 악성 Location이 없다는 이유로 성공 처리했다.
- 운영 script 변경 전 테스트에서 `/auth/v1/admin/generate_link` email-link 검증 경로가 없어 Red를 확인했다.
- 로컬 service role을 임시 status 파일에서만 읽고 실제 Auth email signup link를 두 번 생성한다. 등록된 callback은 그대로 보존되어야 하고 악성 callback은 site URL로 fail-closed되어야 한다.
- 두 요청 모두 HTTP 200, 비어 있지 않은 action link와 정확한 `redirect_to`를 요구하므로 unsupported provider, 빈 Location, 선행 오류는 성공할 수 없다.

### TDD와 검증

- Red 댓글: https://github.com/Timing-Jeju/jeju_BE/issues/9#issuecomment-5107458287
- commit: `f591d8db99de79ab5314bf0cefac50f77bd35220` — `fix: #9 소셜 로그인 timeout과 redirect 검증 강화`
- targeted Naver gateway·admission·social integration·OpenAPI·Architecture 테스트 성공
- scripts 테스트 57개 성공
- `./gradlew --no-daemon clean check`: 성공, 14개 작업
- 전체 quality gate와 별도 Docker smoke 성공
- JaCoCo line 693/737, 약 94.0%, 90% 하한 통과
- 공식 Supabase CLI 2.110.0 checksum 확인, start, reset 2회, 실제 email-link 허용/악성 redirect 대조, ES256 Spring 200·변조 401·인가 403 성공
- 비밀정보와 diff 검사 통과. token·service role·password는 출력하거나 저장소에 남기지 않았고 임시 CLI와 검증 자원을 정리했다.

### 다음 단계

- PM은 `develop...f591d8db99de79ab5314bf0cefac50f77bd35220`을 새 독립 Reviewer에게 전달한다.
- Reviewer 승인 전 PR·merge는 수행하지 않는다.
