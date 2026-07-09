# 2026-06-20 Issue #40 FCM 토큰 등록과 알림 발송 로그

## 작업 범위

- Branch: `feat/40-fcm-token-notification-log`
- APIs:
  - `POST /api/v1/users/me/fcm-tokens`
  - `DELETE /api/v1/users/me/fcm-tokens/{tokenId}`
  - `POST /api/v1/admin/campuses/{campusId}/notifications`
  - `GET /api/v1/admin/campuses/{campusId}/notification-logs`
- Implemented `user_fcm_tokens` lifecycle, `notification_logs` request_id queue logs, admin notification target resolution, FCM send port separation, no-op FCM adapter, after-commit async dispatch, token-level retry/failure handling, and logout FCM token deactivation port wiring.

## Decisions Applied

- Current conversation and GitHub Issue #40 2026-06-20 decisions override older Notion/local no-retry wording.
- Notification send API returns `202 Accepted` after creating `notification_logs` rows.
- Transient FCM failures retry per token up to 3 times with `1s -> 5s -> 30s`.
- Permanent token failures deactivate `user_fcm_tokens`.
- Long-lived PENDING log reprocessing scheduler is excluded from #40 and left for #24/follow-up.

## Verification

- Notification focused tests passed.
- `./gradlew test`: success, 181 tests / 0 failures / 0 errors / 0 skipped.
- `./gradlew build`: success.
- `./gradlew asciidoctor`: success after rerun with workspace permission escalation for Gradle cache lock access.
- REST Docs snippets added:
  - `notification-register-fcm-token`
  - `notification-deactivate-fcm-token`
  - `notification-send-admin-notification`
  - `notification-list-notification-logs`
- Docker/API QA:
  - `docker compose up -d --build postgres redis app`: success.
  - Container and host health checks returned `{"status":"UP"}`.
  - Verified FCM token register, idempotent re-register/upsert, token deactivate `204`, new active token register, admin notification send `202`, no-op FCM adapter background worker `SENT` update, requestId log lookup, and service MANAGER without campus membership forbidden `403`.
  - `docker compose down`: success.
- Static checks:
  - `git diff --check`: success.
  - No Swagger documentation annotations added.
  - No #40 legacy notification endpoints added.
  - New controllers return DTO/ResponseEntity, not Entity.

## PM Verification Follow-Up

- Added a real Firebase Admin SDK adapter that builds a Firebase `Message` and calls `FirebaseMessaging.send(...)`.
- `FIREBASE_CONFIG_JSON` initializes Firebase from an environment JSON string; `FIREBASE_CONFIG_PATH` initializes from a file path.
- NoOp FCM fallback is limited to `local` and `test` profiles. Non-local/non-test profiles fail fast if Firebase credentials are missing.
- Mapped `UNREGISTERED`, token-not-registered, and payload-valid invalid token errors to permanent failures.
- Mapped rate limit, timeout, and temporary Firebase failures to transient failures so existing retry policy applies.
- Changed `NotificationDeliveryWorker` so FCM calls and retry backoff run outside DB transactions; PENDING snapshot reads and SENT/FAILED/SKIPPED/token updates use short transactions only.
- Connected #40 snippets into `src/docs/asciidoc/index.adoc`.
- Follow-up verification:
  - `./gradlew test --rerun-tasks`: success, 186 tests / 0 failures / 0 errors / 0 skipped.
  - `./gradlew build`: success.
  - `./gradlew asciidoctor`: success after permission-escalated rerun for Gradle cache lock access.
  - `git diff --check`: success.
  - Swagger documentation annotation search: 0 results.
  - Firebase secret/key search: 0 results.
  - Docker compose build/up: success; container and host health returned `{"status":"UP"}`; `docker compose down` success.

## Metrics

- Java sources: 358
- Test files: 38
- REST Docs snippet groups: 83

## Notes

- GitHub Issue #40 had no project item in the queried metadata, so there was no Project card to move to In Progress.
- The PM harness gate script was attempted but the local harness files were missing in this worktree, so validation continued with repository-native tests and build checks.
