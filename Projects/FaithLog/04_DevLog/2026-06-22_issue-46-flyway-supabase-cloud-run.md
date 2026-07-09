---
project: FaithLog
type: devlog
issue: #46
status: done
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - flyway
  - cloud-run
  - supabase
---

# #46 Flyway 마이그레이션과 Supabase/Cloud Run 배포 DB 설정 정리

## 1. 작업 배경

Issue #46은 MVP 도메인 모델이 안정화된 뒤 Flyway를 다시 도입하고, Supabase PostgreSQL과 Google Cloud Run 배포 기준을 정리하는 작업이다. 사용자는 새 Supabase DB 기준, 추천 Supabase 연결/설정 문서화 방식, Cloud Run 기준 배포 문서화를 승인했다. Nginx, Certbot, 직접 80/443 포트 구성은 이번 범위에서 제외했다.

## 2. 최종 설계 기준

- 새 Supabase PostgreSQL DB에 Flyway V1 초기 스키마를 적용한다.
- Notion ERD `Ref` 관계는 FK로 반영하되, 별도 승인 없는 delete cascade는 추가하지 않는다.
- `charge_items.source_id`는 `source_type`에 따라 여러 테이블을 가리키는 polymorphic reference라 FK를 두지 않는다.
- Cloud Run은 `PORT`와 환경변수/secret injection으로 실행한다.
- 실제 Supabase URL, DB password, JWT secret, Firebase Admin key는 저장소, 문서, 로그, 커밋, PR에 남기지 않는다.

## 3. 구현 내용

- Flyway dependency와 PostgreSQL database support dependency를 추가했다.
- `src/main/resources/db/migration/V1__initial_schema.sql`에 현재 Entity/Repository 모델 기준 초기 schema를 작성했다.
- prod 실파일 `application-prod.yml`은 제거하고 `application-prod.example.yml`, `.env.example`, Cloud Run/Supabase 배포 문서로 env 계약을 정리했다.
- `docker-compose.yml` app service가 `SPRING_FLYWAY_ENABLED`, Hikari pool size, springdoc enable flags, scheduler flag, `PORT`를 전달하도록 보강했다.
- `docs/deploy/cloud-run-supabase.md`, README, backend policy, decision log, resume metrics를 갱신했다.

## 4. TDD 기록

1. 실패 테스트 작성: `FlywayMigrationContractTest`로 V1 schema, FK, Cloud Run env 문서 계약을 먼저 고정했다.
2. 실패 확인: migration file/doc 부재로 신규 테스트가 실패했다.
3. 최소 구현: V1 migration, prod example/env 문서, Cloud Run/Supabase 문서를 추가했다.
4. 추가 실패 확인: compose app env passthrough 누락을 계약 테스트 실패로 재현했다.
5. 테스트 통과: compose env를 보강한 뒤 계약 테스트와 전체 테스트를 통과시켰다.

## 5. 검증 기록

- `./gradlew test`: 성공, 241 tests / 0 failures / 0 errors / 1 skipped.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- Docker PostgreSQL Flyway clean/migrate test: 성공.
- Docker QA: `faithlog-qa-46-migration` compose project에서 postgres/redis/app 기동, app 로그 Flyway schema version 1 확인, `/api/v1/health` `UP` 확인.
- Secret scan: 실제 Supabase URL/DB password/JWT/Firebase secret 원문 없음. `.env`와 Firebase key JSON 파일 없음.

## 6. 후속 확인 필요

- 실제 Cloud Run 프로젝트 ID, 리전, 서비스명, Artifact Registry repository 이름은 PM 승인 후 확정한다.
- 실제 Supabase/Firebase/JWT secret 주입 방식은 배포 단계에서 secret manager 또는 Cloud Run secret injection 기준으로 확정한다.
- 기존 데이터가 있는 DB에 적용해야 하는 상황이 생기면 별도 baseline 전략을 PM 승인 후 설계한다.

## 7. PM 보강: Upstash Redis와 env/profile 분리

- 추가 결정: 배포 Redis는 Upstash Redis를 사용하고, local/docker/test는 Supabase/Upstash에 의존하지 않는다.
- Dockerfile은 하나만 유지한다. Docker image는 환경을 몰라야 하며, local/docker/prod 차이는 Spring profile과 env 주입으로 분리한다.
- 구현: `application-docker.yml`, `.env.local.example`, `.env.docker.example`, `.env.prod.example` 추가. Docker Compose 기본 profile은 `docker`로 변경했다.
- Upstash 계약: `SPRING_DATA_REDIS_HOST`, `SPRING_DATA_REDIS_PORT`, `SPRING_DATA_REDIS_PASSWORD`, `SPRING_DATA_REDIS_SSL_ENABLED`.
- TDD: Upstash/env split 계약 테스트를 먼저 추가해 실패를 확인한 뒤 구현했다.
- 검증: `./gradlew test` 성공(242 tests / 0 failures / 0 errors / 1 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공.
- Docker QA: `faithlog-qa-46-upstash`에서 Docker PostgreSQL + Docker Redis만 사용해 Flyway V1 migration, app startup, `/api/v1/health` `UP` 확인.
- Secret scan: 실제 Supabase/Upstash/JWT/Firebase secret 원문 없음. 실제 `.env` 파일과 Firebase key JSON 없음.
