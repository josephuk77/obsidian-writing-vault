---
project: FaithLog
type: troubleshooting
created: 2026-07-10
tags:
  - FaithLog
  - troubleshooting
  - spring-boot
  - test-isolation
---

# Spring Context 간 고정 이름 H2 공유로 발생한 테스트 순서 오염

## 문제 상황

`DevotionServiceTest`는 단독으로 성공했지만 Billing/Devotion/Poll/Batch 묶음에서는 10건이 실패했다. 전체 저장소 테스트 실행 순서와 Spring Context cache 상태에 따라 결과가 달라졌다.

## 에러 메시지

- charge count: expected 0, actual 7
- charge count: expected 1, actual 8
- daily check count: expected 0, actual 66

## 원인 분석

테스트 프로필이 고정 URL `jdbc:h2:mem:faithlog-test`를 사용했다. 서로 다른 Context cache key를 가진 service/Controller/REST Docs 테스트가 별도 Spring Context를 만들면서도 같은 H2 DB를 공유했다. 먼저 생성된 service Context가 캐시된 뒤 REST Docs Context가 비트랜잭션 fixture를 커밋하면, 다시 사용된 service Context가 그 행을 관찰했다.

최소 클래스 순서는 `BillingQueryServiceTest -> DevotionApiRestDocsTest -> DevotionServiceTest`였다. 41개 테스트에서 동일 10건 실패와 charge 3건/daily 29건 오염을 재현했다.

## 해결 방법

테스트 H2 URL을 `jdbc:h2:mem:faithlog-test-${random.uuid}`로 바꿔 Spring Context별 DB를 분리했다. 기존 PostgreSQL compatibility option과 `ddl-auto=create-drop`은 유지했다.

## 재발 방지

`TestDatabaseIsolationConfigTest`가 `${random.uuid}` URL을 요구하고 고정 공유 URL을 거부한다. class-wide `@DirtiesContext`, assertion 완화, 테스트 비활성화는 사용하지 않는다.

## 관련 이슈

- #165
