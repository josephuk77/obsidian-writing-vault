---
title: "[Spring] Spring Bean 생명주기(쉬운버전)"
created: "2026-04-09"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Spring-Spring-Bean-생명주기쉬운버전"
---

# [Spring] Spring Bean 생명주기(쉬운버전)

스프링을 공부하다 보면 `Bean`, `IoC`, `DI`는 많이 보는데, 정작 **Bean이 생성된 뒤 어떤 순서로 초기화되고, 언제 소멸되는지**는 흐릿하게 알고 넘어가는 경우가 많다.

나도 처음에는 그냥 `@Component` 붙이면 객체가 만들어지고, `@Autowired`로 주입되고, 끝이라고 생각했다.  
그런데 조금만 깊게 들어가면 스프링은 객체를 단순히 만들기만 하는 게 아니라, **생성 → 의존성 주입 → 초기화 → 사용 → 소멸**까지 꽤 정교하게 관리한다.

이번 글에서는 Spring Bean 생명주기를 **회사에 신입사원이 입사하는 과정**에 비유해서 최대한 쉽게 정리해보려고 한다.  
복잡한 내부 구조를 전부 외우는 것보다, **전체 흐름을 자연스럽게 이해하는 것**에 집중해보자.

---

## Bean 생명주기란?

스프링에서 Bean은 **스프링 컨테이너가 생성하고 관리하는 객체**다.
그냥 `new`로 만든 객체와 다르게, 스프링이 객체를 만들고, 필요한 의존성을 넣어주고, 초기화하고, 종료될 때 정리까지 관리한다.

쉽게 말하면 Bean 생명주기는 이 뜻이다.

> **Bean이 언제 만들어지고, 언제 준비되고, 언제 사용되고, 언제 정리되는가**

이 흐름을 이해하면 다음 같은 것들이 훨씬 잘 보인다.

- `@PostConstruct`는 왜 필요한지
- `@PreDestroy`는 언제 호출되는지
- 왜 생성자 호출이 끝이 아닌지
- 왜 스프링이 객체를 그냥 `new`로만 다루지 않는지

---

## 먼저 아주 쉽게 보면

Bean 생명주기를 한 줄로 줄이면 이거다.

> **등록 → 생성 → 주입 → 초기화 → 사용 → 종료 시 정리**

그런데 이걸 글자로만 보면 잘 안 와닿을 수 있다.
그래서 회사에 신입사원이 들어오는 과정으로 바꿔서 보면 훨씬 쉽다.

---

## 회사원 비유로 이해하는 Bean 생명주기

스프링 Bean을 **회사에 입사한 신입사원**이라고 생각해보자.

### Bean 정의 등록 = 채용 명단에 올리기

스프링은 먼저 “어떤 객체를 관리할지”부터 알아야 한다.
이게 Bean 정의 등록이다.

예를 들어:

- `@Component`
- `@Service`
- `@Repository`
- `@Controller`
- `@Configuration` + `@Bean`

이 단계는 아직 객체가 만들어진 상태가 아니다.
그냥 스프링이 이렇게 생각하는 단계다.

> “이 클래스는 나중에 내가 관리할 거야.”

회사로 비유하면,
아직 입사한 건 아니고 **채용 대상 명단에 올려둔 상태**다.

---

### Bean 인스턴스 생성 = 신입사원이 실제로 입사함

그다음 스프링은 실제 객체를 만든다.

```java
@Component
public class OrderService {
    public OrderService() {
        System.out.println("OrderService 생성자 호출");
    }
}
```

이 시점에는 생성자가 호출된다.

여기서 중요한 건,
**생성자가 호출됐다고 해서 이 Bean이 바로 다 준비된 건 아니라는 점**이다.

회사로 비유하면,
신입사원이 회사 건물에 들어오고 자리에 앉은 상태다.
그런데 아직 노트북도 없고, 사원증도 없고, 업무 설명도 못 들었다.

즉,

- 객체는 생겼다
- 하지만 아직 바로 일할 수는 없다

이렇게 보면 된다.

---

### 의존성 주입 = 노트북, 계정, 사원증 지급

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

`OrderService`가 제대로 동작하려면 `PaymentService`가 필요하다.
그래서 스프링이 `PaymentService`를 넣어준다.

이걸 의존성 주입이라고 한다.

회사 비유로 보면,
신입사원에게 일을 할 수 있도록 필요한 걸 지급하는 단계다.

예를 들면:

- 노트북 지급
- 사내 계정 발급
- 메신저 권한 부여
- 사원증 발급

즉,

> **일하는 데 필요한 준비물을 연결해주는 단계**

라고 생각하면 된다.

---

### Aware 콜백 = 회사 정보 알려주기

이 단계는 실무에서 자주 쓰는 건 아니지만, 흐름상 어디쯤인지 알아두면 좋다.

스프링은 필요하면 Bean에게 자기 정보를 알려줄 수 있다.
예를 들면 이런 것들이다.

- Bean 이름
- BeanFactory
- ApplicationContext

대표 인터페이스는 다음과 같다.

- `BeanNameAware`
- `BeanFactoryAware`
- `ApplicationContextAware`

예시:

```java
import org.springframework.beans.factory.BeanNameAware;

public class MyBean implements BeanNameAware {

    @Override
    public void setBeanName(String name) {
        System.out.println("Bean 이름 = " + name);
    }
}
```

회사 비유로 보면,
입사한 직원에게 이런 정보를 알려주는 느낌이다.

- “너 사번은 1024번이야.”
- “너 부서는 주문팀이야.”
- “우리 회사 시스템은 이렇게 생겼어.”

즉,
**업무 도구를 주는 단계라기보다, 회사에 대한 정보를 알려주는 단계**라고 이해하면 된다.

다만 신입 기준에서는 여기까지 깊게 외울 필요는 없다.

> “의존성 주입 뒤에, 스프링이 필요하면 Bean에게 자기 정보도 알려줄 수 있구나.”

이 정도만 알면 충분하다.

---

### BeanPostProcessor before initialization = 교육 전에 관리자 체크

그다음 단계에서 `BeanPostProcessor`가 개입할 수 있다.
이건 처음엔 어렵게 느껴지는데, 아주 쉽게 말하면 이거다.

> **스프링이 Bean을 그냥 바로 쓰지 않고, 중간에 한 번 더 손보는 단계**

회사 비유로 보면,
신입사원이 배치되기 전에 관리자가 이런 걸 확인하는 느낌이다.

- 노트북 정상 작동하는지
- 계정이 잘 열리는지
- 필요한 기본 설정이 끝났는지

즉,
**본격적으로 쓰기 전에 점검하거나 가공하는 단계**다.

스프링 내부에서는 이 지점에서 여러 기능이 처리된다.
예를 들면:

- `@PostConstruct` 처리
- AOP 프록시 생성
- 각종 어노테이션 기반 후처리

신입 기준으로는 이렇게 기억하면 충분하다.

> **BeanPostProcessor는 스프링이 Bean을 더 똑똑하게 다루기 위해 중간에 개입하는 장치다.**

---

## 초기화 콜백은 진짜 무슨 역할일까?

여기서부터가 진짜 중요하다.
많은 사람들이 생성자 호출이나 의존성 주입까지 끝나면 Bean 준비가 다 끝났다고 생각하는데,
사실 스프링은 그 뒤에 **초기화 단계**를 한 번 더 둔다.

왜냐하면 의존성이 연결됐다고 해서,
그 Bean이 **즉시 사용 가능한 상태**라고 보장할 수는 없기 때문이다.

예를 들면 이런 작업이 남아 있을 수 있다.

- 설정값 검증
- 캐시 미리 로딩
- 외부 서버 연결 준비
- 시작 로그 출력

회사 비유로 보면,
노트북이랑 계정을 받았다고 바로 실무 투입되는 게 아니라,
마지막으로 업무 환경을 세팅하고 교육받는 단계가 한 번 더 있는 거다.

즉,

- 생성 = 사람 들어옴
- 주입 = 준비물 받음
- 초기화 = 일하기 직전 최종 준비

이렇게 보면 된다.

---

## 초기화 콜백 방식

### `@PostConstruct`

가장 많이 쓰고, 가장 직관적이다.

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

이건 이런 뜻이다.

> “의존성 주입 끝났으니까 이제 마지막 준비를 한 번 하자.”

회사 비유로 보면,
업무 시작 전에 필요한 자료를 내려받고 환경을 세팅하는 단계다.

예를 들면:

- 공용 문서 폴더 연결
- 필수 프로그램 설치 확인
- 업무용 캐시 미리 적재

신입 기준에서는 초기화 콜백 하면 일단 `@PostConstruct`를 먼저 떠올리면 된다.

---

### `InitializingBean.afterPropertiesSet()`

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

역할은 `@PostConstruct`와 거의 비슷하다.
다만 Spring 인터페이스를 직접 구현해야 해서,
요즘은 `@PostConstruct`보다 덜 선호되는 편이다.

쉽게 말하면:

> **초기화 작업을 하는 또 다른 방식**

정도로 이해하면 된다.

---

### custom `initMethod`

외부 라이브러리 객체처럼,
내가 코드를 직접 수정할 수 없는 경우에는 이런 방식도 쓸 수 있다.

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

즉,
클래스에 직접 `@PostConstruct`를 붙일 수 없을 때,
스프링 설정에서 “이 메서드를 초기화 메서드로 써라”라고 지정하는 방식이다.

---

### BeanPostProcessor after initialization = 최종 포장 또는 역할 부여

초기화가 끝난 뒤에도 `BeanPostProcessor`가 한 번 더 개입할 수 있다.

이 단계에서는 Bean이 최종적으로 가공될 수 있다.
대표적으로 프록시 객체가 만들어질 수도 있다.

회사 비유로 보면,
교육까지 끝난 신입사원에게 마지막 역할을 부여하는 느낌이다.

예를 들면:

- 이 직원은 기록을 남겨야 하니까 로그 기능 붙이기
- 이 직원은 보안 정책을 더 강하게 적용하기
- 이 직원은 트랜잭션 규칙을 적용한 프록시로 감싸기

즉,
원래 객체를 그대로 쓰는 게 아니라,
**조금 더 기능이 붙은 형태로 최종 사용 준비를 마치는 단계**라고 보면 된다.

이 부분이 중요한 이유는,
`@PostConstruct` 같은 초기화 메서드는 보통 **프록시가 완전히 적용되기 전 raw bean 기준**으로 실행될 수 있기 때문이다.

그래서 이런 건 주의해야 한다.

```java
@PostConstruct
public void init() {
    // 여기서 @Transactional 효과를 기대하는 코드는 주의
}
```

신입 기준으로는 이 문장만 기억하면 충분하다.

> **초기화는 프록시 적용 전 단계일 수 있으니, `@PostConstruct` 안에서 AOP나 트랜잭션을 당연하게 기대하면 안 된다.**

---

## 실제 코드로 흐름 보면 더 쉽다

아래 코드는 순서를 보여주기 위한 예시다.

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

예상 흐름은 이렇다.

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

즉,
초기화는

- `@PostConstruct`
- `afterPropertiesSet()`
- custom initMethod

순서로 진행되고,

소멸은

- `@PreDestroy`
- `destroy()`
- custom destroyMethod

순서로 진행된다.

다만 실무에서는 이걸 한 Bean에 전부 섞어 쓰기보다,
보통 하나의 방식만 선택해서 쓴다.

---

## 실무에서는 주로 어떻게 쓰나?

실무에서는 보통 아래 두 가지를 많이 본다.

### `@PostConstruct` / `@PreDestroy`

가장 직관적이고 많이 쓰는 방식이다.

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

### `@Bean(initMethod, destroyMethod)`

외부 라이브러리 객체일 때 많이 쓴다.

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

---

## 소멸 단계도 생각보다 중요하다

Bean은 생성하고 초기화하는 것만 중요한 게 아니라,
**끝날 때 제대로 정리하는 것**도 중요하다.

예를 들면 이런 자원들이 있다.

- DB 연결 풀
- 소켓 연결
- 스레드 풀
- 파일 핸들
- 외부 API 클라이언트

이런 것들은 열어두기만 하고 닫지 않으면 문제가 생긴다.
그래서 종료 시점에 정리 작업이 필요하다.

회사 비유로 보면,
퇴사하는 직원이 아래 작업을 하는 것과 비슷하다.

- 노트북 반납
- 계정 회수
- 권한 제거
- 사용하던 자료 정리

이 역할을 하는 게 `@PreDestroy`, `destroy()`, `destroyMethod` 같은 소멸 콜백이다.

---

## 여기까지에서 신입 기준으로 꼭 기억할 것

처음부터 내부 동작을 전부 외울 필요는 없다.
신입 기준에서는 아래만 정확히 기억해도 충분하다.

- Bean은 **스프링 컨테이너가 관리하는 객체**다.
- 생성자 호출이 끝이라고 해서 Bean 준비가 끝난 건 아니다.
- 객체 생성 뒤에는 **의존성 주입**이 일어난다.
- 그다음에 **초기화 단계**가 한 번 더 있다.
- 초기화에는 보통 `@PostConstruct`를 많이 쓴다.
- 종료 시에는 `@PreDestroy`로 정리할 수 있다.
- `Aware`, `BeanPostProcessor`는 흐름상 어디 있는지만 알고 있으면 충분하다.

한 줄로 줄이면 이거다.

> **등록 → 생성 → 주입 → 초기화 → 사용 → 종료 시 정리**

---

## 정리

Spring Bean 생명주기는 단순히 객체를 만드는 과정이 아니다.
정확히는,

- 어떤 객체를 관리할지 등록하고
- 실제 객체를 만들고
- 필요한 의존성을 연결하고
- 초기화로 마지막 준비를 마친 뒤
- 사용하다가
- 종료 시 정리까지 하는 과정이다.

회사원 비유로 다시 말하면 이렇다.

> **채용 명단 등록 → 입사 → 장비 지급 → 회사 정보 전달 → 점검 → 교육 및 세팅 → 업무 시작 → 퇴사 정리**

이 흐름이 머릿속에 들어오면,
왜 `@PostConstruct`가 필요하고,
왜 `@PreDestroy`가 존재하는지,
왜 스프링이 객체를 그냥 `new`로만 다루지 않는지가 훨씬 자연스럽게 이해된다.

---

## 한 줄 요약

> **Spring Bean 생명주기는 객체를 단순히 만드는 게 아니라, 준비하고, 사용하고, 끝날 때 정리하는 전체 과정을 스프링이 관리하는 구조다.**

## ✅ 🔥 한 줄 핵심 (짧은 답변)

>“Spring Bean은 생성 → 의존성 주입 → 초기화 → 사용 → 소멸의 생명주기를 가지며,
초기화와 소멸 시점에 각각 @PostConstruct와 @PreDestroy를 사용할 수 있습니다.”

## ✅ 🎯 실전 면접용 (30초 답변)

>“Spring Bean의 생명주기는 먼저 Bean이 생성되고, 이후 의존성 주입이 이루어집니다.
그 다음 초기화 단계에서 @PostConstruct나 InitializingBean이 실행되고,
이후 애플리케이션에서 사용되다가 컨테이너가 종료될 때 @PreDestroy나 destroy 메서드가 호출되며 소멸됩니다.”

## ✅ 💪 제대로 아는 느낌 (깊이 있는 답변)


>“Spring Bean의 생명주기는 먼저 BeanDefinition이 등록된 후 객체가 생성되고,
이후 의존성 주입이 이루어집니다.
그 다음 Aware 인터페이스 콜백이 실행되고, BeanPostProcessor의 before 단계가 적용됩니다.
이후 @PostConstruct나 InitializingBean을 통해 초기화가 이루어지고,
다시 BeanPostProcessor after 단계가 적용된 뒤 Bean이 실제로 사용됩니다.
마지막으로 컨테이너 종료 시 @PreDestroy나 DisposableBean을 통해 소멸됩니다.”
