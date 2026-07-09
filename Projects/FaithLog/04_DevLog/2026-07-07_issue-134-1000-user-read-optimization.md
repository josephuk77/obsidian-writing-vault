---
project: FaithLog
type: devlog
issue: #134
status: done
created: 2026-07-07
tags:
  - FaithLog
  - backend
  - spring-boot
  - performance
  - k6
---

# #134 1000명 기준 기도제목·투표 결과 조회 성능 최적화

## 1. 작업 배경

로컬 Docker `PERF_1000_20260707_A` 데이터셋에서 1000명 규모 read steady-state k6 기준 `prayer_weekly_board`와 `poll_results`가 p95 병목으로 확인됐다.

## 2. 최종 설계 기준

- API path/request/response 계약 변경 없음
- Controller Entity 직접 반환 없음
- Swagger 문서화 annotation 추가 없음
- 기존 V1 Flyway 수정 없음
- 로컬 Docker 기준으로 개선 전후 p95/p99/failure rate 기록

## 3. 구현 내용

- Application/Port: `CampusUserLookupPort.findCampusUsersByIds` batch lookup 추가
- Repository: `UserRepository.findCampusUsersByIds`를 `findAllById` 1회 조회 후 `CampusUserLookupResult`로 매핑
- Prayer: 주간 보드 조립 시 target member user profile을 한 번에 조회해 per-member user lookup 제거
- Poll: 비익명 투표 결과 respondent user profile을 한 번에 조회해 per-response user lookup 제거
- Poll: `targetMemberCount`를 active member entity list `.size()` 대신 `countByCampusIdAndStatus` count query로 계산
- DB: 신규 migration 없음. 기존 unique/index 경로를 활용하는 코드-only 최적화로 제한

## 4. TDD 기록

1. 실패/회귀 evidence: Issue #134 baseline 및 Hibernate statement count 회귀 테스트 기준 수립
2. 테스트 추가: `PrayerServiceTest.weekly_board_fetches_member_profiles_without_per_member_user_lookup`, `PollServiceTest.poll_results_fetch_respondents_without_per_response_user_lookup`
3. 최소 구현: user batch lookup port/repository와 prayer/poll read path 적용
4. 테스트 통과: focused service tests, 전체 `./gradlew test`, `./gradlew build`, `./gradlew asciidoctor` 성공
5. 리팩토링: 인덱스 추가 없이 code-only batch query로 범위 축소

## 5. 테스트 결과

- `./gradlew test --tests com.faithlog.prayer.application.PrayerServiceTest --tests com.faithlog.poll.application.PollServiceTest`: BUILD SUCCESSFUL
- `./gradlew test`: BUILD SUCCESSFUL
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: 최초 sandbox lock 실패, 권한 상승 재실행 BUILD SUCCESSFUL
- `git diff --check`: 성공
- Docker health: `UP`

## 6. 성능 결과

Baseline: 63,877 requests, failure 0.00%, 211.88 req/s, avg 57.12ms, p95 192.65ms, p99 290.45ms.

After: 89,173 requests, failure 0.00%, 295.92 req/s, avg 16.93ms, p95 44.60ms, p99 89.37ms.

주요 endpoint 개선:

- `prayer_weekly_board`: p95 316.82ms -> 76.96ms, p99 417.07ms -> 165.64ms
- `poll_results`: p95 244.84ms -> 51.19ms, p99 340.02ms -> 108.48ms
- `admin_dashboard_summary`: p95 138.50ms -> 61.64ms

리포트 파일:

- `build/reports/k6/issue-134-after-smoke.json`
- `build/reports/k6/issue-134-after-vus30-5m.json`

## 7. 고민한 부분

인덱스 후보는 있었지만 기존 unique constraint/index 경로로 주요 조회가 처리 가능하고, N+1 제거만으로 p95가 크게 개선되어 새 Flyway migration은 추가하지 않았다.

## 8. 다음 작업

- [ ] PM 검증 후 PR 생성
- [ ] 운영 DB/Cloud Run 성능 판단은 별도 승인 후 진행
