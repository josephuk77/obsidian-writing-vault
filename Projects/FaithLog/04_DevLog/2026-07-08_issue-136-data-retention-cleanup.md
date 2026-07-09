# 2026-07-08 Issue #136 Data Retention Cleanup

## Context

- Issue: #136 `[Build] 운영 데이터 보관 기간과 정리 배치 구현`
- Branch: `build/136-data-retention-cleanup`
- Worktree: `/Users/josephuk77/.codex/worktrees/7d03/FaithLog`
- Project card: GitHub issue `projectItems` was empty, so no Project card was moved.

## User Decisions

- All retention cleanup jobs run at 04:30 in `Asia/Seoul`.
- `prayer_submissions` 1-year retention uses `created_at`.
- Annual `charge_items` retention uses `created_at`.
- Annual charge cleanup deletes only terminal statuses `PAID`, `WAIVED`, and `CANCELED`; `UNPAID` is always preserved.
- No user-facing API and no DB schema change were added.

## Implementation

- Added `DataRetentionCleanupService` and `DataRetentionCleanupResult` under the batch application layer.
- Added a scheduler entry in `FaithLogScheduledJobs` with cron `0 30 4 * * *` and zone `Asia/Seoul`.
- Reused `NotificationLockService` Redis lock abstraction to prevent duplicate daily and annual batch execution.
- Added repository delete queries for notification logs, expired poll graphs, soft-deleted poll comments, prayer submissions, devotion daily checks, weekly devotion records, and terminal charge items.
- Changed logout current-device FCM handling so a matching active `user_fcm_tokens` row is deleted instead of deactivated when `clientInstanceId` or `fcmToken` is supplied. Logout still succeeds when both are omitted.

## TDD Evidence

- Tests were written before implementation.
- Initial focused run failed at `compileTestJava` because `DataRetentionCleanupService` and `DataRetentionCleanupResult` did not exist yet.

## Validation

- Focused retention/scheduler/FCM/auth tests: success.
- Full `./gradlew test`: success, 310 tests / 0 failures / 0 errors / 1 skipped.
- `./gradlew build`: success.
- `./gradlew asciidoctor`: success after rerunning with approval because the first sandbox run could not access the Gradle wrapper lock.
- Docker QA: `docker compose up -d postgres redis app` built and started the app. Host health curl could not connect from the sandbox, but container-internal `GET /api/v1/health` returned `status=UP`. `docker compose down` was completed afterward.

## Safety Notes

- No production Supabase or Upstash data was touched.
- No Swagger documentation annotations were added.
- PR was intentionally not created before PM validation.
