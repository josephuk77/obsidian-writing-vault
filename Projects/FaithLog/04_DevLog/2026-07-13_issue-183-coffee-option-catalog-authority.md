---
project: FaithLog
type: devlog
issue: "#183"
status: done
created: 2026-07-13
tags:
  - FaithLog
  - backend
  - spring-boot
  - security
  - tdd
---

# #183 COFFEE 옵션 가격을 backend catalog로 고정

## 1. 작업 배경

Issue #160 F-160-02에서 direct COFFEE Poll과 COFFEE PollTemplate create/update가 `menuId = null`인 옵션의 client `content`와 `priceAmount`를 그대로 snapshot하고 CLOSED 정산 근거로 사용하는 경로가 확인됐다. #183은 COFFEE 옵션 권한 원천을 active backend `CoffeeMenuCatalog`로 고정한다.

## 2. 최종 설계 기준

- 모든 COFFEE Poll/PollTemplate 옵션은 active catalog `menuId`가 필수다.
- COFFEE snapshot은 catalog의 메뉴명, 메뉴 코드, 가격만 사용한다.
- request DTO의 `content`/`priceAmount`는 프론트 호환을 위해 유지하되 COFFEE에서는 권한 원천으로 사용하지 않는다.
- null은 `400 POLL_COFFEE_OPTION_MENU_REQUIRED`, not-found/inactive는 기존 오류를 재사용한다.
- #179 persisted-target authorization 순서와 cross-campus 404를 유지한다.
- 비-COFFEE custom content/0원, 사용자 COFFEE option-add, `optionIds`/`poll_response_options`, #182 양수 charge 불변식은 유지한다.
- DB/Flyway/dependency는 변경하지 않는다.

## 3. 구현 내용

- Entity/Repository/Controller/DTO: 변경 없음
- ErrorCode: 승인된 `POLL_COFFEE_OPTION_MENU_REQUIRED` 추가
- Resolver: `PollOptionSnapshotResolver`가 `PollType`을 받아 COFFEE와 비-COFFEE를 분리하고 active catalog snapshot을 단일 경계에서 생성
- Direct Poll: 요청 `pollType`을 resolver에 전달
- Template create: 요청 `pollType`을 resolver에 전달
- Template update: #179와 동일하게 persisted `template.pollType()`을 resolver에 전달
- Auto-create/Settlement: 기존 `ScheduledPollFactory`의 snapshot 복사와 `CoffeePollSettlementSupport`의 저장 snapshot 사용을 유지하고 회귀 테스트로 고정
- Test/REST Docs: null/missing/inactive, override, row 불변, auto-create, response-only, manual/scheduler settlement, non-COFFEE/user-add/#179/#182 회귀와 400 계약 보강

## 4. TDD 기록

1. 실패 테스트 작성: direct null, template create/update null, client override, REST Docs 400
2. 실패 확인: `4 tests / 4 failures`
3. 최소 구현: PollType-aware resolver와 COFFEE catalog-only snapshot
4. 테스트 통과: Poll/template/catalog/Batch/REST Docs focused 64 tests GREEN
5. 회귀 확장: #179/#182 포함 Poll·Billing·Batch·REST Docs 87 tests GREEN

## 5. 테스트 결과

- focused: 64 tests / 0 failures / 0 errors / 0 skipped
- #179/#182 포함 집중 회귀: 87 tests / 0 failures / 0 errors / 0 skipped
- 전체 `./gradlew test`: 399 tests / 0 failures / 0 errors / 3 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- `git diff --check`: 성공
- test source: 76개
- REST Docs snippet groups: 124개
- DB migration: V1-V7 유지

## 6. Docker API QA

- #183 전용 PostgreSQL/Redis/app 컨테이너, DB, 포트, named volume로 격리
- Flyway V1-V7, Hibernate validate, health UP, catalog seed 확인
- direct/template/update에서 client 메뉴명·1원 override를 보내도 catalog `아메리카노`/`AMERICANO_HOT`/1,500원 저장·조회
- direct/template create/update null `menuId` 400 및 row/charge 불변
- inactive `menuId` 400 `POLL_MENU_INACTIVE` 및 row 불변
- template→자동 생성 Poll snapshot 일치
- response API 직후 charge 미생성
- scheduler CLOSED 뒤 charge title/amount가 저장 catalog snapshot과 일치
- 총 11개 시나리오 PASS
- volume 삭제 없이 `docker compose down`; 마지막 Docker 명령 `docker builder prune -f`, 696.7MB 회수

## 7. 고민한 부분

COFFEE request DTO 필드를 제거하거나 override를 명시 오류로 거부하면 기존 프론트 fixture와 호환성이 깨질 수 있다. 사용자 승인에 따라 필드는 유지하고 서버가 catalog 값으로 덮어쓰되, null/inactive menu만 명확히 거부했다. 또한 update 검증은 요청 body가 아니라 persisted poll type을 사용해 #179의 인가 대상 고정을 약화하지 않았다.

## 8. 트러블슈팅

- 기본 Gradle cache metadata와 sandbox file-lock socket 문제는 격리 `GRADLE_USER_HOME=/private/tmp/faithlog-gradle-183` 및 승인된 단일 Gradle 실행으로 해결했다.
- 격리 cache 초기 다운로드 중 디스크 여유 경고가 있었으나 파일 삭제나 volume 정리를 임의 수행하지 않았고, 테스트·빌드·Docker QA는 최종 성공했다.
- 별도 PM harness 자료가 없어 임의 생성하지 않고 FaithLog TDD gate를 적용했다.

## 9. 다음 작업

- [ ] PM 코드리뷰 및 독립 검증
- [ ] PM 승인 후 push/PR 결정

## 10. 이력서 문장 후보

COFFEE Poll/template 옵션의 이름·코드·가격 권한을 backend catalog로 고정하고 client override와 null/inactive 우회를 차단했으며, persisted-target 인가 순서를 보존한 채 4개 RED 실패·87개 집중 회귀·399개 전체 테스트·11개 격리 Docker API/스케줄러 정산 시나리오로 검증했다.
