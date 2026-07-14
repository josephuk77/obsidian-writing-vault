---
project: FaithLog
type: security-audit
issue: 159
status: done
created: 2026-07-12
tags:
  - FaithLog
  - security
  - IDOR
  - BOLA
  - authorization
  - OWASP
---

# #159 캠퍼스 격리와 IDOR 권한 보안 감사

## 1. 감사 배경

#157, #158, #176이 반영된 `origin/develop` `5b078b5f` 기준으로 path/query/body 식별자의
campus, parent, owner 범위와 service/campus role, COFFEE duty 기능 권한을 보안 동작 변경 없이
읽기 전용으로 감사했다.

#176은 Refresh mismatch 감지, refresh 삭제, revoked marker 저장을 단일 Redis Lua 전이로
원자화했다. 재개 감사에서 Controller/identifier/campus authorization/repository manifest를 다시
계수했으며 코드 표면은 변하지 않았다. PM 리뷰에서 기존 문서가 누락한 penalty `ruleId`, global
coffee catalog `brandId`/`menuId`, campus `inviteCode`, devotion `recordDate` 4개 범주를 보강해
identifier manifest를 17개에서 21개로 바로잡았다. #158 finding과 #176 수정은 #159 finding으로
중복 집계하지 않았다.

## 2. 감사 범위와 수치

- 21개 Controller, 80개 endpoint
- 21개 객체 식별자 범주
- 56개 authorization service/policy/support 파일
- 25개 concrete repository 파일
- Campus/Admin/Billing/Devotion/Poll/Prayer/Notification/User 도메인
- pageable/filter/sort/keyword campus predicate
- 익명 Poll identity, Prayer board read/write, Billing owner/snapshot, FCM owner,
  Notification campus target/log scope

## 3. 감사 결과

- Confirmed: Critical 0 / High 0 / Medium 1 / Low 0
- F-159-01: active COFFEE duty 사용자가 persisted non-COFFEE template을 대상으로
  update request body의 `paymentCategory=COFFEE`를 권한 분기에 주입하면 duty guard를 통과해
  제목, 선택 방식, 옵션, 자동 생성 스케줄을 변경할 수 있다.
- Severity Medium, confidence 10/10
- CWE-863, 보조 CWE-639
- OWASP API5:2023 BFLA, API1:2023 BOLA
- 최소 확정 영향은 같은 캠퍼스 비-COFFEE template 무단 변경이다. 자동 생성이 활성화되면
  후속 Poll 전파가 조건부 최대 영향이다.
- `pollType=COFFEE`가 필요한 정산 guard 때문에 청구 생성 영향은 확정 범위에서 제외했다.

## 4. 방어 확인

- path campus와 persisted resource campus 불일치는 주요 Poll/template/parent API에서 404로 은닉
- `membershipId`, `campusMemberId`, `assignmentId`는 campus와 결합 조회
- penalty `ruleId`는 persisted rule의 `campusId`로 manager 권한을 검사
- global coffee catalog `brandId`/`menuId`는 존재·활성 및 brand parent를 검증
- `inviteCode`는 campus를 선택한 뒤 resolved campus와 principal membership을 결합
- devotion `recordDate`는 path campus·principal·derived week parent와 결합해 daily row를 upsert
- self API는 request user ID가 아니라 principal 사용
- Billing charge/account는 campus, owner, account type/status 조건 결합
- anonymous Poll은 user map과 respondents를 생성하지 않음
- Prayer는 전체 ACTIVE member board read와 group/self/manager write 범위를 분리
- FCM token은 `tokenId + principal userId`, Notification log는 campus predicate 강제

## 5. False positive와 미확인

- false positive/의도 정책 8개
- 운영·정책 미확인 4개
- #157 F-157-01과 #158 F-158-01 중복 finding 0개
- Supabase RLS/DB role, production constraint health, ID enumeration 동적 실효성은 운영/동적
  증거가 없어 confirmed로 올리지 않았다.

## 6. 검증

- 기존 focused test 13 classes
- 최신 `5b078b5f`에서 172 tests / 0 failures / 0 errors / 0 skipped
- PM manifest 보강 후 2026-07-13 동일 13 classes 재실행 결과도 172 / 0 / 0 / 0
- `BUILD SUCCESSFUL`
- production/test/config/DB/Flyway 변경 0건
- 실제 secret/token/개인정보/계좌번호/기도제목 값 출력·기록 0건
- Docker, push, PR, 수정 Issue 생성 0건
- 저장소 문서:
  - `docs/security/159-campus-isolation-idor-matrix.md`
  - `docs/security/159-audit-findings.md`
  - `docs/resume-metrics.md`

## 7. 후속 후보

- [ ] PM 승인 후 persisted `template.pollType` 기준으로 COFFEE duty update 권한 고정
- [ ] active duty가 CUSTOM/WED_SERVICE/SATURDAY_LEADER template을 수정하지 못하는 회귀 테스트
- [ ] 403/404 존재 은닉 공통 정책 승인 여부 확인
- [ ] Supabase tenant/RLS와 production constraint 운영 검증

이 감사는 AI 보조 정적 감사이며 전문 보안 감사나 침투 테스트를 대체하지 않는다.
