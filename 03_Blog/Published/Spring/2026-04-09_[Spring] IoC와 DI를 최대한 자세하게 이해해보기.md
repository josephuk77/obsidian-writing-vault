---
title: "[Spring] IoC와 DI를 최대한 자세하게 이해해보기"
created: "2026-04-09"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Spring-IoC와-DI를-최대한-자세하게-이해해보기"
---

# [Spring] IoC와 DI를 최대한 자세하게 이해해보기

> 왜 필요한지, 안 쓰면 뭐가 문제인지, 실제 코드로 정리

스프링을 공부하다 보면 **IoC**, **DI**라는 말을 정말 많이 보게 된다.  
나도 처음에는 둘이 너무 비슷해 보여서 헷갈렸고, 그냥 `@Autowired` 쓰는 정도로만 이해했었다.

그런데 실제로 코드를 비교해보면 왜 스프링이 IoC와 DI를 그렇게 중요하게 다루는지 바로 이해된다.  
이번 글에서는 **IoC와 DI가 정확히 무엇인지**, **왜 필요한지**, **안 쓰면 어떤 문제가 생기는지**, **실제 코드에서는 어떻게 적용되는지**까지 한 번에 정리해보려고 한다.

---

## 목차

1. [IoC와 DI를 왜 배우는가](#ioc와-di를-왜-배우는가)
2. [IoC란 무엇인가](#ioc란-무엇인가)
3. [DI란 무엇인가](#di란-무엇인가)
4. [IoC와 DI의 관계](#ioc와-di의-관계)
5. [IoC/DI를 쓰지 않았을 때의 코드](#iocdi를-쓰지-않았을-때의-코드)
6. [안 썼을 때 생기는 문제점](#안-썼을-때-생기는-문제점)
7. [IoC/DI를 적용한 코드](#iocdi를-적용한-코드)
8. [적용했을 때 좋아지는 점](#적용했을-때-좋아지는-점)
9. [Spring에서는 실제로 어떻게 동작하는가](#spring에서는-실제로-어떻게-동작하는가)
10. [여러 구현체가 있을 때는 어떻게 선택할까](#여러-구현체가-있을-때는-어떻게-선택할까)
11. [생성자 주입을 권장하는 이유](#생성자-주입을-권장하는-이유)
12. [정리](#정리)

---

# IoC와 DI를 왜 배우는가

애플리케이션을 만들다 보면 어떤 클래스는 혼자 동작하지 못한다.  
대부분 다른 객체의 도움을 받아야 한다.

예를 들어 주문 서비스를 생각해보면:

- 주문 서비스는 결제 서비스가 필요하고
- 결제 서비스는 할인 정책이 필요할 수도 있고
- 또 로그를 남기는 객체도 필요할 수 있다

즉, 객체는 서로 의존하면서 동작한다.

문제는 이 의존 관계를 **어떻게 맺느냐**에 따라 코드 품질이 크게 달라진다는 점이다.

- 직접 객체를 만들어서 쓰면 빠르게는 짤 수 있다
- 하지만 변경이 생기면 수정 범위가 커진다
- 테스트도 어려워진다
- 코드가 점점 단단하게 엉켜간다

그래서 등장하는 개념이 바로 **IoC**와 **DI**다.

---

# IoC란 무엇인가

## IoC(Inversion of Control) = 제어의 역전

말 그대로 **제어권이 뒤집힌 것**이다.

원래는 개발자가 직접 객체를 만들고, 연결하고, 필요한 시점에 호출한다.

예를 들면 이런 코드다.
```java
class OrderService {
    private CardPaymentService paymentService = new CardPaymentService();
}
```
이 경우 `OrderService`가 하는 일은 두 가지다.

1. 주문을 처리한다
2. 어떤 결제 객체를 쓸지도 직접 결정한다

즉, 객체 생성과 제어의 중심이 `OrderService` 안에 있다.

그런데 IoC를 적용하면 이 제어권이 바깥으로 나간다.
```java
PaymentService paymentService = new CardPaymentService();
OrderService orderService = new OrderService(paymentService);
```
이제 `OrderService`는 더 이상 결제 객체를 직접 만들지 않는다.  
누군가 외부에서 만들어서 넣어준다.

즉, **객체 생성과 연결의 제어권이 클래스 자신에게 있지 않고 외부로 넘어간 것**이다.  
이걸 **제어의 역전(IoC)** 이라고 한다.

---

## 왜 이름이 "역전"일까?

원래는 객체가 자기에게 필요한 객체를 직접 찾고 만들었다.

- 내가 필요한 거 내가 만든다
- 내가 어떤 구현체를 쓸지 내가 정한다

그런데 IoC에서는 반대로 된다.

- 내가 필요한 객체를 직접 만들지 않는다
- 외부가 만들어서 넣어준다
- 나는 받은 객체를 사용만 한다

즉, **주도권이 바뀐 것**이다.

---

## Spring에서 IoC는 누가 담당할까?

스프링에서는 **IoC 컨테이너**가 이 역할을 담당한다.  
대표적으로 `ApplicationContext`가 있다.

IoC 컨테이너는 다음과 같은 일을 한다.

- 객체(Bean)를 생성한다
- 객체 간의 의존 관계를 연결한다
- 생명주기를 관리한다
- 필요한 시점에 꺼내 쓸 수 있게 보관한다

즉, 스프링에서는 객체 관리를 개발자가 일일이 하지 않고  
**스프링 컨테이너가 대신 관리**해준다.

---

# DI란 무엇인가

## DI(Dependency Injection) = 의존성 주입

의존성 주입은 말 그대로 **필요한 의존 객체를 외부에서 넣어주는 것**이다.

여기서 의존성(Dependency)이란,  
한 객체가 동작하기 위해 다른 객체가 필요한 관계를 말한다.

예를 들어:
```java
class OrderService {
    private PaymentService paymentService;
}
```
`OrderService`는 결제를 하려면 `PaymentService`가 필요하다.  
즉, `OrderService`는 `PaymentService`에 의존한다.

---

## 의존성을 "주입"한다는 건 무슨 뜻일까?

직접 만들지 않고 밖에서 넣어준다는 뜻이다.

### 직접 생성하는 방식
```java
class OrderService {
    private PaymentService paymentService = new CardPaymentService();
}
```
### 주입받는 방식
```java
class OrderService {
    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```
두 코드의 차이는 엄청 크다.

첫 번째는 `OrderService`가 스스로 의존 객체를 생성한다.  
두 번째는 `OrderService`가 필요한 의존성을 외부로부터 받기만 한다.

이게 바로 DI다.

---

# IoC와 DI의 관계

이 둘은 비슷하지만 완전히 같은 말은 아니다.

## 정리하면

- **IoC**: 객체 생성과 제어의 주도권이 외부로 넘어간 것
- **DI**: 그 IoC를 실현하는 대표적인 방법

즉, **DI는 IoC를 구현하는 방식 중 하나**라고 이해하면 된다.

---

## 비유로 이해해보기

### IoC
"내가 필요한 부품을 내가 직접 사서 조립하는 게 아니라,  
외부에서 완성된 부품을 전달받는 구조"

### DI
"그 전달받는 구체적인 방법"

---

# IoC/DI를 쓰지 않았을 때의 코드

이제 실제 코드로 보자.  
예시는 주문 서비스와 결제 서비스다.

## 1. IoC/DI를 사용하지 않은 코드
```java
class CardPaymentService {
    public void pay(int amount) {
        System.out.println("카드로 " + amount + "원 결제");
    }
}

class OrderService {
    private CardPaymentService paymentService;

    public OrderService() {
        this.paymentService = new CardPaymentService();
    }

    public void order(int amount) {
        System.out.println("주문이 생성되었습니다.");
        paymentService.pay(amount);
    }
}

public class Main {
    public static void main(String[] args) {
        OrderService orderService = new OrderService();
        orderService.order(10000);
    }
}
```
겉으로 보면 큰 문제 없어 보인다.  
실제로 간단한 프로그램에서는 이렇게 짜도 동작은 잘 한다.

하지만 구조적으로는 여러 문제가 숨어 있다.

---

# 안 썼을 때 생기는 문제점

## 1. 구체 클래스에 강하게 결합된다

`OrderService`는 `CardPaymentService`를 직접 생성하고 있다.
```java
this.paymentService = new CardPaymentService();
```
이 말은 곧 `OrderService`가 "결제 기능"에 의존하는 게 아니라  
**"카드 결제 구현체"** 에 직접 의존하고 있다는 뜻이다.

즉, **추상에 의존하는 게 아니라 구체 구현에 의존**하고 있다.

이걸 흔히 **강한 결합(Tight Coupling)** 이라고 한다.

---

## 2. 결제 방식이 바뀌면 OrderService도 수정해야 한다

예를 들어 카드 결제에서 카카오페이 결제로 바꾸고 싶다고 해보자.
```java
class KakaoPaymentService {
    public void pay(int amount) {
        System.out.println("카카오페이로 " + amount + "원 결제");
    }
}
```
그러면 `OrderService`도 이렇게 바뀌어야 한다.
```java
class OrderService {
    private KakaoPaymentService paymentService;

    public OrderService() {
        this.paymentService = new KakaoPaymentService();
    }

    public void order(int amount) {
        System.out.println("주문이 생성되었습니다.");
        paymentService.pay(amount);
    }
}
```
문제는 결제 구현이 바뀌었을 뿐인데  
**주문 서비스 코드까지 수정해야 한다는 점**이다.

즉, 변경의 영향이 여기저기 퍼진다.

---

## 3. 새로운 결제 수단이 추가될수록 수정 포인트가 늘어난다

예를 들어 나중에 이런 요구사항이 들어올 수 있다.

- 카드 결제 추가
- 카카오페이 추가
- 토스페이 추가
- 네이버페이 추가

그런데 각 구현체를 서비스 내부에서 직접 생성하는 구조라면  
구현체가 늘어날수록 서비스 코드도 계속 바뀐다.

즉, 확장에 불리하다.

---

## 4. 테스트가 어렵다

단위 테스트에서는 실제 결제를 하지 않고  
가짜 객체(Fake, Mock)를 넣어서 테스트하는 경우가 많다.

그런데 지금 구조에서는 `OrderService`가 내부에서 직접 `new CardPaymentService()`를 해버린다.

즉, 테스트 코드에서 이런 식으로 끼워 넣기가 어렵다.
```java
OrderService orderService = new OrderService(fakePaymentService); // 불가능
```
왜냐하면 생성자에 받는 구조가 아니기 때문이다.

---

## 5. 객체 생성 책임과 비즈니스 책임이 섞인다

`OrderService`는 원래 주문 로직에 집중해야 한다.  
그런데 현재는 이런 책임까지 함께 갖고 있다.

- 어떤 결제 객체를 생성할지 결정
- 객체를 직접 생성
- 주문 로직 수행

즉, 역할이 섞였다.

이런 구조는 유지보수할수록 점점 복잡해진다.

---

## 6. 의존 관계가 숨겨진다

이 코드를 보면 `OrderService`가 결제 서비스에 의존한다는 걸  
겉으로는 바로 알기 어려울 수 있다.
```java
class OrderService {
    private CardPaymentService paymentService;

    public OrderService() {
        this.paymentService = new CardPaymentService();
    }
}
```
의존성이 생성자 파라미터로 드러나는 것이 아니라  
내부 구현 속에 숨어 있기 때문이다.

---

# IoC/DI를 적용한 코드

이제 구조를 바꿔보자.  
핵심은 다음 두 가지다.

1. **구체 클래스가 아니라 추상(인터페이스)에 의존하기**
2. **필요한 의존 객체를 외부에서 주입받기**

---

## 1. 인터페이스부터 만든다
```java
public interface PaymentService {
    void pay(int amount);
}
```
---

## 2. 구현체를 분리한다
```java
public class CardPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카드로 " + amount + "원 결제");
    }
}
```
```java
public class KakaoPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카카오페이로 " + amount + "원 결제");
    }
}
```
---

## 3. OrderService는 필요한 의존성을 생성자에서 받는다
```java
public class OrderService {
    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void order(int amount) {
        System.out.println("주문이 생성되었습니다.");
        paymentService.pay(amount);
    }
}
```
여기서 중요한 포인트는  
`OrderService`가 이제 `CardPaymentService`도 모르고, `KakaoPaymentService`도 모른다는 점이다.

오직 이것만 안다.
```java
private final PaymentService paymentService;
```
즉, **"결제 기능이 있는 객체"만 있으면 된다.**

---

## 4. 실제 객체 조립은 외부에서 한다
```java
public class Main {
    public static void main(String[] args) {
        PaymentService paymentService = new CardPaymentService();
        OrderService orderService = new OrderService(paymentService);

        orderService.order(10000);
    }
}
```
카카오페이로 바꾸고 싶다면?
```java
public class Main {
    public static void main(String[] args) {
        PaymentService paymentService = new KakaoPaymentService();
        OrderService orderService = new OrderService(paymentService);

        orderService.order(10000);
    }
}
```
놀랍게도 **OrderService는 한 줄도 수정할 필요가 없다.**

이게 바로 IoC와 DI가 주는 가장 큰 힘이다.

---

# 적용했을 때 좋아지는 점

## 1. 결합도가 낮아진다

이전에는 `OrderService`가 `CardPaymentService`라는 구체 클래스에 묶여 있었다.

지금은 `PaymentService`라는 추상에 의존한다.
```java
private final PaymentService paymentService;
```
즉, 구현체가 바뀌어도 서비스의 핵심 로직은 바뀌지 않는다.

이걸 **느슨한 결합(Loose Coupling)** 이라고 한다.

---

## 2. 구현체 교체가 쉬워진다

이전 구조에서는 결제 방식을 바꾸기 위해 `OrderService` 코드를 수정해야 했다.

하지만 지금은 객체를 조립하는 외부 코드만 바꾸면 된다.
```java
PaymentService paymentService = new CardPaymentService();
```
↓
```java
PaymentService paymentService = new KakaoPaymentService();
```
즉, 변경이 훨씬 쉽다.

---

## 3. 테스트가 쉬워진다

이건 실무에서 정말 크다.

예를 들어 테스트용 가짜 결제 서비스를 하나 만든다고 해보자.
```java
public class FakePaymentService implements PaymentService {
    public int calledAmount = 0;

    @Override
    public void pay(int amount) {
        calledAmount = amount;
    }
}
```
테스트 코드는 이렇게 쓸 수 있다.
```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class OrderServiceTest {

    @Test
    void 주문을_하면_결제서비스가_호출된다() {
        FakePaymentService fakePaymentService = new FakePaymentService();
        OrderService orderService = new OrderService(fakePaymentService);

        orderService.order(10000);

        assertEquals(10000, fakePaymentService.calledAmount);
    }
}
```
만약 `OrderService`가 내부에서 직접 `new CardPaymentService()`를 했다면  
이런 테스트는 훨씬 어려워진다.

---

## 4. 책임 분리가 명확해진다

이제 각 객체의 역할이 분명해진다.

- `OrderService`: 주문 처리
- `PaymentService`: 결제 기능 제공
- 외부 조립 코드: 어떤 구현체를 연결할지 결정

역할이 분리되면 코드가 읽기 쉬워지고 유지보수가 쉬워진다.

---

## 5. 확장에 유리하다

새로운 결제 수단이 필요하다고 해보자.
```java
public class TossPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("토스페이로 " + amount + "원 결제");
    }
}
```
기존 `OrderService`는 수정할 필요가 없다.  
그냥 새 구현체를 만들어 주입만 하면 된다.

즉, 확장이 쉽다.

---

## 6. 코드 재사용성이 좋아진다

`OrderService`는 특정 결제 방식에 묶여 있지 않으므로  
다양한 구현체와 함께 재사용될 수 있다.

예를 들어 운영 환경에서는 `CardPaymentService`,  
테스트 환경에서는 `FakePaymentService`,  
이벤트 환경에서는 `DiscountPaymentService` 같은 식으로 바꿔 끼울 수 있다.

---

# Spring에서는 실제로 어떻게 동작하는가

위 예시는 순수 자바 코드였고,  
스프링에서는 이 "외부 조립자" 역할을 **스프링 컨테이너**가 대신해준다.

---

## Spring 코드 예시

### PaymentService 인터페이스
```java
public interface PaymentService {
    void pay(int amount);
}
```
### 구현체
```java
import org.springframework.stereotype.Component;

@Component
public class CardPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카드로 " + amount + "원 결제");
    }
}
```
### OrderService
```java
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void order(int amount) {
        System.out.println("주문이 생성되었습니다.");
        paymentService.pay(amount);
    }
}
```
---

## 여기서 실제로 무슨 일이 일어날까?

스프링은 애플리케이션이 시작될 때 다음 순서로 동작한다.

### 1. 컴포넌트 스캔
`@Component`, `@Service`, `@Repository`, `@Controller` 같은 어노테이션이 붙은 클래스를 찾는다.

### 2. Bean 등록
찾아낸 클래스를 스프링 컨테이너가 관리할 객체(Bean)로 등록한다.

### 3. 의존성 분석
`OrderService` 생성자를 보고 `PaymentService` 타입의 Bean이 필요하다는 걸 확인한다.

### 4. 의존성 주입
스프링 컨테이너가 `PaymentService` 구현체를 찾아 `OrderService` 생성자에 넣어준다.

### 5. 생명주기 관리
생성 이후에도 Bean의 생명주기와 상태를 스프링이 관리한다.

즉, 개발자가 직접 이렇게 하지 않아도 된다.
```java
PaymentService paymentService = new CardPaymentService();
OrderService orderService = new OrderService(paymentService);
```
이걸 스프링이 대신 해주는 것이다.

---

# 여러 구현체가 있을 때는 어떻게 선택할까

현실에서는 `PaymentService` 구현체가 하나만 있는 경우보다  
여러 개 있는 경우가 더 많다.

예를 들어:

- `CardPaymentService`
- `KakaoPaymentService`
- `TossPaymentService`

이 상황에서 `OrderService`가 `PaymentService`를 주입받으려고 하면  
스프링은 어떤 구현체를 넣어야 할지 모르게 된다.

---

## 1. @Primary 사용
```java
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
public class CardPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카드로 " + amount + "원 결제");
    }
}
```
`@Primary`가 붙은 Bean이 기본 선택 대상이 된다.

---

## 2. @Qualifier 사용
```java
import org.springframework.stereotype.Component;

@Component("cardPaymentService")
public class CardPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카드로 " + amount + "원 결제");
    }
}
```
```java
import org.springframework.stereotype.Component;

@Component("kakaoPaymentService")
public class KakaoPaymentService implements PaymentService {
    @Override
    public void pay(int amount) {
        System.out.println("카카오페이로 " + amount + "원 결제");
    }
}
```
```java
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final PaymentService paymentService;

    public OrderService(@Qualifier("kakaoPaymentService") PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void order(int amount) {
        paymentService.pay(amount);
    }
}
```
이렇게 하면 원하는 구현체를 명시적으로 선택할 수 있다.

---

# 생성자 주입을 권장하는 이유

DI에도 여러 방식이 있다.

- 생성자 주입
- setter 주입
- 필드 주입

그중에서 가장 권장되는 방식은 **생성자 주입**이다.

---

## 1. 의존성이 명확하게 드러난다
```java
public OrderService(PaymentService paymentService) {
    this.paymentService = paymentService;
}
```
이 생성자만 봐도 `OrderService`가 `PaymentService`에 의존한다는 걸 바로 알 수 있다.

---

## 2. 객체를 불변으로 만들 수 있다
```java
private final PaymentService paymentService;
```
생성 시점에 한 번 주입받고 이후에는 변경하지 않도록 만들 수 있다.  
이건 안정적인 설계에 큰 도움이 된다.

---

## 3. 테스트가 쉽다

생성자에 원하는 구현체를 넣기만 하면 되기 때문에  
테스트용 객체 주입이 매우 쉽다.

---

## 4. 필드 주입보다 숨겨진 의존성이 적다

필드 주입은 코드가 짧아 보여도 의존성이 외부에 잘 드러나지 않는다.

### 필드 주입 예시
```java
@Service
public class OrderService {

    @Autowired
    private PaymentService paymentService;
}
```
이 방식은 간단해 보이지만:

- 테스트하기 불편하고
- final 사용이 어렵고
- 의존성이 생성자에 드러나지 않는다

그래서 일반적으로는 **생성자 주입**이 가장 권장된다.

---

# IoC/DI를 안 쓰는 구조와 쓰는 구조를 한 번에 비교

## IoC/DI를 안 쓴 구조
```java
class OrderService {
    private CardPaymentService paymentService = new CardPaymentService();

    public void order(int amount) {
        paymentService.pay(amount);
    }
}
```
### 문제
- 구체 클래스에 직접 의존
- 변경에 약함
- 테스트 어려움
- 객체 생성 책임과 비즈니스 책임이 섞임
- 확장 불리

---

## IoC/DI를 쓴 구조
```java
public interface PaymentService {
    void pay(int amount);
}

public class OrderService {
    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void order(int amount) {
        paymentService.pay(amount);
    }
}
```
### 장점
- 추상에 의존
- 구현 교체 쉬움
- 테스트 쉬움
- 역할 분리
- 유지보수 쉬움
- 확장 쉬움

---

# "주입하면 왜 결합이 느슨해질까?"를 한 문장으로 정리하면

이 부분이 핵심이다.

의존 객체를 직접 생성하면:
```java
new CardPaymentService()
```
이 순간 이미 특정 구현체에 묶인다.

반대로 주입받으면:
```java
public OrderService(PaymentService paymentService)
```
`OrderService`는 어떤 구현체가 들어오는지 모른다.  
그냥 `PaymentService`라는 기능만 바라본다.

즉, **구현이 아니라 추상에 의존하게 되므로 결합이 느슨해진다.**

---

# 한 번 더 정리: IoC와 DI의 핵심 차이

| 구분 | 의미 |
|---|---|
| IoC | 객체 생성과 제어권이 외부(스프링 컨테이너)로 넘어간 것 |
| DI | 필요한 의존 객체를 외부에서 주입받는 것 |
| 관계 | DI는 IoC를 구현하는 대표적인 방식 |

---

# 마무리

처음에는 IoC와 DI가 단순히 스프링 문법처럼 느껴질 수 있다.  
하지만 실제 코드를 비교해보면 이건 단순한 문법이 아니라 **설계 방식의 차이**라는 걸 알 수 있다.

IoC와 DI를 사용하지 않으면:

- 객체가 서로 강하게 결합되고
- 변경이 어려워지고
- 테스트가 힘들어지고
- 유지보수가 점점 어려워진다

반대로 IoC와 DI를 사용하면:

- 객체 생성 책임이 분리되고
- 추상에 의존하게 되고
- 구현체 교체가 쉬워지고
- 테스트가 쉬워지고
- 확장 가능한 구조를 만들 수 있다

결국 IoC와 DI의 진짜 목적은  
**"스프링스럽게 코드를 짜는 것"** 이 아니라

> **변경에 강하고, 테스트하기 쉽고, 유지보수하기 좋은 구조를 만드는 것**

이라고 생각하면 이해가 훨씬 잘 된다.

---

# 한 줄 요약

> **IoC는 제어권을 외부로 넘기는 것이고, DI는 그 제어를 실제 코드에서 의존성 주입으로 구현하는 방식이다.**

---
---

## 관련 글

- [[2023-12-18_Spring-개발환경 구축]]
- [[Spring]]
- [[Spring Boot]]
- [[IoC]]
- [[DI]]
- [[Velog]]
