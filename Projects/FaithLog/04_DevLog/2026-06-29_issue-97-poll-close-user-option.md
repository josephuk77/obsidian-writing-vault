---
project: FaithLog
type: devlog
issue: #97
status: done
created: 2026-06-29
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #97 투표 종료와 사용자 항목 추가 구현

## 1. 작업 배경

투표 운영 중 관리자가 투표를 수동 종료할 수 있어야 하고, 특정 투표에서는 일반 ACTIVE 캠퍼스 멤버가 투표 중 새 선택지를 추가할 수 있어야 했다. PM 세션에서 종료 API는 종료만 수행하고, 정산/알림/청구 생성을 하지 않는 것으로 확정했다.

## 2. 최종 설계 기준

- 관리자 종료 API: `PATCH /api/v1/admin/campuses/{campusId}/polls/{pollId}/close`
- 사용자 옵션 추가 API: `POST /api/v1/campuses/{campusId}/polls/{pollId}/options`
- `poll_templates.allow_user_option_add`와 `polls.allow_user_option_add`를 둘 다 둔다.
- 템플릿 기반 투표 생성은 템플릿 설정을 복사한다.
- 직접 투표 생성의 `allowUserOptionAdd`는 optional이며 null/생략 시 false다.
- 기존 응답 계약 `optionIds`와 `poll_response_options` 구조는 변경하지 않는다.
- Swagger 문서화 annotation은 추가하지 않고 Spring REST Docs로 상세 계약을 검증한다.

## 3. 구현 내용

- Entity: `Poll`, `PollTemplate`, `PollOption`에 사용자 옵션 추가 설정과 사용자 추가 선택지 추적 필드 추가.
- Command: `AddPollOptionCommand`, `allowUserOptionAdd` command 필드 추가.
- Service: `PollService.closePoll`, `PollService.addUserOption` 구현. 종료는 OPEN만 허용하고 `endsAt`을 현재 시각으로 당긴다. 옵션 추가는 ACTIVE 멤버, OPEN 기간, 허용 설정, trim/대소문자 무시 중복을 검증한다.
- Repository: 기존 `PollOptionRepository.findByPollIdOrderBySortOrderAsc`를 사용해 중복 검사와 다음 정렬 순서를 계산.
- Controller: Admin poll close endpoint와 member poll option add endpoint 연결.
- Test: `PollServiceTest`, `PollApiRestDocsTest`에 종료/옵션 추가/중복/권한/문서 계약 테스트 추가.
- Schema: `V1__initial_schema.sql`에 `allow_user_option_add`, `user_added`, `created_by_user_id` 반영.

## 4. TDD 기록

1. 실패 테스트 작성: 선행 커밋 `de0e40f test: #97 투표 종료와 사용자 항목 추가 실패 테스트 추가`.
2. 실패 확인: focused test가 `compileTestJava` 31 errors로 실패했다.
3. 최소 구현: ErrorCode, domain field, service use case, controller, DTO, REST Docs descriptor, schema를 연결했다.
4. 테스트 통과: focused test와 전체 `./gradlew test` 통과.
5. 리팩토링: 기존 command 호출부 호환성을 위해 record 보조 생성자를 두고, 기존 테스트 호출을 대량 변경하지 않도록 했다.

## 5. 테스트 결과

명령:

`./gradlew test --tests com.faithlog.poll.application.PollServiceTest --tests com.faithlog.poll.presentation.PollApiRestDocsTest`

결과:

`BUILD SUCCESSFUL`

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 249 tests / 0 failures / 0 errors / 1 skipped

명령:

`./gradlew build`

결과:

`BUILD SUCCESSFUL`

명령:

`./gradlew asciidoctor`

결과:

`BUILD SUCCESSFUL`

## 6. 고민한 부분

종료 API가 커피 정산과 연결될 수 있는 위치였지만, 승인된 범위가 종료만이므로 `CoffeePollSettlementService` 호출을 넣지 않았다. 또한 사용자 옵션 추가를 응답 API에 섞지 않고 별도 API로 분리해 기존 `optionIds` 계약을 보존했다.

## 7. 트러블슈팅

- 문제: 새 command 필드 추가 후 기존 테스트 호출부가 컴파일 실패했다.
- 원인: `CreatePollCommand`, `CreatePollTemplateCommand`, `UpdatePollTemplateCommand`의 canonical constructor 인자가 늘었다.
- 해결: 기존 호출을 기본값 false/null로 유지하는 보조 생성자를 추가했다.
- 재발 방지: API request field는 optional/default false로 문서화하고, 새 동작이 필요한 테스트만 명시적으로 true를 보낸다.

- 문제: `./gradlew asciidoctor`가 sandbox에서 `~/.gradle` wrapper lock 파일 접근 권한 오류로 실패했다.
- 원인: Gradle wrapper lock 경로가 workspace 밖이었다.
- 해결: 동일 명령을 권한 상승으로 단독 실행해 성공 확인했다.
- 재발 방지: Gradle wrapper lock 권한 문제가 나면 sandbox 실패를 기록하고 동일 명령을 권한 상승으로 재시도한다.

## 8. 다음 작업

- [ ] PR review에서 API docs와 모바일 연동 요구를 확인한다.
- [ ] Docker QA는 기존 `faithlog-postgres` 컨테이너가 compose project `faithlog` 소유로 감지되어 script guard에서 중단됐다. 기존 개발/PM stack을 임의로 중지하지 않고, 필요 시 별도 승인 후 재실행한다.

## 9. Velog 글감

- 기존 응답 계약을 유지하면서 사용자 생성 선택지를 추가하는 API 설계
- 상태 전이 API를 정산/알림 side effect와 분리하는 이유


## 10. PR #98 Flyway V2 Migration 보강

PM 결정에 따라 Supabase/Cloud Run 운영 DB에서 이미 적용될 수 있는 `V1__initial_schema.sql`에는 #97 feature schema 변경을 남기지 않기로 했다. 기존 PR 커밋에서 V1에 추가했던 아래 항목을 제거하고, 새 migration `V2__add_poll_user_option_fields.sql`로 분리했다.

V1에서 제거한 항목:

- `poll_templates.allow_user_option_add`
- `polls.allow_user_option_add`
- `poll_options.user_added`
- `poll_options.created_by_user_id`
- `fk_poll_options_created_by_user`

V2 추가 항목:

- `ALTER TABLE poll_templates ADD COLUMN allow_user_option_add BOOLEAN NOT NULL DEFAULT FALSE;`
- `ALTER TABLE polls ADD COLUMN allow_user_option_add BOOLEAN NOT NULL DEFAULT FALSE;`
- `ALTER TABLE poll_options ADD COLUMN user_added BOOLEAN NOT NULL DEFAULT FALSE;`
- `ALTER TABLE poll_options ADD COLUMN created_by_user_id BIGINT;`
- `ALTER TABLE poll_options ADD CONSTRAINT fk_poll_options_created_by_user FOREIGN KEY (created_by_user_id) REFERENCES users (id);`

검증:

- `./gradlew test --tests com.faithlog.poll.application.PollServiceTest --tests com.faithlog.poll.presentation.PollApiRestDocsTest` 성공
- `./gradlew test` 성공: 249 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build` 성공
- `./gradlew asciidoctor` 성공


## 11. PR #98 CI Flyway Test 보강

GitHub Actions `Spring Boot build and test`에서 `PostgresFlywayMigrationTest.flywayMigratesCleanPostgresDatabase()`가 실패했다.

문제:

- #97에서 `V2__add_poll_user_option_fields.sql`을 추가해 clean PostgreSQL 기준 적용 migration 수가 2가 됐다.
- 기존 테스트는 `result.migrationsExecuted`를 1로 고정 검증해 V2 추가 후 실패했다.

해결:

- `migrationsExecuted >= 2`로 다중 migration 기준을 반영했다.
- Flyway current version이 `2` 이상인지 검증했다.
- PostgreSQL `information_schema`로 #97 신규 컬럼 4개와 FK 존재를 검증했다.

추가 검증 항목:

- `poll_templates.allow_user_option_add`
- `polls.allow_user_option_add`
- `poll_options.user_added`
- `poll_options.created_by_user_id`
- `fk_poll_options_created_by_user`

검증:

- `./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest` 성공
- `FAITHLOG_RUN_POSTGRES_FLYWAY_TEST=true FLYWAY_TEST_JDBC_URL=jdbc:postgresql://localhost:55432/faithlog_test ./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest --rerun-tasks` 성공
