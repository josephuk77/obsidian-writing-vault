---
title: "[Network] WS와 WAS의 차이"
created: "2026-04-21"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Network-WS와-WAS의-차이"
---

# [Network] WS와 WAS의 차이

스프링 MVC 흐름을 공부하다 보면 WS와 WAS라는 단어도 자주 보게 된다.

처음에는 둘 다 서버 아닌가 싶었는데, 역할을 나눠서 보면 차이가 있다.

WS는 Web Server의 줄임말이고, WAS는 Web Application Server의 줄임말이다.

## Web Server

Web Server는 클라이언트의 요청을 받아서 정적인 파일을 응답해주는 서버다.

예를 들면 다음과 같은 파일들이 정적 리소스에 해당한다.
```text
HTML
CSS
JavaScript
Image
Font
```
대표적인 Web Server로는 Nginx, Apache가 있다.

브라우저가 서버에 이미지를 요청하거나, CSS 파일을 요청하면 Web Server는 해당 파일을 찾아서 그대로 응답해준다.
```text
Client → Web Server → Static File
```
정적인 파일은 매번 결과가 바뀌지 않는다.

예를 들어 로고 이미지는 누가 요청해도 같은 이미지가 내려간다. 이런 요청은 복잡한 비즈니스 로직을 거칠 필요가 없기 때문에 Web Server가 빠르게 처리할 수 있다.

## WAS

WAS는 동적인 요청을 처리하는 서버다.

사용자의 요청에 따라 결과가 달라지는 작업을 처리한다.

예를 들면 다음과 같은 요청들이 있다.
```text
회원가입
로그인
게시글 작성
댓글 조회
상품 주문
마이페이지 조회
```
이런 요청은 단순히 파일을 찾아서 내려주는 것이 아니라, Java 코드가 실행되고 비즈니스 로직이 처리되어야 한다.

스프링에서는 이런 요청이 들어오면 Controller, Service, Repository를 거쳐서 처리된다.
```text
Client
  ↓
WAS
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```
Spring Boot에서 자주 사용하는 내장 Tomcat도 WAS 역할을 한다고 볼 수 있다.

정확히 말하면 Tomcat은 Servlet Container지만, 스프링 웹 애플리케이션을 실행하고 동적인 요청을 처리하는 역할을 하기 때문에 WAS처럼 이해하면 된다.

## WS와 WAS의 요청 처리 흐름

실제 서비스에서는 Web Server와 WAS를 같이 사용하는 경우가 많다.

전체 흐름은 보통 이런 식이다.
```text
Client
  ↓
Web Server
  ↓
WAS
  ↓
Spring MVC
  ↓
Database
```
예를 들어 사용자가 게시글 목록을 조회한다고 하면 흐름은 다음과 같다.
```text
Client
  ↓
Nginx
  ↓
Tomcat
  ↓
DispatcherServlet
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```
여기서 Nginx는 Web Server 역할을 하고, Tomcat은 WAS 역할을 한다.

정적 파일 요청이면 Web Server가 바로 처리할 수 있다.
```text
Client → Nginx → Image, CSS, JS
```
하지만 회원 정보 조회처럼 동적인 처리가 필요한 요청이면 WAS로 넘긴다.
```text
Client → Nginx → Tomcat → Spring MVC → Database
```
## 왜 Web Server와 WAS를 나눌까

처음에는 그냥 WAS 하나만 써도 되지 않을까라는 생각이 들 수 있다.

실제로 Spring Boot는 내장 Tomcat을 가지고 있기 때문에 단독으로 실행해도 웹 요청을 받을 수 있다.

하지만 실제 운영 환경에서는 Web Server를 앞에 두는 경우가 많다.

이유는 여러 가지가 있다.

Web Server는 정적 파일을 빠르게 처리할 수 있다.

이미지, CSS, JavaScript 같은 파일까지 모두 WAS가 처리하면 WAS에 불필요한 부담이 생긴다. 정적인 파일은 Web Server가 처리하고, 동적인 요청만 WAS로 넘기면 더 효율적이다.

또 Web Server는 리버스 프록시 역할도 할 수 있다.
```text
Client → Nginx → WAS
```
클라이언트는 실제 WAS 주소를 직접 알 필요가 없다. Web Server가 앞에서 요청을 받아서 내부 WAS로 전달해준다.

이렇게 하면 보안적으로도 좋고, 여러 WAS 서버로 요청을 분산시키기도 쉽다.
```text
Client
  ↓
Nginx
  ↓
WAS 1
WAS 2
WAS 3
```
서비스 트래픽이 많아지면 WAS를 여러 대 띄우고, Web Server가 요청을 적절히 나눠줄 수 있다.

## Spring MVC는 어디서 실행될까

Spring MVC는 WAS 안에서 실행된다.

조금 더 정확히 보면, 클라이언트의 요청이 WAS에 도착하면 Servlet Container가 요청을 받고, 그 요청을 DispatcherServlet에게 전달한다.

DispatcherServlet은 Spring MVC의 핵심이다.
```text
Client
  ↓
Web Server
  ↓
WAS
  ↓
DispatcherServlet
  ↓
Controller
  ↓
Service
  ↓
Repository
```
즉, Web Server가 Spring MVC를 직접 실행하는 것은 아니다.

Web Server는 요청을 받고, 필요한 경우 WAS로 넘긴다.

Spring MVC의 Controller, Service, Repository 같은 코드는 WAS 안에서 실행된다.

## WS와 WAS 차이 정리
구분	WS	WAS
의미	Web Server	Web Application Server
역할	정적 리소스 처리	동적 요청 처리
처리 대상	HTML, CSS, JS, Image	로그인, 회원가입, 게시글 작성 등
대표 예시	Nginx, Apache	Tomcat, Jetty, JBoss
비즈니스 로직 실행	하지 않음	실행함
데이터베이스 접근	보통 하지 않음	가능
스프링 MVC 실행	하지 않음	실행함
## 정리

WS는 정적인 요청을 처리하는 서버이고, WAS는 동적인 요청을 처리하는 서버다.

Web Server는 이미지, CSS, JavaScript 같은 정적 파일을 빠르게 응답할 수 있다.

WAS는 사용자의 요청에 따라 Java 코드를 실행하고, 비즈니스 로직을 처리하고, 데이터베이스와 통신한다.

스프링 MVC는 WAS 안에서 실행된다.

그래서 실제 요청 흐름을 보면 Client → Web Server → WAS → Spring MVC → Database 형태로 이해할 수 있다.

Spring Boot를 처음 공부할 때는 내장 Tomcat 덕분에 Web Server와 WAS의 구분이 잘 느껴지지 않을 수 있다.

하지만 운영 환경으로 갈수록 Nginx 같은 Web Server를 앞에 두고, 뒤에서 Spring Boot 애플리케이션이 WAS 역할을 하는 구조를 많이 사용한다.
---

## 관련 글

- [[Network]]
- [[HTTP]]
- [[Web Server]]
- [[WAS]]
- [[Velog]]
