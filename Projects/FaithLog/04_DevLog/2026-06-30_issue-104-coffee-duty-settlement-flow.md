---
project: FaithLog
type: devlog
issue: #104
status: done
created: 2026-06-30
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - coffee
  - billing
---

# Issue #104 Coffee Duty Settlement Flow

## Context

QA found two coffee backend gaps: active COFFEE duty USER flows needed stronger account/poll/charge permission coverage, and closing a COFFEE poll did not trigger charge settlement from final `poll_responses` and `poll_response_options`.

PM also approved the user-added option contract:

- COFFEE poll option add uses `menuId` only.
- COFFEE user-added options snapshot menu name, menu code, and price from the backend catalog.
- COFFEE content-only option add returns 400.
- CUSTOM and other non-COFFEE polls keep `{ "content": "..." }` only.
- Non-COFFEE `menuId`, including content plus menuId, returns 400.

## Changes

- Added the #104 decision to `docs/decision-log.md`.
- Changed manual close so CUSTOM polls close only, while COFFEE polls close and then call `CoffeePollSettlementService` in the same transaction.
- Extended `POST /api/v1/campuses/{campusId}/polls/{pollId}/options` to accept `menuId` for COFFEE polls and save menu snapshots into `poll_options`.
- Added detailed poll error codes for invalid user option contracts:
  - `POLL_USER_OPTION_MENU_REQUIRED`
  - `POLL_USER_OPTION_CONTENT_NOT_ALLOWED`
  - `POLL_USER_OPTION_MENU_NOT_ALLOWED`
- Updated Spring REST Docs snippets and `src/docs/asciidoc/index.adoc`.

## Validation

- RED: focused test failed before implementation because `AddPollOptionCommand` and new ErrorCode values did not exist.
- Focused poll service/docs tests passed.
- Billing/poll authorization focused suite passed.
- `./gradlew test`: 259 tests / 0 failures / 0 errors / 1 skipped.
- `./gradlew build`: success.
- `./gradlew asciidoctor`: success.
- `git diff --check`: success.

## Docker API QA

Isolated compose project: `faithlog-qa104api`.

Verified by real HTTP API:

- signup/login and local QA manager setup.
- campus create and ACTIVE member join.
- active COFFEE duty assignment.
- COFFEE account create and deactivate by duty USER.
- PENALTY account create/deactivate denied to duty USER with 403.
- other campus COFFEE account denied with 403.
- COFFEE poll create allowed to duty USER.
- CUSTOM poll create denied to duty USER with 403.
- regular member added a COFFEE option with `menuId`; snapshot stored `AMERICANO_HOT` and 1,500 KRW.
- COFFEE content-only option add returned 400.
- response saved, close triggered settlement, and one COFFEE charge for 1,500 KRW was created.
- duplicate close returned 409 without creating a duplicate charge.
- COFFEE admin charge query allowed to duty USER; PENALTY query denied with 403.
- non-member access returned 403; missing token returned 401.

QA shutdown used `docker compose -p faithlog-qa104api down` without deleting volumes.
