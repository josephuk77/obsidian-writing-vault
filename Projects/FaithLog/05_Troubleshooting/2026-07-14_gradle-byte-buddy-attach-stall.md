---
project: FaithLog
type: troubleshooting
created: 2026-07-14
tags:
  - FaithLog
  - troubleshooting
  - gradle
  - byte-buddy
---

# macOS 전체 테스트 Byte Buddy dynamic attach 정지

## 문제 상황

Issue #194는 production Java를 바꾸지 않았지만 완료 게이트 확인을 위해 `./gradlew test build asciidoctor --no-daemon --max-workers=1`을 실행했다. `:test` 진입과 JVM bootstrap classpath 경고 뒤 장시간 새 출력 없이 정지했고 test XML도 생성되지 않았다.

## 에러 메시지

명시적 assertion failure나 stack trace는 없었다. 테스트 task가 완료되지 않는 정지 상태였으며 해당 Gradle 실행만 interrupt했다.

## 원인 분석

이 저장소에서 이전에도 관찰된 macOS Mockito/Byte Buddy 동적 agent attach 보조 프로세스 정지 패턴과 일치했다. `testRuntimeClasspath`를 확인한 결과 현재 resolve된 agent는 `net.bytebuddy:byte-buddy-agent:1.17.8`이었다.

## 해결 방법

소스나 dependency를 바꾸지 않고 resolved cache JAR를 실행 시점에만 JVM agent로 선로딩했다.

```text
JAVA_TOOL_OPTIONS=-javaagent:<Gradle cache>/byte-buddy-agent-1.17.8.jar
```

동일 test/build/asciidoctor 직렬 실행이 `449 tests / 0 failures / 0 errors / 3 skipped`와 `BUILD SUCCESSFUL`로 완료됐다.

## 재발 방지

- 먼저 `dependencyInsight --dependency byte-buddy-agent --configuration testRuntimeClasspath`로 현재 resolved 버전을 확인한다.
- 캐시에 존재한다는 이유만으로 이전 버전 agent를 선택하지 않는다.
- agent 선로딩은 실행 시점 검증 우회로만 사용하고 build script나 production dependency에 조용히 추가하지 않는다.
- 정지한 실행은 성공으로 집계하지 않고, 재실행 결과를 별도로 기록한다.

## 관련 이슈

- #194
