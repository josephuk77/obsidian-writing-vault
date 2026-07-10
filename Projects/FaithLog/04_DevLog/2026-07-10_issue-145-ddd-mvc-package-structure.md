---
project: FaithLog
type: devlog
issue: "#145"
status: done
created: 2026-07-10
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - ddd
  - refactoring
---

# #145 DDD 도메인 내부 MVC 패키지 구조 정리

## 1. 작업 배경

도메인 최상위 경계는 이미 존재했지만 `application` 바로 아래에 Service, Command, Query, Result가 섞여 있었고 Controller/DTO는 `presentation`에 함께 배치되어 책임 탐색이 일관되지 않았다.

## 2. 최종 설계 기준

- 최상위 경계: admin, batch, billing, campus, devotion, notification, poll, prayer, user
- 내부 책임: controller, service, domain, infrastructure
- DTO: controller/dto/request, controller/dto/response
- 서비스 모델: service/command, service/query, service/result, service/policy, service/port
- 도메인 모델: domain/entity, domain/type
- 인프라: infrastructure/repository, adapter, redis, fcm, seed, scheduler 등 실제 책임명
- 빈 패키지는 만들지 않고 global은 공통 config/security/exception/response/controller 책임을 유지한다.

## 3. 구현 내용

- Java 이동 파일: 443개
- 도메인별: admin 29, batch 14, billing 58, campus 51, devotion 53, notification 56, poll 88, prayer 47, user 45, global 2
- 운영/테스트 package 선언과 import를 새 경로로 갱신했다.
- JPQL constructor expression의 FQCN도 새 Result 경로로 갱신했다.
- port/adapter 방향은 유지하고 JPA Repository와 외부 adapter를 분리했다.
- `README.md`, `docs/decision-log.md`, `docs/resume-metrics.md`에 구조와 검증 증거를 기록했다.

## 4. TDD 기록

1. 실패 테스트 작성: 기존 의존성만 사용하는 `DomainPackageStructureTest` 추가
2. 실패 확인: 운영 구조와 테스트 미러링 2개 규칙 RED
3. 최소 구현: 도메인 묶음별 파일 이동과 package/import 갱신
4. 테스트 통과: 구조 테스트 2개 GREEN
5. 리팩토링: `AdminAccessPolicy`를 service/policy, JPA 기반 token-version checker를 infrastructure/adapter로 보정

## 5. 테스트 결과

- `./gradlew test`: BUILD SUCCESSFUL, 315 tests / 0 failures / 0 errors / 1 skipped
- `./gradlew build`: BUILD SUCCESSFUL
- `./gradlew asciidoctor`: BUILD SUCCESSFUL
- Docker isolated QA: PostgreSQL/Redis healthy, `/api/v1/health` status UP, compose down 성공
- `git diff --check`: 성공

## 6. 고민한 부분

- Port 전용 Command/Result는 service/command 또는 service/result로 강제하지 않고 service/port에 함께 유지해 경계 계약의 응집도를 보존했다.
- `DevotionFineCalculator`는 Entity나 enum/value type이 아닌 Domain Service이므로 devotion/domain 루트에 유지했다.
- 외부 Billing 연결은 repository로 부르지 않고 devotion/poll infrastructure/adapter에 배치했다.

## 7. 트러블슈팅

- 문제: 전체 테스트에서 admin/billing service 테스트 5건 실패
- 원인: package 이름 변경으로 controller 테스트가 service 테스트보다 먼저 실행돼 비트랜잭션 테스트 데이터가 전역 count 전제에 남음
- 해결: 두 service 통합 테스트 class 시작 전에 Spring context를 재생성해 격리 복원
- 재발 방지: 구조 테스트와 전체 suite를 함께 실행하고 테스트 순서에 의존하는 전역 count 검증을 격리한다.

## 8. 다음 작업

- [ ] 후속 이슈에서 Service 책임 분리와 코드 책임 리팩터링
- [ ] 별도 보안 이슈에서 인증/인가/입력 검증/민감정보 점검

## 9. Velog 글감

- 대규모 Java package 이동에서 API/비즈니스 로직 무변경을 증명하는 방법
- 파일시스템 기반 패키지 구조 회귀 테스트와 테스트 실행 순서 문제
