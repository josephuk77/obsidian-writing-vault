---
project: FaithLog
type: security-audit
issue: 161
status: review
created: 2026-07-13
tags:
  - FaithLog
  - security
  - deployment
  - supply-chain
  - Cloud-Run
---

# #161 배포 인프라와 공급망 보안 감사

## 1. 감사 배경

#183/PR #185가 전체 CI를 통과해 rebase merge된 `origin/develop` `f3e81fb9` 기준으로 저장소 secret과
Git history, Gradle dependency 공급망, GitHub Actions, Docker, Cloud Run/GCP, Supabase PostgreSQL,
Upstash Redis, Firebase Admin/FCM 경계를 코드와 설정을 수정하지 않고 감사했다.

#157~#160과 #176/#179/#182/#183의 finding·수정 결정은 중복 집계하지 않았고 실제 secret/token,
private key, Firebase JSON, DB/Redis credential, 개인정보 값은 출력하거나 기록하지 않았다.

## 2. counted manifest

- GitHub Actions workflow 2개, action 호출 8개(고유 좌표 6개)
- Docker/build-context 파일 3개
- Gradle 공급망 파일 6개, direct dependency 20개, plugin 5개
- runtime first-level 15개, 고유 resolved module 208개, unresolved 0개
- env template 4개, Spring profile 6개, 배포 계약 1개
- 보안 header/CORS/actuator/SpringDoc surface 4개
- Firebase infrastructure 8개/실패·source-of-truth trace 14개
- Redis infrastructure 7개/fail-open·fail-closed trace 9개
- Flyway migration 7개

## 3. 감사 결과

- Confirmed: Critical 0 / High 1 / Medium 1 / Low 0
- F-161-01: transitive Spring Security 6.5.0과 servlet 기본 lazy header mode가 vendor Critical
  CVE-2026-22732 영향 범위에 있다. FaithLog 최소 영향을 High, confidence 9/10으로 좁혔고 실제
  민감 응답의 cache disclosure는 response commit 조건과 upstream cache 존재에 의존하는 조건부 최대
  영향으로 분리했다.
- F-161-02: GitHub API에서 `main`/`develop` classic branch protection 0개와 repository ruleset 0개를
  확인했다. write credential이 PR/review/required-check gate 없이 branch를 변경할 수 있는
  source-integrity gap을 Medium, confidence 10/10으로 확정했다.
- False positive/의도 정책 12개, console 미확인 14개, 신규 Low hardening 후보 2개
- Gradle distribution SHA/dependency locking·verification metadata와 Docker base digest 부재는 악성
  artifact가 확인되지 않아 confirmed 취약점으로 올리지 않았다.
- PM 승인 전 보안 동작 변경이나 후속 Issue 생성은 하지 않았다.

## 4. Secret과 공급망 결과

- current/history high-signal credential candidate 0개
- non-example sensitive-path file/commit 0개
- untracked/ignored sensitive file 0개
- direct dependency/plugin dynamic·SNAPSHOT·range 0개
- wrapper JAR checksum은 공식 Gradle 8.14.5 checksum과 일치
- PM 독립 리뷰 후 official primary endpoint
  `https://services.gradle.org/distributions/gradle-8.14.5-wrapper.jar.sha256`와 로컬
  `shasum -a 256 gradle/wrapper/gradle-wrapper.jar` 비교 명령을 저장소 감사 문서에 고정
- open Dependabot alert 0개지만 SBOM endpoint 404와 exhaustive scanner 부재 때문에
  `vulnerable component 0개`로 해석하지 않음

## 5. 검증과 제약

- focused 기존 test class 7개 실행을 시도했지만 Gradle Plugin Portal에서 이미 선언된 Spring Boot
  3.5.0 plugin을 resolve하지 못해 test 0개 실행으로 종료됐다. stale XML은 집계하지 않았다.
- 저장소 findings에 7개 class의 정확한 FQCN과 실행 명령을 추가했다. 요청 denominator는 7개지만
  executed suite/test는 0개라는 한계를 유지했다.
- 저장소 matrix에 baseline-pinned high-signal pattern class와 count-only/filename-only/commit-only 명령을
  추가했다. 재현 수치는 high-signal current/history 0/0, generic-reference file/commit 17/25다.
- 동일 baseline의 PR #185 repository checks는 성공했고 저장소 기존 기록은 전체
  `399 tests / 0 failures / 0 errors / 3 skipped`다. 이 수치는 이번 실행 결과가 아니라 baseline
  evidence로만 사용했다.
- `git diff --check` 성공, 문서 link/path/count 대조 완료
- production/test/config/DB/Flyway/운영 인프라 변경 0건
- Docker, 운영 smoke/부하/credential 사용, push, PR 0건
- Issue #161에는 Project card가 없어 `In Progress` 전환을 수행할 수 없었다.
- 새 제품 결정을 만들지 않아 `docs/decision-log.md`는 변경하지 않았다.
- PM 독립 리뷰 finding 3건(P2 2건, P3 1건)의 문서 재현성 보강을 완료했다.

## 6. 산출물과 후속 후보

- `docs/security/161-deployment-supply-chain-matrix.md`
- `docs/security/161-audit-findings.md`
- `docs/resume-metrics.md`
- High 후보: PM 승인 후 Spring Security 6.5.11 이상 또는 이를 제공하는 Spring Boot maintenance BOM으로
  업데이트하고 default response header와 auth 회귀 검증
- Medium 후보: PM 승인 후 `main`/`develop` ruleset과 required checks/review/bypass/force-push 정책 확정
- Low 후보: Gradle distribution/dependency verification·locking, Docker digest refresh 정책

이 감사는 AI 보조 정적 감사이며 전문 침투 테스트나 비공개 운영 콘솔 감사를 대체하지 않는다.
