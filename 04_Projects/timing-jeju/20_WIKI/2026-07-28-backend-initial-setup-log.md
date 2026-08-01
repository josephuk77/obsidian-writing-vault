# 2026-07-28 Timing Jeju 백엔드 개발 일지

---
title: "2026-07-28 Timing Jeju 백엔드 초기 환경 구축"
created: "2026-07-28"
tags:
  - type/project
  - status/active
  - area/backend
  - area/infra
---

## 오늘 작업한 내용

Timing Jeju 백엔드 저장소에 Java 21과 Spring Boot 기반 초기 환경을 구축했다. 아직 실제 기능 Issue가 없기 때문에 예시용 Member/Auth 도메인이나 가짜 Entity는 만들지 않았다.

추가한 개발 기반은 다음과 같다.

- 도메인 중심 Package-by-Feature와 도메인 내부 MVC 규칙
- JUnit 5, Spring Test, ArchUnit, JaCoCo, Spotless
- Red → Green → Refactor 강제 개발 흐름
- PM, Developer, Reviewer 역할과 저장소 전용 Codex Skill
- Codex Lifecycle Hook과 Python 단위 테스트
- 브랜치, 커밋, 비밀정보, 테스트 짝을 검사하는 Git Hook
- GitHub Issue Form 9종, PR 템플릿, Label과 Ruleset dry-run 스크립트
- GitHub Actions CI와 로컬 공통 품질 게이트
- non-root 다단계 Docker 이미지와 PostgreSQL/PostGIS smoke test

## 주요 기술 결정

| 항목 | 결정 | 이유 |
| --- | --- | --- |
| 프로젝트 | Timing Jeju API | 기존 문서와 DB 명칭을 기준으로 확정 |
| 기본 패키지 | `com.timingjeju.api` | 프로젝트 명칭과 API 역할을 명확히 표현 |
| Java | 21 | 초기 환경 요구사항과 LTS 기준 |
| Spring Boot | 4.1.0 | 작업일 기준 공식 안정 버전 |
| Gradle | 9.5.1 Wrapper | Spring Initializr가 생성한 공식 Wrapper 고정 |
| 데이터베이스 | PostgreSQL 16 + PostGIS 3.4 | 기존 DB 스키마와 Docker 구성을 보존 |
| 커버리지 기준 | 초기 0% | 아직 비즈니스 코드가 없어 첫 핵심 도메인 Issue에서 상향 예정 |
| 원격 설정 | 저장소·Issue·브랜치 연결 | Label과 Ruleset은 계속 dry-run 유지 |

## 검증 결과

| 검증 | 결과 |
| --- | --- |
| `./gradlew clean check` | 성공 |
| 분류별 단위·Slice·통합·Architecture 테스트 | 성공 |
| JaCoCo 보고서와 커버리지 검증 | 성공 |
| Codex Hook 단위 테스트 12개 | 성공 |
| Git Hook 단위 테스트 7개 | 성공 |
| 모노레포 구조 테스트 5개 | 성공 |
| CI 계약 테스트 4개 | 성공 |
| Skill 4개 구조 검증 | 성공 |
| GitHub YAML 12개 파싱 | 성공 |
| JSON/TOML/Shell 문법 | 성공 |
| Git Hook 설치 | 성공, `core.hooksPath=.githooks` |
| 브랜치·커밋·Issue 번호 정책 | 정상 허용과 오류 차단 확인 |
| `.env`와 실제 형태의 안전한 가짜 토큰 | 차단 확인 |
| placeholder 비밀값 | 허용 확인 |
| Docker 이미지 빌드 | 성공 |
| PostgreSQL/PostGIS Compose 기동 | 성공 |
| Actuator Health Check | 성공 |
| 컨테이너와 임시 볼륨 정리 | 성공 |
| 전체 `quality-gate --setup-validation` | 성공 |
| 작업 브랜치 pre-push 품질 게이트 | 성공 후 원격 push 완료 |

## 해결한 문제

### Gradle 캐시 권한

Codex 샌드박스에서 사용자 홈의 Gradle 캐시에 쓸 수 없어 임시 캐시 경로를 사용했다. 실제 개발 환경에서는 기본 Gradle 캐시를 그대로 사용할 수 있다.

### Spotless 플러그인 ID 변경

Spotless 8.8.0에서 기존 플러그인 ID가 폐기된 것을 첫 실행 오류로 확인했다. `com.diffplug.spotless`로 수정한 뒤 포맷과 전체 빌드가 통과했다.

### ARM Mac의 PostGIS 이미지

기존 `postgis/postgis:16-3.4` 이미지가 amd64라 ARM Mac에서 에뮬레이션 경고가 있었지만 스키마 초기화와 Health Check는 정상 통과했다.

### 비밀정보 스캐너 placeholder 오탐

Spring의 `${VAR:default}` placeholder와 값이 비어 있는 YAML `password:` 다음 줄을 비밀값으로 오탐하는 문제를 Red 테스트로 재현했다. 환경변수 기본값 자체는 계속 검사하면서 안전한 placeholder와 빈 값을 허용하도록 수정했고 단위 테스트 4개를 통과했다.

## 원격 반영 결과

- 저장소: [Timing-Jeju/jeju_BE](https://github.com/Timing-Jeju/jeju_BE)
- Issue: [#1 백엔드 초기 개발 환경 및 협업 품질 게이트 구축](https://github.com/Timing-Jeju/jeju_BE/issues/1)
- 기준 브랜치: `develop`, 기존 `main`과 같은 `c3aea51`
- 작업 브랜치: `chore/1-backend-initial-setup`
- 원격 HEAD: `f70de7e`

| SHA | 작업 단위 |
| --- | --- |
| `ceee1d7` | 프로젝트 기획 및 데이터 기준선 등록 |
| `5b3ba14` | Spring Boot 애플리케이션과 테스트 골격 구성 |
| `3f5d42a` | Codex와 Git 협업 정책 구성 |
| `8d00c53` | GitHub와 Docker 품질 게이트 구성 |
| `3abc3da` | 한국어 프로젝트와 아키텍처 안내 정리 |
| `82fb3df` | Spring API를 모노레포 서비스 경계로 이동 |
| `0a993dc` | 모노레포 CI 운영 안정성 강화 |
| `7471c57` | CI 실행과 검증 기준 문서화 |
| `65d62e6` | FastAPI 최소 개발 환경 구성 |
| `f34ea77` | 서비스별 모노레포 CI 분리 |
| `4903f20` | FastAPI 초기 설정과 CI 경계 문서화 |
| `8798d0b` | Swagger OpenAPI 문서화 기반 추가 |
| `f70de7e` | Swagger 협업과 문서 분리 규칙 정리 |

## 모노레포 전환

- 공통 계약·DB·fixture·GitHub/Codex/Git 정책은 저장소 루트에 유지했다.
- Spring Boot 전용 코드·Gradle Wrapper·Dockerfile을 `services/spring-api/`로 이동했다.
- FastAPI MCP는 `services/fastapi-mcp/`에 배치하도록 경계를 만들었다.
- FastAPI 원본 저장소 URL이 없어 가짜 구현은 추가하지 않고 한국어 README와 AGENTS만 작성했다.
- 루트 Hook·CI·품질 게이트·Compose가 새 Spring 경로를 사용하도록 갱신했다.
- 구조 테스트는 이동 전 19개 subtest 실패로 Red를 확인했고, 이동 후 테스트 5개가 모두 성공했다.

Issue #1에는 커밋 목록과 품질 게이트 성공 증거를 댓글로 남겼다. PR은 만들지 않았으며 Reviewer 승인 후 `$create-pr` 절차로 진행한다.

## CI 운영 안정성 강화

- 기존 GitHub Actions CI가 PR 메타데이터, Java 21, Gradle Wrapper, 전체 품질 게이트와 테스트 리포트 보존을 수행하는지 계약 테스트로 고정했다.
- 동일 브랜치에 새 커밋이 올라오면 이전 실행을 취소하도록 `concurrency` 정책을 추가했다.
- Red 단계에서는 CI 계약 테스트 4개 중 중복 실행 취소 검증 1개가 실패했고, 정책 추가 후 4개가 모두 통과했다.
- 루트 품질 게이트가 `scripts/tests`의 모든 회귀 테스트를 자동 검색하도록 macOS/Linux와 Windows 스크립트를 함께 수정했다.
- 최종 품질 게이트에서 저장소 자동화 테스트 28개, Gradle 전체 검사, JaCoCo, Docker Compose와 Actuator Health Check가 모두 성공했다.

## FastAPI 최소 초기 설정과 서비스별 CI

- Python 3.12, uv, FastAPI 0.139와 MCP Python SDK 안정 버전 1.x를 `pyproject.toml`과 `uv.lock`으로 고정했다.
- Ruff, mypy와 pytest만 기본 품질 도구로 추가하고 `app/`, `src/`, 테스트 디렉터리와 실행 엔트리포인트는 만들지 않았다.
- 실제 Python 구현 파일이 생기면 테스트 파일을 요구하도록 FastAPI 전용 품질 게이트를 작성했다.
- CI를 공통, Spring, FastAPI, 서비스 계약, 최종 집계 Job으로 분리했다.
- Spring 또는 FastAPI만 바뀌면 해당 서비스만 검사하고, 계약 문서가 바뀌면 두 서비스와 계약 검사를 모두 실행하도록 경로 감지기를 추가했다.
- Red 단계에서는 FastAPI 설정 파일 누락, 변경 경로 감지 모듈 부재와 단일 CI Job 때문에 계약 테스트가 실패했다.
- Green 단계에서는 저장소 자동화 테스트 19개, Git Hook 7개, Codex Hook 12개로 총 38개가 성공했다.
- 최종 통합 품질 게이트에서 Spring 전체 검사, Docker Health Check, FastAPI 잠금 동기화와 Ruff 검사가 모두 성공했다.
- FastAPI 실행 코드가 아직 없으므로 mypy와 pytest는 명시적으로 생략되며, 첫 기능 Issue에서 구현과 테스트가 함께 추가되면 자동 실행된다.

## Swagger와 OpenAPI 기반 API 문서화

- 프론트엔드의 API 탐색과 타입·클라이언트 생성을 위해 Spring REST Docs 대신 springdoc-openapi 3.0.3과 Swagger UI를 선택했다.
- Red 단계에서 `/v3/api-docs`와 `/swagger-ui/index.html`이 404를 반환하는 것을 확인했고, 전역 설정·공개 경로 제한·문서 규칙 계약 테스트도 실패했다.
- `OpenApiConfig`에서 한국어 서비스 설명과 v1 정보를 관리하고 `/api/v1/**` 공개 API만 문서에 포함하도록 제한했다.
- Controller 구현에는 Swagger 애노테이션을 누적하지 않고 추가 설명은 `controller/docs/{Domain}ApiDocs` 문서 계약 인터페이스로 분리하는 규칙을 만들었다.
- 공통 인증과 오류 응답은 향후 `OpenApiCustomizer`에서 한 번만 등록하고 DTO의 `@Schema`도 자동 추론이 부족한 필드에만 사용하도록 정했다.
- `openApiDocs` Gradle Task가 실제 애플리케이션의 `/v3/api-docs` 응답을 `build/openapi/openapi.json`으로 저장한다.
- CI는 OpenAPI JSON을 Spring 테스트 리포트와 함께 14일 동안 Artifact로 보존한다.
- 운영 환경에서는 `SPRINGDOC_API_DOCS_ENABLED=false`, `SPRINGDOC_SWAGGER_UI_ENABLED=false`로 문서 접근을 끌 수 있다.
- Green 단계에서 OpenAPI JSON, Swagger UI, 공개 경로 제한 테스트가 통과했고 저장소 자동화 테스트는 23개로 증가했다.

## PR 전 검토와 PR 생성

- `origin/develop...f70de7e` 범위의 Issue 충족 여부, TDD 증거, 보안, 아키텍처, CI, Docker와 서비스 경계를 검토했다.
- 현재 HEAD에서 전체 품질 게이트를 다시 실행해 비밀정보 검사, 자동화 테스트 42개, Spring 테스트·ArchUnit·JaCoCo·OpenAPI, Docker Health Check와 FastAPI Ruff 성공을 확인했다.
- 필수 수정사항 0건으로 Reviewer `APPROVED`를 기록했다.
- 저장소의 `scripts/create-pr.sh`로 `develop` 대상 PR #2를 생성했다.
- PR 정책, 변경 범위 감지, Spring, FastAPI, 공통 정책과 계약 CI가 모두 통과했고 PR #2가 `develop`에 병합됐다.
- 자동 머지는 설정하지 않았다.

## FastAPI MCP 별도 저장소 분리

- 백엔드 [Issue #3](https://github.com/Timing-Jeju/jeju_BE/issues/3)을 만들고 최신 `develop`에서 `chore/3-separate-fastapi-repository` 브랜치를 생성했다.
- `services/fastapi-mcp`의 Git 이력을 subtree로 보존해 공개 [Timing-Jeju/jeju_AI](https://github.com/Timing-Jeju/jeju_AI) 저장소로 이전했다.
- AI 저장소 기본 브랜치를 `develop`로 설정하고 Python 3.12, uv 잠금, Ruff, mypy, pytest와 독립 GitHub Actions CI를 구성했다.
- FastAPI 구현 계약을 `jeju_AI/docs/FASTAPI_MCP_CONTRACT.md`로 옮기고 Spring 연동 계약과 상호 링크했다.
- `app/`, `src/`, 실행 엔트리포인트와 예시 MCP Tool은 만들지 않아 첫 기능 Issue 개발자가 구조를 결정할 수 있게 했다.
- AI 저장소 [Issue #1](https://github.com/Timing-Jeju/jeju_AI/issues/1)과 [PR #2](https://github.com/Timing-Jeju/jeju_AI/pull/2)를 만들었고 전용 CI 통과 후 `develop`에 수동 병합했다.
- 백엔드에서는 FastAPI 소스·uv·Python CI를 제거하고 변경 감지, 품질 게이트, README, 아키텍처와 완료 기준을 Spring 전용으로 정리했다.
- `pre-commit` 훅은 모노레포 구조 테스트 대신 Spring 백엔드 전용 구조 테스트를 실행하도록 변경했다. `pre-push` 훅의 보호 브랜치·force push 차단은 유지하고 Spring 전체 품질 게이트와 Docker smoke test를 실행한다.
- 백엔드 Red 단계에서 구조·CI·계약 테스트 19개 중 13개 실패를 확인했고 Green 단계에서 19개 모두 통과했다.
- AI Red 단계에서 독립 CI·계약 문서 부재로 3개 테스트가 실패했고 Green 단계에서 pytest 3개와 Ruff 검사가 통과했다. 운영 Python 구현이 없어 mypy는 명시적으로 생략됐다.
- 백엔드 전체 품질 게이트에서 자동화 테스트 42개, Spring 포맷·컴파일·단위·슬라이스·통합·ArchUnit·JaCoCo·OpenAPI·bootJar, Docker Compose와 Actuator Health Check가 모두 성공했다.
- 작업 단위를 `e8fd438`, `854c9d8`, `693c58c` 세 커밋으로 나눠 푸시하고 [백엔드 PR #4](https://github.com/Timing-Jeju/jeju_BE/pull/4)를 생성했다.
- GitHub CI 6개 Job과 Reviewer 승인을 확인한 뒤 자동 머지 없이 PR #4를 `develop`에 수동 병합했다. 병합 커밋은 `bcd57f8`이며 Issue #3은 자동 종료됐다.
- 기존 칸반 프로젝트에 `jeju_AI` 저장소를 연결하고 Issue #3을 FastAPI·P1·L·완료 상태로 배치했다.

## Issue #5 Supabase 로컬 개발 환경과 운영 마이그레이션 분리

### 목표

- 로컬 개발은 로컬 Supabase Auth·PostgreSQL/PostGIS를 사용하고 운영은 호스팅된 Supabase Auth·PostgreSQL/PostGIS를 사용하도록 경계를 명확히 한다.
- 운영 마이그레이션이 Supabase 소유 `auth` 스키마, `auth.users`, `auth.uid()`를 변경하거나 `auth.users`에 직접 INSERT하지 못하게 한다.
- 기존 일반 PostgreSQL/PostGIS Docker 검증 경로를 유지하면서 public 애플리케이션 스키마 기준을 `supabase/migrations` 하나로 통합한다.
- Flyway는 도입하지 않고 향후 별도 Issue에서 검토한다.

### 변경 사항

- Supabase CLI 2.110.0용 `supabase/config.toml`과 빈 운영 시드 `supabase/seed.sql`을 추가했다.
- 기존 public 스키마와 `pgcrypto`, `postgis`, `btree_gist` 확장을 `supabase/migrations/20260728000000_initial_public_schema.sql`로 이전했다.
- 일반 PostgreSQL 전용 Auth 호환 객체와 fixture를 `db/local-postgres`에 격리했다.
- 배포 SQL의 Supabase Auth 소유권 침해를 자동 탐지하는 `scripts/deploy_sql_policy.py`와 단위 테스트를 추가했다.
- `scripts/supabase-smoke-test.sh`가 `supabase start`, `supabase db reset` 2회, 확장·46개 public 테이블·빈 시드와 자동 정리를 검증하도록 했다.
- 기존 Docker 스모크 테스트가 Actuator Health Check뿐 아니라 `db/queries/smoke_check.sql`의 PostGIS·스키마·fixture 계약까지 실행하도록 강화했다.
- 로컬·운영 연결 관계, 환경 변수, 초기화, Auth API 기반 테스트 사용자 준비, Flyway 제외 경계를 한국어로 문서화했다.

### Red → Green → Refactor 증거

#### Red

- `python3 -m unittest scripts.tests.test_deploy_sql_policy` 실행에서 현재 `db/init` 구조의 정책 위반 4건을 의도대로 탐지했다.
  - `db/init/002_schema.sql:1`의 auth 스키마 DDL
  - `db/init/002_schema.sql:27`의 `auth.users` 테이블 DDL
  - `db/init/002_schema.sql:45`의 `auth.uid()` 함수 DDL
  - `db/init/003_seed_fixtures.sql:28`의 `auth.users` 직접 INSERT
- Supabase 레이아웃 테스트는 `supabase/config.toml` 부재와 두 Compose 파일의 구형 `db/init` 마운트 때문에 실패했다.
- 반복 초기화·품질 게이트 테스트는 `scripts/supabase-smoke-test.sh`와 독립 정책 검사 단계가 없어 실패했다.
- Docker 계약 테스트는 `compose.test.yml`의 검증 쿼리 마운트와 `psql /queries/smoke_check.sql` 실행이 없어 실패했다.

#### Green

- 정책 분리 후 관련 테스트 10개와 배포 SQL 정책 검사가 모두 성공했다.
- 실제 Supabase CLI 2.110.0으로 `supabase start`와 `supabase db reset` 2회를 수행해 Auth·PostGIS·public 스키마·빈 시드 반복 초기화가 성공했다.
- CLI 미설치, Docker 미설치, Docker daemon 비실행 조건에서 각각 이해 가능한 한국어 오류와 종료 코드 1을 확인했다.
- 일반 PostgreSQL/PostGIS Docker 경로에서 `schema_contract PASS`, `negative_constraints PASS`, fixture와 공간 쿼리 검사가 성공했다.

#### Refactor

- 운영 마이그레이션, 로컬 Supabase 설정, 일반 PostgreSQL Auth 호환 계층, 로컬 fixture, 정책 검사, 두 스모크 실행 경로를 책임별 파일로 분리했다.
- 새 SQL을 파일 목록에 매번 등록하지 않도록 정책 검사기가 저장소 SQL을 자동 탐색하고 `db/local-postgres`만 명시적으로 제외하게 했다.
- `SUPABASE_BIN`과 `DOCKER_BIN`을 입력으로 받아 로컬 설치 경로와 경계 조건을 바꿔 검증할 수 있게 했다.
- Supabase CLI가 출력할 수 있는 로컬 키를 검증 로그에서 숨기고 성공·실패와 관계없이 컨테이너를 정리하게 했다.

### 검증 결과

| 검증 | 결과 |
| --- | --- |
| `python3 scripts/deploy_sql_policy.py` | 성공, 위반 0건 |
| `python3 -m unittest discover -s scripts/tests -p 'test_*.py'` | 성공, 34개 |
| Supabase CLI 미설치 경계 | 의도한 실패, 필요한 버전 2.110.0 안내 |
| Docker 미설치·daemon 비실행 경계 | 의도한 실패, 한국어 원인 안내 |
| `SUPABASE_BIN=... ./scripts/supabase-smoke-test.sh` | 성공, reset 2회와 자동 정리 |
| `./scripts/docker-smoke-test.sh` | 성공, Health Check·PostGIS·스키마·fixture 계약과 자동 정리 |
| `./gradlew clean check` | 성공, 14개 Gradle 작업 |
| `./scripts/quality-gate.sh` | 성공 |
| pre-push 전체 품질 게이트 | 성공 |
| 비밀정보 검사 | 성공 |
| Supabase·timing-jeju-smoke 잔여 컨테이너 | 0개 |

### 주요 결정

- public 스키마의 단일 마이그레이션 기준은 `supabase/migrations`이며 Flyway 의존성·설정·`db/migration`은 추가하지 않는다.
- 운영 적용 가능한 시드는 비워 두고 테스트 사용자는 Supabase Auth API를 통해서만 만든다.
- 일반 PostgreSQL 호환 SQL과 직접 Auth fixture는 `db/local-postgres` 전용이며 운영 적용 대상에서 제외한다.
- 로컬 Supabase는 이 이슈에 필요한 Auth·PostgreSQL·Data API만 켜고 Studio·Storage·Realtime·Edge Runtime·Analytics는 비활성화한다.
- 로컬 Supabase PostgreSQL 17과 기존 Docker PostGIS 16 경로를 각각 실제 실행해 스키마 호환성을 검증한다.

### 커밋과 원격 반영

| SHA | 작업 단위 |
| --- | --- |
| `bc6584f` | Supabase 마이그레이션과 로컬 DB 경로 분리 |
| `aac17a1` | Supabase 환경 분리와 초기화 절차 문서화 |

- 작업 브랜치: `build/5-supabase-local-development`
- 원격 HEAD: `aac17a1dd61b46d946bfe7e7d44223cd0951067c`
- GitHub Issue #5 칸반 상태: `👀 리뷰 대기`
- PR은 만들지 않았으며 Reviewer가 `develop...HEAD`를 검토할 차례다.

### 남은 위험

- 첫 Supabase 이미지 다운로드에서 공개 레지스트리 rate limit이 한 번 발생했다. 재시도 후 성공했지만 새 환경의 네트워크·레지스트리 상태에 따라 최초 시작 시간이 길어질 수 있다.
- ARM Mac에서 기존 `postgis/postgis:16-3.4` amd64 에뮬레이션 경고가 계속 발생하지만 전체 계약 검사는 성공했다.
- 실제 운영 Supabase 프로젝트 생성·연결·`db push`는 범위 밖이라 실행하지 않았다. Reviewer는 운영 소유권 정책과 문서 경계를 중심으로 확인해야 한다.
- Spring Security/JWT와 로그인 API는 후속 Issue 범위다.

## Issue #5 Reviewer MAJOR finding 보완

### Reviewer finding

- Reviewer가 HEAD `aac17a1dd61b46d946bfe7e7d44223cd0951067c`의 `scripts/deploy_sql_policy.py`에 `CHANGES_REQUESTED`를 판정했다.
- 기존 `_strip_comments`가 정규식으로 `--`, `/* */`를 제거해 SQL 문자열 literal 안의 주석 기호까지 실제 주석으로 오인했다.
- 다음 유효 SQL 뒤의 금지 DDL이 잘려 위반 0건으로 통과하는 보안 우회가 있었다.
  - `select '--'; create table auth.users(id uuid);`
  - `select '/*'; create or replace function auth.uid() returns uuid language sql as 'select null'; select '*/';`
- Issue #5의 핵심 인수 조건인 Supabase 소유 객체 변경 차단을 우회할 수 있어 MAJOR finding으로 처리했다.

### Red

- 운영 코드를 수정하기 전에 두 Reviewer 재현을 각각 독립 테스트로 추가했다.
- 실행 명령:
  - `python3 -m unittest scripts.tests.test_deploy_sql_policy.DeploySqlPolicyTest.test_line_comment_marker_inside_string_does_not_hide_following_auth_users_ddl scripts.tests.test_deploy_sql_policy.DeploySqlPolicyTest.test_block_comment_markers_inside_strings_do_not_hide_following_auth_uid_ddl`
- 두 테스트 모두 예상 위반 수 1에 실제 0으로 `FAILED (failures=2)`를 기록했다.
- 동적 `EXECUTE` 보수 정책의 한국어 문서 계약 테스트도 문서 설명 부재로 Red를 확인했다.

### Green

- 실제 SQL 주석만 공백으로 마스킹하고 literal 본문은 보존하는 작은 lexer/state machine으로 교체했다.
- 다음 lexical context를 구분한다.
  - doubled quote가 있는 single-quoted string
  - backslash escape를 지원하는 PostgreSQL E-string
  - doubled quote가 있는 quoted identifier
  - `$$` 및 `$tag$` dollar-quoted body
  - 실제 `--` line comment
  - 중첩된 실제 `/* */` block comment
- 실제 주석을 공백으로 바꿔 토큰 경계와 줄 번호를 보존했다.
- 문자열과 dollar body를 그대로 검사하므로 동적 `EXECUTE` 문자열 안의 금지 SQL도 보수적으로 차단한다.
- 관련 정책·레이아웃 테스트 19개와 전체 `scripts/tests` 42개가 통과했다.

### Refactor

- 함수 이름을 `_mask_comments_preserving_literals`로 바꿔 실제 책임을 드러냈다.
- 범용 SQL 파서를 도입하지 않고 Issue #5의 주석 경계 판별에 필요한 상태만 구현했다.
- SQL 파일의 단순 안내 문자열도 동적 SQL로 간주될 수 있어 금지 문구를 허용하지 않는 보수 정책과 trade-off를 `db/README.md`에 한국어로 명시했다.
- 실제 주석 무시, 줄바꿈·quoted identifier, standard/E-string escaped quote, 무태그·태그 dollar quote, 동적 `EXECUTE`를 회귀 테스트로 고정했다.

### 재검증 결과

| 검증 | 결과 |
| --- | --- |
| 정책·레이아웃 테스트 19개 | 성공 |
| `python3 scripts/deploy_sql_policy.py` | 성공, 위반 0건 |
| 전체 `scripts/tests` 42개 | 성공 |
| `./gradlew clean check` | 성공, 14개 Gradle 작업 |
| Supabase CLI 2.110.0 `start` | 성공 |
| `supabase db reset` 2회 | 성공 |
| Auth·PostGIS·46개 public 테이블·빈 시드 | 성공 |
| `./scripts/docker-smoke-test.sh` | 성공 |
| `schema_contract`, `negative_constraints`, PostGIS 공간 쿼리 | 모두 PASS |
| `./scripts/quality-gate.sh` | 성공 |
| pre-push 전체 품질 게이트 | 성공 |
| 비밀정보 검사·`git diff --check` | 성공 |
| 잔여 컨테이너·네트워크·볼륨·임시 CLI | 0개 |

### 커밋과 인계

- 수정 커밋: `e16fd4d` — `fix: #5 SQL 주석 우회 정책 검사 보완`
- 새 원격 HEAD: `e16fd4dfd848a000ea5e71e2998749a4692d112d`
- 작업 브랜치: `build/5-supabase-local-development`
- force push 없이 동일 원격 브랜치에 일반 push했다.
- PR, 승인 파일, develop 머지는 생성하지 않았다.
- Reviewer는 문자열 상태 전환, E-string backslash escape, dollar quote 종료, 중첩 block comment와 동적 SQL의 보수 정책을 집중 검토해야 한다.

## Issue #5 두 번째 Reviewer MAJOR·MINOR finding 보완

### Reviewer finding

- 두 번째 독립 Reviewer가 HEAD `e16fd4dfd848a000ea5e71e2998749a4692d112d`에 `CHANGES_REQUESTED`를 판정했다.
- MAJOR 1: dollar-quote 태그가 ASCII 정규식에 한정되어 `$한글$`, `$é$` 본문의 `--`, `/*`를 실제 주석으로 오인했고, 반대로 `public.foo$guard$` 같은 식별자 내부 표기를 dollar quote로 오인했다.
- MAJOR 2: 정규식 DDL 검사가 `ALTER TABLE ONLY`, `CREATE UNLOGGED TABLE`, `CREATE FOREIGN TABLE`, `ALTER TABLE IF EXISTS ONLY` 수식어를 처리하지 못해 Supabase 소유 객체 변경을 놓쳤다.
- MINOR: 동적 SQL 우회 차단 문구가 실제 보장보다 넓었고 문자열 연결과 `format(...)` 의미 분석 한계가 문서에 없었다.

### Red

- 운영 스크립트를 수정하기 전에 Unicode dollar tag, 앞 식별자 토큰 경계, 정상 종료, 닫히지 않은 delimiter/EOF 테스트를 추가했다.
- dollar tag Red 명령에서 `$한글$--$한글$`와 `$é$/*$é$` 뒤 금지 DDL, 닫히지 않은 `$미종료$`의 금지 DDL이 예상 1건 대신 0건으로 실패했다.
- `public.foo$guard$-- create table auth.users...`는 실제 주석인데 1건으로 오탐해 실패했다.
- DDL 수식어 Red 명령에서 `ONLY`, `UNLOGGED`, `FOREIGN`, `IF EXISTS ONLY`, 대소문자·줄바꿈·실제 주석·quoted identifier 조합 5개가 모두 예상 1건 대신 0건으로 실패했다.
- 문서 계약 테스트는 `문자열 연결`, `format(...)`, `의미 분석`, `코드 리뷰` 설명이 없어 실패했다.

### Green

- PostgreSQL 식별자 규칙의 underscore·letter·non-ASCII 시작 문자와 숫자·`$` 후속 문자를 반영해 Unicode dollar tag를 인식했다.
- dollar delimiter 앞 문자가 식별자 연속 문자이면 시작 delimiter로 보지 않아 `foo$guard$` 뒤 실제 주석을 정확히 제외했다.
- 주석 마스킹 뒤 원문 위치를 보존하는 작은 SQL token scanner를 추가했다.
- scanner는 DDL verb, create modifier, object type, `IF EXISTS`, `ONLY`, `auth.users`·`auth.uid()` qualified name 순서만 검사한다.
- `FOREIGN TABLE`, `MATERIALIZED VIEW`, table/view와 function/procedure/routine 보호 대상을 선언적으로 분리했다.
- 정책·레이아웃 테스트 26개, 전체 scripts 테스트 49개와 배포 SQL 정책 검사가 모두 통과했다.

### Refactor

- lexical context 판별과 statement/object 정책 매칭 책임을 `_dollar_quote_delimiter_at`, `_sql_tokens`, `_match_ddl`, `_qualified_owned_name` 등 작은 함수로 분리했다.
- 정규식 변형 나열을 없애고 object type tuple을 추가할 수 있는 구조로 바꿨다.
- 범용 SQL 파서나 실행 의미 평가기는 만들지 않았다. 직접 문자열의 연속 금지 토큰은 보수적으로 검사하지만 문자열 연결과 `format(...)`으로 만들어지는 객체명은 자동 의미 분석 범위 밖이다.
- 이 한계를 `db/README.md`에 한국어로 명시하고 자동 검사 통과와 별개로 코드 리뷰가 필요하다고 기록했다.

### 재검증 결과

| 검증 | 결과 |
| --- | --- |
| 정책·레이아웃 테스트 26개 | 성공 |
| `python3 scripts/deploy_sql_policy.py` | 성공, 위반 0건 |
| 전체 `scripts/tests` 49개 | 성공 |
| `./gradlew clean check` | 성공, 14개 Gradle 작업 |
| Supabase CLI 2.110.0 `start` | 성공 |
| `supabase db reset` 2회 | 성공 |
| Auth·PostGIS·public 스키마·빈 시드 | 성공 |
| `./scripts/docker-smoke-test.sh` | 성공, Health Check·계약·PostGIS PASS |
| `./scripts/quality-gate.sh` | 성공 |
| 비밀정보 검사·`git diff --check` | 성공 |
| 잔여 컨테이너·네트워크·볼륨·임시 CLI | 0개 |

### 커밋과 남은 위험

- 수정 커밋: `cc1ba08` — `fix: #5 PostgreSQL 정책 검사 경계 보완`
- 작업 브랜치: `build/5-supabase-local-development`
- 문자열 연결과 `format(...)` 동적 SQL은 의미 분석하지 않으므로 Reviewer가 문서화된 코드리뷰 경계와 token adjacency 동작을 집중 확인해야 한다.
- PostgreSQL 16·17에서 Reviewer가 유효성을 확인한 DDL 수식어 문법을 정책 회귀 입력으로 유지했다.
- ARM Mac의 PostGIS amd64 에뮬레이션 경고는 남지만 전체 Docker 계약은 성공했다.

## Issue #5 세 번째 Reviewer DROP 다중 대상 finding 보완

### Finding과 Red

- 세 번째 Reviewer가 HEAD `cc1ba0849d34b2ffd554b4ea8e5ef10378043a09`의 DROP 다중 대상 검사를 MAJOR로 판정했다.
- 기존 `_match_ddl`은 첫 qualified target이 안전하면 바로 반환해 다음 두 PostgreSQL 16 유효 문장을 놓쳤다.
  - `DROP SCHEMA public_review_safe, auth CASCADE;`
  - `DROP TABLE public.review_safe_table, auth.users CASCADE;`
- 운영 코드 수정 전에 safe-first/protected-later, 보호 대상 첫째·중간·마지막, 선언된 DROP 객체 유형, 함수 인자 쉼표, 안전 대상 목록 테스트를 추가했다.
- Reviewer 재현은 위반 2건 예상 대비 0건, 중간·마지막 및 객체 유형 subtest 8개가 예상 1건 대비 0건으로 실패했다.

### Green과 Refactor

- 기존 scanner 안에 `_drop_target_starts`만 추가했다.
- 괄호 깊이 0의 쉼표만 다음 DROP target 경계로 처리하고 함수 인자 괄호 내부 쉼표는 무시한다.
- 세미콜론과 target 뒤 `CASCADE`·`RESTRICT`에서 statement scan을 종료한다.
- 기존 schema/object matcher를 첫째·중간·마지막 target 시작 위치에 재사용했다.
- `SCHEMA`, `TABLE`, `FOREIGN TABLE`, `MATERIALIZED VIEW`, `FUNCTION`, `PROCEDURE`, `ROUTINE` 외 정책 범위로 확장하지 않았다.
- 안전 target만 여러 개인 DROP은 0건을 유지했다.

### 재검증

| 검증 | 결과 |
| --- | --- |
| 정책·레이아웃 테스트 | 30개 성공 |
| 전체 `scripts/tests` | 53개 성공 |
| Reviewer 임시 migration | exit 1, DROP 줄 1·3에서 위반 2건 |
| `python3 scripts/deploy_sql_policy.py` | 성공, 저장소 위반 0건 |
| `./gradlew clean check` | 성공, 14개 Gradle 작업 |
| Supabase CLI 2.110.0 start/reset 2회 | 성공 |
| `./scripts/docker-smoke-test.sh` | 성공 |
| `./scripts/quality-gate.sh` | 모든 단계 성공 |
| 비밀정보·`git diff --check` | 성공 |
| 잔여 컨테이너·네트워크·볼륨·임시 파일 | 0개 |

### 커밋과 위험

- 커밋: `908f804` — `fix: #5 DROP 다중 대상 정책 검사 보완`
- 범용 parser나 새 문법 탐색은 하지 않았고 확정된 DROP 목록 경계만 보완했다.
- ARM Mac의 PostGIS amd64 에뮬레이션 경고는 유지되지만 모든 계약 검사가 성공했다.

## 다음 작업

- [x] Chore Issue #1을 생성한다.
- [x] Issue 번호가 포함된 작업 단위별 커밋 6개를 만든다.
- [x] 원격 저장소와 `develop` 브랜치를 연결한다.
- [x] 작업 브랜치를 품질 게이트 통과 후 push한다.
- [x] Spring API를 `services/spring-api`로 이동하고 FastAPI MCP 경계를 만든다.
- [x] GitHub Actions CI 계약 테스트와 중복 실행 취소 정책을 추가한다.
- [x] FastAPI의 구조 중립적인 Python·uv·품질 도구 기반을 추가한다.
- [x] CI를 공통·Spring·FastAPI·계약·최종 집계 Job으로 분리한다.
- [x] Swagger UI와 OpenAPI JSON 생성 및 CI Artifact 보존을 구성한다.
- [x] Controller 애노테이션을 줄이는 문서 계약 인터페이스 규칙을 작성한다.
- [x] `$pre-pr-review`로 Reviewer 검토를 수행한다.
- [x] Reviewer 승인 후 `$create-pr`로 `develop` 대상 PR #2를 만든다.
- [ ] dry-run으로 준비한 Label과 Ruleset을 검토한 뒤 적용한다.
- [ ] 첫 핵심 도메인 Issue에서 의미 있는 JaCoCo 기준으로 상향한다.

## GitHub Projects 칸반 구성

- Timing-Jeju 조직에 공개 프로젝트 `🧭 Timing Jeju 개발 로드맵`을 생성하고 `jeju_BE` 저장소에 연결했다.
- 기본 뷰를 상태별 `칸반 보드` 레이아웃으로 구성했다.
- 상태를 `📥 백로그 → 📝 준비 → 🚧 진행 중 → 👀 리뷰 대기 → ✅ 완료`로 정리했다.
- 카드에 `우선순위`, `작업 영역`, `규모`가 바로 표시되도록 구성했다.
- 완료된 Issue #1과 병합 PR #2를 완료 카드로 연결했다.
- 관광·교통 데이터, Spring API, FastAPI MCP, 서비스 계약, 프론트 협업, 운영 기반은 이슈를 미리 남발하지 않도록 초안 Epic 카드로 추가했다.
- 다음 착수 후보인 관광·교통 데이터 Epic만 `📝 준비`로 두고 나머지는 `📥 백로그`로 배치했다.
- 실제 개발 직전에 초안 카드를 Issue로 전환하고 Acceptance Criteria를 구체화하는 운영 원칙을 프로젝트 README에 기록했다.

프로젝트: https://github.com/orgs/Timing-Jeju/projects/1

## 나의 한 줄 평

오늘은 기능을 서두르기 전에 테스트, 리뷰, Docker와 Git 정책이 같은 기준으로 움직이는 개발 레일을 만들고 Spring과 FastAPI가 함께 성장할 모노레포 경계까지 세웠다.
