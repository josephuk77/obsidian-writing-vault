---
title: "백준 16713번 — Generic Queries (Java)"
created: "2026-04-02"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/백준-16713번-Generic-Queries-Java"
---

# 백준 16713번 — Generic Queries (Java)

## 문제 설명

길이가 `N`인 수열이 주어지고,
`Q`개의 구간 쿼리가 주어진다.

각 쿼리는 다음과 같다.
```text
[s, e] 구간의 모든 값 XOR
```
그리고 모든 쿼리 결과를 다시 XOR한 값을 출력해야 한다.

---

## 입력

첫째 줄
```text
N Q
```
둘째 줄
```text
a1 a2 a3 ... aN
```
다음 Q줄
```text
s e
```
조건
```text
1 ≤ N ≤ 1,000,000
1 ≤ Q ≤ 3,000,000
```
---

## 출력

모든 쿼리 결과를 XOR한 값 출력

---

## 입력 예시
```text
5 3
4 4 4 4 4
1 1
1 2
1 3
```
## 출력 예시
```text
0
```
---

# 문제 해결 아이디어

이 문제의 핵심은 다음이다.
```text
구간 XOR → 누적 XOR(prefix XOR)
```
---

## XOR 누적합 개념

누적 XOR 배열을 만들면
```text
acc[i] = a1 ^ a2 ^ ... ^ ai
```
이 된다.

---

## 구간 XOR 공식
```text
[s, e] = acc[e] ^ acc[s-1]
```
이 공식을 이용하면
구간 XOR을 O(1)에 구할 수 있다.

---

# 내가 작성한 코드

나는 입력을 받으면서 누적 XOR을 바로 계산했다.

## 코드
```java
import java.util.*;

class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int N = sc.nextInt();
        int Q = sc.nextInt();

        int[] nums = new int[N+1];
        int sum = 0;
        int xor = 0;

        for(int i = 1; i < N+1; i++) {
            sum ^= sc.nextInt();
            nums[i] = sum;
        }

        for(int j = 0; j < Q; j++) {
            int start = sc.nextInt();
            int end = sc.nextInt();
            xor ^= (nums[end] ^ nums[start-1]);
        }

        System.out.println(xor);
    }
}
```
---

# 강의 코드

강의에서는 배열을 먼저 저장한 뒤
누적 XOR 배열을 따로 만들었다.

## 코드
```java
import java.util.Scanner;

class Main
{
    public static void main (String[] args) {

        Scanner sc = new Scanner(System.in);

        int N = sc.nextInt();
        int M = sc.nextInt();

        int[] arr = new int[N + 1];

        for (int i = 1; i <= N; i++)
            arr[i] = sc.nextInt();

        int[] acc = new int[N + 1];

        for (int i = 1; i <= N; i++)
            acc[i] = acc[i - 1] ^ arr[i];

        int ans = 0;

        while (M-- > 0) {
            int i = sc.nextInt();
            int j = sc.nextInt();
            ans ^= acc[j] ^ acc[i - 1];
        }

        System.out.println(ans);
    }
}
```
---

# 내 코드 vs 강의 코드 비교

## 1. 누적 XOR 생성 방식

### 내 코드
```java
sum ^= sc.nextInt();
nums[i] = sum;
```
→ 입력과 동시에 누적 XOR 계산

---

### 강의 코드
```java
arr[i] 저장 → acc[i] 따로 계산
```
→ 입력과 누적합을 분리

---

## 핵심 차이

| 방식    | 특징      |
| ----- | ------- |
| 내 코드  | 한 번에 처리 |
| 강의 코드 | 단계 분리   |

---

## 2. 코드 구조

### 내 코드
```text
입력 + 누적합 동시에 처리
```
→ 코드가 짧음

---

### 강의 코드
```text
입력 → 누적합 → 쿼리 처리
```
→ 구조가 명확

---

## 3. 핵심 로직은 동일

두 코드 모두
```java
acc[j] ^ acc[i-1]
```
을 사용한다.

즉,
```text
풀이 방식은 완전히 동일
```
---

## 4. 성능 차이

이 문제에서 중요한 것은
```text
입력 속도
```
이다.

조건
```text
Q ≤ 3,000,000
```
→ Scanner는 느릴 수 있음

---

### 내 코드 문제 가능성
```text
Scanner → 입력 속도 느림
```
---

### 강의 코드

Scanner를 쓰지만
실전에서는 보통
```text
BufferedReader
```
를 사용해야 안정적이다.

---

# 핵심 개념

## 1. XOR 누적합
```text
acc[i] = acc[i-1] ^ arr[i]
```
---

## 2. 구간 XOR
```text
[s, e] = acc[e] ^ acc[s-1]
```
---

## 3. XOR 성질
```text
A ^ A = 0
A ^ 0 = A
```
이 성질 때문에 누적 XOR이 가능하다.

---

# 시간 복잡도

* 누적합: O(N)
* 쿼리 처리: O(Q)

전체
```text
O(N + Q)
```
---

# 정리

이 문제는 구간 합 문제의 XOR 버전이다.

핵심은
```text
누적합 → XOR로 변환
```
이다.

내 코드와 강의 코드는 방식은 동일하지만
구조만 다르다.
```text
내 코드   → 입력과 누적합 동시에 처리
강의 코드 → 단계 분리
```
또한 이 문제에서 중요한 포인트는
```text
입력 속도
```
이다.

즉,
```text
BufferedReader 사용이 안정적
```
이라는 점도 함께 기억해야 한다.
---

## 관련 글

- [[2026-04-01_백준 11659번 — 구간 합 구하기 4 (Java)]]
- [[2026-04-03_백준 11660번 — 구간 합 구하기 5 (Java)]]
- [[2026-02-27_📘 Week 01 — 자료구조 기초 (배열 · 구간 합 · 투 포인터 · 슬라이딩 윈도우)]]
- [[백준]]
- [[Java]]
- [[코딩테스트]]
- [[누적합]]
