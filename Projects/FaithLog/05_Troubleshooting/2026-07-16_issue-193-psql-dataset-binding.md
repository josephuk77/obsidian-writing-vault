---
project: FaithLog
type: troubleshooting
created: 2026-07-16
tags:
  - FaithLog
  - troubleshooting
  - performance
  - postgresql
  - k6
---

# Issue #193 actual-before B의 psql dataset binding 실패

## 문제 상황

`I193_BEFORE_20260716_B / I193_FIXTURE_20260716_B / EXEC193_BEFORE_20260716_B`로 실제 before runner를 시작했다. 사용자 승인 계정 2개와 임시 ADMIN 로그인, immutable runtime/DB/lock/quiet gate를 통과했고 fresh fixture가 campus ID 17에 ACTIVE membership 1,000개와 charge item 35,000개를 COMMIT했다.

fixture 직후 dataset binding JSON을 조회하는 단계에서 중단됐다. k6 warmup과 measured는 각각 0건이며 summary는 생성되지 않았다.

## 에러 메시지

```text
ERROR: syntax error at or near ":"
```

## 원인 분석

`run-baseline.sh`가 `psql_exec -c`로 전달한 SQL 문자열 안에서 `:'dataset_id'`가 psql variable substitution을 거칠 것으로 가정했다. 실제 `psql -c` 실행 경계에서는 이 placeholder가 치환되지 않은 채 PostgreSQL 서버로 전달되어 `:` syntax error가 발생했다.

## 해결 방법

- dataset binding SELECT를 issue-local `select-dataset-binding.sql`로 분리했다.
- SQL은 stdin으로 `psql_exec`에 전달하고 `-v dataset_id="$DATASET_ID"`만 사용한다.
- dataset ID를 SQL 문자열에 raw shell interpolation하지 않는다.
- fake psql harness에서 동일 SQL이 `-c`일 때 실패하고 stdin+`-v`일 때 binding JSON을 반환하도록 계약을 고정했다.

## 재발 방지

- psql variable placeholder가 있는 SQL은 `-c` 문자열로 실행하지 않는다.
- stdin SQL과 `-v` 조합을 contract test로 유지한다.
- B namespace, DB rows, report directory는 partial rejected evidence로 보존하고 재사용하지 않는다.
- B 결과는 baseline/latency/throughput/개선 성과로 집계하지 않는다.
- 외부 cleanup trap으로 임시 ADMIN이 USER로 복구됐고 memory-only credential은 runner shell 종료와 함께 폐기됐다.
- 후속 actual before는 새 dataset/fixture/execution ID와 별도 승인 credential만 사용한다.

## 관련 이슈

- #193

