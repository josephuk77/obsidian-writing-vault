---
project: FaithLog
type: troubleshooting
created: 2026-07-10
tags:
  - FaithLog
  - troubleshooting
  - architecture
---

# Poll 공통 helper 파일명과 책임 패키지 구조 검사 충돌

## 문제 상황

Poll focused 테스트와 신규 책임 분리 구조 테스트는 통과했지만 첫 전체 `./gradlew test`에서 `DomainPackageStructureTest` 1건이 실패했다.

## 에러 메시지

`poll/service/PollLookupPolicy.java -> Policy는 service/policy에 둔다`

## 원인 분석

Issue #145 구조 테스트는 이름이 `*Policy.java`인 파일을 `service/policy` 아래에 두도록 강제한다. 새 helper는 package-private Poll service와 같은 패키지 접근이 필요했지만 이름을 `PollLookupPolicy`로 정해 파일명 규칙과 충돌했다.

## 해결 방법

기능, transaction, repository 호출, 접근 범위를 바꾸지 않고 helper 이름만 `PollLookupSupport`로 변경했다. 구조 테스트와 전체 343개 테스트가 모두 통과했다.

## 재발 방지

도메인 service helper 이름을 정할 때 `Command`, `Query`, `Result`, `Policy`, `Port`, `Repository` suffix의 책임 패키지 규칙을 먼저 확인한다.

## 관련 이슈

- #151
