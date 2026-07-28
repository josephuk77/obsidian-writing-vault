---
project: FaithLog
type: devlog
issue: "#202"
status: done
created: 2026-07-15
tags:
  - FaithLog
  - backend
  - security
  - supabase
  - postgresql
  - rls
---

# #202 Supabase Data API 공개 접근 차단

## 1. 작업 배경

Supabase Security Advisor가 `public`의 26개 테이블에 `rls_disabled_in_public` Critical을 보고했다. `payment_accounts.account_number`와 `user_fcm_tokens.token`에는 `sensitive_columns_exposed` Critical도 함께 보고됐다.

읽기 전용 감사에서 모든 테이블의 RLS가 꺼져 있고 `anon`, `authenticated`, `service_role`에 CRUD 권한이 부여된 것을 확인했다. FaithLog는 Supabase Data API/Auth를 사용하지 않고 `postgres` JDBC로만 접근한다.

## 2. 최종 보안 계약

- Data API는 FaithLog의 승인된 데이터 경로가 아니다.
- 모든 `public` 테이블에 RLS를 활성화하고 permissive policy는 만들지 않는다.
- `PUBLIC`, `anon`, `authenticated`, `service_role`의 schema/table/sequence/function 권한을 회수한다.
- 현재 Flyway 실행 역할의 default privileges도 회수해 새 Flyway 객체의 자동 공개를 막는다.
- `FORCE ROW LEVEL SECURITY`는 사용하지 않아 table owner인 JDBC 역할은 유지한다.
- Flyway가 실행 중 잠그는 `flyway_schema_history`는 V11 loop에서 제외하고 hosted Supabase DDL에서 별도로 RLS를 활성화한다.
- 사용자 데이터 DML, credential rotation, policy 기반 client access는 수행하지 않는다.

## 3. TDD 기록

1. V11 파일이 없을 때 `FlywayMigrationContractTest` 10개 중 신규 1개가 실패했다.
2. 첫 V11 구현을 임시 PostgreSQL에서 실행해 Flyway가 `flyway_schema_history` relation lock을 기다리는 문제를 재현했다.
3. history 제외 계약을 추가해 static RED를 다시 확인했다.
4. V11에서 application table RLS와 현재·미래 Data API 권한 회수를 구현했다.
5. hosted Supabase migration에서는 history RLS를 별도 DDL로 함께 적용했다.

## 4. 검증 결과

- focused migration contract: GREEN
- 임시 PostgreSQL V1-V11 clean migration: GREEN, 기존 DB/volume 영향 없음
- Supabase public table RLS: 26/26
- `anon`/`authenticated`/`service_role` table grants: 0
- Data API role schema usage: false
- public RLS policies: 0
- `SET ROLE anon` 후 `public.users` 조회: permission denied
- active `postgres` JDBC sessions: 5
- Supabase Security Advisor: 기존 두 Critical 유형 0, deny-all 상태의 `rls_enabled_no_policy` INFO만 유지

## 5. 운영 주의

- Dashboard에서 Data API를 사용하지 않도록 유지한다.
- Flyway 외 managed role이 `public` 객체를 만들면 Security Advisor와 grants를 다시 감사한다.
- 새 hosted 환경은 Flyway 완료 후 `flyway_schema_history` RLS를 별도 적용한다.
