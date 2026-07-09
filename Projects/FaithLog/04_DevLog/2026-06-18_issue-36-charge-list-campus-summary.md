---
project: FaithLog
type: devlog
issue: "#36"
status: done
created: 2026-06-18
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #36 청구 목록 조회와 캠퍼스별 집계 구현

## 1. 작업 배경

사용자가 본인 청구 목록과 월별 납부 요약을 확인하고, 캠퍼스 관리자/서비스 ADMIN이 캠퍼스 전체 청구 현황과 회원별 청구 상세를 조회할 수 있게 했다.

## 2. 최종 설계 기준

- `startDate`/`endDate`는 #36 조회 API에서 제거한다.
- 백엔드는 전체 청구 이력을 보존하고 pagination/sort/filter로 조회한다.
- 앱 기본 화면에서 최근 납부 항목 중심 UX를 처리한다.
- 월별 요약은 `monthlyPaidAmount`는 `paidAt`, 미납/총 청구/카테고리 집계는 `createdAt` 기준으로 계산한다.
- 관리자 캠퍼스 전체 조회는 `summary + members[]`만 반환하고 개별 item 목록은 포함하지 않는다.
- 관리자 회원별 상세 응답에는 대상 회원 `userId`, `name`, `email`을 포함한다.

## 3. 구현 내용

- Entity: `ChargeItem.createdAt()` 조회 accessor 추가
- Command/Query: `MyChargeListQuery`, `MyChargeSummaryQuery`, `AdminCampusChargeListQuery`, `AdminMemberChargeListQuery`
- Service: `BillingQueryService`
- Repository: `ChargeSearchCriteria`, `ChargeItemRepositoryPort.searchCharges`
- Controller: 내 청구 목록/요약, 관리자 캠퍼스 집계, 관리자 회원 상세 조회 API
- Test: `BillingQueryServiceTest`, `BillingControllerTest`, `BillingApiRestDocsTest`

## 4. TDD 기록

1. 실패 테스트 작성: `BillingQueryServiceTest`, `BillingControllerTest`
2. 실패 확인: Query service/result 타입 부재로 `compileTestJava` 실패, 새 조회 endpoint 미구현으로 Controller 테스트 200 assertion 실패
3. 최소 구현: 조회 전용 service/result/DTO/controller 추가
4. 테스트 통과: focused query/controller/docs tests 통과
5. 리팩토링: 기존 상태 변경 응답 DTO와 목록 item DTO 분리

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL`, 79 tests / 0 failures / 0 errors / 0 skipped

추가 검증:

- `./gradlew test --tests 'com.faithlog.billing.*'`: 성공
- `./gradlew build`: 성공
- `./gradlew asciidoctor`: 성공
- `docker compose build app`: 성공
- `docker compose up -d postgres redis app`: 성공
- 컨테이너 내부 `GET /api/v1/health`: `status=UP`
- `docker compose down`: 성공

## 6. 고민한 부분

- 날짜 필터는 사용자 UX 관점에서 제거하고, 이력 보존과 pagination을 백엔드 책임으로 유지했다.
- 관리자 캠퍼스 전체 조회에서 개별 item을 빼고 회원별 aggregate만 반환해 화면과 API 책임을 단순화했다.
- 월별 요약은 실제 납부액과 청구 생성액이 서로 다른 날짜 기준을 갖기 때문에 테스트와 REST Docs에 기준을 명시했다.

## 7. PM 재검증 보강

- GitHub Issue #36 본문에서 `startDate`/`endDate` query parameter를 제거하고 최신 확정 결정을 정리했다.
- Notion `16.1`, `16.4`, `16.5`, `API 설계`, `FaithLog 통합 기획서·ERD·API 설계`를 최신 조회 정책에 맞게 동기화했다.
- 관리자 캠퍼스 청구 조회 `status=UNPAID` 회귀 테스트를 추가해 미납 청구가 있는 회원만 `members[]`에 포함되고 paid/waived/canceled만 있는 회원은 제외되는 계약을 고정했다.
- `BillingController`와 `AdminBillingController`의 page/size/sort 파싱 중복을 `BillingPageRequests`로 추출했다.
- 구현 변경 전 추가 회귀 테스트는 이미 통과해 기존 동작이 정책을 만족함을 확인했고, 이후 리팩터링 후 전체 검증을 다시 통과했다.

## 8. PM 재검토 sort 버그 수정

- 문제: 관리자 캠퍼스 청구 회원별 집계 조회에서 `amount`, `status`, `paymentCategory` 같은 charge item 전용 sort 값이 유효 요청처럼 통과하지만 실제로는 `latestChargeCreatedAt` 기준으로 정렬될 수 있었다.
- TDD 실패 확인: `sort=amount,asc`는 `400 Bad Request`, `sort=unpaidAmount,desc`는 정상 동작해야 하는 컨트롤러 테스트를 먼저 추가했고, 구현 수정 전 8 tests / 1 failed로 실패했다.
- 수정: 관리자 회원 집계 정렬 허용 목록을 `createdAt`, `userId`, `name`, `email`, `totalAmount`, `unpaidAmount`, `paidAmount`, `waivedAmount`, `canceledAmount`로 제한했다.
- 재검증: `./gradlew test --tests 'com.faithlog.billing.*'`, `./gradlew test`, `./gradlew build`, `./gradlew asciidoctor` 모두 성공했다.
- 추가 문제: `sort=name,wrong`, `sort=createdAt,ascending`, `sort=unpaidAmount,foo` 같은 잘못된 direction 값이 조용히 `DESC`로 처리될 수 있었다.
- 추가 TDD 실패 확인: `sort=unpaidAmount,wrong`과 `sort=createdAt,ascending`이 `400 Bad Request`와 `지원하지 않는 정렬 방향입니다.`를 반환해야 하는 테스트를 먼저 추가했고, 구현 수정 전 8 tests / 1 failed로 실패했다.
- 추가 수정: direction이 없으면 기본 `DESC`를 유지하고, direction이 있으면 `asc` 또는 `desc`만 허용하도록 `BillingPageRequests` 내부에 검증을 추가했다.
- 추가 재검증: `./gradlew test --tests 'com.faithlog.billing.*'`, `./gradlew test`, `./gradlew build`, `./gradlew asciidoctor` 모두 성공했다.
- 추가 문제: `sort=createdAt,desc,extra`, `sort=unpaidAmount,asc,ignored`처럼 쉼표 토큰이 3개 이상인 malformed sort가 앞의 두 토큰만 사용되어 정상 처리될 수 있었다.
- 추가 TDD 실패 확인: malformed sort가 `400 Bad Request`와 `지원하지 않는 정렬 형식입니다.`를 반환해야 하는 테스트를 먼저 추가했고, 구현 수정 전 8 tests / 1 failed로 실패했다.
- 추가 수정: `BillingPageRequests.sort()`에서 comma token이 2개를 초과하면 `INVALID_REQUEST`로 차단했다.
- 추가 재검증: `./gradlew test --tests 'com.faithlog.billing.*'`, `./gradlew test`, `./gradlew build`, `./gradlew asciidoctor` 모두 성공했다.

## 9. 트러블슈팅

- 문제: `./gradlew asciidoctor`가 샌드박스에서 Gradle wrapper lock 파일 접근 실패
- 원인: `~/.gradle/wrapper`가 샌드박스 쓰기 범위 밖
- 해결: 권한 상승 재실행으로 문서 렌더 성공
- 재발 방지: Gradle wrapper lock 실패 시 동일 명령을 권한 상승으로 재실행

## 10. 다음 작업

- [ ] PM 리뷰 후 브랜치 push 여부 확인
- [ ] 프론트 기본 화면에서 최근 납부 항목 노출 UX 구체화

## 11. Velog 글감

- 조회 API에서 날짜 필터를 제거하고 이력 보존 + UX 노출 정책으로 분리한 이유
