---
title: "[Spring] Spring Bean 생명주기 완전 정리"
created: "2026-04-09"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Spring-Spring-Bean-생명주기-완전-정리"
---

# [Spring] Spring Bean 생명주기 완전 정리

> Bean은 언제 생성되고, 언제 초기화되고, 언제 소멸될까?

스프링을 공부하다 보면 `Bean`, `IoC`, `DI`는 많이 보는데, 정작 **Bean이 생성된 뒤 어떤 순서로 초기화되고, 언제 소멸되는지**는 흐릿하게 알고 넘어가는 경우가 많다.

나도 처음에는 그냥 `@Component` 붙이면 객체가 만들어지고, `@Autowired`로 주입되고, 끝이라고 생각했다.  
그런데 조금만 깊게 들어가면 스프링은 객체를 단순히 만들기만 하는 게 아니라, **생성 → 의존성 주입 → 초기화 콜백 → 사용 → 종료 시 소멸 콜백**까지 꽤 정교하게 관리한다.

이번 글에서는 **Spring Bean 생명주기**를 최대한 자세하게 정리해보려고 한다.  
단순히 개념만 적는 게 아니라, **실제 코드 예시**, **어떤 순서로 호출되는지**, **잘 활용했을 때 장점**, **남용했을 때 단점과 주의점**까지 같이 정리해본다.

---

## 목차

- [1. Bean 생명주기란?](#1-bean-생명주기란)
- [2. Bean 생명주기의 큰 흐름](#2-bean-생명주기의-큰-흐름)
- [3. Bean 생성부터 초기화까지 자세히 보기](#3-bean-생성부터-초기화까지-자세히-보기)
- [4. 실제 코드로 생명주기 순서 확인하기](#4-실제-코드로-생명주기-순서-확인하기)
- [5. 실무에서는 보통 어떤 방식으로 쓰는가](#5-실무에서는-보통-어떤-방식으로-쓰는가)
- [6. BeanPostProcessor는 어디에 끼어드는가](#6-beanpostprocessor는-어디에-끼어드는가)
- [7. 소멸 단계에서 꼭 알아야 할 것들](#7-소멸-단계에서-꼭-알아야-할-것들)
- [8. scope에 따라 생명주기가 달라진다](#8-scope에-따라-생명주기가-달라진다)
- [9. lazy initialization이 생명주기에 주는 영향](#9-lazy-initialization이-생명주기에-주는-영향)
- [10. Lifecycle / SmartLifecycle은 또 뭐지?](#10-lifecycle--smartlifecycle은-또-뭐지)
- [11. Bean 생명주기를 잘 활용했을 때 장점](#11-bean-생명주기를-잘-활용했을-때-장점)
- [12. 단점과 주의점](#12-단점과-주의점)
- [13. 정리](#13-정리)

---

# Bean 생명주기란?

스프링에서 Bean은 **Spring IoC 컨테이너가 생성하고, 조립하고, 관리하는 객체**다.  
즉, 그냥 `new`로 만든 평범한 객체와 달리, 스프링 컨테이너 안에서 일정한 규칙과 시점에 따라 관리된다.

Bean 생명주기라는 말은 결국 이걸 뜻한다.

> **Bean이 언제 생성되고, 언제 의존성이 주입되고, 언제 초기화 작업을 하고, 언제 소멸되는가**

이걸 이해하면 다음 같은 것들이 잘 보이기 시작한다.

- `@PostConstruct`는 왜 필요한지
- `@PreDestroy`는 언제 호출되는지
- `@Transactional`이 어떤 시점에는 왜 안 먹는지
- `prototype` Bean은 왜 소멸 콜백이 안 불리는지
- `@Lazy`를 쓰면 생성 시점이 왜 달라지는지

---

# Bean 생명주기의 큰 흐름

Bean 생명주기는 크게 보면 아래 순서로 이해하면 된다.

1. **Bean 정의(BeanDefinition) 등록**
2. **Bean 인스턴스 생성**
3. **의존성 주입**
4. **Aware 콜백 처리**
5. **BeanPostProcessor before initialization**
6. **초기화 콜백 실행**
   - `@PostConstruct`
   - `afterPropertiesSet()`
   - custom `initMethod`
7. **BeanPostProcessor after initialization**
8. **Bean 사용**
9. **컨테이너 종료 시 소멸 콜백 실행**
   - `@PreDestroy`
   - `destroy()`
   - custom `destroyMethod`

즉, 스프링은 단순히 객체를 만들기만 하는 게 아니라  
**객체가 준비되고, 사용되고, 정리되는 전체 과정**을 관리한다고 보면 된다.

---

# Bean 생성부터 초기화까지 자세히 보기

## Bean 정의 등록

가장 먼저 스프링은 어떤 객체를 Bean으로 관리할지 알아야 한다.

예를 들면 이런 방식들이 있다.

- `@Component`
- `@Service`
- `@Repository`
- `@Controller`
- `@Configuration` + `@Bean`

이 단계에서는 아직 객체가 만들어진 게 아니라,  
“이 클래스는 나중에 Bean으로 관리할 거야” 라는 **설계도(BeanDefinition)** 가 등록되는 단계라고 보면 된다.

---

## Bean 인스턴스 생성

그다음 스프링은 실제 객체를 만든다.

예를 들어 이런 Bean이 있다고 해보자.

```java
@Component
public class OrderService {
    public OrderService() {
        System.out.println("OrderService 생성자 호출");
    }
}
```

Bean 생성 시점에는 생성자가 호출된다.

여기서 중요한 건, **생성자 호출 = 생명주기 끝이 아니다** 는 점이다.  
이 시점은 그냥 객체가 메모리에 올라온 것뿐이고, 아직 의존성 주입도 끝나지 않았고 초기화도 끝나지 않았다.

---

## 의존성 주입

객체가 생성된 뒤에는 필요한 의존성이 주입된다.

```java
@Component
public class OrderService {

    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

스프링은 Bean을 만들면서 생성자 인자, 필드, setter 등을 통해 필요한 의존성을 주입한다.

실무에서는 대부분 **생성자 주입**을 사용하지만, 생명주기 자체는 어떤 주입 방식을 쓰든  
“객체 생성 뒤, 초기화 전에 의존성 연결이 끝난다” 정도로 이해하면 된다.

---

## Aware 콜백

스프링은 필요하면 Bean에게 자기 이름이나 BeanFactory, ApplicationContext 같은 인프라 객체를 알려줄 수 있다.

대표적으로 이런 인터페이스가 있다.

- `BeanNameAware`
- `BeanFactoryAware`
- `ApplicationContextAware`

예를 들면:

```java
import org.springframework.beans.factory.BeanNameAware;

public class MyBean implements BeanNameAware {

    @Override
    public void setBeanName(String name) {
        System.out.println("Bean 이름 = " + name);
    }
}
```

다만 실무에서는 이걸 많이 쓰는 편은 아니다.  
비즈니스 로직이 스프링 인프라에 너무 가까워질 수 있기 때문이다.

---

## BeanPostProcessor before initialization

그다음 단계에서 `BeanPostProcessor`가 동작할 수 있다.

`BeanPostProcessor`는 Bean이 초기화되기 전후에 개입해서 공통 로직을 넣거나, Bean을 감싸거나, 프록시를 만들 수 있게 해주는 확장 포인트다.

이 지점이 중요한 이유는, 스프링 내부의 많은 기능이 여기서 구현되기 때문이다.

예를 들면:

- `@PostConstruct` 처리
- AOP 프록시 생성
- 여러 애노테이션 기반 후처리

즉, `BeanPostProcessor`는 “스프링이 Bean을 더 똑똑하게 다루게 해주는 장치”라고 보면 된다.

---

## 초기화 콜백

이제 진짜 “초기화 완료 직전” 단계다.

스프링은 Bean이 필요한 의존성을 다 받은 뒤,  
초기화 작업을 할 수 있도록 콜백을 제공한다.

대표적인 방식은 3가지다.

### 1) `@PostConstruct`

```java
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

@Component
public class CacheManager {

    @PostConstruct
    public void init() {
        System.out.println("캐시 초기 데이터 적재");
    }
}
```

가장 많이 쓰고, 가장 무난하다.

---

### 2) `InitializingBean.afterPropertiesSet()`

```java
import org.springframework.beans.factory.InitializingBean;
import org.springframework.stereotype.Component;

@Component
public class CacheManager implements InitializingBean {

    @Override
    public void afterPropertiesSet() {
        System.out.println("초기화 작업 수행");
    }
}
```

이 방식은 Spring 인터페이스에 직접 의존하게 된다는 점에서  
요즘은 `@PostConstruct`보다 선호도가 낮은 편이다.

---

### 3) custom `initMethod`

```java
public class ExternalClient {

    public void connect() {
        System.out.println("외부 서버 연결");
    }
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean(initMethod = "connect")
    public ExternalClient externalClient() {
        return new ExternalClient();
    }
}
```

이 방식은 내가 직접 수정할 수 없는 외부 라이브러리 객체에도 적용할 수 있다는 장점이 있다.

---

## BeanPostProcessor after initialization

초기화까지 끝나면 `postProcessAfterInitialization()`가 호출된다.

이 단계에서는 Bean이 프록시로 감싸질 수도 있고, 최종적으로 컨테이너에 “사용 가능한 Bean”으로 올라간다.

이 부분은 실무에서 은근 중요하다.  
왜냐하면 **초기화 메서드는 프록시 적용 전 raw bean 기준으로 실행될 수 있기 때문**이다.

그래서 `@PostConstruct` 안에서 트랜잭션이나 AOP 같은 프록시 기반 기능을 기대하는 코드는 주의해야 한다.

---

# 실제 코드로 생명주기 순서 확인하기

이번에는 코드로 직접 보자.  
아래 예시는 **순서를 보여주기 위한 데모 코드**다.

> 참고로 실무에서는 `InitializingBean`, `DisposableBean`, custom init/destroy method를 전부 한 Bean에 다 쓰지 않는다.  
> 여기서는 순서를 확인하려고 일부러 다 넣은 예시다.

```java
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.InitializingBean;

public class LifeCycleBean implements InitializingBean, DisposableBean {

    public LifeCycleBean() {
        System.out.println("1. 생성자 호출");
    }

    @PostConstruct
    public void postConstruct() {
        System.out.println("2. @PostConstruct 호출");
    }

    @Override
    public void afterPropertiesSet() {
        System.out.println("3. afterPropertiesSet 호출");
    }

    public void customInit() {
        System.out.println("4. custom initMethod 호출");
    }

    @PreDestroy
    public void preDestroy() {
        System.out.println("5. @PreDestroy 호출");
    }

    @Override
    public void destroy() {
        System.out.println("6. destroy 호출");
    }

    public void customDestroy() {
        System.out.println("7. custom destroyMethod 호출");
    }
}
```

```java
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean(initMethod = "customInit", destroyMethod = "customDestroy")
    public LifeCycleBean lifeCycleBean() {
        return new LifeCycleBean();
    }

    public static void main(String[] args) {
        AnnotationConfigApplicationContext context =
                new AnnotationConfigApplicationContext(AppConfig.class);

        System.out.println("=== 컨테이너 사용 중 ===");

        context.close();
    }
}
```

예상 출력은 이런 느낌이다.

```text
1. 생성자 호출
2. @PostConstruct 호출
3. afterPropertiesSet 호출
4. custom initMethod 호출
=== 컨테이너 사용 중 ===
5. @PreDestroy 호출
6. destroy 호출
7. custom destroyMethod 호출
```

즉, 초기화는

- `@PostConstruct`
- `afterPropertiesSet()`
- custom initMethod

순서로 진행되고,

소멸은

- `@PreDestroy`
- `destroy()`
- custom destroyMethod

순서로 진행된다고 이해하면 된다.

---

# 실무에서는 보통 어떤 방식으로 쓰는가

실무에서는 위처럼 여러 메커니즘을 섞기보다 보통 아래 두 가지를 많이 쓴다.

## `@PostConstruct` / `@PreDestroy`

가장 흔하고 무난하다.

```java
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.springframework.stereotype.Component;

@Component
public class CacheManager {

    @PostConstruct
    public void init() {
        System.out.println("캐시 초기 데이터 적재");
    }

    @PreDestroy
    public void clear() {
        System.out.println("캐시 비우기");
    }
}
```

이 방식의 장점은 코드가 직관적이고, Spring 인터페이스에 직접 의존하지 않는다는 점이다.

---

## `@Bean(initMethod, destroyMethod)`

외부 라이브러리 객체처럼 내가 코드를 수정할 수 없는 경우에 특히 유용하다.

```java
public class ExternalClient {

    public void connect() {
        System.out.println("외부 서버 연결");
    }

    public void close() {
        System.out.println("외부 서버 연결 종료");
    }
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ClientConfig {

    @Bean(initMethod = "connect", destroyMethod = "close")
    public ExternalClient externalClient() {
        return new ExternalClient();
    }
}
```

이 방식은 “내가 만든 클래스가 아니어도 생명주기 메서드를 연결할 수 있다”는 점이 강력하다.

---

# BeanPostProcessor는 어디에 끼어드는가

`BeanPostProcessor`는 일반 비즈니스 개발자가 매일 쓰는 기능은 아니지만,  
스프링을 이해하려면 꼭 알아야 한다.

간단한 예시를 보면:

```java
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.stereotype.Component;

@Component
public class LoggingBeanPostProcessor implements BeanPostProcessor {

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        if (beanName.equals("orderService")) {
            System.out.println("before initialization: " + beanName);
        }
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        if (beanName.equals("orderService")) {
            System.out.println("after initialization: " + beanName);
        }
        return bean;
    }
}
```

이 코드는 특정 Bean이 초기화되기 전후에 로그를 찍는다.

이게 왜 중요하냐면,  
스프링 내부의 많은 기능이 바로 이 구조 위에서 돌아가기 때문이다.

예를 들어:

- `@PostConstruct` 처리
- AOP 프록시 생성
- `@Autowired` 관련 후처리
- 각종 인프라성 확장

즉, Bean 생명주기는 단순히 “객체 생성하고 끝”이 아니라,  
중간에 **후처리기(BeanPostProcessor)** 가 깊숙이 개입하는 구조다.

---

# 소멸 단계에서 꼭 알아야 할 것들

Bean은 생성만 중요한 게 아니라 **정리(clean-up)** 도 중요하다.

특히 아래 같은 리소스를 다룰 때는 소멸 단계가 매우 중요하다.

- DB 연결 풀
- 소켓 연결
- 스레드 풀
- 캐시
- 파일 핸들
- 외부 API 클라이언트

예를 들어:

```java
import jakarta.annotation.PreDestroy;
import org.springframework.stereotype.Component;

@Component
public class SocketClient {

    public SocketClient() {
        System.out.println("소켓 연결 생성");
    }

    @PreDestroy
    public void close() {
        System.out.println("소켓 연결 정리");
    }
}
```

이런 식으로 종료 시 자원을 정리하지 않으면:

- 메모리 누수
- 연결 누수
- 스레드 누수
- 비정상 종료

같은 문제가 생길 수 있다.

---

# scope에 따라 생명주기가 달라진다

이 부분은 꼭 알아야 한다.

많은 사람들이 `@PreDestroy`는 모든 Bean에 다 호출될 거라고 생각하는데, 그렇지 않다.

## singleton Bean

기본 scope다.  
컨테이너가 생성하고, 컨테이너가 끝날 때 소멸도 관리한다.

즉:

- 생성 시 초기화 콜백 호출
- 종료 시 소멸 콜백 호출

---

## prototype Bean

문제는 `prototype`이다.

`prototype` Bean은 **생성/초기화까지는 스프링이 해주지만**,  
그 이후에는 컨테이너가 더 이상 추적하지 않는다.

예를 들면:

```java
import jakarta.annotation.PreDestroy;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@Scope("prototype")
public class PrototypeBean {

    public PrototypeBean() {
        System.out.println("prototype bean 생성");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("prototype bean 소멸");
    }
}
```

이 경우 `destroy()`는 자동으로 호출되지 않는다.

즉, prototype Bean에서 비싼 자원을 들고 있다면  
**정리 책임은 클라이언트 쪽이 직접 져야 한다**는 뜻이다.

이건 실무에서 꽤 중요하다.  
괜히 prototype Bean에 네트워크 연결이나 파일 핸들을 넣어두고 자동 정리를 기대하면 문제 생긴다.

---

# lazy initialization이 생명주기에 주는 영향

스프링은 기본적으로 singleton Bean을 애플리케이션 시작 시 eager하게 미리 생성한다.

그런데 `@Lazy`를 쓰면 생성 시점이 달라진다.

```java
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Lazy
public class ExpensiveBean {

    public ExpensiveBean() {
        System.out.println("ExpensiveBean 생성");
    }
}
```

이 Bean은 애플리케이션 시작 시점이 아니라, **처음 요청될 때 생성**된다.

이건 장단점이 분명하다.

### 장점
- 시작 속도 개선 가능
- 당장 안 쓰는 Bean은 늦게 만들 수 있음

### 단점
- 문제 발견이 늦어진다
- 시작할 때는 멀쩡해 보이다가 실제 요청 시점에 터질 수 있다

즉, lazy는 무조건 좋은 최적화가 아니라  
“언제 만들지”를 뒤로 미루는 전략이라고 이해하는 게 맞다.

---

# Lifecycle / SmartLifecycle은 또 뭐지?

여기서 하나 더 있다.

지금까지 본 건 주로 **init / destroy** 중심의 생명주기였다.  
그런데 백그라운드 작업처럼 “시작(start)”과 “정지(stop)”가 중요한 Bean도 있다.

이럴 때 쓰는 게 `Lifecycle`, `SmartLifecycle`이다.

예를 들면:

```java
import org.springframework.context.SmartLifecycle;
import org.springframework.stereotype.Component;

@Component
public class MessageConsumer implements SmartLifecycle {

    private boolean running = false;

    @Override
    public void start() {
        System.out.println("메시지 컨슈머 시작");
        running = true;
    }

    @Override
    public void stop() {
        System.out.println("메시지 컨슈머 중지");
        running = false;
    }

    @Override
    public boolean isRunning() {
        return running;
    }

    @Override
    public boolean isAutoStartup() {
        return true;
    }

    @Override
    public int getPhase() {
        return 0;
    }

    @Override
    public void stop(Runnable callback) {
        stop();
        callback.run();
    }
}
```

이건 단순한 “초기화/소멸”과는 좀 결이 다르다.

- `@PostConstruct`, `@PreDestroy` → 설정 검증, 자원 준비/해제
- `SmartLifecycle` → 실제 런타임 컴포넌트 시작/정지

즉, 메시지 소비기, 스케줄러, 장시간 실행되는 백그라운드 컴포넌트에는 `SmartLifecycle` 쪽이 더 잘 맞는다.

---

# Bean 생명주기를 잘 활용했을 때 장점

## 초기화 로직을 한 곳에 모을 수 있다

예를 들어 캐시 워밍업, 필수 설정값 검증, 외부 리소스 연결 같은 걸  
객체가 준비되는 시점에 한 번에 처리할 수 있다.

```java
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

@Component
public class ProductCache {

    @PostConstruct
    public void load() {
        System.out.println("애플리케이션 시작 시 캐시 적재");
    }
}
```

이런 구조는 “이 Bean이 사용 가능해지기 전에 꼭 해야 하는 일”을 명확하게 표현할 수 있다는 장점이 있다.

---

## 종료 시 자원 정리가 쉬워진다

`@PreDestroy`나 `destroyMethod`를 잘 써두면  
컨테이너 종료 시 자원 해제를 일관되게 처리할 수 있다.

```java
import jakarta.annotation.PreDestroy;
import org.springframework.stereotype.Component;

@Component
public class FileManager {

    @PreDestroy
    public void close() {
        System.out.println("파일 리소스 정리");
    }
}
```

특히 DB 풀, 소켓, 스레드 풀처럼 “열었으면 닫아야 하는 자원”에 강력하다.

---

## fail-fast에 도움이 된다

스프링은 기본적으로 singleton Bean을 시작 시점에 미리 만들기 때문에,  
구성 오류나 환경 문제를 애플리케이션 시작 단계에서 빨리 발견할 수 있다.

예를 들어 잘못된 설정값이 있으면:

```java
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

@Component
public class ApiClient {

    private final String host = "";

    @PostConstruct
    public void validate() {
        if (host == null || host.isBlank()) {
            throw new IllegalStateException("host 설정은 필수입니다.");
        }
    }
}
```

애플리케이션이 올라갈 때 바로 터지므로,  
나중에 요청이 들어와서야 발견하는 것보다 훨씬 낫다.

---

## 스프링 인프라와 자연스럽게 통합된다

BeanPostProcessor, AOP, ApplicationContext, SmartLifecycle 같은 기능들과 자연스럽게 이어지기 때문에  
단순 객체보다 훨씬 강력한 관리가 가능하다.

즉, 스프링이 단순한 객체 저장소가 아니라  
“객체의 생애 전반을 관리하는 컨테이너”라는 걸 제대로 활용할 수 있게 된다.

---

# 단점과 주의점

장점이 많지만, 그렇다고 무조건 남용하면 좋은 건 아니다.

## 초기화 메서드에 무거운 로직을 넣으면 시작 속도가 느려진다

예를 들어 `@PostConstruct`에서 외부 API 수십 번 호출하고, 파일 읽고, 캐시 다 적재하고, 스레드까지 띄우면  
애플리케이션 시작 시간이 길어진다.

초기화 로직은 꼭 필요한 최소한의 준비 작업 위주로 두는 게 좋다.

---

## 숨은 부작용이 생기기 쉽다

생성자나 `@PostConstruct` 안에서 너무 많은 일을 하면  
Bean을 하나 주입받는 것만으로도 내부에서 예상치 못한 동작이 일어날 수 있다.

예를 들어:

- 외부 서버에 연결한다
- 테이블을 조회한다
- 파일을 만든다
- 다른 Bean들을 광범위하게 호출한다

이런 작업이 숨어 있으면 테스트도 까다로워지고 디버깅도 어려워진다.

---

## 프록시 기반 기능과 섞일 때 주의해야 한다

`@PostConstruct` 안에서 트랜잭션, AOP, 자기 자신 프록시 호출 같은 동작에 기대는 코드는 조심해야 한다.

즉, 이런 코드는 주의가 필요하다.

```java
@PostConstruct
public void init() {
    // 여기서 @Transactional 효과를 기대하는 코드는 주의
}
```

초기화는 “Bean이 준비되는 시점”이지,  
항상 “프록시 기반 부가기능까지 완벽하게 보장되는 시점”이라고 생각하면 안 된다.

---

## prototype Bean은 소멸을 자동 관리하지 않는다

이건 진짜 많이 놓치는 포인트다.  
prototype Bean은 destroy callback이 자동 호출되지 않는다.

그래서 prototype Bean이 비싼 리소스를 들고 있다면 정리를 직접 책임져야 한다.

---

## lazy initialization은 문제 발견을 늦출 수 있다

lazy initialization은 startup 최적화에는 도움이 될 수 있지만,  
대신 Bean 생성과 오류 발견이 뒤로 밀린다.

즉, “시작은 빠른데 운영 중 첫 요청에서 터지는” 상황이 생길 수 있다.

---

## Spring 인터페이스에 직접 결합될 수 있다

`InitializingBean`, `DisposableBean` 같은 인터페이스는 동작은 분명하지만,  
Spring API에 직접 의존하게 된다.

그래서 보통은 `@PostConstruct`, `@PreDestroy`나  
POJO 스타일의 init/destroy method를 더 선호하는 편이다.

---

# 정리

Spring Bean 생명주기는 그냥 “객체 생성”만 의미하는 게 아니다.

정확히는 이 흐름이다.

1. Bean 정의 등록
2. 객체 생성
3. 의존성 주입
4. Aware 콜백
5. BeanPostProcessor before init
6. 초기화 콜백
7. BeanPostProcessor after init
8. 사용
9. 종료 시 소멸 콜백

그리고 초기화/소멸 메커니즘을 같이 쓰면 순서는 다음과 같다.

- 초기화: `@PostConstruct` → `afterPropertiesSet()` → custom init method
- 소멸: `@PreDestroy` → `destroy()` → custom destroy method

내가 이걸 공부하면서 느낀 핵심은 이거였다.

> **스프링은 단순히 객체를 보관하는 게 아니라, 객체의 생애 전체를 관리하는 컨테이너다.**

그래서 Bean 생명주기를 이해하면  
IoC, DI, AOP, 프록시, scope, lazy initialization 같은 개념들이 전부 자연스럽게 연결된다.

---

## 한 줄 요약

> **Spring Bean 생명주기는 "생성 → 주입 → 초기화 → 사용 → 소멸"의 흐름이며, 이를 잘 이해하면 스프링이 객체를 어떻게 관리하는지 훨씬 선명하게 보인다.**
