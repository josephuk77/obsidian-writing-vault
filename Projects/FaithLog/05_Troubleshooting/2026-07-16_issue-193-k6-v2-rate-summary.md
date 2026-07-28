# Issue #193 k6 v2 Rate summary semantics

## E partial evidence

actual-before attempt E (`I193_BEFORE_20260716_E / I193_FIXTURE_20260716_E / EXEC193_BEFORE_20260716_E`)는 campus ID 23에 ACTIVE membership 1,000개와 charge item 35,000개를 생성했다. Warmup은 5 iterations와 80 HTTP request를 완료했고 HTTP failure는 0이었다.

Warmup summary validation에서 중단되어 measured k6, measured DB/resource boundary, measured summary와 classification은 생성되지 않았다. 측정 계정 15016/15017은 모두 USER로 복구됐고 canonical performance lock 제거를 확인했다. E namespace와 report는 partial rejected evidence로만 보존하며 재사용하지 않는다. 유효 baseline, latency, throughput 또는 개선 성과로 채택하지 않는다.

## 원인

실제 k6 v2 custom Rate의 무오류 summary는 다음 형태였다.

```json
{"passes": 0, "fails": 5, "value": 0}
```

`Rate.add(false)`의 수가 `fails`에 기록되므로, 실패 여부를 넣는 custom Rate가 전부 false면 `passes=0`, `fails=total`, `value=0`이다. 기존 validator는 `rate` 필드를 읽어 정상 summary를 모두 거부했다.

## 보정 계약

- Direct metric과 `metric.values` wrapper를 모두 지원한다.
- Warmup의 explicit expected count와 measured의 observed count 경로에 같은 검증을 적용한다.
- 무오류는 `value=0`, `passes=0`, `fails=request count`여야 한다.
- Positive value, passes 증가, fails 불일치, request count 불일치, missing/string/nonfinite value는 fail-closed다.
- `accepted=false`, `automaticAdoption=false`와 final evidence adoption 경계는 변경하지 않는다.

후속 F는 PM 독립 리뷰와 사용자 승인 후 별도 fresh namespace로 실행됐지만 resource normalization에서 중단되어 rejected됐다. 자세한 기록은 [[2026-07-16_issue-193-docker-memory-rounding-evidence]]에 있다.
