---
project: FaithLog
type: devlog
issue: none
status: done
created: 2026-06-17
tags:
  - FaithLog
  - backend
  - spring-boot
  - flyway
---

# Flyway Runtime Removal

## 1. 작업 배경

사용자가 현재 PR을 다시 올리기 전에 Flyway를 제거하라고 명시적으로 요청했다.

## 2. 최종 설계 기준

- Flyway는 주요 기능 개발이 끝난 뒤 도메인 모델이 안정화되면 consolidated migration 작업으로 재도입한다.
- 초기 기능 개발 중에는 Flyway dependency, `spring.flyway` 설정, placeholder migration file을 active runtime에 두지 않는다.

## 3. 변경 내용

- `build.gradle.kts`에서 `org.flywaydb:flyway-core`, `org.flywaydb:flyway-database-postgresql` 의존성을 제거했다.
- `src/main/resources/application.yml`에서 `spring.flyway` 설정을 제거했다.
- `src/main/resources/db/migration/V1__init_schema.sql` placeholder migration을 제거했다.
- `docs/backend-implementation-policy.md`, `docs/decision-log.md`, `docs/resume-metrics.md`에 Flyway 제거 결정과 검증 결과를 기록했다.

## 4. 검증

- `./gradlew test`: 성공, 35초.
- `./gradlew build`: 성공, 26초.
- `./gradlew dependencies --configuration runtimeClasspath`: 성공, Flyway 항목 없음.
- `rg "org\\.flywaydb|spring\\.flyway|flyway-core|flyway-database-postgresql" build.gradle.kts src -S`: 결과 없음.

## 5. 후속 작업

- 최종 도메인 모델이 안정화된 뒤 별도 infra/build task로 Flyway migration consolidation을 진행한다.
