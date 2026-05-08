---
title: "[Spring] @Transactional은 왜 Service에 붙일까"
created: "2026-05-08"
type: blog
status: published
tags:
  - spring
  - transaction
  - jpa
  - mybatis
publish_url:
---

# [Spring] @Transactional은 왜 Service에 붙일까

스프링을 공부하다 보면 `@Transactional`을 자주 보게 된다.

처음에는 단순히 DB 작업을 할 때 붙이는 어노테이션처럼 보이지만, 실제로는 데이터 정합성을 지키기 위한 중요한 기능이다.

이번 글에서는 취준생 입장에서 Spring Transaction을 공부할 때 꼭 알아야 할 내용만 정리해보려고 한다.

너무 깊은 내부 구현보다는 다음 질문에 답할 수 있는 것을 목표로 한다.

- 트랜잭션은 왜 필요한가
- `@Transactional`은 어디에 붙이는가
- 언제 롤백되는가
- JPA와 MyBatis에서는 어떤 차이가 있는가

## 트랜잭션이 필요한 이유

트랜잭션은 여러 DB 작업을 하나의 작업처럼 묶기 위해 사용한다.

예를 들어 주문 기능을 생각해보자.

주문을 생성할 때는 보통 하나의 SQL만 실행되지 않는다.

- 주문 저장
- 재고 감소
- 결제 내역 저장

이 작업들이 따로따로 성공하거나 실패하면 문제가 생길 수 있다.

예를 들어 주문 저장은 성공했는데 재고 감소 중 예외가 발생했다고 해보자. 그러면 사용자는 주문한 상태인데 실제 재고는 줄어들지 않은 이상한 데이터가 생길 수 있다.

이런 상황을 막기 위해 트랜잭션을 사용한다.

트랜잭션으로 묶으면 모든 작업이 성공했을 때만 커밋하고, 중간에 실패하면 앞에서 실행된 작업도 함께 롤백한다.

즉, 핵심은 이 문장이다.

> 트랜잭션은 여러 DB 작업을 하나의 작업 단위로 묶어서 데이터 정합성을 지키는 기능이다.

## Spring에서는 어떻게 사용하는가

Spring에서는 보통 `@Transactional`을 사용한다.

```java
@Transactional
public void createOrder(OrderRequest request) {
    orderRepository.save(order);
    stockRepository.decrease(productId, quantity);
    paymentRepository.save(payment);
}
```

이 메서드가 정상적으로 끝나면 트랜잭션은 커밋된다.

반대로 중간에 예외가 발생하면 트랜잭션은 롤백된다.

```java
@Transactional
public void createOrder(OrderRequest request) {
    orderRepository.save(order);
    stockRepository.decrease(productId, quantity);

    throw new RuntimeException("결제 실패");
}
```

위 코드에서는 주문 저장과 재고 감소가 이미 실행되었더라도, `RuntimeException`이 발생했기 때문에 전체 작업이 롤백된다.

## 어디에 붙이는가

`@Transactional`은 보통 Service 계층에 붙인다.

그 이유는 트랜잭션이 개별 SQL 하나가 아니라 하나의 비즈니스 작업 단위에 걸려야 하기 때문이다.

Repository나 Mapper는 DB에 접근하는 역할을 한다.

반면 Service는 하나의 기능 흐름을 담당한다.

예를 들어 주문 생성이라는 기능은 주문 저장, 재고 감소, 결제 내역 저장을 포함할 수 있다. 이 전체 흐름이 하나의 트랜잭션으로 묶여야 하므로 Service 계층에 `@Transactional`을 붙이는 것이 자연스럽다.

```java
@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final StockRepository stockRepository;

    @Transactional
    public void createOrder(OrderRequest request) {
        orderRepository.save(request.toOrder());
        stockRepository.decrease(request.productId(), request.quantity());
    }
}
```

정리하면 이렇게 말할 수 있다.

> 트랜잭션은 개별 DB 접근 코드가 아니라 하나의 비즈니스 작업 단위에 거는 것이 좋다.

## 언제 롤백되는가

Spring Transaction에서 취준생이 먼저 알아야 할 롤백 규칙은 간단하다.

기본적으로 `RuntimeException`이 발생하면 롤백된다.

```java
@Transactional
public void createOrder() {
    throw new RuntimeException("주문 실패");
}
```

이 경우 트랜잭션은 롤백된다.

하지만 checked exception은 기본적으로 롤백 대상이 아니다.

```java
@Transactional
public void createOrder() throws Exception {
    throw new Exception("주문 실패");
}
```

이런 checked exception까지 롤백하고 싶다면 `rollbackFor`를 사용할 수 있다.

```java
@Transactional(rollbackFor = Exception.class)
public void createOrder() throws Exception {
    throw new Exception("주문 실패");
}
```

처음 공부할 때는 모든 예외 규칙을 외우려고 하기보다, 기본 롤백 대상이 `RuntimeException`이라는 점을 먼저 기억하는 것이 좋다.

## 자주 하는 실수

트랜잭션을 사용할 때 자주 하는 실수는 예외를 잡고 다시 던지지 않는 것이다.

```java
@Transactional
public void createOrder() {
    try {
        payment();
    } catch (RuntimeException e) {
        System.out.println("결제 실패");
    }
}
```

이 코드는 `payment()`에서 예외가 발생해도 catch 블록에서 예외를 처리하고 끝난다.

Spring 입장에서는 메서드가 정상 종료된 것으로 볼 수 있다. 그러면 롤백이 아니라 커밋될 수 있다.

롤백이 필요하다면 예외를 다시 던지거나, 상황에 맞게 트랜잭션 상태를 롤백으로 표시해야 한다.

취준생 입장에서는 우선 이렇게 이해하면 된다.

> 롤백이 필요하다면 예외를 조용히 삼키면 안 된다.

## 내부 메서드 호출도 조심해야 한다

`@Transactional`은 Spring AOP 기반으로 동작한다.

쉽게 말하면 Spring이 만든 프록시 객체를 통해 메서드가 호출될 때 트랜잭션이 적용된다.

그래서 같은 클래스 안에서 자기 자신의 메서드를 직접 호출하면 트랜잭션이 기대대로 동작하지 않을 수 있다.

```java
public void order() {
    this.saveOrder();
}

@Transactional
public void saveOrder() {
    // 트랜잭션이 적용되지 않을 수 있음
}
```

이 경우 `saveOrder()`를 외부에서 Spring Bean을 통해 호출한 것이 아니라, 같은 객체 내부에서 직접 호출한 것이다.

그래서 프록시를 거치지 못하고 `@Transactional`이 적용되지 않을 수 있다.

면접에서는 깊은 구현보다 이 정도를 말할 수 있으면 충분하다.

> `@Transactional`은 프록시 기반으로 동작하기 때문에 같은 클래스 내부 호출에서는 적용되지 않을 수 있다.

## MyBatis에서도 트랜잭션이 중요한가

중요하다.

다만 JPA와 MyBatis에서 트랜잭션을 신경 쓰는 이유가 조금 다르다.

MyBatis는 SQL을 직접 작성하고 Mapper를 통해 실행한다.

```java
@Transactional
public void createOrder(OrderRequest request) {
    orderMapper.insertOrder(request);
    stockMapper.decreaseStock(request.productId(), request.quantity());
    paymentMapper.insertPayment(request);
}
```

이 코드에서도 주문 저장, 재고 감소, 결제 내역 저장은 하나의 작업으로 묶여야 한다.

중간에 실패하면 앞에서 실행한 SQL도 함께 롤백되어야 한다.

즉, MyBatis에서도 트랜잭션은 중요하다.

다만 MyBatis에는 JPA의 영속성 컨텍스트나 dirty checking 같은 개념은 없다. 필요한 SQL을 직접 호출해야 한다.

그래서 MyBatis에서 트랜잭션의 핵심은 여러 SQL을 하나의 작업 단위로 묶는 것이다.

## JPA와 MyBatis의 차이

JPA에서는 트랜잭션이 객체 상태 관리와도 연결된다.

예를 들어 JPA에서는 트랜잭션 안에서 엔티티를 조회한 뒤 값을 바꾸면, 트랜잭션이 끝날 때 변경 감지가 일어날 수 있다.

```java
@Transactional
public void changeName(Long memberId, String name) {
    Member member = memberRepository.findById(memberId).orElseThrow();
    member.changeName(name);
}
```

위 코드에는 `update` 메서드를 직접 호출하는 부분이 없다.

하지만 JPA는 트랜잭션 안에서 관리 중인 엔티티의 변경을 감지하고, 커밋 시점에 필요한 update 쿼리를 실행할 수 있다.

반면 MyBatis는 이런 방식으로 동작하지 않는다.

```java
@Transactional
public void changeName(Long memberId, String name) {
    memberMapper.updateName(memberId, name);
}
```

MyBatis에서는 변경이 필요하면 직접 update SQL을 호출해야 한다.

정리하면 다음과 같다.

- JPA는 트랜잭션이 영속성 컨텍스트, dirty checking, lazy loading과 관련이 깊다
- MyBatis는 직접 실행한 여러 SQL을 하나의 작업 단위로 묶는 것이 핵심이다
- 둘 다 데이터 정합성을 지키기 위해 트랜잭션이 중요하다

## 면접에서는 이렇게 정리할 수 있다

Spring Transaction은 여러 DB 작업을 하나의 작업 단위로 묶기 위해 사용합니다.

정상적으로 끝나면 커밋하고, 중간에 예외가 발생하면 롤백해서 데이터 정합성을 지킵니다.

보통 `@Transactional`은 Service 계층에 붙입니다. Repository나 Mapper는 개별 DB 접근을 담당하지만, Service는 하나의 비즈니스 흐름을 담당하기 때문입니다.

JPA에서는 트랜잭션이 영속성 컨텍스트와 dirty checking 같은 객체 상태 관리와 관련이 깊습니다.

MyBatis에서는 그런 개념은 없지만, 여러 SQL을 하나의 작업으로 묶고 실패 시 롤백해야 하므로 트랜잭션은 여전히 중요합니다.

## 정리

Spring Transaction을 처음 공부할 때 모든 옵션을 한 번에 외우려고 하면 오히려 헷갈린다.

취준생 입장에서는 먼저 다음 내용부터 정확히 이해하는 것이 좋다.

- 트랜잭션은 여러 DB 작업을 하나의 작업 단위로 묶는다
- `@Transactional`은 보통 Service 계층에 붙인다
- 기본적으로 `RuntimeException`이 발생하면 롤백된다
- 예외를 잡고 삼키면 롤백되지 않을 수 있다
- 같은 클래스 내부 호출에서는 트랜잭션이 적용되지 않을 수 있다
- JPA와 MyBatis 모두 트랜잭션이 중요하지만, 신경 써야 하는 포인트는 다르다

결국 트랜잭션의 목적은 하나다.

데이터가 어긋나지 않도록 하나의 작업은 하나의 작업답게 성공하거나 실패하게 만드는 것이다.

## 관련 노트

- [[Spring Transaction 글쓰기 계획]]
- [[2026-04-21_[Spring] 스프링 생태계 정리]]
- [[2026-04-09_[Spring] IoC와 DI를 최대한 자세하게 이해해보기]]
- [[Spring]]
- [[Spring Boot]]
- [[Transaction]]
- [[JPA]]
- [[MyBatis]]
- [[Service]]
- [[Repository]]
- [[Mapper]]
