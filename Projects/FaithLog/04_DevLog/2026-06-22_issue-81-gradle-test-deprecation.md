---
project: FaithLog
type: devlog
issue: "#81"
status: done
created: 2026-06-22
tags:
  - FaithLog
  - backend
  - spring-boot
  - gradle
  - test
---

# #81 [Chore] Gradle 9 호환성과 테스트 deprecation 정리

## 1. 작업 배경

Gradle 9 호환성과 테스트 deprecation 경고를 정리하기 위해 baseline을 재현했다.
기능 동작, API 계약, DB 스키마, 사용자-facing 동작은 변경하지 않았다.

## 2. 최종 설계 기준

- 의존성 major upgrade, Gradle wrapper upgrade, Spring Boot major/minor upgrade는 진행하지 않는다.
- Swagger 문서화 annotation은 추가하지 않는다.
- 테스트 의미를 약하게 만들지 않는다.
- 안전하게 제거 가능한 테스트 deprecation만 수정한다.

## 3. 구현 내용

- Test: deprecated `org.springframework.boot.test.mock.mockito.MockBean` 11건을 `org.springframework.test.context.bean.override.mockito.MockitoBean`으로 교체했다.
- Gradle: `org.asciidoctor.jvm.convert` 4.0.5 내부 `StartParameter.isConfigurationCacheRequested` 경고는 플러그인 내부 경고로 분류하고 코드 변경하지 않았다. 후속 추적 이슈 #82를 생성했다.

## 4. TDD 기록

1. 실패 테스트 작성: 기능 변경이 아닌 deprecation 정리라 신규 실패 테스트는 추가하지 않았다.
2. 실패 확인: `./gradlew test --warning-mode all` baseline에서 Problems report 12 warnings를 확인했다.
3. 최소 구현: 테스트 annotation import와 annotation명만 교체했다.
4. 테스트 통과: `./gradlew test --warning-mode all` 성공.
5. 리팩토링: 추가 리팩터링 없음.

## 5. 테스트 결과

명령:

`./gradlew test --warning-mode all`

`./gradlew test`

`./gradlew build`

`./gradlew build --warning-mode all`

`./gradlew asciidoctor`

`git diff --check`

결과:

`BUILD SUCCESSFUL`

경고 변화:

- 수정 전: Problems report 12 warnings
- 수정 후: Problems report 1 warning
- 제거: `@MockBean` removal warning 11건
- 잔여: Asciidoctor Gradle plugin 내부 Gradle API deprecation 1건
- 전체 테스트: 236 tests / 0 failures / 0 errors / 0 skipped
- Docker QA: 앱/빌드 설정 및 런타임 동작 변경이 없어 생략

## 6. 고민한 부분

Asciidoctor 경고는 stacktrace 기준 `org.asciidoctor.gradle.jvm` -> `org.ysb33r.grolifant` 내부에서 발생했다.
Gradle Plugin Portal 기준 `org.asciidoctor.jvm.convert` 4.0.5가 최신이라 현재 설정 변경만으로 제거하지 않았다.

## 7. 트러블슈팅

- 문제: `StartParameter.isConfigurationCacheRequested` deprecation 경고
- 원인: Asciidoctor Gradle plugin 내부 grolifant 호출
- 해결: 현재 최신 플러그인 내부 경고로 분류하고 후속 추적 대상으로 남김
- 재발 방지: plugin update 가능 버전이 나오면 별도 build chore로 검증

## 8. 다음 작업

- [x] 남은 Asciidoctor Gradle plugin 내부 경고 후속 이슈 #82 생성

## 9. Velog 글감

- Spring Boot 3.5 테스트 mock override API 전환 기록
