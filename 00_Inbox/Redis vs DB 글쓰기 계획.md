---
title: "Redis vs DB 글쓰기 계획"
created: "2026-05-14"
updated: "2026-05-14"
type: planning
status: draft
tags: [redis, database, transaction, acid, lock, backend, blog]
source_notes:
  - "사용자 제공 ChatGPT 공유 링크: https://chatgpt.com/share/6a05765d-06e8-83ab-88c7-007b7f3072ca"
  - "Redis Docs - Transactions: https://redis.io/docs/latest/develop/using-commands/transactions/"
  - "Redis Docs - Distributed Locks: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"
  - "PostgreSQL Docs - Transactions: https://www.postgresql.org/docs/current/tutorial-transactions.html"
  - "PostgreSQL Docs - Explicit Locking: https://www.postgresql.org/docs/current/explicit-locking.html"
publish_url:
---

# Redis vs DB 글쓰기 계획

## 작성된 글

- 아직 없음

## 글의 방향

Redis와 일반적인 DB를 단순히 "빠르다 / 느리다"로 비교하지 않는다.

이번 글의 핵심은 Redis와 DB가 트랜잭션, ACID, Lock을 바라보는 방식이 다르다는 점을 정리하는 것이다.

특히 취준생이나 백엔드 입문자가 자주 헷갈리는 지점을 중심으로 쓴다.

- Redis도 트랜잭션이 있는데 DB 트랜잭션과 같은가?
- Redis의 원자성은 ACID의 Atomicity와 같은 의미인가?
- Redis는 싱글 스레드라는데 Lock이 왜 필요한가?
- DB Lock과 Redis Lock은 같은 문제를 푸는가?
- 데이터 정합성이 중요한 작업을 Redis에 맡겨도 되는가?

## 예상 독자

- Spring Boot 프로젝트에서 Redis를 캐시나 세션 저장소로 써본 사람
- DB 트랜잭션과 `@Transactional`은 공부했지만 Redis 트랜잭션은 생소한 사람
- 동시성 문제를 해결할 때 DB Lock과 Redis Lock 중 무엇을 써야 할지 헷갈리는 사람
- 면접에서 "Redis와 DB의 차이", "Redis는 ACID를 보장하나요?", "분산락이 뭔가요?" 같은 질문을 대비하고 싶은 사람

## 핵심 결론

Redis와 DB는 둘 다 데이터를 저장할 수 있지만, 기본 목적과 보장 범위가 다르다.

DB 트랜잭션은 여러 SQL 작업을 하나의 논리적 작업 단위로 묶고, 실패 시 롤백하며, 격리 수준과 Lock을 통해 데이터 정합성을 지키는 데 초점이 있다.

Redis는 빠른 메모리 기반 처리를 위해 설계되었고, 개별 명령과 `MULTI/EXEC` 블록의 원자적 실행을 제공하지만, 일반적인 RDBMS처럼 롤백 중심의 ACID 트랜잭션을 제공하는 것은 아니다.

Redis Lock은 DB 내부의 행 잠금과 다르다. Redis Lock은 여러 서버나 프로세스가 같은 작업을 동시에 수행하지 못하게 막기 위한 애플리케이션 레벨의 분산락에 가깝다.

## 글을 나누는 기준

한 글에 모두 넣으면 너무 길어지고 초점이 흐려진다.

따라서 아래처럼 3개의 글로 나누는 것이 좋다.

- 1편: Redis vs DB, 저장소의 목적과 트랜잭션 차이
- 2편: Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가
- 3편: Redis Lock과 DB Lock은 언제 다르게 써야 할까

## 시리즈 전체 제목 후보

- Redis vs DB, 트랜잭션과 Lock 관점에서 이해하기
- Redis는 DB를 대체할 수 있을까?
- Redis 트랜잭션과 DB 트랜잭션은 왜 다를까?
- Redis Lock과 DB Lock, 언제 무엇을 써야 할까?

## 1편 계획: Redis vs DB, 저장소의 목적부터 다르다

## 글의 목적

Redis와 DB를 비교할 때 먼저 "무엇을 보장하려는 저장소인가"를 잡는다.

Redis는 캐시, 세션, 카운터, 랭킹, 임시 상태 저장처럼 빠른 접근과 TTL이 중요한 곳에 강하다.

RDBMS는 주문, 결제, 재고, 회원 정보처럼 정합성과 영속성이 중요한 핵심 데이터를 다루는 데 강하다.

## 핵심 문장

> Redis와 DB는 둘 다 데이터를 저장하지만, Redis는 빠른 접근과 단순한 원자 연산에 강하고, DB는 데이터 정합성과 영속성 보장에 강하다.

## 목차

## Redis와 DB를 왜 비교하게 되는가

프로젝트에서 조회 성능을 높이기 위해 Redis를 붙이거나, 동시성 제어를 위해 Redis Lock을 도입하면서 둘의 경계가 헷갈리기 시작한다.

예시:

- 로그인 세션을 Redis에 저장한다
- 게시글 조회수를 Redis에서 증가시킨다
- 상품 재고 차감을 Redis Lock으로 감싼다
- 주문 데이터는 DB에 저장한다

여기서 "Redis도 저장소인데 DB처럼 쓰면 안 되나?"라는 질문이 나온다.

## DB가 강한 영역

DB는 데이터 정합성이 핵심인 저장소다.

주문 생성, 결제 기록 저장, 재고 감소 같은 작업은 일부만 성공하면 안 된다.

```sql
BEGIN;
UPDATE product SET stock = stock - 1 WHERE id = 1;
INSERT INTO orders(product_id, quantity) VALUES (1, 1);
COMMIT;
```

중간에 실패하면 `ROLLBACK`으로 이전 상태로 되돌릴 수 있다.

## Redis가 강한 영역

Redis는 메모리 기반이라 빠르고, TTL과 자료구조가 강점이다.

예시:

- 인증 토큰 TTL 관리
- 실시간 랭킹
- 조회수 카운터
- 중복 요청 방지 키
- 캐시

```redis
INCR post:1:view_count
EXPIRE login:token:abc 3600
```

Redis의 개별 명령은 원자적으로 처리되므로 단순 카운터 증가 같은 작업에 잘 맞는다.

## Redis를 DB처럼 쓸 때 조심할 점

Redis에도 persistence 설정이 있지만, 보통 RDBMS와 같은 방식의 트랜잭션/롤백/영속성 보장을 기대하고 쓰면 위험하다.

중요한 원본 데이터는 DB에 두고, Redis는 빠른 조회나 임시 상태 관리에 사용하는 구조가 기본이다.

핵심 문장:

> Redis를 쓰더라도 원본 데이터의 최종 정합성은 DB가 책임지도록 설계하는 경우가 많다.

## 1편에서 제외할 내용

- Redis Cluster 내부 구조
- AOF/RDB persistence 상세 옵션
- 모든 Redis 자료구조 설명
- CAP 이론 상세 설명

## 2편 계획: Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가

## 글의 목적

Redis에도 `MULTI`, `EXEC`, `DISCARD`, `WATCH`가 있기 때문에 "Redis 트랜잭션도 DB 트랜잭션처럼 ACID를 보장한다"고 오해하기 쉽다.

이 글에서는 Redis 트랜잭션의 보장 범위를 DB 트랜잭션과 비교한다.

## 핵심 문장

> Redis 트랜잭션은 여러 명령을 중간 끼어들기 없이 순서대로 실행하는 기능에 가깝고, DB 트랜잭션처럼 실패한 작업을 롤백하는 모델은 아니다.

## 목차

## DB 트랜잭션의 기본 이미지

DB 트랜잭션은 여러 작업을 하나의 작업 단위로 묶는다.

정상 종료되면 `COMMIT`, 문제가 생기면 `ROLLBACK`한다.

```sql
BEGIN;
UPDATE account SET balance = balance - 10000 WHERE id = 1;
UPDATE account SET balance = balance + 10000 WHERE id = 2;
COMMIT;
```

계좌 이체처럼 일부만 성공하면 안 되는 작업에 적합하다.

## ACID를 간단히 정리하기

- Atomicity: 모두 성공하거나 모두 실패해야 한다
- Consistency: 트랜잭션 전후로 데이터 규칙이 깨지지 않아야 한다
- Isolation: 동시에 실행되는 트랜잭션끼리 중간 상태를 함부로 보지 않아야 한다
- Durability: 커밋된 데이터는 장애 이후에도 남아야 한다

이 글에서는 ACID를 깊게 파기보다, Redis와 비교할 기준으로만 사용한다.

## Redis의 `MULTI/EXEC`

Redis에서는 `MULTI` 이후 명령을 큐에 쌓고, `EXEC` 시점에 순서대로 실행한다.

```redis
MULTI
INCR user:1:point
INCR event:1:count
EXEC
```

Redis 트랜잭션의 중요한 특징:

- 트랜잭션 안의 명령은 순서대로 실행된다
- 다른 클라이언트의 명령이 중간에 끼어들지 않는다
- `EXEC` 전에 연결이 끊기면 실행되지 않는다
- `EXEC` 후 일부 명령이 실행 중 에러가 나도 Redis가 자동 롤백하지 않는다

## Redis에는 왜 Rollback이 없을까

Redis 공식 문서에서는 Redis 트랜잭션이 rollback을 지원하지 않는다고 설명한다.

Redis는 단순성과 성능을 중요하게 설계되었기 때문에, RDBMS처럼 undo log를 기반으로 롤백하는 방식과 다르다.

예시:

```redis
MULTI
SET a abc
LPOP a
EXEC
```

`LPOP a`가 타입 오류로 실패하더라도 앞의 `SET a abc`가 자동으로 되돌아가는 모델은 아니다.

## `WATCH`와 낙관적 락

`WATCH`는 특정 키를 감시하다가, `EXEC` 전에 다른 클라이언트가 그 키를 변경하면 트랜잭션을 실패시킨다.

```redis
WATCH stock:1
GET stock:1
MULTI
DECR stock:1
EXEC
```

이 방식은 DB의 비관적 락처럼 먼저 막아두는 방식이 아니라, 충돌이 생기면 나중에 실패시키는 낙관적 락에 가깝다.

## Lua Script와 원자성

Redis에서는 Lua script도 하나의 원자적인 작업처럼 실행할 수 있다.

그래서 "조회 후 조건 검사 후 변경" 같은 작업은 `GET`과 `SET`을 따로 보내기보다 Lua script로 묶는 것이 더 안전한 경우가 있다.

예시 주제:

- 재고가 0보다 클 때만 감소
- 특정 값일 때만 삭제
- 중복 요청 키가 없을 때만 처리

## DB 트랜잭션과 Redis 트랜잭션 비교표

| 기준 | DB 트랜잭션 | Redis 트랜잭션 |
| --- | --- | --- |
| 시작/종료 | `BEGIN`, `COMMIT`, `ROLLBACK` | `MULTI`, `EXEC`, `DISCARD` |
| 핵심 목적 | 정합성 보장 | 명령 묶음의 순차 실행 |
| 롤백 | 지원 | `EXEC` 후 실행 에러 자동 롤백 없음 |
| 격리 | 격리 수준과 Lock/MVCC로 제어 | 실행 중 다른 명령 끼어들기 없음 |
| 내구성 | WAL 등으로 커밋 데이터 보장 | persistence 설정에 의존 |
| 사용 예 | 주문, 결제, 계좌 이체 | 카운터, 캐시 상태 변경, 간단한 조건부 갱신 |

## 2편에서 제외할 내용

- 모든 isolation level 상세 비교
- Redis persistence 옵션 전체 설명
- Redis Cluster에서 multi-key transaction 제약 상세
- 분산 트랜잭션, 2PC

## 3편 계획: Redis Lock과 DB Lock은 언제 다르게 써야 할까

## 글의 목적

동시성 문제를 해결할 때 DB Lock과 Redis Lock을 같은 것으로 생각하면 위험하다.

이 글에서는 DB Lock은 DB 데이터 정합성을 지키기 위한 장치이고, Redis Lock은 여러 애플리케이션 인스턴스 사이에서 특정 작업을 동시에 실행하지 않게 하는 분산락에 가깝다는 점을 정리한다.

## 핵심 문장

> DB Lock은 트랜잭션 안에서 데이터 변경 충돌을 제어하고, Redis Lock은 여러 서버가 같은 작업을 동시에 수행하지 못하게 막는 애플리케이션 레벨의 잠금이다.

## 목차

## Lock이 필요한 상황

동시에 같은 데이터를 수정하면 문제가 생길 수 있다.

예시:

- 같은 상품의 재고를 동시에 차감한다
- 같은 쿠폰을 여러 번 발급한다
- 같은 사용자의 포인트를 동시에 변경한다
- 여러 서버가 같은 배치 작업을 동시에 실행한다

## DB Lock

DB Lock은 DB 트랜잭션과 함께 동작한다.

예를 들어 `SELECT ... FOR UPDATE`를 사용하면 해당 row를 잠그고, 다른 트랜잭션이 같은 row를 수정하지 못하게 기다리게 할 수 있다.

```sql
BEGIN;
SELECT * FROM product WHERE id = 1 FOR UPDATE;
UPDATE product SET stock = stock - 1 WHERE id = 1;
COMMIT;
```

DB Lock의 특징:

- 트랜잭션이 끝날 때까지 유지된다
- 같은 row를 수정하려는 다른 트랜잭션을 대기시킬 수 있다
- 데이터 정합성을 DB 내부에서 보장하는 방향이다
- deadlock이 생길 수 있으므로 접근 순서와 트랜잭션 범위를 조심해야 한다

## Redis Lock

Redis Lock은 보통 `SET key value NX PX timeout` 같은 방식으로 구현한다.

```redis
SET lock:coupon:1 unique-request-id NX PX 3000
```

의미:

- `NX`: 키가 없을 때만 설정한다
- `PX`: 일정 시간이 지나면 자동 만료되게 한다
- `value`: 락을 잡은 주체를 구분하기 위한 고유 값이다

락을 해제할 때는 단순히 `DEL`하면 안 된다.

내가 잡은 락인지 확인한 뒤 삭제해야 한다.

```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

## Redis는 싱글 스레드인데 왜 Lock이 필요한가

Redis가 명령을 하나씩 처리한다는 말은 Redis 내부 명령 실행이 원자적이라는 뜻이다.

하지만 애플리케이션에서 아래처럼 여러 단계로 나누어 처리하면 그 사이에 다른 요청이 끼어들 수 있다.

```text
1. Redis에서 값 조회
2. 애플리케이션에서 조건 판단
3. Redis 또는 DB에 다시 저장
```

이런 경우에는 Redis의 단일 명령 원자성만으로는 전체 비즈니스 흐름의 동시성 문제가 해결되지 않는다.

## DB Lock을 써야 하는 경우

데이터의 최종 원본이 DB이고, 정합성이 가장 중요하다면 DB Lock이나 DB의 조건부 update를 먼저 검토한다.

예시:

```sql
UPDATE product
SET stock = stock - 1
WHERE id = 1 AND stock > 0;
```

영향 받은 row 수가 1이면 성공, 0이면 재고 부족으로 처리할 수 있다.

이런 방식은 별도의 Redis Lock 없이도 DB의 원자적 update로 해결할 수 있다.

## Redis Lock을 검토할 수 있는 경우

Redis Lock은 여러 애플리케이션 인스턴스 사이에서 "같은 작업을 동시에 실행하지 않게" 막고 싶을 때 유용하다.

예시:

- 동일 유저의 중복 요청 방지
- 같은 배치 작업 중복 실행 방지
- 외부 API 호출 중복 방지
- DB에 들어가기 전 작업 단위의 임계 구역 설정

다만 Redis Lock은 TTL, 락 해제 실패, 네트워크 지연, 프로세스 중단 같은 상황을 고려해야 한다.

## Redis Lock 사용 시 주의할 점

- 락에는 반드시 TTL을 둔다
- 락 value는 UUID 같은 고유 값으로 둔다
- 해제할 때는 내가 잡은 락인지 확인한다
- 작업 시간이 TTL보다 길어질 수 있는지 고려한다
- 정말 정합성이 중요한 데이터라면 DB 제약 조건이나 DB 트랜잭션을 함께 사용한다
- 분산락이 실패해도 데이터가 깨지지 않도록 최종 방어선을 DB에 둔다

## DB Lock과 Redis Lock 비교표

| 기준 | DB Lock | Redis Lock |
| --- | --- | --- |
| 위치 | DB 내부 | 애플리케이션/외부 저장소 |
| 목적 | 데이터 변경 충돌 제어 | 여러 서버의 작업 동시 실행 제어 |
| 범위 | row/table/transaction | 특정 key 기반 임계 구역 |
| 해제 | 트랜잭션 종료 시 | 직접 해제 또는 TTL 만료 |
| 강점 | 원본 데이터 정합성 | 분산 환경의 작업 중복 방지 |
| 주의점 | deadlock, 긴 트랜잭션 | TTL, 락 소유자 확인, 네트워크 문제 |

## 면접에서 말할 수 있는 답변

Redis와 DB는 트랜잭션과 Lock의 목적이 다릅니다.

DB 트랜잭션은 여러 SQL 작업을 하나의 단위로 묶고, 실패하면 롤백해서 데이터 정합성을 지킵니다. DB Lock은 트랜잭션 안에서 같은 row를 동시에 수정하지 못하게 제어하는 데 사용됩니다.

Redis도 `MULTI/EXEC` 트랜잭션을 제공하지만, RDBMS처럼 실행 중 오류가 난 작업을 자동 롤백하는 방식은 아닙니다. Redis는 개별 명령의 원자성과 빠른 실행에 강하고, `WATCH`나 Lua script를 통해 조건부 원자 연산을 만들 수 있습니다.

Redis Lock은 DB Lock과 다르게 여러 서버가 같은 작업을 동시에 수행하지 못하게 막는 분산락에 가깝습니다. 따라서 원본 데이터 정합성이 중요한 작업은 DB 트랜잭션과 제약 조건을 최종 방어선으로 두고, Redis Lock은 중복 실행을 줄이는 보조 수단으로 보는 것이 좋습니다.

## 글에서 꼭 잡아야 할 오해

## 오해 1: Redis는 싱글 스레드니까 동시성 문제가 없다

Redis 명령 하나는 원자적으로 실행되지만, 애플리케이션의 비즈니스 로직 전체가 자동으로 원자적이 되는 것은 아니다.

## 오해 2: Redis 트랜잭션은 DB 트랜잭션과 같다

Redis 트랜잭션은 중간 끼어들기 없이 명령을 순서대로 실행하는 기능에 가깝다. RDBMS처럼 자동 rollback을 기대하면 안 된다.

## 오해 3: Redis Lock을 쓰면 DB 정합성 문제는 해결된다

Redis Lock이 실패하거나 만료되거나 잘못 해제될 수 있다. 최종 데이터 정합성은 DB 제약 조건, 트랜잭션, 조건부 update로 방어해야 한다.

## 오해 4: 분산락은 항상 필요하다

단순 재고 차감처럼 DB의 조건부 update 하나로 해결할 수 있는 문제라면 Redis Lock보다 DB 원자 연산이 더 단순하고 안전할 수 있다.

## 작성 순서

먼저 1편에서 Redis와 DB의 목적 차이를 잡는다.

그 다음 2편에서 Redis 트랜잭션과 DB 트랜잭션의 차이를 비교한다.

마지막 3편에서 Redis Lock과 DB Lock을 비교하고, 실제 프로젝트에서 어떤 기준으로 선택하면 좋을지 정리한다.

## 최종 글의 분위기

면접 대비와 실무 입문 사이의 글로 작성한다.

Redis를 과하게 무서워하거나, 반대로 DB처럼 만능 저장소로 생각하지 않도록 균형 있게 설명한다.

독자가 글을 다 읽고 나면 다음 질문에 답할 수 있어야 한다.

- Redis와 DB는 각각 어떤 상황에 강한가?
- Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가?
- Redis의 원자성과 ACID의 Atomicity는 어떻게 구분해야 하는가?
- Redis는 rollback을 지원하는가?
- `WATCH`는 어떤 의미에서 낙관적 락인가?
- Redis Lock을 구현할 때 왜 TTL과 고유 value가 필요한가?
- DB Lock과 Redis Lock은 각각 언제 사용하는가?

## 추가로 공부하면 좋은 키워드

- Redis `MULTI`, `EXEC`, `DISCARD`, `WATCH`
- Redis Lua script
- Redis `SET NX PX`
- DB `SELECT FOR UPDATE`
- 낙관적 락과 비관적 락
- 조건부 update
- deadlock
- idempotency key
- fencing token
