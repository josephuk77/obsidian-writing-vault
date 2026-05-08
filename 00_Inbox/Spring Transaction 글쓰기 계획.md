---
title: "Spring Transaction 글쓰기 계획"
created: "2026-05-08"
updated: "2026-05-08"
type: planning
status: draft
tags: [spring, transaction, java, backend, blog]
source_notes:
publish_url:
---

# Spring Transaction 글쓰기 계획

## 작성된 글

- [[2026-05-08_[Spring] @Transactional은 왜 Service에 붙일까]]

## 글의 방향

취준생이 Spring Transaction을 공부할 때 꼭 알아야 하는 내용만 정리한다.

너무 깊은 내부 구현이나 모든 옵션을 나열하기보다, `@Transactional`을 왜 쓰는지, 어디에 붙이는지, 언제 롤백되는지, JPA와 MyBatis에서는 어떤 차이가 있는지를 중심으로 쓴다.

## 예상 독자

- Spring Boot로 CRUD 프로젝트를 만들어본 취준생
- `@Transactional`을 붙여본 적은 있지만 정확한 이유는 모르는 사람
- JPA와 MyBatis에서 트랜잭션이 어떻게 다른지 헷갈리는 사람
- 면접에서 트랜잭션 질문을 받았을 때 핵심만 말하고 싶은 사람

## 핵심 결론

Spring Transaction은 여러 DB 작업을 하나의 작업 단위로 묶어서, 모두 성공하면 커밋하고 중간에 실패하면 롤백하기 위해 사용한다.

`@Transactional`은 단순히 붙이는 어노테이션이 아니라, 데이터 정합성을 지키기 위한 장치다.

## 제목 후보

- Spring Transaction, 취준생이 꼭 알아야 할 핵심
- `@Transactional`을 왜 Service에 붙일까?
- JPA와 MyBatis에서 트랜잭션은 어떻게 다를까?

## 글의 목차

## 트랜잭션이 필요한 이유

주문 기능을 예시로 시작한다.

주문 생성, 재고 감소, 결제 기록 저장이 각각 따로 성공하면 문제가 생길 수 있다. 예를 들어 주문은 생성됐는데 재고 감소 중 예외가 발생하면 데이터가 어긋난다.

이런 상황을 막기 위해 여러 DB 작업을 하나의 단위로 묶는다.

핵심 문장:

> 트랜잭션은 여러 DB 작업을 하나의 작업처럼 다루기 위한 기능이다.

## Spring에서 트랜잭션을 사용하는 방법

Spring에서는 보통 `@Transactional`을 사용한다.

```java
@Transactional
public void createOrder(OrderRequest request) {
    orderRepository.save(order);
    stockRepository.decrease(productId, quantity);
    paymentRepository.save(payment);
}
```

정상적으로 끝나면 커밋되고, 중간에 예외가 발생하면 롤백된다.

이 부분에서는 내부 구현을 길게 설명하지 않는다. 대신 Spring이 메서드 실행 전후로 트랜잭션을 관리해준다는 정도로 설명한다.

## 어디에 붙이는가

`@Transactional`은 보통 Service 계층에 붙인다.

Repository나 Mapper는 DB에 접근하는 역할이고, Service는 하나의 비즈니스 흐름을 담당한다.

예를 들어 주문 생성이라는 하나의 기능 안에서 주문 저장, 재고 감소, 결제 저장이 함께 실행된다. 이 작업 전체가 하나의 트랜잭션이 되어야 하므로 Service 계층에 붙이는 것이 자연스럽다.

핵심 문장:

> 트랜잭션은 개별 SQL이 아니라 하나의 비즈니스 작업 단위에 거는 것이 좋다.

## 롤백은 언제 되는가

Spring은 기본적으로 `RuntimeException`이 발생하면 롤백한다.

checked exception은 기본적으로 롤백되지 않는다.

취준생 글에서는 예외 계층을 깊게 파기보다 이 정도를 핵심으로 잡는다.

```java
@Transactional
public void createOrder() {
    throw new RuntimeException("주문 실패");
}
```

이 경우 트랜잭션은 롤백된다.

checked exception까지 롤백하고 싶다면 `rollbackFor`를 사용할 수 있다고 짧게 언급한다.

```java
@Transactional(rollbackFor = Exception.class)
public void createOrder() throws Exception {
    throw new Exception("주문 실패");
}
```

## 자주 하는 실수

예외를 잡고 다시 던지지 않으면 롤백되지 않을 수 있다.

```java
@Transactional
public void createOrder() {
    try {
        payment();
    } catch (RuntimeException e) {
        // 예외를 밖으로 던지지 않으면 정상 종료로 판단될 수 있다
    }
}
```

같은 클래스 내부에서 메서드를 호출하면 `@Transactional`이 기대대로 동작하지 않을 수 있다.

```java
public void order() {
    this.saveOrder();
}

@Transactional
public void saveOrder() {
    // 트랜잭션이 적용되지 않을 수 있음
}
```

이유는 Spring의 트랜잭션이 프록시 기반으로 동작하기 때문이다. 다만 글에서는 프록시 개념을 너무 깊게 설명하지 않고, 내부 호출은 주의해야 한다는 정도로 정리한다.

## MyBatis에서도 트랜잭션이 중요한가

중요하다.

MyBatis는 직접 SQL을 작성하고 Mapper를 통해 실행한다. JPA처럼 영속성 컨텍스트나 dirty checking 개념은 없지만, 여러 SQL을 하나의 작업 단위로 묶어야 하는 상황은 똑같이 존재한다.

```java
@Transactional
public void createOrder(OrderRequest request) {
    orderMapper.insertOrder(request);
    stockMapper.decreaseStock(request.productId(), request.quantity());
    paymentMapper.insertPayment(request);
}
```

중간에 실패하면 앞에서 실행된 SQL도 함께 롤백되어야 한다.

핵심 문장:

> MyBatis에서는 JPA 특유의 영속성 컨텍스트 문제는 적지만, 여러 SQL의 성공과 실패를 하나로 묶기 위해 트랜잭션은 여전히 중요하다.

## JPA와 MyBatis에서 트랜잭션 차이

JPA에서는 트랜잭션이 객체 상태 관리와 밀접하게 연결된다.

- dirty checking
- lazy loading
- 영속성 컨텍스트

예를 들어 JPA에서는 엔티티를 조회한 뒤 값을 바꾸면, 트랜잭션이 끝날 때 변경 감지를 통해 update 쿼리가 나갈 수 있다.

```java
@Transactional
public void changeName(Long memberId, String name) {
    Member member = memberRepository.findById(memberId).orElseThrow();
    member.changeName(name);
}
```

MyBatis에서는 이런 변경 감지가 없다. update가 필요하면 직접 SQL을 호출해야 한다.

```java
@Transactional
public void changeName(Long memberId, String name) {
    memberMapper.updateName(memberId, name);
}
```

정리하면 JPA는 트랜잭션이 객체 상태 관리와도 연결되고, MyBatis는 실행한 SQL들을 하나의 작업 단위로 묶는 역할이 더 중심이다.

## 면접에서 말할 수 있는 답변

Spring Transaction은 여러 DB 작업을 하나의 작업 단위로 묶기 위해 사용합니다. 정상적으로 끝나면 커밋하고, 중간에 예외가 발생하면 롤백해서 데이터 정합성을 지킵니다.

보통 `@Transactional`은 Service 계층에 붙입니다. Repository나 Mapper는 개별 DB 접근을 담당하지만, Service는 하나의 비즈니스 흐름을 담당하기 때문입니다.

JPA에서는 트랜잭션이 영속성 컨텍스트, dirty checking, lazy loading과 관련이 깊습니다. MyBatis에서는 그런 개념은 없지만, 여러 SQL을 하나의 작업으로 묶고 실패 시 롤백해야 하므로 트랜잭션은 여전히 중요합니다.

## 글에서 제외할 내용

- 모든 propagation 옵션
- 모든 isolation level
- 분산 트랜잭션
- Spring Batch 트랜잭션
- Reactive Transaction
- `PlatformTransactionManager` 내부 구조

## 작성 순서

주문 예시로 트랜잭션이 왜 필요한지 설명한다.

그 다음 `@Transactional`을 Service에 붙이는 이유를 설명한다.

롤백 조건과 자주 하는 실수를 정리한다.

마지막으로 JPA와 MyBatis에서 트랜잭션을 바라보는 차이를 비교한다.

## 최종 글의 분위기

면접 대비와 실무 입문 사이의 글로 작성한다.

독자가 글을 다 읽고 나면 다음 질문에 답할 수 있어야 한다.

- 트랜잭션이 왜 필요한가?
- `@Transactional`은 어디에 붙이는가?
- 언제 롤백되는가?
- JPA와 MyBatis에서 트랜잭션은 어떻게 다른가?
