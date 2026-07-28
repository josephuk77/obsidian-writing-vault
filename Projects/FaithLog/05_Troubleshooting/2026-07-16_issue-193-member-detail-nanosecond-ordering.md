# Issue #193 member-detail nanosecond ordering false reject

## 현상

actual-before attempt C (`I193_BEFORE_20260716_C / I193_FIXTURE_20260716_C / EXEC193_BEFORE_20260716_C`)는 dataset binding, runtime/DB/lock/quiet gate, fresh fixture와 ADMIN/duty 인증까지 통과했다. campus ID 19에 ACTIVE membership 1,000개와 charge item 35,000개를 COMMIT한 뒤, k6 전 preflight가 `Member-detail items are not in createdAt desc, id desc order`로 중단됐다.

SQL expectation의 실제 순서는 `...37.542110`, `...37.542109`, `...37.542108`의 마이크로초 내림차순이고 각 exact timestamp 안에서는 ID 내림차순이었다. 기존 validator는 `new Date`/`getTime`/`toISOString` 경로에서 millisecond 아래를 버려 여섯 recent item을 같은 instant로 취급했고, 서로 다른 timestamp 사이에도 ID 내림차순을 잘못 요구했다.

## 보정

- RFC3339 timestamp를 최대 9자리 fraction과 `Z`/offset까지 strict parse한다.
- 달력 날짜와 시간/offset 범위를 직접 검증하고 epoch nanoseconds를 `BigInt`로 계산한다.
- `createdAt` 내림차순을 lossless instant로 비교하고 exact instant tie에서만 ID 내림차순을 적용한다.
- date-only, malformed, invalid calendar date, `24:00`, 9자리 초과 fraction은 fail-closed다.
- 실제 설치된 k6의 `inspect`로 scenario module의 BigInt parse/instantiate 성공을 확인한다. 이는 load 실행이 아니다.

## 측정 상태

C는 k6 warmup 0건, measured 0건, summary 없음이다. cleanup trap으로 임시 ADMIN은 USER로 복구됐고 memory-only credential은 폐기됐다. C namespace와 report는 partial rejected evidence로만 보존하며 재사용하지 않는다. 유효 baseline이나 성능 개선 수치로 집계하지 않는다.
