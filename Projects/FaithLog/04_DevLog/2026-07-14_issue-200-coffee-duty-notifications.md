---
project: FaithLog
type: devlog
issue: "#200"
status: review
created: 2026-07-14
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - notification
  - billing
  - authorization
  - rest-docs
---

# #200 커피 담당자 다중 지정·전용 권한과 밥·커피 미납 알림

## 1. 작업 배경

기존 COFFEE 담당은 캠퍼스별 한 명만 ACTIVE로 둘 수 있어 새 지정이 이전 담당자를 해제했다. 관리자 역할은 담당 여부와 무관하게 COFFEE write를 우회할 수 있었고, 범용 미납 알림은 담당자 소유 계좌와 category를 분리하지 않았다.

## 2. 최종 설계 기준

- 캠퍼스별 ACTIVE COFFEE 담당자 수 제한 제거
- 동일 campus/user/dutyType ACTIVE 지정은 additive/idempotent
- 관리자 읽기 권한은 유지하되 COFFEE write 우회는 제거
- COFFEE 투표는 생성 담당자, 계좌와 청구는 계좌 소유 담당자만 관리
- COFFEE 템플릿은 같은 캠퍼스 ACTIVE COFFEE 담당자 공동 관리
- COFFEE 템플릿은 계좌 중립으로 저장하고 실제 투표 생성 시 requester 소유 active COFFEE 계좌 지정
- 본인 소유 COFFEE/MEAL 계좌에 UNPAID가 있으면 담당 해제 409
- ACTIVE COFFEE/MEAL 담당 배정이 남은 회원 삭제와 stale 담당 재가입은 `CAMPUS_MEMBER_ACTIVE_DUTY_CONFLICT` 409
- 담당 회원 삭제 전 프론트가 개별 담당 해제를 수행하며 서버는 자동 revoke나 책임 이전을 하지 않음
- 알림은 선택 ID 없이 담당자 소유 계좌의 해당 category 전체 UNPAID를 계좌·수신자별 합산
- 제목은 서버 고정이며 본문은 청구 title별 건수·금액을 최대 5종, 초과 시 `외 N종`, 마지막에 전체 미납 합계로 표시
- 같은 계좌·수신자·Asia/Seoul 날짜는 하루 1회 Redis dedupe
- COFFEE 투표는 scheduler 자동 생성에서 제외하고 담당자가 수동 생성
- 수동 생성된 COFFEE 투표의 예정 마감과 CLOSED 정산은 유지
- 공개 API 경로와 승인된 request/202 response 계약은 변경하지 않음

## 3. 구현 내용

- Campus: 다중 ACTIVE 지정과 동일 사용자 idempotency, 사용자별 duty 조회
- Authorization: COFFEE 투표 생성자, 계좌 owner, 청구 계좌 owner를 command 경계에서 검증
- Billing: 비활성·soft deleted 계좌까지 포함한 해제 전 UNPAID 조회
- Notification: body 없는 COFFEE/MEAL reminder controller와 담당 범위 집계 service 추가
- Concurrency: 담당 해제와 COFFEE/MEAL 정산이 동일 ACTIVE duty assignment의 `PESSIMISTIC_WRITE`를 공유
- Concurrency: campus row를 쓰는 지정·해제·계좌 생성은 `campus -> duty -> entity`, 나머지는 `duty -> poll/template/account/charge` 순서로 직렬화
- Campus membership: 회원 삭제·재가입은 `campus -> duty -> member` 순서로 직렬화하고, 담당 목록은 ACTIVE assignment와 ACTIVE membership을 함께 조회
- Redis: rollback이면 daily dedupe를 먼저 정리한 뒤 transaction completion에서 manual lock을 해제하고, commit 뒤 lock release 실패는 커밋된 log/dedupe를 보존
- Performance: reminder는 requester 소유 account ID `IN`으로 DB 조회하고 empty set은 query를 생략하며, dispatch는 request 전체 FCM token bulk query 1회를 유지
- Notification: 영구 실패 token을 request-local snapshot에서도 제거해 같은 수신자의 다음 account log에서 재사용하지 않음
- Scheduler: 단일 COFFEE classifier로 canonical·legacy mixed COFFEE operation을 자동 생성에서 제외
- DB: V9에서 캠퍼스 단일 ACTIVE COFFEE index를 사용자별 active partial unique index로 교체하고, V10에서 정상 template 계좌를 null로 중립화하며 legacy mixed row는 보존·비활성 격리
- REST Docs: 두 reminder endpoint와 additive PUT, unpaid DELETE conflict 정책을 AsciiDoc에 반영

## 4. TDD 기록

1. 담당자 cardinality RED: focused 28 tests 중 승인 계약 3건 실패
2. 권한·소유권·해제·알림 RED: expanded 35 tests 중 10건 실패
3. 최소 production/API/Redis/Flyway 구현 후 관련 focused suite GREEN
4. 사용자 결정으로 COFFEE 자동 생성 제외 테스트 추가: 6 tests 중 신규 1건 RED
5. scheduler COFFEE 필터 후 6/6 GREEN, 수동 생성 투표의 자동 마감·정산 유지
6. 전체 회귀에서 기존 픽스처 11건이 새 권한 계약과 충돌한 것을 확인하고 담당자/생성자 fixture만 보정
7. 1차 전체 461 tests / 0 failures / 0 errors / 3 skipped
8. 미납 title 상세·5종 제한과 해제/정산 동시성 focused 13 tests 중 6건 RED
9. 상세 본문과 공유 assignment write lock 구현 후 focused 13/13 GREEN
10. 자체 리뷰에서 수신자별 token N+1 구조 테스트 신규 1건 RED 후 bulk query로 GREEN
11. 최종 전체 466 tests / 0 failures / 0 errors / 3 skipped
12. PM 전체 diff 재리뷰 finding 8건을 4개 test-only 커밋으로 추가해 focused `5`, `1`, `3+2`, `4` failures 재현
13. COFFEE 단일 분류, 계좌 중립 공용 template, 삭제 계좌 reminder, rollback dedupe 보상, 관리자 read filter, dispatch bulk token을 최소 수정으로 GREEN
14. duty-gated write와 수동/기한 마감을 duty-first lock으로 통일하고 실제 동시성 테스트 3건 GREEN
15. 동시 마감에서 잠금 전 managed Poll이 stale OPEN으로 재사용되는 추가 race를 발견해 projection scope 후 duty/Poll 순차 잠금으로 해결
16. 자체 리뷰에서 MEAL 계좌 목록의 read-only duty write lock과 계좌 비활성화의 duty/account lock 누락을 focused 8 tests 중 2 failures로 재현
17. 목록은 non-locking duty 조회로 복원하고 비활성화는 `duty -> account` 잠금으로 통일한 뒤 focused GREEN
18. 전체 483 tests / 0 failures / 0 errors / 3 skipped
19. PM 3차 재리뷰 7 findings를 회원 상세 소유권, 혼합 template, 공유 template 경합 3종, 해제/재지정 2종, rollback retry gap, 영구 실패 token, scoped DB query RED로 각각 재현
20. 최소 잠금·query·transaction completion·token snapshot 수정 후 focused suite GREEN
21. 전체 회귀 첫 실행에서 장기 test transaction이 manual lock completion을 지연한 MockMvc fixture 1건을 발견해 실제 HTTP transaction 경계로 보정
22. 최종 전체 495 tests / 0 failures / 0 errors / 3 skipped
23. PM 최종 재리뷰 3 findings를 레거시 혼합 Poll 종료, duty lock 대기 중 회원 PAID stale overwrite, 담당 해제의 campus-wide UNPAID overfetch RED로 각각 재현
24. Poll 분류/잠금 후 구성 검증, scalar ChargeItem lock scope와 `duty -> charge FOR UPDATE`, owned account ID scoped UNPAID query로 최소 수정
25. 자체 리뷰에서 불일치 `pollType=COFFEE` legacy Poll의 due 자동 마감·무정산 경계를 신규 1 test RED로 재현하고 공통 classifier로 OPEN 유지
26. 신규 5 tests와 인접 focused suites GREEN, 최종 전체 500 tests / 0 failures / 0 errors / 3 skipped
27. 프론트 계약 대조 후 사용자 최종 결정에 따라 공개 Poll 목록/상세에는 서버 계산 `manageableByMe`만 추가하고 `createdByUserId`는 공개 DTO·REST Docs에서 제거. 내부 creator는 COFFEE 소유권 계산에만 사용
28. PM finding의 MEAL manageable 권한과 revoke exists query를 RED/GREEN으로 보강
29. 전체 diff 자체 리뷰에서 비활성 멤버의 잔존 COFFEE duty가 capability·due close·settlement를 통과하는 3건, duty lock 대기 뒤 stale COFFEE account 중복 삭제, dispatch lock 전 stale PENDING snapshot을 RED로 재현
30. ACTIVE membership fail-closed, immutable account scope + 잠금 후 재검증, dispatch lock 뒤 PENDING 재조회로 수정
31. Redis daily dedupe owner token + compare-delete, manual/dispatch lock lease 갱신, recovery의 active dispatch 보호를 추가하고 focused GREEN
32. 알림 403/409/503과 COFFEE/MEAL 담당 해제 미납 409 REST Docs를 추가하고 전체 518 tests GREEN
33. PM 후속 finding에서 담당 회원 삭제가 revoke 미납 차단을 우회하고 재가입이 stale duty를 복원하는 경계를 서비스·동시성 6 failures와 REST Docs 2 failures로 재현
34. 사용자 승인대로 회원 삭제/재가입 409, 자동 revoke 금지, `campus -> duty -> member` 잠금과 ACTIVE membership 결속 목록을 구현해 전체 526 tests GREEN
35. 최종 전체 diff 리뷰에서 숨겨진 stale duty의 공개 API 복구 불가, ACTIVE 담당 계정 탈퇴 우회, 역할 변경 stale flush의 회원 삭제 되살림 경계를 발견하고 사용자 추천안 승인 후 4 tests RED로 고정
36. 기존 담당 목록에 optional `staleOnly=true`를 추가해 기존 응답 구조로 stale assignment ID를 제공하고, 조회→기존 해제→재가입 경로를 실제 API 테스트로 통과
37. ACTIVE COFFEE/MEAL 담당이 어느 캠퍼스든 남아 있으면 계정 탈퇴도 `409 CAMPUS_MEMBER_ACTIVE_DUTY_CONFLICT`로 차단하고 자동 해제 금지
38. 계정 탈퇴는 campus ID 순서로 `campus -> duty -> member -> user`, 역할 변경은 `campus -> member` 잠금을 사용해 지정·해제·삭제와 직렬화
39. PM residual finding에서 관리자 직접 stale 재활성화, invalid `staleOnly`, 담당 목록 N+1, MEAL 오류 문구, stale 미납 복구 5건을 RED로 재현
40. 실제 2-transaction 테스트에서 탈퇴 중 신규 가입 성공, login stale flush의 탈퇴 계정 부활, requester 역할 강등 뒤 회원 삭제 성공 3건을 추가 RED로 재현
41. 사용자 승인대로 user ID 오름차순 `user -> campus -> duty -> member` 잠금을 login/join/create/admin add/role/member/withdrawal writer에 적용하고 캠퍼스 잠금 뒤 requester 권한을 재검증
42. INACTIVE 멤버십 + ACTIVE 동일 담당 + 담당자 소유 UNPAID에만 서비스 ADMIN의 기존 status PATCH 명시 복구를 허용하고 정상 담당/일반 관리자 bypass는 유지 차단
43. invalid `staleOnly` 400, 담당 목록 bulk user 조회, 중립 담당 not-found 문구와 REST Docs를 반영
44. 최종 전체 539 tests, build/asciidoctor, REST Docs 167 groups GREEN

## 5. 테스트 결과

- `./gradlew test`: BUILD SUCCESSFUL, 539 tests / 0 failures / 0 errors / 3 skipped, 84 suites
- `./gradlew build`: BUILD SUCCESSFUL, 12초
- `./gradlew asciidoctor`: BUILD SUCCESSFUL, 19초
- REST Docs snippet group: 167개
- test source: 89개
- Flyway: V1-V10
- `git diff --check`: 성공
- Docker/실데이터/PostgreSQL 실마이그레이션: 사용자 승인 범위 밖이므로 미실행

## 6. 고민한 부분

자동 생성 COFFEE 투표는 사람이 생성하지 않아 `createdBy`가 null이었고 생성자 소유권과 충돌했다. 계좌 owner를 자동 투표 owner로 추정하지 않고 사용자에게 확인했으며, 최종적으로 COFFEE를 자동 생성 대상에서 제외했다. API 필드는 호환을 위해 유지하고 scheduler 동작만 제한했다.

담당 해제의 미납 검증과 정산의 청구 생성이 동시에 실행되면 해제 검증 직후 새 UNPAID가 만들어질 수 있었다. 두 경로가 같은 ACTIVE duty assignment 쓰기 잠금을 사용하게 해 정산 선행 시 해제가 새 미납을 보고 409를 반환하고, 해제 선행 시 정산이 ACTIVE duty 검증에 실패하도록 직렬화했다.

PM 재리뷰 후 이 잠금 원칙을 투표·템플릿·계좌·청구 상태·미납 알림과 MEAL command까지 확장했다. 수동 마감과 기한 마감의 실제 동시 실행에서는 duty lock 대기 전에 읽은 Poll Entity가 영속성 컨텍스트에 남아 잠금 후에도 stale OPEN으로 재사용됐다. 잠금 전에는 Entity가 아닌 projection으로 campus/creator/type만 읽고, duty 잠금 뒤 Poll Entity를 처음 `FOR UPDATE` 로드하도록 바꿨다.

최종 자체 리뷰에서 MEAL 계좌 목록이 read-only transaction인데도 duty write lock을 사용하고, 실제 계좌 비활성화 command는 반대로 duty/account lock을 사용하지 않는 비대칭을 발견했다. 목록은 일반 ACTIVE duty 조회를 사용하고 비활성화는 duty row를 먼저 잠근 뒤 계좌 row를 잠그도록 수정해 담당 해제와 직렬화했다.

공동 COFFEE 템플릿에 원 작성자의 계좌를 저장하면 다른 담당자가 사용할 수 없었다. 사용자 승인에 따라 template은 계좌 중립으로 저장하고 기존 `paymentAccountId` 필드는 호환용으로 유지했다. 실제 template 기반 Poll 생성에서 requester가 본인 소유 active 계좌 ID를 보내며 V10은 정상 template의 기존 계좌 연결을 null로 갱신한다.

V10은 아직 `origin/develop`에 없는 feature-branch migration이므로 새 V11을 만들지 않았다. 정상 COFFEE row는 계좌만 중립화하고, 기존 CUSTOM/OPTION_PRICE/COFFEE 같은 혼합 row는 삭제하지 않은 채 active·auto-create를 끄고 계좌를 null로 만들어 fail-closed로 격리했다.

공유 template은 담당자마다 서로 다른 duty row를 잠그기 때문에 template 자체 경합을 막지 못했다. 잠금 전 projection으로 범위를 읽고 `duty -> template FOR UPDATE` 후 active/config/options를 다시 읽게 해 update/update, update/deactivate, create-from-template/update를 같은 row에서 직렬화했다.

## 7. 트러블슈팅

- 문제: 전체 회귀 460 tests 중 11 failures
- 원인: 기존 query/docs/integration fixture가 COFFEE 담당 지정 없이 관리자 계좌를 만들거나 다른 사용자가 만든 COFFEE 투표를 관리자로 마감
- 해결: production 권한을 완화하지 않고 fixture에 실제 ACTIVE duty를 지정하고 COFFEE 마감 호출자를 생성 담당자로 변경
- 재발 방지: COFFEE write fixture는 duty와 owner/creator를 명시하고, 관리자 읽기 테스트와 write 권한 테스트를 분리
- 추가 문제: Redis daily reservation은 service body 성공 뒤 DB commit 또는 manual lock release가 실패하면 25시간 남을 수 있었음
- 해결: transaction synchronization `afterCompletion`에서 COMMITTED가 아닌 모든 예약을 해제하고 commit/release failure 재시도를 테스트로 고정
- 추가 문제: rollback DB lock 해제와 `afterCompletion` dedupe cleanup 사이에 재시도가 들어오면 stale key를 duplicate로 commit한 뒤 원 요청 cleanup이 key를 지워 두 요청 모두 log 없이 끝날 수 있었음
- 해결: transaction completion까지 manual lock을 유지하고 rollback 시 `dedupe cleanup -> manual lock release` 순서를 고정. commit 뒤 lock release 실패는 이미 커밋된 PENDING log와 dedupe를 보존
- 추가 문제: 레거시 혼합 Poll close가 `pollType`만으로 권한과 정산을 분류해 비담당 관리자 종료와 무정산 CLOSED를 허용할 수 있었음
- 해결: lock scope의 pollType/chargeGenerationType/paymentCategory 전체로 COFFEE operation을 먼저 분류하고, Poll row 잠금 뒤 구성 일관성을 재검증해 fail-closed
- 추가 문제: 청구 상태 command가 duty lock 전에 managed ChargeItem을 읽어 회원 PAID commit 뒤에도 stale UNPAID를 덮을 수 있었음
- 해결: 잠금 전 scalar projection만 조회하고 duty 잠금 뒤 ChargeItem을 처음 `FOR UPDATE`로 로드해 최신 status와 account ownership을 기준으로 전이
- 추가 문제: 담당 해제가 소유 계좌 0개여도 캠퍼스 전체 category UNPAID entity를 조회했음
- 해결: 빈 account ID 집합은 query 없이 통과하고, 나머지는 requester owned account ID `IN` 범위로만 조회
- 추가 문제: `pollType=COFFEE`인 레거시 불일치 Poll을 due scheduler가 CLOSED로 만든 뒤 정산을 조용히 생략할 수 있었음
- 해결: due 마감 전 공통 classifier consistency를 검사해 불일치 행은 OPEN으로 유지하고 정상 COFFEE만 기존 마감·정산
- 추가 문제: Poll 목록/상세는 모든 캠퍼스 투표를 반환하지만 생성자와 현재 요청자의 관리 가능 여부를 노출하지 않아 다른 COFFEE 담당자 투표의 write 버튼을 프론트가 안전하게 숨길 수 없었음
- 해결: 사용자 최종 결정대로 목록·상세에는 `manageableByMe`만 추가하고 creator ID는 비공개 유지. COFFEE는 ACTIVE membership + ACTIVE duty + 내부 creator, MEAL은 ACTIVE MEAL duty, 그 외 Poll은 관리자 command 권한으로 서버 계산
- 추가 문제: 비활성 캠퍼스 멤버에게 잔존 ACTIVE duty row가 있으면 capability·due close·settlement가 실제 command 권한과 달라질 수 있었음
- 해결: capability, scheduler, settlement 모두 ACTIVE membership을 먼저 확인하고 실패 행은 OPEN/무청구 상태로 격리
- 추가 문제: Redis lock 10분 lease 만료와 소유권 없는 dedupe 삭제, dispatch lock 전 PENDING snapshot이 알림 유실·중복 발송 경계를 만들 수 있었음
- 해결: owner token 기반 lock 갱신과 dedupe compare-delete를 적용하고 dispatch lock 뒤 PENDING 재조회, active worker lock을 recovery가 덮지 않는 계약을 테스트로 고정
- 추가 문제: 캠퍼스 회원 삭제가 ACTIVE COFFEE/MEAL duty를 남긴 채 membership만 INACTIVE로 바꿔 미납 해제 차단을 우회하고 재가입 시 과거 capability를 되살릴 수 있었음
- 해결: ACTIVE duty가 하나라도 남으면 회원 삭제와 stale 재가입을 `409 CAMPUS_MEMBER_ACTIVE_DUTY_CONFLICT`로 거부하고, 담당 목록에서 INACTIVE membership을 제외했다. 회원 삭제·재가입과 지정·해제는 campus 선행 잠금으로 직렬화했다.
- 추가 문제: stale 담당을 기본 목록에서 숨긴 뒤 재가입도 차단하면 기존 해제 API에 필요한 assignment ID를 얻을 수 없어 공개 API 복구가 불가능했음
- 해결: 기본 목록 호환은 유지하면서 `staleOnly=true`일 때만 INACTIVE membership의 ACTIVE 담당을 반환해 기존 해제 API와 재가입을 이어서 수행하도록 했다.
- 추가 문제: 본인 계정 탈퇴는 캠퍼스 회원 삭제 보호를 거치지 않아 ACTIVE 담당과 owned UNPAID 해제 차단을 우회할 수 있었고, 역할 변경의 stale managed membership은 동시 회원 삭제를 ACTIVE로 되살릴 수 있었음
- 해결: 계정 탈퇴도 ACTIVE 담당 409를 적용하고 모든 소속 캠퍼스를 순서대로 잠근 뒤 membership/user를 처리한다. 역할 변경은 campus/member 잠금 뒤 최신 ACTIVE 상태에만 적용한다.
- 추가 문제: 계정 탈퇴가 멤버십 scope를 읽은 뒤 신규 가입이 들어오거나 login/admin role writer가 stale User entity를 flush하면 탈퇴 계정·멤버십이 다시 활성화될 수 있었음
- 해결: 모든 사용자 생명주기 writer가 동일 user row를 먼저 잠그고 여러 사용자는 ID 오름차순, 여러 캠퍼스는 ID 오름차순으로 `user -> campus -> duty -> member` 순서를 공유한다.
- 추가 문제: stale 담당 소유 계좌에 UNPAID가 남으면 담당 해제도 재가입도 막혀 공개 API 복구가 끝나지 않았음
- 해결: 서비스 ADMIN이 기존 청구 상태 PATCH로 해당 stale 담당 소유 UNPAID만 PAID/WAIVED/CANCELED 중 하나로 명시 처리한 뒤 담당 해제하도록 제한된 복구 경로를 추가했다.
- 추가 문제: stale 복구가 requester ADMIN과 charge의 잠금 전 snapshot을 믿으면 동시 권한 강등이나 최신 회원 PAID 뒤 상태를 덮을 수 있고, campus/member와 duty 잠금 순서가 교차할 수 있었음
- 해결: requester user를 먼저 잠그고 `user -> campus -> duty -> member -> charge` 순서로 직렬화하며 locked charge가 계속 UNPAID인지 재검증했다. 복구 target은 PAID/WAIVED/CANCELED만 허용하고 UNPAID는 409로 거부한다.
- 추가 문제: 전역 ADMIN 두 명의 동시 자기 강등 또는 USER→ADMIN 승격과 stale 자기 강등이 교차하면 마지막 ACTIVE ADMIN 불변식이 깨질 수 있었음
- 해결: 전역 역할 변경은 가장 작은 user row를 공통 DB 직렬화 지점으로 잠근 뒤 requester/target 최신 역할과 ADMIN 수를 판단한다. 동시성 RED로 정확히 한 명의 ADMIN이 남는 것을 고정했다.
- 추가 검증: `staleOnly` 잘못된 값의 400 변환을 해당 controller로 제한하고, stale COFFEE 일반 관리자 403·ACTIVE MEAL service ADMIN 404·stale MEAL 성공 REST Docs를 추가했다. 최종 86 suites / 548 tests / 실패·오류 0 / skipped 3, build/asciidoctor, REST Docs 170 groups를 통과했다.

## 8. 다음 작업

- [ ] 최신 `origin/develop...HEAD` 전체 diff PM 재리뷰 finding 0 확인
- [ ] PM이 최신 API·권한·ErrorCode·프론트 UI 명세를 프론트 작업 세션에 전달하고 프론트 정적 검증 완료
- [ ] 양쪽 준비 뒤 PM이 backend develop 통합, PostgreSQL V9/V10 migration, Docker + iOS Simulator 연결 QA 수행
- [ ] QA 디스크 부족 시 승인된 재생성 cache만 순서대로 정리하고 전후 `df`/`du`와 삭제 범위 기록
- [ ] PM 통합 승인 전 push/PR/merge 금지 유지

## 9. Velog 글감

- 역할 기반 권한에서 리소스 소유권 기반 권한으로 전환하며 관리자 bypass를 제거한 과정
- Redis dedupe와 DB transaction 사이의 실패 보상 및 재시도 설계
- 단일 partial unique index를 사용자별 partial unique index로 안전하게 확장하는 migration
