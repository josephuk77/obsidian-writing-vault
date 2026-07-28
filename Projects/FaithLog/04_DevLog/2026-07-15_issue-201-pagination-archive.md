---
project: FaithLog
type: devlog
issue: "#201"
status: integrated
created: 2026-07-15
tags:
  - FaithLog
  - backend
  - spring-boot
  - tdd
  - pagination
  - billing
  - rest-docs
---

# #201 목록 페이징 메타데이터와 이전 기록 조회

## 1. 작업 배경

청구 조회 5개가 `members` 또는 `items`만 반환해 프론트가 다음 페이지 존재 여부를 정확히 판단할 수 없었다. 완료 청구와 마감 투표는 계속 누적되지만, 미납과 진행 중 데이터는 기간과 무관하게 유지해야 했다.

## 2. 최종 설계 기준

- 관리자 사용자·캠퍼스·정산·알림 로그 기본 20개 유지
- 사용자·담당자 모바일 목록 기본 10개
- 청구 5개 응답에 `page`, `size`, `totalElements`, `totalPages` 필수 추가
- `includeArchived=false`: 모든 UNPAID + 최근 1개월 PAID/WAIVED/CANCELED
- PAID 완료 시점은 `paidAt`, WAIVED/CANCELED는 `updatedAt`
- MEAL 관리 투표는 OPEN/SCHEDULED 전체 + 최근 90일 CLOSED
- `includeArchived=true`로 이전 완료·마감 기록 조회
- 과거 row 삭제 없음

## 3. 구현 내용

- Controller: 청구 5개와 MEAL 관리 투표에 `includeArchived` 추가
- Query: 청구 terminal cutoff와 MEAL CLOSED cutoff를 DB 조건으로 적용
- DTO: 기존 목록 필드를 유지하며 페이지 메타데이터 추가
- UI 계약: `이전 기록 보기` 전환 시 0페이지부터 재조회
- REST Docs: 기본 크기, 완료 시점, 이전 기록 의미와 페이지 응답 문서화

## 4. TDD 기록

1. 페이지 메타데이터, 기본 크기, 이전 기록 경계를 test-only RED로 고정
2. RED: 26 tests 중 6 failures
3. 조회 policy와 응답 metadata 최소 구현
4. focused REST Docs/controller 계약 GREEN

## 5. 테스트 결과

- test-only RED: 26 tests 중 20 pass / 6 fail
- 전체 회귀: 551 tests / 0 failures / 3 skipped
- focused 최종 회귀: BUILD SUCCESSFUL
- `./gradlew build -x test`: BUILD SUCCESSFUL
- `./gradlew asciidoctor -x test`: BUILD SUCCESSFUL
- REST Docs: 170 snippet groups, `build/docs/asciidoc/index.html` 생성
- local `develop@952ab34` fast-forward 완료
- 최신 Docker app image로 `faithlog-latest-app`만 교체, 기존 `127.0.0.1:28080` 유지
- `GET /api/v1/health`: `UP`
- Flyway: 10 migrations validated, schema version 10, no migration necessary
- PostgreSQL/Redis 컨테이너와 named volume 유지
- 디스크 정리: backend `build/` 169MB와 Xcode DerivedData 2.7GB만 삭제, 여유 759MB -> 3.6GB 확보
- iOS Simulator 재빌드 없이 refresh 완료
- 관리자 청구와 MEAL 투표의 `includeArchived=false/true`, page metadata, 관리자 20/담당자 10 실서버 확인
- 기존 `관리자 정보를 불러오지 못했습니다` 오류 해소 및 관리자 정산 데이터 표시 확인
- 실제 데이터 삭제·DB migration: 없음

## 6. 다음 작업

- [x] 전체 backend 회귀·build·asciidoctor 완료
- [x] frontend 최신 계약과 타입/화면 대조
- [x] develop 통합 및 Docker backend 교체
- [x] iOS Simulator 연결 QA 최종 확인
