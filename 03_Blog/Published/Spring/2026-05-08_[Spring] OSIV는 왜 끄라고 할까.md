---
title: "[Spring] OSIV는 왜 끄라고 할까"
created: "2026-05-08"
type: blog
status: published
tags:
  - spring
  - jpa
  - osiv
  - transaction
publish_url:
---

# [Spring] OSIV는 왜 끄라고 할까

Spring Boot와 JPA를 공부하다 보면 이런 설정을 볼 때가 있다.

```yaml
spring:
  jpa:
    open-in-view: false
```

또는 애플리케이션을 실행했을 때 `spring.jpa.open-in-view`와 관련된 경고 메시지를 보기도 한다.

처음에는 이 설정이 왜 필요한지 헷갈릴 수 있다.

OSIV는 JPA의 영속성 컨텍스트와 지연 로딩을 이해해야 제대로 이해할 수 있는 개념이다.

이번 글에서는 취준생 입장에서 OSIV를 공부할 때 꼭 알아야 할 핵심만 정리해보려고 한다.

## OSIV란 무엇인가

OSIV는 Open Session In View의 줄임말이다.

JPA 관점에서는 Open EntityManager In View라고 이해해도 된다.

쉽게 말하면 HTTP 요청이 시작될 때 영속성 컨텍스트를 열고, 응답이 끝날 때까지 유지하는 방식이다.

핵심은 이 문장이다.

> OSIV는 HTTP 요청이 끝날 때까지 JPA 영속성 컨텍스트를 열어두는 설정이다.

여기서 중요한 점은 OSIV가 트랜잭션을 요청 끝까지 유지한다는 뜻은 아니라는 것이다.

트랜잭션은 보통 Service 계층의 `@Transactional` 메서드 범위에서 시작하고 끝난다.

OSIV는 트랜잭션이 아니라 영속성 컨텍스트를 요청이 끝날 때까지 열어두는 설정이다.

## OSIV가 왜 필요한가

OSIV는 JPA의 지연 로딩과 관련이 깊다.

JPA에서는 연관된 객체를 실제로 사용할 때 조회하는 지연 로딩을 사용할 수 있다.

```java
Member member = memberRepository.findById(id).orElseThrow();
String teamName = member.getTeam().getName();
```

위 코드에서 `member.getTeam()`을 호출하는 순간 팀 정보를 조회하는 쿼리가 추가로 나갈 수 있다.

문제는 영속성 컨텍스트가 이미 닫힌 뒤에 지연 로딩을 시도하는 경우다.

이때는 JPA가 추가 조회를 할 수 없어서 `LazyInitializationException`이 발생할 수 있다.

OSIV가 켜져 있으면 Service 계층의 트랜잭션이 끝난 뒤에도 요청이 끝나기 전까지 영속성 컨텍스트가 열려 있다.

그래서 Controller나 View 계층에서도 지연 로딩이 가능해질 수 있다.

## OSIV가 켜져 있을 때

OSIV가 켜져 있으면 다음과 같은 코드가 동작할 수 있다.

```java
@GetMapping("/members/{id}")
public MemberResponse getMember(@PathVariable Long id) {
    Member member = memberService.findMember(id);
    return new MemberResponse(member.getName(), member.getTeam().getName());
}
```

`memberService.findMember(id)` 안에서 트랜잭션이 끝났더라도, OSIV가 켜져 있으면 Controller에서 `member.getTeam().getName()`을 호출할 때 지연 로딩이 발생할 수 있다.

처음에는 편해 보인다.

Service에서 필요한 연관 데이터를 모두 미리 준비하지 않아도 Controller에서 객체를 탐색할 수 있기 때문이다.

하지만 이 편함 때문에 문제가 생길 수 있다.

Controller에서 응답을 만드는 도중에 DB 쿼리가 숨어서 발생할 수 있다.

즉, 어디서 쿼리가 나가는지 파악하기 어려워진다.

## OSIV의 문제점

OSIV가 켜져 있으면 요청이 끝날 때까지 영속성 컨텍스트가 유지된다.

상황에 따라 DB 커넥션을 오래 잡고 있을 수 있다.

예를 들어 하나의 요청 안에서 외부 API 호출, 파일 처리, 복잡한 응답 생성이 함께 일어난다면 DB 커넥션 반환이 늦어질 수 있다.

트래픽이 적을 때는 잘 티가 나지 않을 수 있다.

하지만 요청이 많아지면 커넥션 풀이 부족해지고, 전체 응답 속도에 문제가 생길 수 있다.

또 다른 문제는 계층 책임이 흐려진다는 점이다.

Controller는 요청과 응답을 다루는 계층이고, Service는 비즈니스 로직을 처리하는 계층이다.

그런데 Controller에서 지연 로딩이 발생하면 Controller가 사실상 DB 조회까지 유발하게 된다.

정리하면 OSIV가 켜져 있을 때 주의할 점은 다음과 같다.

- DB 커넥션을 오래 점유할 수 있다
- Controller나 View에서 쿼리가 발생할 수 있다
- 어느 시점에 SQL이 실행되는지 파악하기 어려워질 수 있다
- N+1 문제를 늦게 발견할 수 있다

## OSIV를 끄면 생기는 일

OSIV를 끄려면 다음처럼 설정한다.

```yaml
spring:
  jpa:
    open-in-view: false
```

OSIV를 끄면 Service 계층의 트랜잭션이 끝난 뒤 영속성 컨텍스트도 닫힌다.

그래서 Controller에서 지연 로딩을 시도하면 `LazyInitializationException`이 발생할 수 있다.

```java
@GetMapping("/members/{id}")
public MemberResponse getMember(@PathVariable Long id) {
    Member member = memberService.findMember(id);
    return new MemberResponse(member.getName(), member.getTeam().getName());
}
```

OSIV가 꺼져 있다면 위 코드는 위험하다.

`member.getTeam()`을 호출하는 시점에는 이미 영속성 컨텍스트가 닫혀 있을 수 있기 때문이다.

처음에는 불편해 보이지만, 오히려 좋은 습관을 만들 수 있다.

필요한 데이터는 Service 계층에서 명확히 조회하고 DTO로 변환하게 되기 때문이다.

## OSIV를 끈 상태에서의 해결 방법

OSIV를 끈 상태에서는 필요한 데이터를 Service 계층 안에서 준비해야 한다.

```java
@Transactional(readOnly = true)
public MemberResponse getMember(Long id) {
    Member member = memberRepository.findById(id).orElseThrow();
    return new MemberResponse(member.getName(), member.getTeam().getName());
}
```

이렇게 하면 트랜잭션과 영속성 컨텍스트가 살아 있는 Service 계층 안에서 필요한 데이터를 사용하고, Controller에는 DTO만 반환할 수 있다.

연관 데이터가 많거나 성능이 중요하다면 fetch join, EntityGraph, DTO projection 같은 방법을 사용할 수 있다.

취준생 입장에서는 모든 방법을 깊게 외우기보다, 우선 방향을 이해하는 것이 중요하다.

> 필요한 데이터는 Service 계층에서 명확히 조회하고 DTO로 반환한다.

## API 서버에서는 보통 왜 끄는가

API 서버에서는 보통 OSIV를 끄는 방향이 권장된다.

API 서버는 View에서 엔티티를 탐색해 화면을 만드는 구조보다, Controller가 정해진 응답 DTO를 반환하는 구조가 많다.

이런 구조에서는 Controller에서 지연 로딩이 발생하는 것보다, Service에서 필요한 데이터를 명확히 조회해서 DTO를 만드는 편이 더 좋다.

쿼리가 어디서 발생하는지도 더 명확해지고, 트랜잭션 경계도 이해하기 쉬워진다.

반대로 서버 사이드 렌더링처럼 View에서 엔티티를 탐색해야 하는 구조라면 OSIV가 편하게 느껴질 수 있다.

그래서 무조건 켜라, 무조건 꺼라가 아니라 애플리케이션 구조에 따라 판단해야 한다.

다만 취준생이 API 서버를 만든다면 이렇게 정리해도 좋다.

> API 서버라면 OSIV를 끄고, Service 계층에서 필요한 데이터를 DTO로 만들어 반환하는 습관이 좋다.

## MyBatis에는 OSIV가 있을까

MyBatis에는 OSIV 개념이 없다고 보면 된다.

OSIV는 JPA의 영속성 컨텍스트와 지연 로딩 때문에 나오는 개념이다.

JPA에서는 엔티티를 조회한 뒤 연관 객체를 나중에 탐색할 때 추가 쿼리가 나갈 수 있다.

```java
Member member = memberRepository.findById(id).orElseThrow();
member.getTeam().getName();
```

하지만 MyBatis는 SQL을 직접 작성하고 Mapper를 통해 실행한다.

```java
MemberResponse member = memberMapper.findMemberWithTeam(id);
```

필요한 데이터가 있으면 SQL에서 직접 조회해야 한다.

JPA처럼 영속성 컨텍스트가 엔티티를 관리하고, 나중에 연관 객체를 탐색할 때 자동으로 지연 로딩하는 구조가 아니다.

그래서 MyBatis에서는 OSIV를 켜고 끄는 문제가 아니라, 필요한 데이터를 어떤 SQL로 조회할지와 트랜잭션 경계를 어떻게 잡을지가 더 중요하다.

정리하면 다음과 같다.

- JPA는 영속성 컨텍스트와 지연 로딩이 있어서 OSIV 개념이 있다
- MyBatis는 직접 SQL을 실행하는 방식이라 OSIV 개념이 없다
- MyBatis에서는 OSIV보다 트랜잭션 경계와 SQL 조회 범위가 중요하다

## Transaction과 OSIV의 차이

OSIV를 이해할 때 Transaction과 헷갈리면 안 된다.

`@Transactional`은 트랜잭션을 시작하고, 정상 종료 시 커밋하고, 예외 발생 시 롤백하는 역할을 한다.

반면 OSIV는 영속성 컨텍스트를 HTTP 요청이 끝날 때까지 유지하는 설정이다.

둘은 관련은 있지만 같은 개념은 아니다.

```java
@Transactional(readOnly = true)
public Member findMember(Long id) {
    return memberRepository.findById(id).orElseThrow();
}
```

위 메서드에서 트랜잭션은 메서드가 끝나면 종료된다.

하지만 OSIV가 켜져 있으면 영속성 컨텍스트는 요청이 끝날 때까지 유지될 수 있다.

핵심은 이렇게 정리할 수 있다.

> Transaction은 커밋과 롤백의 범위이고, OSIV는 영속성 컨텍스트를 어디까지 열어둘지에 대한 설정이다.

## 면접에서는 이렇게 정리할 수 있다

OSIV는 Open Session In View의 약자로, HTTP 요청이 끝날 때까지 JPA 영속성 컨텍스트를 열어두는 설정입니다.

OSIV가 켜져 있으면 Service 계층의 트랜잭션이 끝난 뒤에도 Controller나 View에서 지연 로딩이 가능할 수 있습니다.

하지만 요청이 끝날 때까지 DB 커넥션을 오래 잡을 수 있고, Controller에서 쿼리가 발생해 계층 책임이 흐려질 수 있습니다.

그래서 API 서버에서는 보통 OSIV를 끄고, Service 계층에서 필요한 데이터를 조회한 뒤 DTO로 반환하는 방식이 권장됩니다.

MyBatis는 JPA의 영속성 컨텍스트와 지연 로딩 구조가 아니기 때문에 OSIV 개념이 없습니다.

## 정리

OSIV는 처음 보면 단순한 설정처럼 보이지만, JPA의 동작 방식과 계층 설계에 영향을 주는 중요한 개념이다.

취준생 입장에서는 다음 내용을 먼저 이해하면 된다.

- OSIV는 요청이 끝날 때까지 JPA 영속성 컨텍스트를 열어두는 설정이다
- OSIV가 켜져 있으면 Controller나 View에서도 지연 로딩이 가능할 수 있다
- 대신 DB 커넥션을 오래 잡거나 Controller에서 쿼리가 발생할 수 있다
- OSIV를 끄면 Service 계층에서 필요한 데이터를 명확히 조회해야 한다
- API 서버에서는 보통 OSIV를 끄고 DTO로 응답을 만드는 방향이 권장된다
- MyBatis에는 OSIV 개념이 없다
- Transaction과 OSIV는 같은 개념이 아니다

결국 OSIV를 이해한다는 것은 JPA에서 데이터 조회 책임을 어디에 둘 것인지 이해하는 것과 연결된다.

## 관련 노트

- [[Spring OSIV 글쓰기 계획]]
- [[2026-05-08_[Spring] @Transactional은 왜 Service에 붙일까]]
- [[2026-04-21_[Spring] 스프링 생태계 정리]]
- [[Spring]]
- [[Spring Boot]]
- [[JPA]]
- [[OSIV]]
- [[Transaction]]
- [[영속성 컨텍스트]]
- [[지연 로딩]]
- [[MyBatis]]
- [[DTO]]
