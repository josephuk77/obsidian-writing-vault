---
title: "Spring OSIV 글쓰기 계획"
created: "2026-05-08"
updated: "2026-05-08"
type: planning
status: draft
tags: [spring, jpa, osiv, transaction, blog]
source_notes:
publish_url:
---

# Spring OSIV 글쓰기 계획

## 작성된 글

- [[2026-05-08_[Spring] OSIV는 왜 끄라고 할까]]

## 글의 방향

취준생이 Spring OSIV를 공부할 때 꼭 알아야 하는 내용만 정리한다.

OSIV를 단순히 켜야 하는지 꺼야 하는지로 설명하기보다, OSIV가 왜 생겼고, 켜져 있으면 어떤 일이 가능해지고, 꺼져 있으면 어떤 문제가 드러나는지를 중심으로 쓴다.

## 예상 독자

- Spring Boot와 JPA로 프로젝트를 만들어본 취준생
- `LazyInitializationException`을 본 적이 있는 사람
- `spring.jpa.open-in-view` 경고 메시지를 보고 의미가 궁금했던 사람
- OSIV를 켜야 하는지 꺼야 하는지 헷갈리는 사람

## 핵심 결론

OSIV는 View나 Controller 계층까지 JPA 영속성 컨텍스트를 열어두는 설정이다.

켜져 있으면 트랜잭션이 끝난 뒤에도 지연 로딩이 가능해져 편하지만, DB 커넥션을 오래 잡고 있을 수 있고 계층 책임이 흐려질 수 있다.

실무에서는 API 서버라면 OSIV를 끄고, Service 계층에서 필요한 데이터를 명확히 조회해서 DTO로 반환하는 방향이 더 권장된다.

## 제목 후보

- Spring OSIV, 취준생이 꼭 알아야 할 핵심
- OSIV는 왜 켜져 있고 왜 끄라고 할까?
- `spring.jpa.open-in-view` 경고 메시지 이해하기

## 글의 목차

## OSIV란 무엇인가

OSIV는 Open Session In View의 줄임말이다.

JPA에서는 보통 Open EntityManager In View라고 이해하면 된다.

요청이 들어왔을 때 영속성 컨텍스트를 열고, 응답이 끝날 때까지 유지하는 방식이다.

핵심 문장:

> OSIV는 HTTP 요청이 끝날 때까지 JPA 영속성 컨텍스트를 열어두는 설정이다.

## OSIV가 왜 필요한가

JPA에는 지연 로딩이 있다.

연관된 데이터를 실제로 사용할 때 조회하는 방식이다.

```java
Member member = memberRepository.findById(id).orElseThrow();
String teamName = member.getTeam().getName();
```

문제는 영속성 컨텍스트가 닫힌 뒤에 지연 로딩을 시도하면 `LazyInitializationException`이 발생할 수 있다는 점이다.

OSIV가 켜져 있으면 Controller나 View 계층에서도 영속성 컨텍스트가 열려 있기 때문에 지연 로딩이 가능하다.

## OSIV가 켜져 있을 때

Spring Boot는 JPA 사용 시 OSIV가 기본적으로 켜져 있는 경우가 많다.

OSIV가 켜져 있으면 Service 계층의 트랜잭션이 끝난 뒤에도 Controller에서 지연 로딩이 가능할 수 있다.

```java
@GetMapping("/members/{id}")
public MemberResponse getMember(@PathVariable Long id) {
    Member member = memberService.findMember(id);
    return new MemberResponse(member.getName(), member.getTeam().getName());
}
```

이 코드는 편해 보이지만, Controller에서 추가 쿼리가 발생할 수 있다.

즉, 화면이나 응답을 만드는 계층에서 DB 조회가 숨어서 발생할 수 있다.

## OSIV의 문제점

OSIV가 켜져 있으면 요청이 끝날 때까지 영속성 컨텍스트가 유지된다.

이 과정에서 DB 커넥션을 오래 잡고 있을 수 있다.

특히 외부 API 호출, 파일 처리, 복잡한 응답 생성 등이 같은 요청 안에 있으면 커넥션 반환이 늦어질 수 있다.

또한 Controller나 View에서 지연 로딩이 발생하면 어디서 쿼리가 나가는지 파악하기 어려워진다.

핵심 문제:

- DB 커넥션을 오래 점유할 수 있다
- Controller나 View에서 쿼리가 발생할 수 있다
- 계층 책임이 흐려질 수 있다
- N+1 문제를 늦게 발견할 수 있다

## OSIV를 끄면 생기는 일

OSIV를 끄면 Service 계층의 트랜잭션이 끝난 뒤 영속성 컨텍스트도 닫힌다.

따라서 Controller에서 지연 로딩을 시도하면 `LazyInitializationException`이 발생할 수 있다.

```yaml
spring:
  jpa:
    open-in-view: false
```

처음에는 불편해 보이지만, 오히려 필요한 데이터를 Service 계층에서 명확히 조회하도록 만들 수 있다.

## OSIV를 끈 상태에서의 해결 방법

필요한 데이터는 Service 계층에서 미리 조회하고 DTO로 변환한다.

```java
@Transactional(readOnly = true)
public MemberResponse getMember(Long id) {
    Member member = memberRepository.findById(id).orElseThrow();
    return new MemberResponse(member.getName(), member.getTeam().getName());
}
```

또는 fetch join, EntityGraph, DTO projection 등을 사용해 필요한 데이터를 한 번에 조회한다.

취준생 글에서는 모든 방법을 깊게 설명하지 않고, 키워드 정도만 정리한다.

## OSIV는 켜야 할까 꺼야 할까

정답은 상황에 따라 다르다.

다만 API 서버에서는 보통 OSIV를 끄는 방향이 권장된다.

이유는 API 서버에서는 View 렌더링보다 명확한 응답 DTO를 만드는 구조가 많고, Controller에서 DB 조회가 숨어서 발생하는 것을 피하는 것이 좋기 때문이다.

반면 서버 사이드 렌더링처럼 View에서 엔티티 탐색이 필요한 구조라면 OSIV가 편하게 느껴질 수 있다.

핵심 문장:

> API 서버라면 OSIV를 끄고, Service 계층에서 필요한 데이터를 명확히 조회해 DTO로 반환하는 습관이 좋다.

## Transaction과 OSIV의 관계

OSIV가 켜져 있다고 해서 트랜잭션이 요청 끝까지 유지되는 것은 아니다.

트랜잭션은 보통 Service 메서드 범위에서 시작하고 끝난다.

OSIV는 트랜잭션이 아니라 영속성 컨텍스트를 요청 끝까지 열어두는 설정이다.

이 차이가 중요하다.

핵심 문장:

> OSIV는 트랜잭션을 길게 유지하는 설정이 아니라, 영속성 컨텍스트를 요청 끝까지 유지하는 설정이다.

## 면접에서 말할 수 있는 답변

OSIV는 Open Session In View의 약자로, HTTP 요청이 끝날 때까지 JPA 영속성 컨텍스트를 열어두는 설정입니다.

OSIV가 켜져 있으면 Service 계층의 트랜잭션이 끝난 뒤에도 Controller나 View에서 지연 로딩이 가능할 수 있습니다.

하지만 요청이 끝날 때까지 DB 커넥션을 오래 잡을 수 있고, Controller에서 쿼리가 발생해 계층 책임이 흐려질 수 있습니다.

그래서 API 서버에서는 보통 OSIV를 끄고, Service 계층에서 필요한 데이터를 조회한 뒤 DTO로 반환하는 방식이 권장됩니다.

## 글에서 제외할 내용

- Hibernate Session 내부 구조 상세 설명
- EntityManager와 Session의 차이 깊은 설명
- 복잡한 fetch join 최적화
- EntityGraph 상세 사용법
- N+1 문제의 모든 해결 방법
- 서버 사이드 렌더링 프레임워크 상세 비교

## 작성 순서

먼저 `spring.jpa.open-in-view` 경고 메시지나 `LazyInitializationException`을 문제 상황으로 제시한다.

그 다음 OSIV가 무엇인지 설명한다.

OSIV가 켜져 있을 때 편한 점과 위험한 점을 설명한다.

OSIV를 껐을 때 생기는 문제와 해결 방향을 설명한다.

마지막으로 API 서버에서는 왜 끄는 방향이 권장되는지 정리한다.

## 최종 글의 분위기

면접 대비와 실무 입문 사이의 글로 작성한다.

독자가 글을 다 읽고 나면 다음 질문에 답할 수 있어야 한다.

- OSIV가 무엇인가?
- OSIV가 켜져 있으면 왜 지연 로딩이 가능한가?
- OSIV가 켜져 있으면 어떤 문제가 생길 수 있는가?
- OSIV를 끄면 왜 `LazyInitializationException`이 발생할 수 있는가?
- API 서버에서는 왜 OSIV를 끄는 방향이 권장되는가?
- OSIV와 Transaction은 무엇이 다른가?
