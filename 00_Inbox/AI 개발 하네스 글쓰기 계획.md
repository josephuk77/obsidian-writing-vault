---
title: "AI 개발 하네스 글쓰기 계획"
created: "2026-05-23"
updated: "2026-05-23"
type: planning
status: draft
tags: [codex, ai, harness, workflow, agents, pm, software-engineering, blog]
source_notes:
  - "/Users/josephuk77/harness/PLAN.md"
  - "/Users/josephuk77/harness/SESSION.md"
  - "/Users/josephuk77/harness/SKILL_ROADMAP.md"
  - "/Users/josephuk77/harness/MCP_SETUP_PLAN.md"
  - "/Users/josephuk77/harness/UX_LANGUAGE_PLAN.md"
  - "/Users/josephuk77/harness/pm-harness/HARNESS_DESIGN.md"
  - "/Users/josephuk77/harness/spring-boot-harness/HARNESS_DESIGN.md"
  - "/Users/josephuk77/harness/react-harness/HARNESS_DESIGN.md"
publish_url:
---

# AI 개발 하네스 글쓰기 계획

## 작성된 글

- [[2026-05-23_AI가 만든 코드 품질은 하네스로 좋아질 수 있을까]]

## 글의 방향

아직 개발을 시작한 회고가 아니라, Codex와 대화하면서 구체화하고 있는 "AI 개발 하네스"의 기획 노트로 쓴다.

핵심은 "AI에게 일을 맡긴다"가 아니다. AI가 프로젝트를 제멋대로 크게 읽고, 임의로 구조를 바꾸고, 검증 없이 끝내는 문제를 줄이기 위해 사람의 개발팀처럼 역할, 책임, 문서, 검증 게이트를 나누려는 시도다.

이 글에서는 완성된 도구를 소개하지 않는다. 대신 "역할과 책임을 나눈 AI 개발 흐름이 코드 품질과 일관성을 높일 수 있다"는 가설을 세우고, 그 가설을 검증하기 위해 어떤 하네스를 만들고 있는지 정리한다.

최종 목표는 특정 프로젝트 하나에만 맞는 하네스가 아니라, Spring Boot, React, Next.js, FastAPI처럼 다양한 프로젝트에 조합해서 적용할 수 있는 범용 AI 개발 하네스다.

## 예상 독자

- Codex, Claude Code 같은 AI 코딩 도구를 써봤지만 결과가 들쭉날쭉하다고 느낀 사람
- AI에게 큰 작업을 맡기면 컨텍스트가 커지고 방향이 흐려지는 문제를 겪은 사람
- 바이브코딩을 하더라도 최소한의 기획, 설계, 리뷰, 테스트 흐름은 유지하고 싶은 사람
- Spring Boot, React 프로젝트에서 AI와 협업하는 방식을 체계화하고 싶은 개발자
- AI agent, skill, MCP, task packet 같은 개념에 관심 있는 사람

## 핵심 문제의식

AI 코딩 도구는 코드를 빠르게 만들어주지만, 프로젝트가 커질수록 다음 문제가 생긴다.

- 처음 합의한 제품 목표와 다른 방향으로 구현이 흐를 수 있다.
- 한 세션에 너무 많은 맥락을 넣으면 판단이 흐려진다.
- 백엔드, 프론트엔드, DB, 보안, QA 관점이 섞여 책임 경계가 애매해진다.
- 작은 수정만 필요한데 전체 구조를 다시 설계하려는 일이 생긴다.
- 구현은 됐지만 리뷰, 테스트, 보안 점검, 최종 검증이 빠질 수 있다.
- 사용자와 AI가 내린 결정이 문서로 남지 않아 다음 세션에서 다시 설명해야 한다.

## 이 프로젝트의 가설

이 하네스는 아직 검증된 정답이 아니다.

지금 세우고 있는 가설은 단순하다. AI에게 큰 작업을 통째로 맡기는 것보다, PM, 프레임워크 리드, 전문가, worker처럼 역할을 나누고, worker에게는 작은 task packet만 전달하고, 구현 후 리뷰와 검증 게이트를 거치게 하면 코드 품질과 일관성이 올라갈 수 있다는 것이다.

즉, 이 하네스는 AI 개발을 더 빠르게만 만들기 위한 도구가 아니라, AI가 만든 코드의 품질 편차를 줄이기 위한 실험이다.

핵심 문장:

> 이 하네스의 첫 번째 가설은 "AI도 역할, 책임, 검증 흐름을 나누면 더 일관된 품질로 일할 수 있다"는 것이다.

## 최종 목표

최종 목표는 특정 프로젝트 하나에만 맞는 하네스가 아니다.

Spring Boot, React, Next.js, FastAPI처럼 서로 다른 기술 스택에서도 사용할 수 있고, 프로젝트 성격에 따라 DBA, 보안, QA, 디자이너 하네스를 조합할 수 있는 범용 AI 개발 하네스를 만드는 것이다.

모든 프로젝트에 같은 규칙을 강제하는 것이 아니라, 프로젝트마다 필요한 하네스를 선택해서 팀처럼 구성하는 방식이 목표다.

핵심 문장:

> 모든 프로젝트에 하나의 거대한 프롬프트를 복붙하는 것이 아니라, 프로젝트에 맞는 AI 개발팀을 조합하는 하네스를 만들고 싶다.

## 핵심 결론

내가 만들고 싶은 하네스는 하나의 거대한 프롬프트가 아니다.

PM 하네스가 전체 제품 목표와 팀 구성을 잡고, Spring Boot나 React 같은 프레임워크 하네스가 각 영역의 팀장 역할을 하며, worker 세션은 작은 task packet 하나만 받아 구현한다.

즉, AI 개발을 "한 명의 만능 AI에게 전부 맡기는 방식"에서 "PM, 백엔드 리드, 프론트엔드 리드, DBA, QA 같은 역할을 가진 작은 AI 팀이 절차에 따라 협업하는 방식"으로 바꾸려는 시도다.

핵심 문장:

> AI 개발 하네스의 목적은 AI를 더 자유롭게 풀어놓는 것이 아니라, 더 좁고 명확한 책임 안에서 일하게 만드는 것이다.

## 제목 후보

- AI에게 코딩을 맡기기 전에 하네스를 만들고 싶어진 이유
- 바이브코딩을 개발팀처럼 통제할 수 있을까?
- Codex와 함께 설계 중인 AI 개발 하네스
- AI가 만든 코드 품질은 하네스로 좋아질 수 있을까?
- AI 코딩을 한 명의 천재가 아니라 작은 개발팀처럼 쓰기
- PM, 리드, 워커로 나누는 AI 개발 하네스 구상
- 모든 프로젝트에 조합해서 쓰는 AI 개발 하네스 만들기

## 글의 목차

## 1. 왜 하네스를 만들고 싶은가

AI 코딩 도구를 쓰다 보면 처음에는 속도에 놀란다.

하지만 조금 큰 작업을 맡기기 시작하면 속도보다 중요한 문제가 보인다. AI가 프로젝트의 목표, 아키텍처, 테스트 기준, 보안 기준을 계속 같은 수준으로 유지하지 못한다.

그래서 필요한 것은 더 긴 프롬프트가 아니라, 작업을 시작하기 전의 구조다.

핵심 문장:

> 좋은 AI 협업은 "무엇을 시킬까"보다 "어떤 경계 안에서 일하게 할까"가 더 중요해진다.

## 2. 먼저 세운 가설

이 글에서 하네스를 정답처럼 말하지 않는다.

지금 단계에서는 다음 가설을 검증하고 싶다.

- AI에게 큰 일을 한 번에 맡기는 것보다 역할을 나누면 결과가 더 안정적일 것이다.
- worker에게 전체 대화가 아니라 작은 task packet만 주면 아키텍처 드리프트가 줄어들 것이다.
- 리드 리뷰와 PM 최종 리뷰를 두면 구현 품질의 편차가 줄어들 것이다.
- 프로젝트 시작 전에 `AGENTS.md`, `harness.yaml`, decisions 문서를 남기면 다음 세션의 재설명 비용이 줄어들 것이다.
- 보안, 테스트, 접근성, DB 같은 관점을 필요한 시점에 전문가 하네스로 불러오면 놓치는 문제가 줄어들 것이다.

이 가설이 맞는지는 아직 모른다. 그래서 먼저 작은 Spring Boot + React 프로젝트에서 실제로 검증하려고 한다.

## 3. 하네스라는 단어로 부르고 싶은 것

여기서 하네스는 AI를 묶어두는 작업 흐름이다.

포함하려는 요소:

- 프로젝트 목표를 정리하는 PM 역할
- 프레임워크별 설계와 구현 기준
- 작업을 작게 나누는 task packet
- worker가 건드릴 수 있는 파일 범위
- 구현 후 리드 리뷰
- 보안, 테스트, 접근성, 클린 코드 게이트
- 최종 PM 리뷰
- 다음 세션을 위한 결정 기록

하네스는 AI의 능력을 키우는 장치라기보다, AI가 이상한 방향으로 뻗어나가지 않게 만드는 레일에 가깝다.

## 4. 모든 프로젝트에 적용 가능한 구조로 만들고 싶은 이유

처음부터 특정 Spring Boot 프로젝트 하나만 위한 규칙을 만들 수도 있다.

하지만 그렇게 만들면 다음 프로젝트에서 다시 비슷한 구조를 복사하고 고쳐야 한다.

그래서 목표는 프로젝트별 전용 프롬프트가 아니라, 프로젝트에 맞게 조합할 수 있는 하네스다.

예시:

```text
PM Harness
+ Spring Boot Harness
+ React Harness
+ PostgreSQL DBA Harness
+ QA Harness
= Spring Boot + React 프로젝트용 AI 개발팀
```

다른 프로젝트에서는 조합이 달라질 수 있다.

```text
PM Harness
+ Next.js Harness
+ Designer Harness
+ Web Security Harness
= UI 중심 SaaS 프로젝트용 AI 개발팀
```

핵심은 모든 프로젝트를 하나의 방식으로 강제하지 않는 것이다. 공통 흐름은 유지하되, 필요한 역할과 규칙은 프로젝트에 맞게 선택한다.

## 5. 하나의 거대한 프롬프트로 만들지 않는 이유

처음에는 모든 규칙을 하나의 큰 문서에 넣고 AI에게 읽히면 될 것처럼 보인다.

하지만 실제로는 다음 문제가 생긴다.

- 모든 세션이 불필요한 맥락까지 읽는다.
- 작업자가 전체 설계를 다시 판단하려고 한다.
- 프론트엔드 worker에게 DBA 규칙까지 들어가는 식으로 컨텍스트가 낭비된다.
- 긴 대화가 이어질수록 중요한 결정이 희석된다.

그래서 현재 방향은 "작은 task packet"이다.

worker에게는 전체 대화가 아니라 다음 정보만 전달한다.

- 역할
- 프레임워크
- 아키텍처
- 도메인
- 보안 수준
- 목표
- 허용 파일
- 구현 규칙
- acceptance check
- 반환 형식

핵심 문장:

> worker 세션은 프로젝트를 다시 설계하는 존재가 아니라, 리드가 잘라준 작은 일을 끝내는 존재여야 한다.

## 6. PM 하네스가 맡을 일

PM 하네스는 전역으로 설치하는 유일한 하네스다.

사용자는 새 프로젝트에서 `$setup`을 실행한다. 그러면 PM 하네스가 프로젝트 목표를 묻고, 필요한 기술 스택과 하네스 팀을 추천하고, 연결 가능한 MCP를 확인하고, 개발 전에 계획 문서를 남긴다.

PM 하네스의 책임:

- 제품 목표 확인
- 사용자 수준 선택: 초보자, 중급자, 전문가
- 프레임워크와 아키텍처 추천
- 필요한 하네스 팀 구성
- GitHub, Notion, Figma, Browser QA 같은 MCP 확인
- `AGENTS.md`, `harness.yaml`, `.harness/decisions.md` 생성
- clear planning gate 실행
- 최종 cross-functional review

PM 하네스는 구현 전문가가 아니라 오케스트레이터다.

## 7. 프레임워크 하네스와 전문가 하네스

PM 하네스 하나에 모든 지식을 넣지 않는다.

대신 필요한 하네스만 프로젝트 안에 clone한다.

초기 구상:

- `spring-boot-harness`: 백엔드 리드
- `react-harness`: 프론트엔드 리드
- `postgres-dba-harness`: DB 전문가
- `web-security-harness`: 보안 리뷰
- `designer-harness`: UX/UI 리뷰
- `qa-harness`: QA와 release gate

Spring Boot 하네스는 Controller, Application, Domain, Infrastructure 경계와 transaction, validation, security, repository 규칙을 본다.

React 하네스는 route, component, feature structure, API client, loading/error/empty state, accessibility, browser QA를 본다.

DBA나 QA 같은 전문가 하네스는 모든 프로젝트에 항상 들어오지 않는다. 프로젝트가 실제로 그 관점을 필요로 할 때만 PM이 팀에 추가한다.

## 8. `$setup`에서 하고 싶은 일

하네스의 시작점은 `$setup`이다.

상상하는 흐름:

```text
사용자: $setup
-> 안내 수준 선택
-> 제품 아이디어 정리
-> 프레임워크/아키텍처 추천
-> 도메인과 위험도 확인
-> 필요한 MCP 확인
-> 필요한 하네스 repo clone
-> AGENTS.md, harness.yaml, decisions.md 작성
-> 개발 시작 전 clear planning gate
```

사람이 읽는 설명은 한국어로 하고, 기계가 읽는 키와 파일명은 영어로 둔다.

예시:

```yaml
backend:
  framework: spring-boot
  architecture: ddd-modular-monolith

setup:
  guidance_level: beginner
  language: ko
```

## 9. 왜 한국어 UX가 중요한가

이 하네스는 나 혼자 쓰는 실험으로 시작하지만, 결국 AI와 협업하는 사람에게 선택지를 설명해야 한다.

아키텍처, 보안, DB, 배포, QA 선택지는 초보자에게 너무 추상적일 수 있다. 그래서 `$setup`은 사용자의 숙련도에 따라 질문 방식을 바꿔야 한다.

- 초보자: 쉬운 한국어 설명, 안전한 기본값, 질문 적게
- 중급자: 중요한 트레이드오프 설명, 핵심 결정만 질문
- 전문가: 짧은 설명, 고급 옵션, custom 허용

핵심 문장:

> 하네스가 좋은 선택지를 갖고 있어도, 사용자가 왜 그 선택을 해야 하는지 이해하지 못하면 좋은 도구가 되기 어렵다.

## 10. 현재 MVP 범위

처음부터 모든 하네스를 만들지 않는다.

현재 MVP 순서:

1. `pm-harness`의 기본 skeleton을 만든다.
2. `spring-boot-harness`를 만든다.
3. `react-harness`를 만든다.
4. 작은 Spring Boot + React 샘플 프로젝트를 만든다.
5. PM -> Backend Lead -> Frontend Lead -> Worker -> Lead Review -> PM Review 흐름을 검증한다.
6. 그 다음 `postgres-dba-harness`, `qa-harness`, `designer-harness`, `web-security-harness`를 붙인다.

이미 GitHub 조직과 초기 repo는 만들어둔 상태로 기록한다.

```text
AI-harness-lab-Lee

pm-harness
spring-boot-harness
react-harness
example-spring-react-app
postgres-dba-harness
web-security-harness
designer-harness
qa-harness
```

단, 이 글에서는 아직 "동작한다"고 쓰면 안 된다. 지금은 설계와 기획 단계다.

## 11. 이 실험에서 확인하고 싶은 것

MVP를 만들면서 확인할 질문:

- 역할을 나누는 방식이 실제 코드 품질을 올리는가?
- 범용 하네스 구조가 특정 프로젝트 전용 규칙보다 재사용성이 높은가?
- PM 하네스만 전역 설치하고 나머지는 프로젝트별로 clone하는 모델이 편한가?
- task packet만으로 worker가 충분히 일할 수 있는가?
- context 사용량을 50% 이하로 유지하는 설계가 실제로 가능한가?
- Spring Boot와 React 리드가 worker 결과를 제대로 리뷰할 수 있는가?
- Notion, GitHub, Figma, Browser QA 같은 MCP를 setup 단계에 넣는 것이 과하지 않은가?
- 초보자/중급자/전문가 안내 수준 구분이 실제 사용성을 높이는가?
- 개발 전 clear planning gate가 AI 작업 품질을 높이는가?

## 12. 글의 마무리 방향

마지막에는 완성된 도구처럼 말하지 않는다.

대신 "지금은 Codex와 대화하면서 구조를 잡는 중이고, 첫 목표는 Spring Boot + React 샘플 프로젝트로 이 팀 모델이 실제로 코드 품질과 일관성을 높이는지 검증하는 것"이라고 정리한다.

마무리 핵심 문장:

> 이 하네스가 성공했는지는 프롬프트가 멋진지로 판단할 수 없다. 작은 프로젝트 하나를 실제로 끝까지 만들고, 기획부터 리뷰까지 흐름이 무너지지 않는지 확인해야 한다.

## 글에서 제외할 내용

- Codex skill 구현 세부 문법
- MCP별 설치 방법
- GitHub 조직 생성 과정의 상세 명령어
- Spring Boot/React 하네스의 모든 규칙 전문
- DBA, QA, 보안, 디자이너 하네스의 깊은 세부 설계
- 실제 구현 결과처럼 보이는 표현
- "AI가 개발자를 대체한다"는 식의 과장된 주장

## 작성 순서

먼저 AI 코딩 도구를 쓰면서 느낀 문제를 짧게 제시한다.

그 다음 이 프로젝트가 검증하려는 가설을 밝힌다.

그 다음 하네스를 "AI 개발을 위한 팀 운영 구조"로 정의한다.

이후 범용 하네스 목표를 설명하고, PM 하네스, 프레임워크 하네스, 전문가 하네스, worker task packet으로 역할을 나눈다.

중간에 `$setup` 흐름과 한국어 UX 정책을 설명한다.

마지막에는 아직 기획 단계라는 점과 MVP 검증 계획을 분명히 밝힌다.

## 최종 글의 분위기

완성된 오픈소스 발표문이 아니라, 만들고 있는 도구의 설계 일지처럼 쓴다.

너무 거창한 선언보다 "왜 이런 구조가 필요하다고 느꼈는지"와 "어디까지를 첫 검증 범위로 잡았는지"를 차분히 정리한다.

독자가 글을 다 읽고 나면 다음 질문에 답할 수 있어야 한다.

- 왜 AI 개발에 하네스가 필요한가?
- 이 하네스가 검증하려는 가설은 무엇인가?
- 왜 모든 프로젝트에 조합 가능한 범용 하네스를 목표로 하는가?
- 왜 하나의 큰 프롬프트가 아니라 역할별 하네스로 나누는가?
- PM 하네스는 무엇을 하고, worker는 무엇을 하지 말아야 하는가?
- task packet은 왜 중요한가?
- `$setup`은 어떤 문제를 해결하려는가?
- 지금 MVP는 어디까지인가?
