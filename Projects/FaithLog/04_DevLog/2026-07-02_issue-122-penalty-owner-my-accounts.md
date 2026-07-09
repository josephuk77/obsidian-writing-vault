---
project: FaithLog
type: devlog
issue: #122
status: done
created: 2026-07-02
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - billing
---

# #122 PENALTY 계좌 owner와 내 계좌 정산 조회 정책 보강

## 1. 작업 배경

프론트 정산 화면이 `GET /api/v1/admin/campuses/{campusId}/charges/my-accounts` 기준으로 이동하면서, 캠퍼스 공용 `PENALTY` 계좌를 사용자 owner 기준으로만 필터링하면 캠퍼스 관리자가 벌금 정산을 볼 수 없는 문제가 생겼다.

## 2. 최종 설계 기준

- `PENALTY ownerUserId`는 등록자/관리 담당자 메타데이터다.
- `PENALTY` 생성 시 owner 생략은 requester userId로 저장한다.
- 캠퍼스 관리자와 전역 ADMIN의 `my-accounts`는 active `PENALTY` 계좌를 owner와 무관하게 포함한다.
- 기존 `ownerUserId = null` active `PENALTY` 계좌도 포함한다.
- `COFFEE`는 계속 requester-owned active 계좌만 포함한다.
- MEMBER는 403, 인증 없음은 401을 유지한다.

## 3. 구현 내용

- Service: `BillingService.resolveOwnerUserId`에서 `PENALTY` owner 생략 시 requester userId 저장.
- Query Service: campus manager/service ADMIN 후보 계좌를 active `PENALTY` 전체 + requester-owned active `COFFEE`로 분리.
- Test: service/query/controller/REST Docs 테스트로 owner 기본값, 명시 owner, null owner legacy, 다른 owner PENALTY, COFFEE owner 제한, MEMBER 403을 고정.
- Docs: `decision-log`, backend policy, REST Docs 설명, `index.adoc`, resume metrics 갱신.

## 4. TDD 기록

1. 실패 테스트 작성: `BillingServiceTest`, `BillingQueryServiceTest`, `BillingControllerTest`, `BillingApiRestDocsTest`.
2. 실패 확인: focused billing 테스트 54개 중 5 failures.
3. 최소 구현: owner resolve와 my-account 후보 계좌 계산만 수정.
4. 테스트 통과: focused billing 테스트 성공.
5. 리팩토링: 문서 문구와 HTTP test fixture 정리.

## 5. 테스트 결과

명령:

`./gradlew test`

결과:

`BUILD SUCCESSFUL` / 291 tests / 0 failures / 0 errors / 1 skipped

추가 검증:

- `./gradlew build` 성공
- `./gradlew asciidoctor` 성공
- Docker compose health `UP`
- Docker API QA: PENALTY owner 생략/명시, manager my-accounts 200, member my-accounts 403 확인

## 6. 고민한 부분

`my-accounts`라는 이름은 owner 기준처럼 보이지만, #122 결정에서는 `PENALTY`가 캠퍼스 공용 계좌라 owner를 정산 필터의 핵심 기준으로 쓰지 않는다. 그래서 `PENALTY`와 `COFFEE` 후보 계좌 계산을 분리해 정책이 코드에 그대로 드러나게 했다.

## 7. 트러블슈팅

- 문제: `./gradlew asciidoctor`가 sandbox에서 `~/.gradle` lock 파일 접근 실패.
- 원인: Gradle wrapper lock 파일이 workspace 밖에 있음.
- 해결: 승인 경로로 동일 명령 재실행.
- 재발 방지: Gradle wrapper lock 접근 오류는 문서 렌더링 실패가 아니라 sandbox 권한 실패로 구분한다.

- 문제: Docker API QA 첫 assertion에서 `managerId=1UPDATE1`로 파싱됨.
- 원인: psql `UPDATE ... returning` 결과에 command tag가 함께 출력됨.
- 해결: DB select 기반으로 id를 다시 읽어 검증.
- 재발 방지: QA assertion에는 update 결과와 id 조회를 분리한다.

## 8. 다음 작업

- [ ] PM 검증 후 PR 생성 여부 결정

## 9. Velog 글감

- 공용 계좌와 사용자 소유 계좌가 섞인 정산 API에서 owner 필터를 분리하는 방법
