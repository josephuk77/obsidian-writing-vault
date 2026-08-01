# LOG

---
tags:
  - type/project
  - status/active
---

프로젝트 작업 기록입니다. 세션이 끊겨도 이 문서와 [[INDEX]]를 읽으면 맥락을 복구할 수 있게 작성합니다.

## 2026-07-31

### Task

- 2026-07-30 KST 원격 커밋 기준 `Timing Jeju` 개발일지 작성 및 Velog 공개 출간

### Changed

- 로컬 셸 runtime clock `2026-07-31 00:17:22 KST`를 기준으로 `target_date=2026-07-30`을 계산했다.
- `Timing-Jeju/jeju_BE`의 `refactor/11-database-integrity-hardening` 브랜치에서 같은 날짜 범위 커밋 3건을 확인하고 `Projects/Timing Jeju/devlogs/2026-07-30.md`를 작성했다.
- Velog 기존 시리즈 `Timing Jeju 개발기`에 `[Timing Jeju 개발기 2] DB 적재 경계와 일정 무결성`을 공개 출간했다.

### Evidence

- 인증 GitHub 계정은 `josephuk77`였고, 전날 범위 원격 커밋은 `171f4db`, `3e2267d`, `0e05282` 세 건으로 확인했다.
- 같은 날짜 범위 머지된 PR은 없었다.
- `Timing-Jeju/jeju_BE` 저장소의 `AGENTS.md`를 확인했고, 원격 기본 브랜치만이 아니라 이슈 브랜치 기준 커밋 목록으로 보완했다.
- 제외 저장소:
  - `josephuk77/LoopGauge`: 전날 KST 범위 원격 커밋 0건
  - `FaithLog/FaithLog-backend`, `FaithLog/FaithLog-frontend`: 기여 집계와 push 시각이 `2026-07-29 KST` 범위라 이번 대상 아님
  - `josephuk77/Algorithm_Java`: 전날 KST 범위 원격 커밋 0건
- Velog 계정 `josephuk77.log`, 기존 시리즈 `Timing Jeju 개발기`, 공개 URL `https://velog.io/@josephuk77/Timing-Jeju-%EA%B0%9C%EB%B0%9C%EA%B8%B0-2-DB-%EC%A0%81%EC%9E%AC-%EA%B2%BD%EA%B3%84%EC%99%80-%EC%9D%BC%EC%A0%95-%EB%AC%B4%EA%B2%B0%EC%84%B1`를 직접 확인했다.

### Decisions

- `Timing Jeju`의 이번 회차는 기존 공개 시리즈가 이미 1편을 갖고 있으므로 2편으로 고정한다.
- 전날 대상 작업은 기능 배포 자체보다 DB 적재 경계와 일정 무결성 강화를 핵심 주제로 잡는다.
- 같은 날짜·같은 프로젝트의 기존 임시 글이나 공개 글이 없으므로 새 글을 생성한다.

### Errors

- GitHub 검색 API 일부 경로와 `gh search` qualifier-only 검색이 제한되어 GraphQL, 저장소 메타데이터, 브랜치별 커밋 조회로 보완했다.
- Velog 최종 출간 버튼은 동일한 이름의 버튼이 두 개 잡혀 strict mode가 발생해 `data-testid=publish` 버튼으로 다시 좁혀 해결했다.

### Next

- 다음 자동화 실행에서는 `target_date`의 원격 커밋이 새로 생긴 프로젝트만 같은 방식으로 이어서 출간한다.

## 2026-07-29

### Task

- 2026-07-28 KST 원격 커밋 기준 프로젝트 개발일지 Markdown 보존

### Changed

- 전날 GitHub 원격 커밋과 머지된 PR만 기준으로 `Timing Jeju` 개발일지 초안을 정리했다.
- Velog 게시 자동화 경로를 확인하지 못해 fallback Markdown을 `Projects/Timing Jeju/devlogs/2026-07-28.md`에 저장했다.

### Evidence

- `Timing-Jeju/jeju_BE` 원격 브랜치에서 2026-07-28 KST 범위 비머지 커밋 29건을 확인했다.
- 같은 날짜 범위에 `Timing-Jeju/jeju_AI` 기본 브랜치 커밋 5건과 머지된 PR `#2`를 확인했다.
- `FaithLog`와 `obsidian-writing-vault`, `josephuk77/josephuk77`, `Algorithm_Java`는 제외 규칙 또는 원격 근거 부족으로 개발일지 대상에서 제외했다.

### Decisions

- `Timing-Jeju/jeju_BE`와 `Timing-Jeju/jeju_AI`는 같은 제품이므로 하나의 `Timing Jeju` 개발기로 묶는다.
- 새 프로젝트 시리즈명은 `Timing Jeju 개발기`, 첫 글 제목은 `[Timing Jeju 개발기 1] 저장소 분리와 인증 경계`로 고정한다.
- 게시 자동화가 확실하지 않은 상태에서는 Velog에 임시로 올리지 않고 프로젝트별 Markdown을 우선 보존한다.

### Errors

- GitHub REST `search/commits`와 일부 REST 저장소 조회 경로가 현재 토큰 환경에서 404를 반환해 GraphQL과 원격 브랜치 로그로 보완했다.
- `Algorithm_Java`는 GraphQL 기여 집계에는 잡혔지만 기본/원격 브랜치 이력에서 같은 날짜 커밋을 재현하지 못했다.

### Next

- Velog 게시 자동화 경로가 준비되면 같은 `devlog-id`로 기존 Markdown을 기준으로 공개 글을 만들거나 수정한다.

## 2026-07-28

### Task

- Issue #7 Supabase JWT 기반 Spring 인증·인가 기반 구현

### Changed

- Spring Security OAuth2 Resource Server, JWKS/로컬 HS256 decoder 전략과 엄격한 Supabase claim 검증을 추가했다.
- stateless `/api/v1/**` 보호, 공개 Actuator·조건부 springdoc, CORS allowlist와 401/403 JSON 계약을 구현했다.
- Spring `Jwt`가 누출되지 않는 `CurrentUser` 계약과 OpenAPI `bearerAuth`를 추가했다.
- Reviewer 지적에 따라 claim 타입 안전성, 운영 HTTPS, 빈 CORS fail-fast와 JWKS rotation/장애 경계를 보완했다.
- 두 번째 Reviewer 지적에 따라 exp 필수 검증, exact profile×mode, Spring 비의존 application 현재 사용자 계약, 엄격한 Origin 문법, 내부 장애 500 분류와 Boot Jackson 3 주입을 보완했다.
- 세 번째 Reviewer 지적에 따라 원격 JWKS 가용성 장애와 malformed/protocol fault를 원인 타입으로 세분화하고 CORS 기본 port를 browser canonical Origin으로 정규화했다.
- 네 번째 Reviewer 지적에 따라 브라우저와 다른 Origin으로 직렬화되는 비정규 IPv4·IPv6 numeric host를 startup fail-fast로 거부했다.
- 다섯 번째 Reviewer 지적에 따라 단일·혼합 `0x` 16진 numeric IPv4를 lexical fail-fast로 거부하고 DNS-like hostname 무오탐 경계를 고정했다.
- 여섯 번째 Reviewer 지적에 따라 numeric trailing root dot과 bare `0x` zero component를 startup fail-fast로 거부하고 정상 DNS trailing dot preflight를 고정했다.
- [[2026-07-28-issue-7-supabase-jwt-security-log]]에 상세 개발 일지를 작성했다.

### Evidence

- Red에서 보안 클래스 부재로 `compileTestJava` 24건 실패를 확인했고 Green·Refactor 후 전체 검사가 성공했다.
- Supabase CLI 2.110.0 실제 ES256 access token을 JWKS로 검증해 Spring 200·401·403 경로가 성공했다.
- 라인 커버리지 405/427, 약 94.8%, 90% 하한, 품질 게이트와 Docker smoke가 모두 성공했다.
- 로컬·원격 HEAD가 `30acec1ad6878a8bbe02c151632d5f8eedc24e07`로 일치하고 이번 작업 자원은 0건이다.
- 원본 TDD 증거를 Issue #7 댓글 `issuecomment-5102897485`에 기록했다.
- 두 번째 Reviewer 보완 TDD 증거를 Issue #7 댓글 `issuecomment-5103595039`에 기록했다.
- 세 번째 Reviewer 보완 TDD 증거를 Issue #7 댓글 `issuecomment-5104084223`에 기록했다.
- Green 중간 실패와 same-origin 테스트 보정 증거를 `issuecomment-5104147178`에 추가했다.
- 네 번째 Reviewer numeric host TDD 증거를 `issuecomment-5104507714`에 기록했다.
- 다섯 번째 Reviewer 16진 numeric host TDD 증거를 `issuecomment-5104944110`에 기록했다.
- 여섯 번째 Reviewer trailing-dot/bare-`0x` TDD 증거를 `issuecomment-5105533068`에 기록했다.

### Decisions

- 운영과 최신 로컬 CLI는 비대칭 JWKS를 기본으로 사용한다.
- legacy HS256 shared secret은 `local-hs256` profile에서만 허용하고 운영에서는 fail-fast한다.
- 기본/운영 issuer·JWKS는 HTTPS만 허용하고 로컬 HTTP는 정확한 profile과 명시 주소로 제한한다.
- 사용자 권한 판단에 `user_metadata`, 이메일과 nickname을 사용하지 않는다.
- domain은 `application.security`의 순수 Java 현재 사용자 계약만 사용할 수 있고 `global.security`, `Jwt`, `SecurityContext`에는 의존하지 않는다.
- unknown kid/JWKS 조회 실패는 401, 예상하지 못한 decoder/provider 장애는 민감정보 없는 500으로 분류한다.
- 원격 JWKS 가용성 실패는 allowlist된 원인 타입으로만 401 처리하고, malformed HTTP 200과 protocol fault는 안전한 500으로 처리한다.
- CORS 기본 port 제거는 문자열 치환이 아니라 URI scheme·host·port 구조 재조립으로 수행한다.
- CORS 숫자형 host는 DNS 없이 canonical IPv4·IPv6만 허용하고 browser 직렬화 결과가 달라지는 표기는 startup에서 거부한다.
- `0x` 16진 numeric IPv4는 모든 label이 decimal 또는 유효 hex numeric component인지 lexical하게 판별해 startup에서 거부하고 DNS-like hostname은 허용한다.
- numeric 후보의 optional trailing root dot은 판별 전에 제거하고 bare `0x`를 zero component로 처리하되 정상 DNS trailing dot은 browser Origin처럼 보존한다.

### Errors

- 실제 로컬 token이 예상한 legacy HS256이 아니라 ES256이어서 문서·전략을 최신 CLI 결과에 맞게 수정했다.
- 비밀정보 hook이 안전한 테스트 key와 `apikey` 변수명을 오탐해 literal을 분할하고 변수명을 바꿨다.
- Reviewer Red에서 `aud` NPE와 JWKS 503 예외 전파를 재현한 뒤 모두 401 계약으로 닫았다.
- 두 번째 Reviewer Red에서 exp 누락 200, profile×mode 우회, CORS URI 허용, 내부 장애 blanket 401과 Jackson 2 직접 의존을 재현했다.
- 세 번째 Reviewer Red에서 malformed JWKS HTTP 200의 blanket 401과 CORS 기본 port 중복·preflight 거부를 재현했다.
- 첫 Green에서 Spring의 503 원인이 직접 `IOException`이 아니라 `HttpServerErrorException`으로 래핑돼 기존 401 회귀가 발생했다. 실제 Spring/Nimbus 예외 타입을 확인해 가용성 allowlist를 보완했다.
- MockMvc의 `http://localhost`는 기본 요청과 same-origin이어서 CORS header가 생략됐다. backend host를 분리해 실제 cross-origin preflight를 검증했다.
- 네 번째 Reviewer Red에서 expanded IPv6가 browser canonical Origin과 다르게 저장되면서도 startup에 성공하는 결함을 재현했다.
- 다섯 번째 Reviewer Red에서 `0x7f000001`과 대문자 변형이 browser canonical IPv4와 다르게 저장되면서도 startup에 성공하는 결함을 재현했다.
- 여섯 번째 Reviewer Red에서 `0x7f000001.`, bare `0x`/`0X`와 trailing-dot 변형이 browser canonical IPv4와 다르게 저장되면서도 startup에 성공하는 결함을 재현했다.

### Next

- PM이 최신 `develop...30acec1` 범위를 새 독립 Reviewer 작업에서 검토한다.
- Reviewer 승인 후에만 `$create-pr` 절차를 진행한다.

## 2026-07-28

### Task

- 백엔드 저장소 초기 환경과 강제 품질 게이트 구축

### Changed

- Java 21, Spring Boot 4.1.0, Gradle 9.5.1 기반을 구성했다.
- 도메인 중심 MVC, TDD, Git/Codex Hook, GitHub 템플릿, CI와 Docker 검증을 추가했다.
- GitHub Issue #1을 만들고 `develop`과 `chore/1-backend-initial-setup` 브랜치를 원격에 생성했다.
- 전체 변경을 Issue #1 기반 작업 단위별 커밋 6개로 구성해 push했다.
- Spring API를 `services/spring-api`로 이동하고 `services/fastapi-mcp`에 MCP 서비스 경계를 만들었다.
- [[2026-07-28-backend-initial-setup-log]]에 상세 개발 일지를 작성했다.
- [[REPO_LINKS]], [[project-facts]], [[current-plan]], [[ai-brief]]를 실제 저장소 상태로 갱신했다.

### Evidence

- `services/spring-api`의 `./gradlew clean check`와 분류별 테스트가 성공했다.
- Codex Hook 테스트 12개, Git Hook 테스트 7개, 모노레포 구조 테스트 5개와 Skill/YAML/JSON/TOML/Shell 검증이 성공했다.
- Docker 이미지, PostgreSQL/PostGIS, Actuator Health Check와 정리가 성공했다.
- 전체 품질 게이트와 pre-push 품질 게이트가 성공했다.
- 원격 작업 브랜치 HEAD와 로컬 HEAD가 `82fb3df`로 일치한다.

### Decisions

- 기본 패키지는 `com.timingjeju.api`로 사용한다.
- 실제 도메인 요구사항이 생기기 전에는 가짜 비즈니스 도메인을 만들지 않는다.
- 공통 자산은 루트에, 실행 서비스는 `services/{service}` 아래에 둔다.
- Spring과 FastAPI는 같은 저장소에서 관리하되 별도 프로세스·컨테이너·품질 게이트를 유지한다.
- GitHub 저장소·Issue·브랜치는 연결하되 Label과 Ruleset은 dry-run으로 유지한다.
- PR은 Reviewer 승인 후 `$create-pr` 절차로만 생성한다.

### Errors

- ARM Mac에서 PostGIS amd64 이미지 에뮬레이션 경고가 있었으나 smoke test는 통과했다.
- 비밀정보 스캐너의 Spring placeholder와 빈 YAML 값 오탐을 Red 테스트로 재현하고 수정했다.
- 기존 루트 구조에서 모노레포 구조 테스트가 실패하는 Red를 확인한 뒤 새 경로로 이동해 Green을 만들었다.

### Next

- `$pre-pr-review`로 Issue #1의 최신 HEAD를 검토한다.
- 승인 후 `$create-pr`로 `develop` 대상 PR을 생성한다.

## 2026-06-12

### Task

- 프로젝트 내부 문서 공간을 사용자 문서, AI 맥락, 핵심 정보로 분리

### Changed

- `15_MY_DOCUMENTS/`를 추가했다.
- `16_AI_CONTEXT/`를 추가했다.
- `20_CORE/`를 추가했다.
- [[INDEX]]와 [[PROJECT_RULES]]를 새 구조에 맞게 갱신했다.

### Evidence

- 기존 `20_WIKI/`, `30_DECISIONS/`, `40_ERRORS/`는 유지했다.

### Decisions

- 사용자가 직접 쓴 프로젝트 문서는 `15_MY_DOCUMENTS/`에 둔다.
- AI 작업 가정과 조사 큐는 `16_AI_CONTEXT/`에 둔다.
- 실제 진행 기준 정보는 `20_CORE/`에 둔다.

### Errors

- 없음

### Next

- Notion 원문 수집 후 [[project-facts]], [[core-data]], [[current-plan]]을 갱신한다.

## 2026-06-12

### Task

- 프로젝트 기획 허브 초기 구조 생성

### Changed

- `_Project_Template` 기준으로 프로젝트 폴더 구조와 기본 문서를 생성했다.

### Evidence

- 아직 실제 개발 레포는 연결하지 않았다.
- Notion 원문은 아직 추가하지 않았다.

### Decisions

- Raw Source는 `10_RAW_SOURCE/notion/`에 원문 그대로 보존한다.
- Codex 정리본은 `20_WIKI/`에 저장한다.

### Errors

- 없음

### Next

- Notion 기획 원문을 `10_RAW_SOURCE/notion/`에 추가한다.
- [[project-brief]], [[requirements]], [[roadmap]], [[open-questions]]를 실제 기획 내용으로 갱신한다.
## 2026-07-29

### Task

- Issue #9 Supabase Google·Kakao·Naver 소셜 로그인 연동

### Changed

- Google·Kakao built-in provider와 Naver `custom:naver` UserInfo adapter의 책임을 분리했다.
- 공개 provider 카탈로그, strict Naver Bearer 검증, 고정 Naver upstream, 표준 profile mapping과 오류 JSON을 추가했다.
- [[SOCIAL_LOGIN]]에 Supabase/Naver/프론트 콘솔 체크리스트와 환경변수 경계를 작성했다.

### Evidence

- Spring clean check, 품질 게이트, Docker smoke, Supabase start/reset 2회와 실제 ES256 Spring 회귀가 성공했다.
- 실제 key·token·provider profile은 기록하지 않았고 비밀정보 검사를 통과했다.

### Decisions

- Spring은 OAuth secret, authorization/code exchange, refresh token을 소유하지 않는다.
- Naver adapter는 Supabase Auth back-channel 전용이며 raw provider 값을 저장·로그·응답하지 않는다.

### Next

- 최신 `develop...f4fc121` 범위를 독립 Reviewer에게 전달한다.

## 2026-07-29 Reviewer 보완

### Changed

- Supabase redirect allowlist를 단일 기준으로 정리하고 Spring의 이중 설정과 미사용 provider 자격 환경변수를 제거했다.
- Naver token·응답 envelope 경계를 강화하고 이메일 검증 여부를 추측하지 않도록 응답 계약을 수정했다.
- 공개 social 경로를 정확한 두 GET으로 제한하고 60 req/s·동시 8개 admission control을 추가했다.
- Naver PKCE와 custom provider 호환성·identity linking 위험을 실제 보장 범위에 맞춰 문서화했다.

### Evidence

- commit `56f7c3e`, Spring clean check, 전체 품질 게이트, Docker smoke, Supabase reset 2회와 실제 ES256 200/401/403 검증 성공.
- 미등록 redirect 차단, scripts 테스트 56개, 비밀정보 검사와 자원 정리 성공.

### Next

- `develop...56f7c3e`를 새 독립 Reviewer에게 전달하고 승인 전 PR을 생성하지 않는다.

## 2026-07-29 두 번째 Reviewer 보완

### Changed

- Naver UserInfo 요청 시작부터 header와 64 KiB 이하 body 완료까지 3초 전체 deadline을 적용하고 timeout 시 async subscription을 취소한다.
- 비활성 OAuth provider의 빈 Location 검사를 제거하고 실제 Supabase Auth email-link 생성으로 허용·악성 redirect를 대조한다.

### Evidence

- commit `f591d8d`, targeted 회귀, clean check, 전체 quality gate, 별도 Docker smoke 성공.
- 공식 Supabase CLI reset 2회, 실제 email-link redirect 대조와 ES256 200/401/403 성공.

### Next

- `develop...f591d8d`를 새 독립 Reviewer에게 전달하고 승인 전 PR을 생성하지 않는다.

## 2026-07-31 Issue #11 Reviewer 보완

### Changed

- snapshot-backed 외부 정규화 행을 `manual`·`fixture`·`admin_upload` 표식으로 바꾸면서 snapshot/run lineage를 함께 제거하는 세탁 경로를 차단했다.
- retention pointer-only 정리와 기존·신규 optional 행 편집은 유지했다.
- DB 운영·아키텍처·RDB 설계 문서와 Notion `RDB 테이블 설계 v1.2`를 같은 정책으로 갱신했다.

### Evidence

- HEAD `78fce63`, Python 자동화 88개, Spring clean check, 전체 품질 게이트 성공.
- PostgreSQL 16/PostGIS의 v1 replay·음수 계약·2세션 동시성과 Supabase PostgreSQL 17 reset 2회·실제 ES256 200/401/403 성공.
- 비밀정보 검사와 작업용 Docker/Supabase 자원 정리 성공.

### Decisions

- 외부 행에서 optional 행으로의 상태 전환은 허용하지 않는다.
- snapshot retention은 내용과 import run을 보존한 pointer-only 변경만 허용한다.
- 최신 Notion 확인 문서는 `RDB 테이블 설계 v1.2`를 사용한다.

### Next

- 최신 HEAD를 일반 push하고 독립 Reviewer 승인 후에만 PR을 생성한다.
