---
title: "📘 TIL - LeetCode 232: Implement Queue using Stacks"
created: "2025-08-06"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/TIL-LeetCode-232-Implement-Queue-using-Stacks"
---

# 📘 TIL - LeetCode 232: Implement Queue using Stacks

## 🔍 문제 요약
- 스택(Stack)만 사용해서 큐(Queue)의 동작을 구현하는 문제.
- FIFO(First-In-First-Out) 구조의 큐를 만들어야 하며, 다음 메서드를 구현해야 함:
  - `push(x)`: 큐 뒤에 요소 x 삽입
  - `pop()`: 큐 앞에서 요소 제거 후 반환
  - `peek()`: 큐 앞에 있는 요소를 반환
  - `empty()`: 큐가 비어있는지 여부 확인

---

## ✨ 핵심 아이디어

- **두 개의 스택 사용 (`inStack`, `outStack`)**
  - `inStack`: push 연산용 (입력)
  - `outStack`: pop / peek 연산용 (출력)
- `pop` 또는 `peek` 시 `outStack`이 비어있으면 `inStack`의 모든 원소를 `outStack`으로 옮겨준다.
  - 이 과정에서 요소의 순서가 뒤집히며, FIFO 구현 가능

---

## 🧠 배운 점

- **스택 두 개로 큐의 FIFO를 시뮬레이션**할 수 있다는 점이 흥미로웠다.
- `shiftStacks()` 함수로 **필요할 때만 옮김으로써 시간 효율성**을 높일 수 있다.
- 각 연산이 **Amortized O(1)** 시간복잡도를 가지도록 설계되어 있다.

---

## ⏱️ 시간/공간 복잡도

| 연산      | 시간 복잡도        | 설명 |
|-----------|--------------------|------|
| push      | O(1)               | `inStack`에 push만 함 |
| pop/peek  | 평균 O(1), 최악 O(n) | `outStack`이 비어있을 때만 이동 |
| empty     | O(1)               | 두 스택이 모두 비었는지 확인 |

- **공간 복잡도**: O(n) → 최대 n개의 요소를 스택 두 개에 저장

---

## 💻 핵심 코드 정리 (Java)

```java
class MyQueue {
    private Stack<Integer> inStack = new Stack<>();
    private Stack<Integer> outStack = new Stack<>();

    public void push(int x) {
        inStack.push(x);
    }

    public int pop() {
        shiftStacks();
        return outStack.pop();
    }

    public int peek() {
        shiftStacks();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    private void shiftStacks() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}
```

---

## 🎯 느낀 점

- 단순한 문제처럼 보여도 자료구조의 특성을 깊이 이해해야 효율적으로 구현할 수 있다는 점을 느꼈다.
- **push는 무조건 inStack**, **pop/peek는 필요한 순간에만 in → out 전송** 전략을 익혔다.
- **큐와 스택의 차이점, 전환 기법**을 다시 복습하는 좋은 문제였다.
