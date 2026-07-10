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
