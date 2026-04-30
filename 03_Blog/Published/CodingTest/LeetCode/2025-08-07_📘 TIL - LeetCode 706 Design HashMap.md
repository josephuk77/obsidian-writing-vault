---
title: "📘 TIL - LeetCode 706: Design HashMap"
created: "2025-08-07"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/TIL-LeetCode-706-Design-HashMap"
---

# 📘 TIL - LeetCode 706: Design HashMap

## 🔍 문제 요약

**해시맵(HashMap)을 내장 라이브러리 없이 직접 구현**하는 문제이다.  
기본적으로 `put`, `get`, `remove`의 기능을 지원하는 HashMap 클래스를 만드는 것이 목표다.

---

## 🔧 요구 기능

- `MyHashMap()`: 해시맵을 초기화한다.
- `void put(int key, int value)`: 키-값 쌍을 삽입 또는 갱신
- `int get(int key)`: 해당 키가 존재하면 값을 반환, 없으면 -1
- `void remove(int key)`: 키와 그에 대응하는 값을 삭제

---

## 💡 해결 전략

### 방법 1: **고정 크기 배열 사용**
- key의 범위가 0~1,000,000이기 때문에 배열 기반 구현 가능
- 배열 초기화 후 기본값을 `-1`로 설정
- 간단하지만 **공간 효율성은 떨어짐**

### 방법 2: **해시 + 체이닝(연결 리스트) 방식**
- 해시 충돌을 고려해 각 버킷에 연결 리스트를 저장
- `key % SIZE`로 인덱스를 계산하여 충돌 방지
- `Node` 클래스를 만들어 연결 리스트 구성
- 충돌이 적으면 평균 시간복잡도는 O(1)

---

## 🧠 배운 점

- 해시맵의 **내부 작동 원리와 충돌 해결 방식**을 직접 구현하면서 확실히 이해할 수 있었다.
- 체이닝 방식은 연결 리스트를 사용해 **충돌을 안전하게 처리**할 수 있는 고전적인 방법이다.
- 배열 기반 방식은 매우 단순하지만 **공간 낭비가 많기 때문에 상황에 따라 적절히 선택해야** 한다.
- 직접 구현 시 **해시 함수 설계와 자료구조 선택**이 핵심이다.

---

## 📊 시간/공간 복잡도

| 연산     | 시간 복잡도       | 설명                            |
|----------|------------------|---------------------------------|
| `put`    | 평균 O(1), 최악 O(n) | 연결 리스트 충돌 시 길이만큼 탐색 |
| `get`    | 평균 O(1), 최악 O(n) |                                 |
| `remove` | 평균 O(1), 최악 O(n) |                                 |
| 공간     | O(n)             | 저장되는 키-값 수에 비례         |

---

## 💻 체이닝 방식 핵심 코드 요약 (Java)
```java
private static final int SIZE = 10000;
private Node[] buckets;

private static class Node {
    int key, value;
    Node next;
    Node(int key, int value) {
        this.key = key;
        this.value = value;
    }
}

private int getIndex(int key) {
    return key % SIZE;
}
```
- put: 연결 리스트에 노드를 찾아서 있으면 갱신, 없으면 추가
- get: 연결 리스트를 순회하면서 key 일치하는 노드 탐색
- remove: key에 해당하는 노드를 리스트에서 제거

---

## 🎯 느낀 점

- 내부 구조를 스스로 구현해 보니 해시맵이 얼마나 효율적인 자료구조인지 체감할 수 있었다.
- **충돌 처리**, **버킷 사이즈**, **해시 함수 설계** 등 실제 구현에서 고려할 요소가 많다는 것을 알게 되었다.
- 단순한 배열 기반 구현부터 체이닝 기반 해시맵까지 확장 학습이 가능한 좋은 문제였다.
---

## 관련 글

- [[2025-08-06_📘 TIL - LeetCode 232 Implement Queue using Stacks]]
- [[2026-04-08_백준 14425번 — 문자열 집합 (Java)]]
- [[2026-02-27_📘 Week 01 — 스택 · 큐 · 힙 자료구조 이해하기]]
- [[LeetCode]]
- [[Java]]
- [[자료구조]]
- [[해시]]
