---
title: "[Database] Redis Lock과 DB Lock은 언제 다르게 써야 할까"
created: "2026-05-14"
updated: "2026-05-14"
type: blog
status: published
tags:
  - database
  - redis
  - lock
  - concurrency
source_notes:
  - "Redis Docs - Distributed Locks: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/"
  - "PostgreSQL Docs - Explicit Locking: https://www.postgresql.org/docs/current/explicit-locking.html"
publish_url:
---

# [Database] Redis Lock과 DB Lock은 언제 다르게 써야 할까

동시성 문제를 공부하다 보면 Lock이라는 단어를 자주 만난다.

DB에도 Lock이 있고, Redis로도 Lock을 구현할 수 있다.

그래서 처음에는 둘을 비슷한 기능으로 생각하기 쉽다.

하지만 DB Lock과 Redis Lock은 목적과 위치가 다르다.

DB Lock은 DB 안에서 데이터 변경 충돌을 제어하기 위한 장치다.

Redis Lock은 여러 애플리케이션 인스턴스가 같은 작업을 동시에 수행하지 못하게 막기 위한 애플리케이션 레벨의 잠금에 가깝다.

이번 글에서는 DB Lock과 Redis Lock이 어떻게 다르고, 어떤 기준으로 선택하면 좋을지 정리해보려고 한다.

## 시리즈 글

- 첫 글: [[2026-05-14_[Database] Redis vs DB, 저장소의 목적부터 다르다]]
- 이전 글: [[2026-05-14_[Database] Redis 트랜잭션은 DB 트랜잭션과 무엇이 다른가]]
- 현재 글: [[2026-05-14_[Database] Redis Lock과 DB Lock은 언제 다르게 써야 할까]]

## Lock이 필요한 상황

Lock은 동시에 실행되면 안 되는 작업이 있을 때 필요하다.

예를 들어 이런 상황을 생각해볼 수 있다.

- 같은 상품의 재고를 동시에 차감한다
- 같은 쿠폰을 여러 번 발급한다
- 같은 사용자의 포인트를 동시에 변경한다
- 여러 서버가 같은 배치 작업을 동시에 실행한다
- 같은 주문에 대해 결제 승인 요청이 중복으로 들어온다

이런 상황에서는 요청이 동시에 들어왔을 때 데이터가 꼬일 수 있다.

예를 들어 재고가 1개 남은 상품에 대해 두 명이 거의 동시에 주문한다고 해보자.

둘 다 재고를 1로 읽고 주문에 성공하면 실제 재고보다 더 많이 팔리는 문제가 생길 수 있다.

이런 문제를 막기 위해 Lock이나 원자적 update 같은 동시성 제어가 필요하다.

## DB Lock

DB Lock은 DB 트랜잭션과 함께 동작한다.

예를 들어 PostgreSQL이나 MySQL에서는 `SELECT ... FOR UPDATE` 같은 방식으로 row를 잠글 수 있다.

```sql
BEGIN;

SELECT *
FROM product
WHERE id = 1
FOR UPDATE;

UPDATE product
SET stock = stock - 1
WHERE id = 1;

COMMIT;
```

이 흐름에서는 `product id = 1`인 row를 잠근다.

다른 트랜잭션이 같은 row를 수정하려고 하면 현재 트랜잭션이 끝날 때까지 기다려야 한다.

DB Lock의 특징은 다음과 같다.

- 트랜잭션 안에서 동작한다
- 보통 트랜잭션이 끝날 때 해제된다
- 같은 row를 수정하려는 다른 트랜잭션을 기다리게 할 수 있다
- 원본 데이터의 정합성을 DB 내부에서 지키는 방향이다
- 잘못 사용하면 deadlock이나 긴 대기 시간이 생길 수 있다

즉, DB Lock은 데이터 자체를 보호하는 데 초점이 있다.

## DB Lock 없이 조건부 update로 해결할 수도 있다

재고 차감 같은 문제는 반드시 `SELECT FOR UPDATE`를 써야만 해결되는 것은 아니다.

상황에 따라 조건부 update 하나로 해결할 수 있다.

```sql
UPDATE product
SET stock = stock - 1
WHERE id = 1
  AND stock > 0;
```

이 SQL은 재고가 0보다 클 때만 감소한다.

그리고 애플리케이션에서는 영향을 받은 row 수를 확인한다.

```text
affected row = 1 -> 재고 차감 성공
affected row = 0 -> 재고 부족
```

이 방식은 DB의 update 자체가 원자적으로 실행된다는 점을 활용한다.

단순한 재고 차감이라면 별도의 Redis Lock을 도입하지 않고도 이 방식이 더 단순할 수 있다.

그래서 동시성 문제가 생겼다고 바로 분산락부터 생각하기보다, DB의 제약 조건이나 조건부 update로 해결할 수 있는지 먼저 보는 것이 좋다.

## Redis Lock

Redis Lock은 Redis에 특정 key를 만들어서 잠금 상태를 표현하는 방식이다.

보통 이런 명령을 사용한다.

```redis
SET lock:coupon:1 unique-request-id NX PX 3000
```

각 옵션의 의미는 이렇다.

- `NX`: key가 없을 때만 설정한다
- `PX 3000`: 3000ms 뒤에 자동 만료되게 한다
- `unique-request-id`: 락을 잡은 주체를 구분하기 위한 고유 값이다

이 명령이 성공하면 락을 얻은 것이다.

이미 같은 key가 있으면 다른 요청이 락을 잡고 있다는 뜻이므로 실패한다.

Redis Lock은 여러 애플리케이션 서버가 같은 Redis를 바라볼 때 유용하다.

예를 들어 서버가 3대 있다고 해보자.

```text
App Server A
App Server B
App Server C
        |
      Redis
```

세 서버가 동시에 같은 쿠폰 발급 작업을 하려고 할 때, Redis에 같은 lock key를 만들게 하면 한 서버만 성공하도록 만들 수 있다.

이런 의미에서 Redis Lock은 분산 환경에서 작업의 중복 실행을 막는 데 자주 사용된다.

## Redis Lock을 해제할 때 조심할 점

Redis Lock을 잡을 때 TTL을 두는 이유는 락을 잡은 서버가 죽을 수 있기 때문이다.

만약 TTL이 없다면 서버가 락을 잡고 죽었을 때 그 락은 영원히 남을 수 있다.

그러면 다른 요청은 계속 락을 얻지 못한다.

하지만 TTL이 있다고 해서 모든 문제가 끝나는 것은 아니다.

예를 들어 A 서버가 락을 잡고 작업을 시작했다고 해보자.

```text
A 서버가 lock:coupon:1 획득
TTL은 3초
작업이 예상보다 오래 걸려 5초 소요
3초 뒤 락 만료
B 서버가 같은 락 획득
A 서버가 작업 종료 후 DEL lock:coupon:1 실행
```

이때 A 서버가 단순히 `DEL lock:coupon:1`을 실행하면 B 서버가 새로 잡은 락을 지워버릴 수 있다.

그래서 락을 해제할 때는 "내가 잡은 락이 맞는지" 확인해야 한다.

Redis 공식 문서에서는 고유 값을 저장하고, 해제할 때 그 값이 일치하는 경우에만 삭제하는 방식을 설명한다.

예전 Redis 버전에서는 보통 Lua script로 처리했다.

```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

핵심은 단순히 `DEL`하지 않는 것이다.

> Redis Lock은 반드시 TTL을 두고, 해제할 때는 내가 잡은 락인지 확인해야 한다.

## Redis는 싱글 스레드인데 왜 Lock이 필요할까

Redis를 공부하면 "Redis는 싱글 스레드라서 명령이 원자적으로 처리된다"는 말을 보게 된다.

그러면 이런 생각이 들 수 있다.

```text
Redis 명령이 하나씩 처리된다면 Lock이 필요 없는 것 아닌가?
```

Redis 명령 하나만 보면 맞는 말이다.

예를 들어 `INCR count`는 원자적으로 실행된다.

```redis
INCR count
```

여러 요청이 동시에 와도 `INCR` 명령 하나가 중간에 쪼개져 실행되지는 않는다.

하지만 애플리케이션의 비즈니스 로직은 보통 Redis 명령 하나로 끝나지 않는다.

예를 들어 아래 흐름을 보자.

```text
1. Redis에서 값 조회
2. 애플리케이션에서 조건 판단
3. DB에 저장
4. Redis 값을 변경
```

이 전체 흐름은 Redis 명령 하나가 아니다.

Redis 내부에서는 명령 하나하나가 원자적이어도, 애플리케이션에서 여러 단계로 나누어 처리하는 동안 다른 요청이 끼어들 수 있다.

그래서 Redis의 단일 명령 원자성과 애플리케이션 전체 흐름의 원자성은 구분해야 한다.

## DB Lock을 써야 하는 경우

데이터의 최종 원본이 DB이고, 정합성이 가장 중요하다면 DB Lock이나 DB 조건부 update를 먼저 검토하는 것이 좋다.

예를 들어 이런 작업이다.

- 상품 재고 차감
- 포인트 사용
- 계좌 잔액 변경
- 주문 상태 변경
- 결제 승인 기록 저장

이런 데이터는 틀리면 비즈니스적으로 큰 문제가 생긴다.

Redis Lock을 사용하더라도 최종 방어선은 DB에 있어야 한다.

예를 들어 재고가 음수가 되면 안 된다면 DB 조건에서도 막는 것이 좋다.

```sql
UPDATE product
SET stock = stock - 1
WHERE id = 1
  AND stock > 0;
```

또는 DB 제약 조건을 둘 수도 있다.

```sql
ALTER TABLE product
ADD CONSTRAINT stock_non_negative CHECK (stock >= 0);
```

이렇게 하면 애플리케이션 레벨에서 실수하더라도 DB가 마지막으로 잘못된 데이터를 막아줄 수 있다.

## Redis Lock을 검토할 수 있는 경우

Redis Lock은 여러 서버가 같은 작업을 동시에 하지 못하게 막고 싶을 때 유용하다.

예를 들면 이런 상황이다.

- 동일 사용자의 중복 요청 방지
- 같은 배치 작업의 중복 실행 방지
- 외부 API 호출 중복 방지
- 쿠폰 발급 로직의 진입 제한
- 일정 시간 동안 하나의 작업만 실행되도록 제한

예를 들어 외부 결제 API를 호출하는 작업을 생각해보자.

사용자가 버튼을 여러 번 누르거나, 네트워크 재시도로 같은 요청이 여러 번 들어올 수 있다.

이때 Redis Lock이나 idempotency key를 사용하면 같은 요청이 중복으로 처리되는 것을 줄일 수 있다.

```redis
SET lock:payment:order:1001 request-uuid NX PX 5000
```

다만 Redis Lock을 잡았다고 해서 DB 정합성까지 자동으로 보장되는 것은 아니다.

락이 만료될 수도 있고, 네트워크 지연이 생길 수도 있고, 작업 시간이 TTL보다 길어질 수도 있다.

그래서 중요한 데이터는 DB 트랜잭션과 제약 조건을 함께 사용해야 한다.

## DB Lock과 Redis Lock 비교

| 기준 | DB Lock | Redis Lock |
| --- | --- | --- |
| 위치 | DB 내부 | Redis를 이용한 애플리케이션 레벨 |
| 목적 | 데이터 변경 충돌 제어 | 여러 서버의 작업 중복 실행 제어 |
| 범위 | row, table, transaction | 특정 key 기반 임계 구역 |
| 해제 | 보통 트랜잭션 종료 시 | 직접 해제 또는 TTL 만료 |
| 강점 | 원본 데이터 정합성 보호 | 분산 환경에서 작업 진입 제어 |
| 주의점 | deadlock, 긴 트랜잭션 | TTL, 락 소유자 확인, 네트워크 문제 |

이 둘은 경쟁 관계라기보다 해결하는 문제가 조금 다르다.

DB Lock은 "이 DB row를 동시에 바꾸면 안 된다"에 가깝다.

Redis Lock은 "이 작업을 여러 서버가 동시에 실행하면 안 된다"에 가깝다.

## 면접에서 말할 수 있는 답변

DB Lock은 DB 트랜잭션 안에서 데이터 변경 충돌을 제어하기 위한 기능입니다.

예를 들어 `SELECT FOR UPDATE`를 사용하면 특정 row를 잠그고, 다른 트랜잭션이 같은 row를 수정하지 못하게 기다리게 할 수 있습니다.

Redis Lock은 Redis의 `SET key value NX PX` 같은 명령을 이용해 여러 애플리케이션 인스턴스 사이에서 같은 작업이 동시에 실행되지 않도록 막는 방식입니다.

다만 Redis Lock은 TTL, 락 소유자 확인, 네트워크 지연, 작업 시간 초과 같은 문제를 고려해야 합니다.

그래서 원본 데이터 정합성이 중요한 작업은 DB 트랜잭션과 제약 조건을 최종 방어선으로 두고, Redis Lock은 중복 실행을 줄이는 보조 수단으로 보는 것이 좋습니다.

## 내가 헷갈렸던 부분

처음에는 동시성 문제가 생기면 Redis Lock을 쓰면 해결된다고 생각했다.

하지만 공부해보니 모든 동시성 문제에 분산락이 필요한 것은 아니었다.

단순 재고 차감처럼 DB의 조건부 update 하나로 해결할 수 있는 문제도 있다.

그리고 Redis Lock은 애플리케이션 레벨의 잠금이기 때문에, 락이 실패하거나 만료되는 상황까지 고려해야 한다.

그래서 중요한 기준은 이것이다.

```text
원본 데이터의 정합성을 지키는 문제인가?
여러 서버의 작업 중복 실행을 막는 문제인가?
```

첫 번째라면 DB 트랜잭션, DB Lock, 조건부 update, 제약 조건을 먼저 본다.

두 번째라면 Redis Lock을 검토할 수 있다.

## 정리

DB Lock과 Redis Lock은 둘 다 동시성 문제를 다루지만 같은 기능은 아니다.

DB Lock은 DB 트랜잭션 안에서 row나 table의 변경 충돌을 제어한다. 원본 데이터의 정합성을 지키는 데 강하다.

Redis Lock은 Redis key를 이용해 여러 애플리케이션 인스턴스가 같은 작업을 동시에 실행하지 못하게 막는다. 분산 환경에서 작업의 중복 실행을 줄이는 데 유용하다.

Redis Lock을 사용할 때는 반드시 TTL을 두고, 고유 value를 저장하고, 해제 시 내가 잡은 락인지 확인해야 한다.

그리고 가장 중요한 것은 최종 데이터 정합성을 Redis Lock 하나에만 맡기지 않는 것이다.

주문, 결제, 재고, 포인트처럼 중요한 데이터라면 DB 트랜잭션과 제약 조건을 마지막 방어선으로 두는 것이 좋다.

한 문장으로 정리하면 이렇다.

> DB Lock은 데이터를 보호하고, Redis Lock은 작업의 중복 실행을 막는다.

## 참고 자료

- Redis Docs - Distributed Locks: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/
- PostgreSQL Docs - Explicit Locking: https://www.postgresql.org/docs/current/explicit-locking.html
