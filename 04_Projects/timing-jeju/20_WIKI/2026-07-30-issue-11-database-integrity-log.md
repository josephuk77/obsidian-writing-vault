# 2026-07-30 Issue #11 DB 무결성 전체 검증 개발 일지

## 작업 개요

- Issue: `#11 [Refactor] DB 무결성과 외부 데이터 적재 기반 강화`
- 브랜치: `refactor/11-database-integrity-hardening`
- 기준 브랜치: `develop` (`3e9cceb271d7018d255135644362433cf35d4127`)
- 최종 HEAD: `0e0528299fc2795ed02a55c9c2d30c817236608c`

이번 작업은 기존 46개 public 테이블을 단순 확인하는 수준이 아니라, 실제 PostgreSQL 16/PostGIS와 Supabase PostgreSQL 17에서 스키마를 초기화하고 정상 입력·거부 입력을 모두 실행해 DB 계약을 검증했다. Flyway는 도입하지 않았고 `supabase/migrations`를 운영 public 스키마의 단일 기준으로 유지했다.

## 발견한 핵심 문제

1. 다른 여행·일정 버전·Day의 행을 일부 계산 결과와 일정 구성에 섞을 수 있었다.
2. candidate/active 일정이 생성된 뒤 Day 날짜·시간이나 여행 날짜를 바꾸거나, draft 내용 변경과 일정 봉인을 동시에 수행할 여지가 있었다.
3. 일정 버전의 base가 미래 버전을 참조해 순환 계보가 생길 수 있었다.
4. 외부 API 원문 snapshot, import run, 정규화 행의 provider/service/operation/scope 계보가 DB에서 강제되지 않았다.
5. 실패·실행 중 run을 마지막 성공 checkpoint로 지정하거나, 참조 이후 run 상태를 되돌릴 수 있었다.
6. TAGO 노선·정류장·시간표가 다른 provider 또는 도시 범위와 섞일 수 있었다.
7. 외부 기준 코드와 시간표의 유효기간이 중복될 수 있었고, 같은 기간에 영업과 휴무가 동시에 저장될 수 있었다.
8. TourAPI 최신 KorService2 법정동·신분류 필드가 스키마와 문서에 없었다.

## 구현 내용

- 일정·Day·compute/item/leg 사이의 복합 FK와 FK 선행 인덱스를 추가했다.
- 일정 봉인 전에 모든 Day의 항목, 시간 창, 이동 구간을 검사하고 candidate/active 이후 Day·여행 날짜 변경을 차단했다.
- draft 내용 변경과 일정 상태 변경을 `FOR SHARE` 잠금으로 직렬화했다.
- base 일정은 같은 여행의 더 작은 `version_no`만 참조하도록 제한했다.
- `data_import_runs`, `external_api_snapshots`, `data_import_checkpoints`에 source scope 복합 계보를 적용했다.
- `parsed` 또는 삭제 사실을 정상 처리한 `tombstoned` snapshot만 정규화할 수 있게 하고 parse 상태 회귀를 차단했다.
- checkpoint는 같은 범위의 `succeeded` run만 참조하며 동시 상태 변경과 교차 커밋되지 않도록 잠갔다.
- TourAPI `lDongRegnCd`, `lDongSignguCd`, `lclsSystm1~3` 원문 컬럼을 추가하고 기존 area/category 컬럼은 과거 snapshot 호환용으로 유지했다.
- TAGO route/stop/timetable의 provider·city 범위를 복합 FK로 강제했다.
- 기준 코드·시간표 유효기간과 영업/휴무 충돌을 GiST exclusion으로 차단했다.
- raw 수집 테이블은 RLS를 유지하고 client policy/grant 없이 서버 전용 경계를 유지했다.

## Red → Green → Refactor

### Red

- DB hardening 정적 계약: 후속 migration 부재와 계보·유효기간·최신 TourAPI 필드 누락으로 실패했다.
- 일정 동시성 추가 계약: `FOR KEY SHARE`가 status 갱신을 직렬화하지 못하고 확정 일정 이후 Day INSERT 경계가 없어 5개 중 2개가 실패했다.
- 독립 실제 DB 검토에서 snapshot parse 전 정규화 허용, checkpoint 상태 race, parse 상태 회귀 경계를 추가로 발견했다.

### Green

- `python3 -m unittest discover -s scripts/tests -p 'test_*.py'`: 75개 성공.
- `python3 scripts/deploy_sql_policy.py`: 위반 0건.
- PostgreSQL 16/PostGIS Docker: 스키마 계약, 음수 제약, fixture, active schedule, 최근접 정류장 공간 쿼리 성공.
- Supabase PostgreSQL 17: `db reset` 2회, Auth, PostGIS, 스키마·음수 계약, 빈 운영 seed 성공.
- 실제 Supabase ES256 access token으로 Spring 보호 API 200, 서명 변조 401, 인가 거부 403 성공.

### Refactor

- 적재 계보, checkpoint 검증, snapshot 불변성, 일정 봉인과 Day 보호 책임을 각각 작은 DB 함수와 constraint trigger로 분리했다.
- DBML·아키텍처·외부 API 매핑 문서를 실제 컬럼과 복합 제약에 맞췄다.
- 테스트 계약, migration/실행 경로, 문서를 세 개의 논리 커밋으로 분리했다.

## 커밋

- `171f4db25959e060675de447f720c59adcced87e` — `test: #11 DB 무결성 계약 추가`
- `3e2267d0d48a780713ea580891b3d2b67c2c6cc6` — `refactor: #11 DB 무결성과 외부 적재 기반 강화`
- `0e0528299fc2795ed02a55c9c2d30c817236608c` — `docs: #11 DB 적재와 일정 무결성 문서화`

## 최종 검증

- `cd services/spring-api && ./gradlew --no-daemon clean check`: 성공, 14개 작업.
- `GITHUB_HEAD_REF=refactor/11-database-integrity-hardening ./scripts/quality-gate.sh`: 전 단계 성공.
- 비밀정보 전체 검사와 `git diff --check`: 성공.
- PostgreSQL 16 및 Supabase PostgreSQL 17 양쪽에서 동일 migration 순서 검증.
- 작업 관련 Docker 컨테이너·네트워크·볼륨과 Supabase 임시 파일 정리.

## 설계 결정과 남은 작업

- 실제 TourAPI/TAGO/KMA/TMAP 호출·파싱·정제·upsert를 수행하는 Spring importer는 아직 없다. 이번 작업은 그 importer가 안전하게 저장할 DB 기반과 계약을 만든 것이다.
- 하나의 read model이 `detailCommon2`와 `detailIntro2`처럼 여러 raw snapshot을 합칠 때는 단일 `source_snapshot_id`만으로 모든 출처를 표현하기 어렵다. 실제 importer 개발 전에 operation별 다대다 provenance link를 별도 Issue로 검토한다.
- 새 환경 변수는 추가하지 않았다. 실제 외부 API importer 개발 시 공급자 API key는 서버 env/secret manager에만 넣고 raw payload·로그·Git에 남기지 않는다.
