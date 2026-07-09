---
project: FaithLog
type: devlog
issue: "#72"
status: done
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #72 전체 QA 발견 이슈 보강

## 1. 작업 배경

전체 QA에서 관리자 직접 투표 생성 시 현재 시간이 `startsAt <= now < endsAt` 범위인데도 poll이 `SCHEDULED`로 남아 detail/response/results/comment 흐름이 막히는 문제가 확인됐다.

## 2. 최종 설계 기준

- 현재 기간 직접 생성 poll은 생성 직후 `OPEN`.
- 시작 전 poll은 `SCHEDULED` 유지.
- 커피 투표 응답 API는 응답 저장만 수행하고, `COFFEE` 청구는 CLOSED 커피 투표 정산 서비스에서 최종 응답 기준으로 생성/갱신.
- 상세 API 계약은 Spring REST Docs index에 generated snippets를 include하는 방식으로 보강.

## 3. 구현 내용

- `PollService`의 직접 생성/템플릿 생성 경로에서 생성 시점 현재 기간이면 `poll.open()` 호출.
- #72 회귀 테스트 추가: 현재 기간 CUSTOM poll detail/response/results/comment CRUD, 현재 기간 템플릿 COFFEE poll 응답 직후 charge 0건과 close settlement 후 1건, future poll SCHEDULED 유지, ended poll response `POLL_CLOSED`.
- REST Docs `index.adoc`에 monthly-summary, penalty-rules, poll results/comments/missing-members, prayer season/group/week/submission 섹션 추가.
- local docs와 Notion API/기획서/ERD의 stale 커피 청구/역할 문구 정리.

## 4. TDD 기록

1. 실패 테스트 작성: `PollServiceTest`에 현재 기간 CUSTOM/COFFEE 직접 생성 회귀 테스트 추가.
2. 실패 확인: `./gradlew test --tests com.faithlog.poll.application.PollServiceTest`가 생성 직후 `SCHEDULED` 상태 assertion으로 2건 실패.
3. 최소 구현: 생성 시점 `startsAt <= now < endsAt`이면 `OPEN`으로 전환.
4. 테스트 통과: 동일 PollService 테스트 성공.

## 5. 테스트 결과

- `./gradlew test --tests com.faithlog.poll.application.PollServiceTest`: 성공.
- `./gradlew test --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest --tests com.faithlog.devotion.presentation.PenaltyRuleApiRestDocsTest --tests com.faithlog.poll.presentation.PollApiRestDocsTest --tests com.faithlog.prayer.presentation.PrayerApiRestDocsTest`: 성공.
- `./gradlew test`: 성공, 232 tests / 0 failures / 0 errors / 0 skipped.
- `./gradlew build`: 성공.
- `./gradlew asciidoctor`: 성공.
- `git diff --check origin/develop...HEAD`: 성공.
- Docker/API QA: `docker compose up -d --build postgres redis app` 성공, `GET /api/v1/health` 200/`UP`, 현재 기간 CUSTOM direct poll 생성 직후 `OPEN` 및 detail/response/results/comment CRUD 성공, 현재 기간 template-based poll 생성 직후 `OPEN`, future direct poll `SCHEDULED`, 현재 기간 COFFEE direct poll 응답 직후 charge 0건, scheduler close/settlement 후 `CLOSED`와 COFFEE charge 1건 확인. `docker compose down` 성공.

## 6. 고민한 부분

- `now >= endsAt` 생성 정책은 새 정책으로 바꾸지 않고 기존 검증과 충돌하지 않게 유지했다. 테스트는 OPEN으로 만들지 않고 응답이 기존 `POLL_CLOSED` 계약으로 막히는지만 확인한다.

## 7. 다음 작업

- [x] 전체 `./gradlew test`, `./gradlew build`, Docker compose API QA 완료.
- [ ] PM 검증 후 PR 생성.
