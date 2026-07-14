---
project: FaithLog
type: security-audit
issue: 160
status: review
created: 2026-07-13
tags:
  - FaithLog
  - security
  - validation
  - sensitive-data
  - OWASP
---

# #160 입력 검증과 민감정보 노출 보안 감사

## 1. 감사 배경

#157~#159 감사와 #176/#179 수정이 반영된 `origin/develop` `52e0b4ae` 기준으로 입력 검증,
민감정보 응답·로그·문서 경계, injection·파일·외부 전송 표면을 코드 변경 없이 감사했다.
선행 finding과 수정은 중복 집계하지 않았고 실제 secret/token/개인정보/계좌번호/기도제목/알림
본문 값은 출력하거나 기록하지 않았다.

## 2. 감사 범위와 수치

- 21개 Controller, 80개 endpoint
- 36개 request DTO, 57개 response DTO
- 123개 path/query binding, 4개 page/sort parser
- 3개 global exception 파일, 2개 production logger-bearing 파일, 8개 application config 파일
- Entity 25개, repository 25개, Flyway 6개를 합친 persistence constraint 파일 56개
- 입력 surface → validation → normalization → persistence constraint → error status 행렬 26행
- 민감 필드 → 저장 위치 → 응답 DTO → 로그/문서 → 허용 역할 행렬 12행

## 3. 감사 결과

- Confirmed: Critical 0 / High 0 / Medium 2 / Low 0
- F-160-01: 상한 없는 토요일 지각 시간과 `int` 벌금 산술이 overflow되어 음수 `UNPAID`
  벌금과 캠퍼스 미납 합계 왜곡으로 이어질 수 있다. Severity Medium, confidence 10/10.
- F-160-02: COFFEE Poll/template의 null `menuId` 옵션에서 client 가격을 backend catalog 검증 없이
  snapshot하고 응답 회원 정산에 사용한다. Severity Medium, confidence 9/10.
- False positive/의도 정책 9개, confidence 8/10 미만 unverified/hardening 3개
- 최소 확정 영향은 각각 본인 음수 청구·재무 집계 무결성 훼손과 응답 회원의 위조 COFFEE
  청구다. 자동 환불·자동 출금·선택 없는 청구·cross-campus 영향은 주장하지 않았다.

## 4. 검증과 제약

- PM 독립 재검증: 격리 `GRADLE_USER_HOME=/private/tmp/faithlog-gradle-160-review`, 단일 Gradle 실행,
  `--no-parallel --rerun-tasks` 조건에서 감사 문서의 16개 focused test class 전부를 재실행해
  `BUILD SUCCESSFUL`, 16 suites / 138 tests / 0 failures / 0 errors / 0 skipped를 확인했다.
- counted manifest와 두 confirmed finding은 PM 기계 검증에서도 실제 코드 경로와 일치했다.
- 초기 감사 세션에서 먼저 관찰된 기본 Gradle cache metadata 읽기 실패와 격리 실행 간 XML 동시 쓰기 충돌은
  코드·테스트 실패가 아닌 실행환경 concern으로 최종 정리했다.
- current tree와 좁은 history의 high-signal secret prefix 후보 0건
- generated high-signal secret prefix 파일 0건
- production/test/config/DB/Flyway/인프라 변경 0건
- Docker, 수정 Issue 생성, push, PR 0건
- 새 제품 결정을 만들지 않아 `docs/decision-log.md` 변경 0건

## 5. 산출물과 후속 후보

- `docs/security/160-input-validation-sensitive-data-matrix.md`
- `docs/security/160-audit-findings.md`
- `docs/resume-metrics.md`
- PM 승인 전 후속 수정 Issue는 생성하지 않았다.
- 후보 1: 경건 벌금 exact arithmetic, 도메인 상한, positive charge·DB constraint
- 후보 2: COFFEE 옵션의 필수 catalog provenance와 client 가격 비권위화
- 후보 3: payload/list 최대치와 provider failure reason 노출 정책 확정

이 감사는 AI 보조 정적 감사이며 전문 보안 감사나 침투 테스트를 대체하지 않는다.
