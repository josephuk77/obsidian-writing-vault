---
title: "[Database] Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가"
created: "2026-05-14"
updated: "2026-05-14"
type: blog
status: published
tags:
  - database
  - redis
  - transaction
  - acid
source_notes:
  - "Redis Docs - Transactions: https://redis.io/docs/latest/develop/using-commands/transactions/"
  - "PostgreSQL Docs - Transactions: https://www.postgresql.org/docs/current/tutorial-transactions.html"
publish_url:
---

# [Database] Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가

DB 트랜잭션을 공부한 뒤 Redis를 보면 헷갈리는 부분이 있다.

Redis에도 트랜잭션이라는 말이 나오기 때문이다.

Redis 공식 문서에서도 `MULTI`, `EXEC`, `DISCARD`, `WATCH`를 중심으로 Redis Transactions를 설명한다.

그러면 이런 질문이 생긴다.

```text
Redis 트랜잭션도 DB 트랜잭션처럼 ACID를 보장하는 걸까?
```

결론부터 말하면 둘은 비슷해 보이지만 목적과 보장 범위가 다르다.

Redis 트랜잭션은 여러 명령을 중간 끼어들기 없이 순서대로 실행하는 기능에 가깝다.

반면 DB 트랜잭션은 여러 SQL 작업을 하나의 논리적 작업 단위로 묶고, 실패 시 롤백하며, 데이터 정합성을 지키는 데 초점이 있다.

## 시리즈 글

- 이전 글: [[2026-05-14_[Database] Redis vs DB, 저장소의 목적부터 다르다]]
- 현재 글: [[2026-05-14_[Database] Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가]]
- 다음 글: [[2026-05-14_[Database] Redis Lock과 DB Lock은 언제 다르게 써야 할까]]

## DB 트랜잭션의 기본 이미지

먼저 DB 트랜잭션을 생각해보자.

가장 많이 드는 예시는 계좌 이체다.

A 계좌에서 10,000원을 빼고, B 계좌에 10,000원을 더한다고 해보자.

```sql
BEGIN;

UPDATE account
SET balance = balance - 10000
WHERE id = 1;

UPDATE account
SET balance = balance + 10000
WHERE id = 2;

COMMIT;
```

이 작업은 둘 다 성공해야 한다.

A 계좌에서 돈은 빠졌는데 B 계좌에 돈이 들어가지 않으면 안 된다.

그래서 중간에 문제가 생기면 `ROLLBACK`한다.

```sql
ROLLBACK;
```

DB 트랜잭션의 핵심은 여러 작업을 하나의 작업처럼 다루는 것이다.

정상적으로 끝나면 모두 반영하고, 실패하면 아무것도 반영되지 않은 것처럼 되돌린다.

## ACID를 간단히 정리하면

DB 트랜잭션을 설명할 때 ACID라는 말을 많이 사용한다.

처음 보면 어렵지만, 입문 단계에서는 아래 정도로 이해하면 된다.

| 속성 | 의미 |
| --- | --- |
| Atomicity | 모두 성공하거나 모두 실패해야 한다 |
| Consistency | 트랜잭션 전후로 데이터 규칙이 깨지지 않아야 한다 |
| Isolation | 동시에 실행되는 트랜잭션끼리 중간 상태를 함부로 보지 않아야 한다 |
| Durability | 커밋된 데이터는 장애 이후에도 남아야 한다 |

예를 들어 계좌 이체에서 Atomicity는 "출금과 입금이 같이 성공하거나 같이 실패해야 한다"는 의미다.

Isolation은 다른 트랜잭션이 이체 중간 상태를 어설프게 보면 안 된다는 의미다.

Durability는 이체가 성공했다고 응답한 뒤에는 장애가 나도 결과가 남아야 한다는 의미다.

DB는 이런 보장을 위해 트랜잭션 로그, Lock, MVCC, 격리 수준 같은 장치를 사용한다.

## Redis의 `MULTI/EXEC`

Redis에서도 여러 명령을 하나의 트랜잭션으로 묶을 수 있다.

기본 흐름은 `MULTI`로 시작하고, 명령을 큐에 쌓은 뒤, `EXEC`로 실행한다.

```redis
MULTI
INCR user:1:point
INCR event:1:count
EXEC
```

`MULTI` 이후 입력한 명령은 바로 실행되지 않고 큐에 쌓인다.

그리고 `EXEC`가 호출되면 큐에 쌓인 명령들이 순서대로 실행된다.

Redis 트랜잭션이 보장하는 중요한 특징은 이것이다.

- 트랜잭션 안의 명령은 순서대로 실행된다
- 실행 중간에 다른 클라이언트의 명령이 끼어들지 않는다
- `EXEC` 전에 연결이 끊기면 큐에 쌓인 명령은 실행되지 않는다
- `DISCARD`를 호출하면 큐에 쌓인 명령을 버릴 수 있다

이 정도만 보면 DB 트랜잭션과 비슷해 보인다.

하지만 중요한 차이가 있다.

## Redis 트랜잭션은 자동 롤백하지 않는다

DB 트랜잭션을 먼저 공부한 사람은 트랜잭션 안에서 에러가 나면 전체가 롤백될 것이라고 기대할 수 있다.

하지만 Redis 트랜잭션은 그런 방식이 아니다.

Redis 공식 문서에서는 Redis가 트랜잭션 rollback을 지원하지 않는다고 설명한다.

예를 들어 아래 상황을 보자.

```redis
MULTI
SET a abc
LPOP a
EXEC
```

`SET a abc`는 문자열 값을 저장한다.

그런데 `LPOP a`는 list에서 값을 꺼내는 명령이다.

문자열 key에 list 명령을 실행하면 타입 오류가 발생한다.

중요한 점은 `LPOP a`가 실패한다고 해서 앞의 `SET a abc`가 자동으로 되돌아가는 것은 아니라는 점이다.

Redis는 `EXEC` 이후 실행 중 발생한 에러를 RDBMS처럼 전체 롤백으로 처리하지 않는다.

이 차이를 꼭 기억해야 한다.

> Redis 트랜잭션은 명령 묶음의 순차 실행을 보장하지만, DB 트랜잭션처럼 실행 결과를 자동 롤백하는 모델은 아니다.

## 그러면 Redis 트랜잭션의 Atomicity는 무엇일까

여기서 "Redis도 atomic하다고 하지 않나?"라는 의문이 생긴다.

Redis에서 말하는 원자성은 주로 이런 의미에 가깝다.

```text
하나의 명령 또는 EXEC로 실행되는 명령 묶음이 중간에 다른 명령과 섞이지 않는다.
```

즉, Redis는 싱글 스레드 이벤트 루프 기반으로 명령을 순서대로 처리한다.

그래서 `INCR count` 같은 단일 명령은 원자적이다.

```redis
INCR view:post:1
```

동시에 여러 요청이 들어와도 `INCR` 하나가 중간에 쪼개져 실행되지는 않는다.

하지만 이 원자성이 DB 트랜잭션의 "모두 성공하거나 모두 실패한다"는 Atomicity와 완전히 같은 의미로 동작한다고 보면 안 된다.

Redis의 `MULTI/EXEC`는 실행 중간에 다른 명령이 끼어들지 않도록 해주지만, 실행된 명령을 자동으로 되돌리는 rollback 기능은 제공하지 않는다.

## `WATCH`와 낙관적 락

Redis 트랜잭션에서 자주 같이 나오는 명령이 `WATCH`다.

`WATCH`는 특정 key를 감시하다가, `EXEC` 전에 그 key가 다른 클라이언트에 의해 변경되면 트랜잭션을 실패시킨다.

예를 들어 재고를 감소시키는 상황을 단순화해보자.

```redis
WATCH stock:1
GET stock:1
MULTI
DECR stock:1
EXEC
```

흐름은 대략 이렇다.

```text
1. stock:1 key를 감시한다
2. 현재 재고를 읽는다
3. 재고가 충분하면 감소 명령을 큐에 넣는다
4. EXEC를 호출한다
5. 그 사이 stock:1이 바뀌었다면 EXEC가 실패한다
```

이 방식은 DB의 비관적 락처럼 먼저 막아두는 방식이 아니다.

누군가 변경했는지 나중에 확인하고, 충돌이 있으면 실패시키는 방식이다.

그래서 `WATCH`는 낙관적 락과 비슷하게 이해할 수 있다.

충돌이 발생하면 애플리케이션에서 다시 시도하거나 실패 응답을 내려야 한다.

## Lua Script와 원자성

Redis에서 여러 단계를 하나의 원자적 작업으로 처리하고 싶을 때 Lua script를 사용할 수 있다.

예를 들어 "재고가 0보다 클 때만 감소"를 생각해보자.

애플리케이션에서 아래처럼 처리하면 문제가 생길 수 있다.

```text
1. GET stock:1
2. 애플리케이션에서 stock > 0 확인
3. DECR stock:1
```

이 과정은 여러 명령으로 나뉘어 있다.

그 사이에 다른 요청이 끼어들 수 있다.

Lua script로 묶으면 Redis 내부에서 하나의 스크립트가 실행되는 동안 다른 명령이 끼어들지 않는다.

```lua
local stock = tonumber(redis.call("GET", KEYS[1]))

if stock == nil or stock <= 0 then
    return 0
end

redis.call("DECR", KEYS[1])
return 1
```

이 스크립트는 재고를 읽고, 조건을 확인하고, 감소시키는 작업을 Redis 안에서 한 번에 처리한다.

Redis에서는 이런 방식이 `WATCH`보다 단순하고 빠른 경우도 있다.

다만 Lua script도 DB 트랜잭션의 대체재는 아니다.

Redis 안의 key에 대한 원자적 처리를 도와주는 도구로 이해하는 것이 좋다.

## DB 트랜잭션과 Redis 트랜잭션 비교

둘의 차이를 표로 정리하면 이렇다.

| 기준 | DB 트랜잭션 | Redis 트랜잭션 |
| --- | --- | --- |
| 시작/종료 | `BEGIN`, `COMMIT`, `ROLLBACK` | `MULTI`, `EXEC`, `DISCARD` |
| 핵심 목적 | 데이터 정합성 보장 | 명령 묶음의 순차 실행 |
| 롤백 | 지원 | `EXEC` 후 실행 에러 자동 롤백 없음 |
| 격리 | 격리 수준, Lock, MVCC로 제어 | 실행 중 다른 명령 끼어들기 없음 |
| 내구성 | WAL 등으로 커밋 데이터 보장 | persistence 설정에 의존 |
| 충돌 제어 | Lock, isolation level, optimistic lock 등 | `WATCH`, Lua script 등 |
| 사용 예 | 주문, 결제, 계좌 이체 | 카운터, 캐시 상태 변경, 조건부 key 변경 |

이 표에서 가장 중요한 차이는 rollback이다.

DB 트랜잭션은 실패 시 되돌리는 것을 핵심 기능으로 본다.

Redis 트랜잭션은 실행할 명령들을 순서대로 묶어서 처리하는 것에 가깝다.

## 실제로 어떻게 판단하면 좋을까

데이터가 틀리면 안 되는 핵심 작업이라면 DB 트랜잭션을 먼저 생각하는 것이 좋다.

예를 들어 이런 작업이다.

- 주문 생성
- 결제 승인 기록 저장
- 재고 차감
- 포인트 사용
- 계좌 이체

이런 작업은 중간에 일부만 성공하면 안 된다.

따라서 DB 트랜잭션과 제약 조건을 중심으로 설계하는 것이 안전하다.

반면 Redis 트랜잭션이나 Lua script는 이런 상황에 잘 맞는다.

- 조회수 증가
- 이벤트 참여 횟수 증가
- 캐시 상태 변경
- 중복 요청 방지 key 설정
- Redis 안의 여러 key를 함께 변경

핵심은 Redis가 나쁘다는 것이 아니다.

Redis가 제공하는 트랜잭션의 의미를 DB 트랜잭션과 구분해서 써야 한다는 것이다.

## 내가 헷갈렸던 부분

처음에는 "Redis도 트랜잭션이 있다"는 문장을 보고 DB 트랜잭션과 비슷하다고 생각했다.

그래서 `MULTI/EXEC`를 쓰면 중간에 실패했을 때 전체가 rollback될 것이라고 막연히 예상했다.

하지만 Redis의 트랜잭션은 그런 모델이 아니었다.

Redis는 명령을 빠르고 단순하게 처리하는 데 초점이 있고, `MULTI/EXEC`는 여러 명령을 중간 끼어들기 없이 순서대로 실행하는 기능에 가깝다.

반면 DB 트랜잭션은 데이터 정합성을 위해 실패 시 되돌리는 것까지 중요한 기능으로 제공한다.

이 차이를 이해하면 Redis를 어디까지 믿고 써야 하는지 판단하기 쉬워진다.

## 정리

Redis와 DB는 둘 다 트랜잭션이라는 단어를 사용하지만 의미가 다르다.

DB 트랜잭션은 여러 SQL 작업을 하나의 논리적 작업 단위로 묶고, 실패하면 롤백해서 데이터 정합성을 지킨다.

Redis 트랜잭션은 `MULTI/EXEC`를 통해 여러 명령을 큐에 쌓고 순서대로 실행한다. 실행 중간에 다른 클라이언트 명령이 끼어들지 않는다는 점이 중요하다.

하지만 Redis는 RDBMS처럼 `EXEC` 이후 실행 중 발생한 에러를 자동 rollback하지 않는다.

그래서 Redis 트랜잭션을 DB 트랜잭션과 같은 것으로 생각하면 안 된다.

한 문장으로 정리하면 이렇다.

> DB 트랜잭션은 데이터 정합성을 지키기 위한 작업 단위이고, Redis 트랜잭션은 명령 묶음을 순서대로 실행하기 위한 기능이다.

다음 글에서는 Redis Lock과 DB Lock이 어떻게 다른지 정리해보겠다.

## 참고 자료

- Redis Docs - Transactions: https://redis.io/docs/latest/develop/using-commands/transactions/
- PostgreSQL Docs - Transactions: https://www.postgresql.org/docs/current/tutorial-transactions.html
