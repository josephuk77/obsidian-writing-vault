---
project: FaithLog
type: devlog
issue: #90
status: in-progress
created: 2026-06-23
tags:
  - FaithLog
  - backend
  - spring-boot
  - performance
  - k6
  - jacoco
  - tdd
---

# #90 성능 테스트와 테스트 커버리지 측정 및 개선

## 1. 작업 배경

이력서/포트폴리오에 사용할 수 있는 수치를 추측이 아니라 재현 가능한 측정 결과로 남기기 위해 JaCoCo 커버리지와 local Docker 기준 k6 성능 baseline을 구축했다.

## 2. 최종 설계 기준

- 성능 기준은 local Docker Compose 기준으로 제한한다.
- 부하 조건은 `VUS=30`, `DURATION=5m`, failure `<1%`, p95 중심으로 본다.
- Cloud Run 고부하 테스트는 하지 않는다.
- API 계약(path/request/response/error code)은 변경하지 않는다.
- DB schema/index/Flyway migration은 PM 승인 전 변경하지 않는다.
- #90 1차 개선 대상은 `campuses_me`이며, `auth_login`은 보안 검토 후속 후보로 남긴다.

## 3. 구현 내용

- Gradle JaCoCo plugin/report 설정 추가.
- `performance/k6/read-baseline.js`와 README 추가.
- endpoint별 k6 Trend metric 추가.
- `CampusMembershipRow` projection 추가.
- `CampusMemberRepository.findMembershipRowsByUserIdAndStatusOrderByIdDesc` JPQL join 조회 추가.
- `CampusService.getMyCampuses`가 membership마다 campus를 단건 조회하지 않고 projection row를 결과로 매핑하도록 변경.

## 4. TDD 기록

1. 실패 테스트 작성: `CampusServiceTest.getMyCampuses_fetches_memberships_and_campuses_without_per_membership_lookup`
2. 실패 확인: 최적화 전 3개 가입 사용자 조회에서 statement count 제한 초과로 실패.
3. 최소 구현: active membership과 campus를 JPQL constructor projection으로 한 번에 조회.
4. 테스트 통과: 신규 query-count 테스트와 `./gradlew test --tests 'com.faithlog.campus.*'` 성공.
5. 리팩토링: API 응답 record는 유지하고 repository 전용 row를 result로 변환.

## 5. 테스트 결과

- `./gradlew test jacocoTestReport`: 성공, 242 tests / 0 failures / 1 skipped.
- JaCoCo baseline: line 94.75%, branch 73.08%, class 97.62%, method 90.58%.
- `./gradlew test --tests com.faithlog.campus.application.CampusServiceTest.getMyCampuses_fetches_memberships_and_campuses_without_per_membership_lookup`: 최적화 전 실패, 최적화 후 성공.
- `./gradlew test --tests 'com.faithlog.campus.*'`: 성공.

## 6. 성능 측정

공통 조건:

- local Docker Compose profile `docker`
- PostgreSQL 17, Redis 7
- `BASE_URL=http://host.docker.internal:8080`
- `VUS=30`, `DURATION=5m`, `THINK_TIME_SECONDS=1`
- `INCLUDE=auth,campuses,admin-dashboard,devotions,billing,polls`
- dataset: users 164, campuses 49, campus_members 123, polls 34, charge_items 22, weekly_devotion_records 20, devotion_daily_checks 65, prayer_submissions 12

Baseline:

- overall: avg 199.83ms, p50 43.51ms, p95 917.06ms, p99 1,756.82ms, 95.87 req/s, failure 0.00%
- `campuses_me`: avg 582.49ms, p50 511.15ms, p95 1,381.89ms, p99 2,862.35ms
- report: `build/reports/k6/read-baseline-local-docker-endpoints.json`

After `campuses_me` optimization:

- overall: avg 199.41ms, p50 64.66ms, p95 906.29ms, p99 1,371.26ms, 95.53 req/s, failure 0.00%
- `campuses_me`: avg 522.84ms, p50 461.72ms, p95 1,170.56ms, p99 1,828.76ms
- report: `build/reports/k6/read-after-campuses-me-local-docker.json`

Improvement:

- `campuses_me` avg 10.24% 개선
- `campuses_me` p50 9.67% 개선
- `campuses_me` p95 15.29% 개선
- `campuses_me` p99 36.11% 개선
- 전체 p95 1.17% 개선

## 7. 고민한 부분

`auth_login`이 가장 느렸지만 password hash/security cost와 인증 보안 정책에 직접 연결되어 임의 최적화하지 않았다. 이번 범위에서는 읽기 API인 `campuses_me`의 N+1 제거만 진행했다.

## 8. 트러블슈팅

- 문제: Docker k6가 host app에 접근해야 해서 `localhost` 대신 `host.docker.internal`이 필요했다.
- 원인: k6가 별도 Docker container에서 실행된다.
- 해결: k6 script remote guard에 Docker-local hostname을 허용하고 README에 Docker 실행 예시를 추가했다.
- 재발 방지: remote target은 `ALLOW_REMOTE_LOAD=true` 없이는 계속 차단한다.

## 9. 다음 작업

- [ ] `auth_login` 성능은 보안 검토 후속 이슈로 분리한다.
- [ ] write API load test는 fixture/멱등성/부작용 관리 후속 이슈로 분리한다.
- [ ] 운영 규모 dataset과 EXPLAIN 근거가 생기면 `campuses_me` index 필요성을 PM에게 다시 질문한다.

## 10. 이력서 문장 후보

`local Docker dataset(users 164, campus_members 123) 기준 k6 VUS 30/5분 부하 테스트를 구축하고, /api/v1/campuses/me N+1 조회를 JPQL projection으로 개선해 p95 응답 시간을 1,381.89ms에서 1,170.56ms로 15.29%, p99를 2,862.35ms에서 1,828.76ms로 36.11% 단축했다.`
