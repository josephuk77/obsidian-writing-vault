## 2026-07-13 Issue #190

- [ready] 벌금 취소와 경건 재제출을 application port 기반 단일 transaction으로 연결하고 상태 전이와 source charge 재활성화를 row lock으로 직렬화해 daily 기록 보존·rollback·terminal conflict를 보장했으며, 148개 focused·425개 전체 테스트와 REST Docs로 검증했다. Evidence: `04_DevLog/2026-07-13_issue-190-penalty-cancel-resubmit-admin-paid`, repository `docs/resume-metrics.md`.

## 2026-07-13 Issue #188

- [ready] 관리자 주차별 경건·실제 벌금 조회와 2-sheet XLSX export를 동일 bulk query model로 구현해 campus 격리와 N+1 회귀를 고정하고, 82개 focused·420개 전체 테스트와 REST Docs 126개 스니펫 기준으로 권한·집계·파일 계약을 검증했다. Evidence: `04_DevLog/2026-07-13_issue-188-admin-weekly-devotion-export`, repository `docs/resume-metrics.md`.

## 2026-07-13 Issue #186

- [ready] Spring Boot 3.5.0→3.5.15 managed BOM으로 취약 Spring Security 6.5.0을 6.5.11로 교체하고 production/test resolved graph 독립 계약과 정식 release 검증으로 false-green을 차단했으며, 209개 runtime 좌표의 81개 전이·413개 전체 테스트·실제 Redis Lua·격리 Docker 인증/200·401·403 헤더 QA로 회귀를 검증했다. Evidence: `04_DevLog/2026-07-13_issue-186-spring-security-maintenance-upgrade`, repository `docs/security/186-spring-security-maintenance-upgrade.md`.

## 2026-07-13 Issue #161

- [ready] 배포·공급망 신뢰 경계의 2개 workflow/8개 action 호출·208개 runtime module·Docker/Cloud Run/Supabase/Upstash/Firebase 경계를 counted manifest로 감사해, vendor Critical 영향 Spring Security 구성 1건(High, 9/10)과 보호되지 않은 main/develop source-integrity gap 1건(Medium, 10/10)을 식별하고 12개 false positive와 14개 console 미확인을 분리했다. PM 독립 리뷰 후 exact 7-class command, count-only secret scan, Gradle primary checksum 비교까지 재현성을 보강했다. Evidence: `04_DevLog/2026-07-13_issue-161-deployment-supply-chain-security-audit`, repository `docs/security/161-*`.

## 2026-07-13 Issue #183

- [ready] COFFEE Poll/template 옵션의 이름·코드·가격 권한을 backend catalog로 고정하고 client override와 null/inactive 우회를 차단했으며, persisted-target 인가 순서를 보존한 채 4개 RED 실패·87개 집중 회귀·399개 전체 테스트·11개 격리 Docker API/스케줄러 정산 시나리오로 검증했다. Evidence: `04_DevLog/2026-07-13_issue-183-coffee-option-catalog-authority`, repository `docs/resume-metrics.md`.

## 2026-07-13 Issue #182

- [ready] 경건 벌금 계산을 long exact arithmetic과 INTEGER 범위 검증으로 보강하고 Billing·Flyway 양수 불변식을 3중 적용해 음수 청구와 dashboard 상쇄를 차단했으며, 11개 RED 실패·396개 전체 테스트·clean/legacy PostgreSQL migration·격리 Docker HTTP rollback QA로 검증했다. Evidence: `04_DevLog/2026-07-13_issue-182-devotion-fine-overflow-positive-charge`, repository `docs/resume-metrics.md`.

## 2026-07-13 Issue #160

- [ready] 21개 Controller·80개 endpoint의 36개 입력 DTO와 57개 응답 DTO를 validation·persistence·오류·민감정보 경계까지 추적해, 벌금 `int` overflow에 의한 음수 청구와 COFFEE catalog 우회 가격 정산 2건(Medium, confidence 10/10·9/10)을 식별하고 PM 독립 재검증 16 suites / 138 tests `BUILD SUCCESSFUL`로 회귀 상태를 확정했다. 초기 Gradle cache metadata/XML 동시 쓰기 문제는 실행환경 concern으로 분리됐다. Evidence: `04_DevLog/2026-07-13_issue-160-input-validation-sensitive-data-security-audit`, repository `docs/security/160-*`.

## 2026-07-13 Issue #179

- [ready] 요청 body가 기존 객체의 권한 등급을 재분류하던 COFFEE duty BFLA를 persisted pollType 기반 선행 인가로 차단하고, 비-COFFEE 3종 무단 수정·완전 불변·계좌 owner/campus/type 회귀를 61개 Poll focused 및 386개 전체 테스트와 격리 Docker HTTP QA로 검증했다. Evidence: `04_DevLog/2026-07-13_issue-179-coffee-template-update-authorization`, repository `docs/resume-metrics.md`.

## 2026-07-12 Issue #176

- [ready] 단일 Redis Lua rotate-or-revoke CAS로 Refresh Token mismatch 판정과 session 폐기 사이 경합을 제거해 동일 credential 병렬 요청을 2개 성공에서 정확히 1개 성공/1개 401로 제한하고, 380개 전체 테스트·수동 revoke 없는 실제 Redis integration·격리 Docker HTTP QA로 검증했다. Evidence: `04_DevLog/2026-07-12_issue-176-refresh-token-rotation-atomicity`, repository `docs/resume-metrics.md`.

## 2026-07-12 Issue #159

- [ready] 최신 `origin/develop` `5b078b5f`에서 21개 Controller·80개 endpoint의 21개 객체 식별자를 56개 권한 경계와 25개 repository predicate까지 추적하고 172개 focused test로 검증해, COFFEE duty가 request body로 비-COFFEE template 권한을 재분류하는 BFLA 1건(Medium, confidence 10/10)을 식별했다. Evidence: `04_DevLog/2026-07-12_issue-159-campus-isolation-idor-security-audit`, repository `docs/security/159-*`.

## 2026-07-12 Issue #156

- [ready] Auth/User의 6개 공개 유스케이스를 전용 Service와 4개 응집 support로 분리해 188줄/103줄 통합 Service를 55줄/19줄 호환 facade로 70.7%/81.6% 축소하고, 6개 구조 게이트·374개 전체 테스트·격리 Docker API QA로 JWT·Redis rotation·FCM·soft-delete 계약 무변경을 검증했다. Evidence: `04_DevLog/2026-07-12_issue-156-user-auth-usecase-separation`, repository `docs/resume-metrics.md`.

## 2026-07-11 Issue #155

- [ready] Batch/Scheduler의 Poll·자동 알림·FCM cleanup 책임을 6개 전용 use case로 분리하고 121줄/296줄 통합 Service를 29줄/34줄 호환 facade로 76.0%/88.5% 축소했으며, 5개 구조 게이트·368개 전체 테스트로 스케줄·정산·Redis fail-closed·retention 정책 무변경을 검증했다. Evidence: `04_DevLog/2026-07-11_issue-155-batch-scheduler-usecase-separation`, repository `docs/resume-metrics.md`.

## 2026-07-11 Issue #154

- [ready] Notification의 FCM token command와 관리자·자동 요청 command를 분리해 105줄/205줄 통합 Service를 33줄/20줄 호환 facade로 각각 68.6%/90.2% 축소하고, 7개 구조 회귀 테스트·362개 전체 테스트로 API·DB·권한·retry·Redis fail-closed 정책 무변경을 보장했다. Evidence: `04_DevLog/2026-07-11_issue-154-notification-fcm-usecase-separation`, repository `docs/resume-metrics.md`.

## 2026-07-11 Issue #153

- [ready] Prayer의 11개 유스케이스를 `PrayerGroupSubmissionCommandService`의 조별 다중 제출을 포함한 7개 응집 Service와 3개 package-private support로 분리해 606줄 통합 Service를 90줄 호환 facade로 85.1% 축소하고, 5개 구조 회귀 테스트·355개 전체 테스트·260개 연관 도메인 테스트로 API·DB·권한·optimistic locking·all-or-nothing 동작 무변경을 보장했다. Evidence: `04_DevLog/2026-07-11_issue-153-prayer-usecase-separation`, repository `docs/resume-metrics.md`.

## 2026-07-10 Issue #152

- [ready] Poll template의 5개 command/query와 자동 생성·커피 정산 책임을 전용 Service/Support/Factory로 분리해 기존 통합 Service를 최대 86.9% 축소하고, 6개 구조 회귀 테스트·350개 전체 테스트·204개 4-domain 테스트·격리 Docker health 검증으로 API·DB·권한·스케줄·정산 동작 무변경을 보장했다. Evidence: `04_DevLog/2026-07-10_issue-152-poll-template-coffee-settlement-separation`, repository `docs/resume-metrics.md`.

<!-- daily-resume-monitor:start:resume-bullet-bank:2026-06-16 -->
## 2026-06-16

- [needs stronger evidence] Maintained a verified local test baseline with 1 tests passing in Gradle XML results. Evidence: daily note for 2026-06-16.
- [needs stronger evidence] Captured previous-day commit evidence for interview and resume follow-up without inferring unstated rationale. Evidence: daily note for 2026-06-16.
<!-- daily-resume-monitor:end:resume-bullet-bank:2026-06-16 -->

<!-- daily-resume-monitor:start:resume-bullet-bank:2026-06-17 -->
## 2026-06-17

- [ready] Implemented Redis-backed JWT refresh/logout flows in Spring Boot and verified the branch with 21 passing local tests, successful build, and 10 REST Docs snippet groups. Evidence: `2026-06-17 Daily Resume Monitor`.
- [ready] Added refresh rotation, reused-token rejection, logout invalidation, and optional current-device FCM deactivation coverage while keeping notification persistence behind an application port. Evidence: `2026-06-17 Auth Refresh Logout Redis`.
- [needs metric] API contract documentation generation is stable through `./gradlew asciidoctor`; add one approved runtime health metric to strengthen the resume story. Evidence: `2026-06-17 Daily Resume Monitor`.
<!-- daily-resume-monitor:end:resume-bullet-bank:2026-06-17 -->
## 2026-07-12 Issue #157

- [ready] Spring Boot API 80개와 service authorization guard를 전수 대조하고, 7개 신뢰 경계·11개 보호 자산·18개 객체 식별자 공격 표면의 위협 모델을 구축해 마지막 active ADMIN 탈퇴 우회 1건(Medium, confidence 10/10)을 코드 수정 없이 확정했다. Evidence: `04_DevLog/2026-07-12_issue-157-threat-model-authorization-matrix`, repository `docs/security/157-*`.

## 2026-07-12 Issue #158

- [ready] JWT/session production·config·schema 47개 파일과 인증·role·FCM API 10개, Redis 인증 흐름 5개를 대조해 refresh rotation의 GET/SET 비원자성으로 동일 credential에서 복수 access token이 발급되고 공격자 SET이 current winner이면 14일 TTL의 refresh를 차단 전 계속 회전해 sliding session persistence를 연장할 수 있는 replay 1건(Medium, confidence 10/10)을 독립 검증하고, 33개 focused test로 기존 lifecycle을 확인했다. Evidence: `04_DevLog/2026-07-12_issue-158-jwt-session-lifecycle-security-audit`, repository `docs/security/158-*`.
<!-- issue-work:start:resume-bullet-bank:2026-07-14-188-189-190-integration -->
## 2026-07-14 Issues #188/#189/#190 Integration

- [ready] 세 기능 브랜치를 merge commit으로 통합하고 경건 재제출 race를 row lock으로 해소해 449개 전체 테스트·151개 REST Docs를 통과했으며, PostgreSQL V1→V8 clean/V7→V8 upgrade와 실제 HTTP 45-step 연결 QA를 실패 0건으로 검증했다. Evidence: `resume-metrics.md` 2026-07-14 integration, `04_DevLog/2026-07-14_issue-188-189-190-integration.md`.
<!-- issue-work:end:resume-bullet-bank:2026-07-14-188-189-190-integration -->
