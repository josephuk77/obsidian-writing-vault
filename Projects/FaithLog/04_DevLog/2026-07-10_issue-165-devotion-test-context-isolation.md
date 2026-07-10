---
project: FaithLog
type: devlog
issue: #165
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
---

# #165 Devotion 테스트 순서 오염과 컨텍스트 격리 보강

## 1. 작업 배경

Billing, Devotion, Poll, Batch 테스트를 함께 실행하면 `DevotionServiceTest` 10건이 실패했지만 단독 실행은 성공했다. 대표 실제값은 charge 7건 또는 8건, daily check 66건으로 테스트 내부 생성량보다 컸다.

## 2. 최종 설계 기준

Production 동작과 트랜잭션 정책은 변경하지 않는다. 테스트 프로필의 H2 PostgreSQL 호환 옵션과 `create-drop`은 유지하고, 서로 다른 Spring Context마다 `${random.uuid}`가 포함된 별도 인메모리 DB를 사용한다.

## 3. 구현 내용

- Test config: `application-test.yml`의 H2 DB 이름을 Context별 고유값으로 변경
- Test: 고정 H2 URL 재도입을 막는 `TestDatabaseIsolationConfigTest` 추가
- Production: 변경 없음

## 4. TDD 기록

1. 실패 테스트 작성: `${random.uuid}` URL을 요구하고 고정 `faithlog-test` URL을 거부하는 구조 검사 추가
2. 실패 확인: 1 test / 1 failure
3. 최소 구현: H2 URL의 DB 이름에만 `${random.uuid}` 추가
4. 테스트 통과: 구조 검사와 최소 3클래스 순서 오염 조합 GREEN
5. 리팩토링: 과도한 `@DirtiesContext`나 repository cleanup은 추가하지 않음

## 5. 테스트 결과

- 수정 전 4-domain baseline: 187 tests / 10 failures
- 최소 RED: `BillingQueryServiceTest + DevotionApiRestDocsTest + DevotionServiceTest`, 41 tests / 10 failures
- 최소 GREEN: 같은 조합 41 tests / 0 failures
- 4-domain: 187 tests / 0 failures
- 4-domain 강제 반복: 187 tests / 0 failures
- 전체: 333 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build`: BUILD SUCCESSFUL

## 6. 고민한 부분

REST Docs fixture를 개별 정리하면 FK cleanup 순서와 새 테스트 누락에 계속 결합된다. class-wide Context 재시작은 원인을 가리고 실행 비용을 키운다. 문제 경계가 Spring Context 사이의 DB 공유였으므로 Context마다 DB를 분리했다.

## 7. 트러블슈팅

- 문제: Context 캐시와 실행 순서에 따라 다른 테스트의 committed fixture 관찰
- 원인: 모든 테스트 Context가 `jdbc:h2:mem:faithlog-test`를 공유
- 해결: Context별 고유 H2 이름
- 재발 방지: 테스트 설정 구조 검사

## 8. 다음 작업

- [ ] PM 코드리뷰 후 PR 생성 여부 결정

## 9. Velog 글감

- Spring TestContext cache와 이름 있는 H2 인메모리 DB가 만드는 순서 의존 테스트
