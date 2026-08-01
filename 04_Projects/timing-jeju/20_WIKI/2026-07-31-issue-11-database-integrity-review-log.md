# 2026-07-31 Issue #11 DB 무결성 Reviewer 보완 개발 일지

## 작업 개요

- Issue: `#11 [Refactor] DB 무결성과 외부 데이터 적재 기반 강화`
- 브랜치: `refactor/11-database-integrity-hardening`
- 기준 `develop`: `3e9cceb271d7018d255135644362433cf35d4127`
- 최종 로컬 HEAD: `7c1066b3bb7b77e6ddaf9e736d963b2fc037191b`
- 상태: 전체 검증·원격 push 완료, 독립 Reviewer 재검토 전

## 오늘 완료한 보완

- 일정 버전 번호와 base 계보를 생성 후 변경할 수 없게 했다.
- 일정 항목의 시작과 종료가 모두 같은 제주 현지 Day 안에 있도록 강화했다.
- 날씨 영향·추천 결과의 NULL Day legacy 행에서 compute/item/leg 부모 계보를 함께 동결했다.
- import run의 멱등 marker와 실행 중 scope marker의 서로 다른 역할을 분리했다.
- checkpoint status/scope guard를 legacy audit보다 먼저 설치해 설치 중 race를 차단했다.
- 16개 정규화 테이블의 기존 non-NULL snapshot/run/provider/service/operation 계보를 소급 감사한다.
- `manual`·`fixture`·`admin_upload` 예외 행은 예외 성격을 유지할 때 편집할 수 있지만 외부 행을 예외 행으로 세탁할 수 없게 했다.

## 마지막 Reviewer finding

snapshot-backed 외부 `tour_place_sources` 행에서 다음 값을 한 번에 바꾸면 기존 trigger가 `UPDATE 1`을 허용했다.

- `source_provider = admin_upload`
- `source_service = manual`
- `external_id` 변경
- `source_snapshot_id = NULL`
- `last_import_run_id = NULL`

원인은 새 행의 optional 여부만 보고 반환해, 기존 외부 행의 성격을 확인하지 않은 것이었다.

### Red

- 독립 Reviewer가 실제 PostgreSQL에서 위 UPDATE가 성공하는 것을 재현했다.
- `database_negative_constraints.sql`에 `snapshot-backed external row cannot become optional without lineage` 음수 계약을 운영 코드보다 먼저 추가했다.

### Green

- `OLD`가 외부 행이고 `NEW`가 optional 행이면 `23514`로 즉시 거부한다.
- retention은 snapshot 행이 실제 삭제된 뒤 내용과 import run을 유지하고 snapshot 포인터만 비우는 기존 예외만 허용한다.
- 기존·신규 행이 모두 optional인 수동/fixture/admin 편집은 계속 허용한다.
- 정상 `parsed`/`tombstoned` snapshot과 같은 범위 run을 함께 연결하는 repair도 유지한다.

### Refactor

- 범용 SQL parser나 새 framework를 추가하지 않고 `validate_normalized_source_lineage()`의 상태 전환 불변조건 한 곳에 최소 조건을 배치했다.
- DB 운영 문서, 아키텍처 문서, RDB 설계 문서를 같은 정책으로 정합화했다.

## 최종 검증

- 저장소 Python 자동화: `88 tests, OK`
- 배포 SQL 정책: 성공
- all-files 비밀정보 검사: 성공
- Spring `./gradlew --no-daemon clean check`: 성공, 14개 작업
- 전체 `./scripts/quality-gate.sh`: 성공
- PostgreSQL 16/PostGIS:
  - clean bootstrap
  - v1→v1.2 migration replay
  - legacy 충돌 audit
  - 실제 2세션 checkpoint·일정 동시성
  - `schema_contract PASS`
  - `database_negative_constraints PASS`
  - fixture와 PostGIS 최근접 정류장 계약 성공
- Supabase PostgreSQL 17:
  - 공식 CLI `2.110.0`, SHA-256 `1c3403305292685090b51dd3c8226cd27b4ee6157688a151715fe74c454ca633`
  - `db reset` 2회
  - Auth·PostGIS·public 스키마·음수 계약·빈 운영 seed 성공
  - 실제 ES256 access token으로 Spring 200, 변조 401, 인가 403 성공
- 작업용 Docker/Supabase 컨테이너·네트워크·볼륨과 임시 CLI를 정리했다.

## 커밋

- `171f4db` — DB 무결성 계약 추가
- `3e2267d` — DB 무결성과 외부 적재 기반 강화
- `0e05282` — DB 적재와 일정 무결성 문서화
- `6bdab10` — 일정 버전과 Day 종료 경계 보강
- `c4883dd` — DB 업그레이드와 경계 계약 보강
- `b5c51ed` — DB 계보와 일정 무결성 경계 보완
- `7b2da3b` — DB 적재와 복구 정책 정합화
- `78fce63` — 외부 적재 계보 세탁 차단
- `7c1066b` — optional 외부 계보 제거 차단

## 추가 Reviewer MAJOR 보완: 이미 optional인 외부 origin

### 문제

`validate_normalized_source_lineage()`는 OLD와 NEW marker가 모두 optional이면 기존 전이 guard를 건너뛰었다. 따라서 실제 `tour_api` snapshot/run에 연결됐지만 `alias_type=user_query`이거나 reserved provider marker를 가진 행은 내용과 두 lineage pointer를 한 번에 바꿔 외부 origin을 지울 수 있었다.

### Red

- 운영 migration을 바꾸기 전에 PostgreSQL 16 실행 음수 계약 두 건을 추가했다.
- external run/snapshot-backed `place_aliases(user_query)`의 alias와 두 pointer를 함께 변경하자 `UPDATE 1` 뒤 `unexpectedly succeeded`로 실패했다.
- `tour_api` run이 reserved `manual` provider snapshot을 가진 `tour_place_sources`도 provider/service/external ID와 두 pointer 변경이 `UPDATE 1`이었다.
- snapshot-backed optional alias legacy fixture를 `.200` 직전에 넣었을 때 migration이 성공해 소급 audit 누락도 확인했다.

### Green

- OLD가 optional일 때 marker가 아니라 snapshot이 가리키는 run과 정규화 run을 `FOR SHARE`로 읽고 실제 `source_kind`·provider로 외부 origin을 판정한다.
- 실제 origin이 외부이면 살아 있는 snapshot pointer 제거를 `23514`로 거부해 내용+계보 제거와 pointer 선삭제 후 내용 변경의 2단계 우회를 함께 차단한다.
- snapshot 삭제 후 내용과 import run을 유지하는 pointer-only clearing, 수동·fixture·admin optional 편집, 유효한 same-scope snapshot/run repair는 유지한다.
- 16개 정규화 테이블 소급 audit에 snapshot/normalized run actual origin을 추가했고, optional legacy fixture는 정확한 alias ID와 `tour_api/한국관광공사` origin detail로 `23514` 중단한다.

### Refactor 및 문서

- actual-origin 조회는 OLD marker가 optional인 UPDATE에서만 수행해 일반 외부 적재 UPDATE의 추가 잠금 비용을 피했다.
- `db/README.md`, `docs/ARCHITECTURE.md`, DB schema·외부 API mapping 설계를 같은 정책으로 정합화했다.
- 별도 읽기 전용 patch review에서 actual-origin 잠금, retention 예외, same-scope repair, dynamic audit 인자와 16개 테이블 공통 적용에 필수 지적이 없었다.

### exact HEAD 최종 검증

- HEAD: `7c1066b3bb7b77e6ddaf9e736d963b2fc037191b`
- 저장소 자동화: `.codex` 12개 + Git hook 7개 + scripts 88개 성공
- Spring `./gradlew --no-daemon clean check`: 14 tasks 성공
- `GITHUB_HEAD_REF=refactor/11-database-integrity-hardening ./scripts/quality-gate.sh`: 모든 단계 성공
- 일반 `git push`의 pre-push hook가 같은 exact HEAD에서 전체 품질 게이트와 Docker 검증을 다시 통과
- PostgreSQL 16/PostGIS: v1 replay, 신규 optional legacy audit, 2세션 동시성, schema/negative/fixture/PostGIS 계약 성공
- Supabase CLI 2.110.0 / PostgreSQL 17: SHA-256 검증, `db reset` 2회, schema/negative/빈 seed 성공
- 실제 Supabase ES256 access token: 허용 redirect·claim과 Spring 보호 API 200, 변조 401, 인가 403 성공
- 배포 SQL 정책, all-files 비밀정보 검사, `git diff --check` 성공
- 임시 CLI와 검증 컨테이너·네트워크를 정리하고 기존 사용자 로컬 DB 영구 볼륨은 보존했다.
- 원격 `refactor/11-database-integrity-hardening`: `7c1066b3bb7b77e6ddaf9e736d963b2fc037191b`로 로컬 HEAD와 일치

## Notion 최신화

- [RDB 테이블 설계 v1.2](https://app.notion.com/p/3a40a87c7ce581dcb98ecb05a61dc8b1)
- [백엔드 허브 v1.2](https://app.notion.com/p/36c0a87c7ce580c49d8fd979b8a4a490)

51개 public 앱 테이블, TourAPI/TAGO/KMA 정규화 구조, 외부 적재 lineage, 일정·Day 무결성, PostgreSQL 16/17 검증 결과를 한국어로 반영했다.

## 남은 작업

- 새 독립 Reviewer가 `develop...HEAD`를 검토한다.
- 승인 뒤에만 PR을 생성하고 CI 성공 후 `develop`에 병합한다.
- 실제 TourAPI/TAGO/KMA importer 구현은 별도 Issue에서 진행한다.
