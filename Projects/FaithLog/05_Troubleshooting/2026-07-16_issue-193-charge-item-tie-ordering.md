# Issue #193 charge-item createdAt tie ordering boundary

## D partial evidence

actual-before attempt D (`I193_BEFORE_20260716_D / I193_FIXTURE_20260716_D / EXEC193_BEFORE_20260716_D`)는 campus ID 21에 ACTIVE membership 1,000개와 charge item 35,000개를 생성했다. correctness preflight에서 중단되어 k6 warmup과 measured는 각각 0건이고 summary는 없다. D namespace, DB rows, report는 partial rejected evidence로만 보존하며 재사용하지 않는다. 유효 baseline이나 성능 수치로 집계하지 않는다.

## 진단

- 요청 sort는 `createdAt,desc`였다.
- DB에서 문제의 charge item status pair들은 `created_at`이 exact tie였다.
- current develop API는 tie pair의 ID 순서를 일부는 오름차순, 일부는 내림차순으로 반환했다.
- Spring `Pageable`에는 primary `createdAt` sort만 있고 stable secondary sort가 없다.
- PM 독립 대조 결과 D 중단은 scenario validator 오판이 아니라 실제 API의 비결정적 pagination/order 경계다.

## 승인된 후속 해결

추천안은 모든 charge-item pageable endpoint에서 사용자가 요청한 primary sort 방향과 같은 방향의 `id` secondary sort를 자동 추가하는 것이다.

- `createdAt,desc` → `createdAt,desc; id,desc`
- `createdAt,asc` → `createdAt,asc; id,asc`

사용자가 이 정책을 승인했고 Issue #206/PR #207이 develop commit `6796ed146244d8f3f5b5dd7048ebe16865084a97`로 병합됐다. `BillingPageRequests.chargeItems()`는 모든 허용 primary sort에 같은 방향의 `id` secondary sort를 추가하며, 내 청구 목록과 관리자 회원별 상세가 같은 계약을 사용한다.

Issue #193 scenario는 exact tie의 `id,desc` 검증을 유지한다. Validator를 느슨하게 하거나 fixture timestamp를 인위적으로 벌리지 않는다. D는 계속 partial rejected evidence이며 fresh E는 PM의 독립 measurement-ready 리뷰 전 실행하지 않는다.
