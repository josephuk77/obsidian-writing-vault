---
project: FaithLog
type: devlog
issue: "#179"
status: done
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - tdd
---

# #179 COFFEE duty 투표 템플릿 수정 권한 대상을 저장 상태로 고정

## 1. 작업 배경

Issue #159의 F-159-01은 active COFFEE duty가 request body의 COFFEE billing 필드로 persisted 비-COFFEE 템플릿 수정 권한을 획득할 수 있음을 확인했다. #179는 기존 객체의 권한 등급을 사용자 입력이 재분류하지 못하도록 update 인가 기준을 persisted `template.pollType()`에 고정한다.

## 2. 최종 설계 기준

- same-campus 확인과 기존 `POLL_TEMPLATE_NOT_FOUND` 404 존재 은닉을 먼저 유지한다.
- persisted `COFFEE` 템플릿만 campus manager/service ADMIN/active COFFEE duty 수정 경계를 사용한다.
- persisted `CUSTOM`, `WED_SERVICE`, `SATURDAY_LEADER`는 campus manager 또는 service ADMIN만 수정한다.
- 인가 뒤 요청 billing/account 조합을 별도 검증하고 requester-owned active same-campus COFFEE account 조건을 유지한다.
- 거부 시 template 필드와 option row를 전혀 변경하지 않는다.

## 3. 구현 내용

- Entity: 변경 없음
- Command/DTO: 변경 없음
- Service: `PollTemplateCommandService.updateTemplate`가 `requirePersistedTemplateManageAccess`로 persisted `pollType`만 먼저 판정하도록 변경
- Repository: 변경 없음
- Controller/API mapping: 변경 없음
- Test: persisted 비-COFFEE 3종 거부/완전 불변, COFFEE 계좌 scope, manager/ADMIN 성공, cross-campus 404, HTTP status/code/message와 REST Docs 회귀 추가

## 4. TDD 기록

1. 실패 테스트 작성: persisted `CUSTOM`, `WED_SERVICE`, `SATURDAY_LEADER` 각각에 duty가 COFFEE body로 update를 시도하는 3건
2. 실패 확인: `3 tests / 3 failures`; 세 유형 모두 기존 권한 우회를 재현
3. 최소 구현: update 인가를 request billing 필드와 분리하고 persisted `pollType` 기반으로 고정
4. 테스트 통과: 신규 6개 시나리오 및 Poll focused 전체 GREEN
5. 리팩토링: create의 기존 body 기반 분류는 유지하고 update 전용 persisted-target helper로 책임을 분명히 함

## 5. 테스트 결과

- Poll focused 4 classes: 61 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 386 tests / 0 failures / 0 errors / 2 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: 성공
- REST Docs snippet groups: 123

## 6. Docker HTTP QA

- 격리 project: `faithlog-qa-179-20260713`
- health: 200
- campus manager persisted 비-COFFEE update: 200
- active duty persisted 비-COFFEE + COFFEE body update: 403 `POLL_TEMPLATE_MANAGE_FORBIDDEN`
- cross-campus update: 404 `POLL_TEMPLATE_NOT_FOUND`
- active duty persisted COFFEE create/update: 201/200
- 거부 뒤 template 전체 필드와 option rows 불변 확인
- token 값은 출력하거나 기록하지 않음
- 동일 project를 volume 삭제 없이 down; 마지막 Docker 명령 `docker builder prune -f`, dangling build cache 696.6MB 회수

## 7. 고민한 부분

인가와 요청된 billing/account 유효성 검증을 한 boolean 분류로 섞으면 request body가 기존 객체의 권한 class를 바꿀 수 있다. 따라서 target authorization은 persisted state로 먼저 종결하고, 요청 configuration 검증은 그 다음 단계로 유지했다. 새 ErrorCode나 전역 403/404 정책은 필요하지 않았다.

## 8. 트러블슈팅

- Asciidoctor 첫 실행에서 sandbox가 Gradle wrapper lock 접근을 거부했다. 동일 명령을 승인된 Gradle 실행으로 재시도해 성공했다.
- Docker host port는 Codex sandbox에서 접근되지 않아 app 컨테이너 내부 loopback으로 실제 HTTP QA를 실행했다.

## 9. 다음 작업

- [ ] PM 검증 후 push/PR 여부 결정

## 10. 이력서 문장 후보

요청 body가 기존 객체의 권한 등급을 재분류하던 COFFEE duty BFLA를 persisted pollType 기반 선행 인가로 차단하고, 비-COFFEE 3종 무단 수정·완전 불변·계좌 owner/campus/type 회귀를 61개 Poll focused 및 386개 전체 테스트와 격리 Docker HTTP QA로 검증했다.
