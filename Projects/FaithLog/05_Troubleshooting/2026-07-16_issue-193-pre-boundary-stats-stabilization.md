---
project: FaithLog
type: troubleshooting
created: 2026-07-16
tags:
  - FaithLog
  - troubleshooting
  - performance
  - postgresql
---

# Issue #193 pre-boundary cumulative stats stabilization

## H partial rejected evidence

Actual-before attempt H 식별자는 `I193_BEFORE_20260716_H / I193_FIXTURE_20260716_H / EXEC193_BEFORE_20260716_H`다. Fresh campus fixture를 COMMIT했고 measured 16 cases를 각각 320 requests, HTTP/custom failure 0으로 완료했다. Resource validation도 통과했다.

Measurement-integrity에서 `users.nModSinceAnalyze`가 before 51, after 52로 보여 중단됐다. Runtime-final과 adoption/classification은 생성되지 않았다. 측정 계정 15022/15023은 모두 USER로 복구됐고 canonical lock free와 running k6 없음이 확인됐다. H namespace, DB rows, report는 partial rejected evidence로만 보존하고 재사용하지 않는다. H의 request count·latency·throughput·resource 수치를 baseline 또는 개선 성과로 채택하지 않는다.

## 원인

Fresh measured ADMIN login은 `last_login_at=2026-07-16T05:07:13.053898Z`에 users row를 갱신했다. 단일 measurement-state-before는 약 478ms 뒤인 `capturedAt=2026-07-16T05:07:13.531998Z`에 수집됐다. PostgreSQL cumulative stats flush가 HTTP 응답보다 늦어 login UPDATE가 before snapshot에 아직 반영되지 않았다가 measured 구간 중 51→52로 보인 false contamination이다. 이를 measured GET workload 자체의 users write로 추정하지 않는다.

## 보정 계약

- Fresh measured login 뒤 단일 maintenance snapshot을 before로 채택하지 않는다.
- Issue-local 상수로 최대 5회 `capture → 1초 sleep → capture`를 수행한다. 새 runtime 입력이나 default는 추가하지 않는다.
- 별도 helper가 두 state JSON의 database identity/postmaster/stats reset, planner settings, 4개 table analyze/vacuum maintenance state를 exact 비교한다.
- Stable pair의 두 번째 snapshot만 `measurement-state-before.json`으로 이동한다.
- 안정화 실패는 counter-before와 measured window 시작 전에 fail-closed한다.
- Measured 이후 기존 exact before/after continuity, final runtime continuity와 `automaticAdoption=false` 경계는 완화하지 않는다.

후속 I는 PM 독립 리뷰와 사용자 승인 후 별도 fresh namespace로 실행됐으며 users stable-pair는 통과했지만 measured-window `charge_items` autoanalyze 사유로 rejected됐다. I 상세와 J 제안은 [[2026-07-16_issue-193-fixture-analyze-boundary]]에 기록한다.

## 관련 이슈

- #193
