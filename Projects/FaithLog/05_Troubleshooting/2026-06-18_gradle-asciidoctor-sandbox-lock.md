---
project: FaithLog
type: troubleshooting
created: 2026-06-18
tags:
  - FaithLog
  - troubleshooting
  - gradle
---

# Gradle asciidoctor sandbox lock 파일 접근 실패

## 문제 상황

#35 REST Docs Asciidoc include 검증을 위해 `./gradlew asciidoctor`를 실행했지만, Codex workspace-write sandbox가 Gradle wrapper distribution lock 파일에 접근하지 못해 즉시 실패했다.

## 에러 메시지

```text
java.io.FileNotFoundException: /Users/josephuk77/.gradle/wrapper/dists/gradle-8.14.5-bin/.../gradle-8.14.5-bin.zip.lck (Operation not permitted)
```

## 원인 분석

Gradle wrapper가 사용하는 `~/.gradle/wrapper` 경로는 현재 Codex workspace-write sandbox의 쓰기 허용 범위 밖이다. `test`/`build`는 이미 wrapper 캐시가 준비된 상태에서 통과했지만, `asciidoctor` 실행 시 wrapper lock 접근이 다시 발생했다.

## 해결 방법

동일한 `./gradlew asciidoctor` 명령을 권한 상승으로 재실행했고, REST Docs snippets include와 Asciidoc 렌더링이 성공했다.

## 재발 방지

Gradle 기반 문서 생성 검증이 wrapper lock 파일 권한 문제로 실패하면 명령 자체를 바꾸지 말고 동일 명령을 권한 상승으로 재시도한다.

## 관련 이슈

- #35
