# architecture-memo

---
tags:
  - type/project
  - status/planning
  - area/backend
---

## 현재 가정

- 앱은 React Native + TypeScript로 만든다.
- 백엔드는 Spring Boot REST API 서버다.
- 데이터베이스는 Supabase PostgreSQL이다.
- 푸시 알림은 Firebase Cloud Messaging이다.
- Supabase는 DB로만 사용하고, 인증/권한/정산/알림 로직은 Spring Boot가 담당한다.
- 초기 배포 대상은 한 캠퍼스지만, 데이터 구조는 여러 캠퍼스를 지원한다.

## 시스템 경계

```text
React Native App
  -> Spring Boot REST API
    -> Supabase PostgreSQL
    -> Firebase Cloud Messaging
```

앱은 DB에 직접 접근하지 않는다. 이 경계는 인증, 권한, 벌금 계산, 청구 중복 방지, 알림 중복 방지를 서버에서 통제하기 위한 핵심 결정이다.

## 주요 컴포넌트

| 컴포넌트 | 책임 |
| --- | --- |
| React Native App | 로그인, 캠퍼스 선택, 경건생활 체크, 투표 응답, 청구 확인, 납부 완료 처리, 알림 토큰 등록 |
| Spring Boot API | 인증, 권한, 캠퍼스/멤버 관리, 경건생활 제출, 벌금 계산, 투표/청구 생성, 알림 발송 |
| Supabase PostgreSQL | users, campuses, campus_members, weekly/devotion records, polls, charge_items, notification_logs 저장 |
| Firebase Cloud Messaging | 경건생활/투표/청구 관련 푸시 알림 전달 |
| Scheduler | 반복 투표 생성, 일요일 경건생활 안내, 월요일 미제출/미납 점검, 미응답자 리마인드 |

## 핵심 데이터 모델

```text
users
  1:N refresh_tokens
  1:N campus_members
  1:N weekly_devotion_records
  1:N poll_responses
  1:N charge_items
  1:N user_fcm_tokens

campuses
  1:N campus_members
  1:N campus_duty_assignments
  1:N penalty_rules
  1:N payment_accounts
  1:N poll_templates
  1:N polls
  1:N charge_items
  1:N notification_logs

weekly_devotion_records
  1:N devotion_daily_checks
  1:1 charge_items where source_type = DEVOTION_RECORD and payment_category = PENALTY

polls
  1:N poll_options
  1:N poll_responses

poll_responses
  1:1 charge_items where source_type = POLL_RESPONSE and payment_category = COFFEE
```

## 데이터 흐름

### 경건생활 하루 체크

```text
사용자 날짜별 체크
-> PUT /campuses/{campusId}/devotions/me/days/{recordDate}
-> weekly_devotion_records 생성 또는 조회
-> devotion_daily_checks 생성 또는 수정
-> 주간 count 재계산
-> submitted_at 변경 없음
-> charge_items 생성 없음
```

### 주간 제출과 벌금 생성

```text
사용자 주간 제출
-> 7일치 devotion_daily_checks 보장
-> weekly_devotion_records count 저장
-> submitted_at 갱신
-> penalty_rules 조회
-> 부족 횟수/지각 시간으로 벌금 계산
-> charge_items에 PENALTY 1줄 생성 또는 갱신
```

중복 방지 기준은 `campus_id + user_id + payment_category + source_type + source_id`다.

### 커피 주문과 청구 생성

```text
관리자 또는 커피 담당자 커피 투표 생성
-> poll_options에 compose_menu_code, content, price_amount 저장
-> 사용자 poll_response 저장
-> 선택지 price_amount > 0이면 charge_items에 COFFEE 1줄 생성 또는 갱신
```

메뉴 가격은 Spring enum의 기본값을 투표 선택지 생성 시점에 복사한다. 과거 투표 금액이 메뉴 가격 변경에 따라 바뀌면 안 되기 때문이다.

### 납부 처리

```text
사용자 계좌이체
-> 앱에서 납부했어요 클릭
-> PATCH /campuses/{campusId}/charges/me/{chargeItemId}/paid
-> 본인 청구 항목인지 검증
-> 현재 status가 UNPAID인지 검증
-> status = PAID, paid_at = 요청값 또는 now()
```

현재 MVP 기준에서는 관리자 승인 과정이 없다. 관리자는 별도 API로 상태를 변경할 수 있다.

### 알림

```text
Scheduler 또는 관리자 수동 요청
-> 대상자 조회
-> FCM 발송
-> notification_logs 저장
-> 실패 토큰 비활성화 또는 재등록 유도
```

## 구현 우선순위

1. 인증/쿠키/JWT/Refresh Token hash
2. 캠퍼스/멤버/권한 구조
3. 경건생활 하루 체크 및 주간 제출
4. 벌금 규칙과 `PENALTY` 청구 생성
5. 투표 기본 구조와 미응답자 조회
6. 커피 담당/커피 투표/`COFFEE` 청구 생성
7. FCM 토큰/알림 로그/수동 알림
8. Scheduler와 관리자 대시보드

## 리스크와 주의점

| 리스크 | 왜 문제인가 | 처리 기준 |
| --- | --- | --- |
| 기획서와 ERD/API의 납부 흐름 충돌 | 관리자 승인 플로우를 구현하면 상태 enum/API가 달라진다 | MVP는 사용자 직접 `PAID` 처리로 고정 |
| 기획서의 그룹 구조 잔존 | `app_groups/group_members`를 살리면 모델이 복잡해진다 | 최신 ERD 기준으로 `campuses/campus_members` 사용 |
| 점심 기능 혼재 | MVP 범위가 커지고 커피 기능과 충돌한다 | 점심은 제외, 커피만 포함 |
| 하루 체크와 주간 제출 혼동 | 하루 체크 때 청구가 생성되면 중복/미완성 청구가 생긴다 | 청구는 `submit = true`에서만 생성/갱신 |
| 계좌 정보 변경 | 과거 청구의 납부 정보가 바뀔 수 있다 | charge_items에 계좌 snapshot 저장 |

## 아직 모르는 것

- 실제 캠퍼스의 주차 기준은 월요일 시작으로 고정해도 되는가?
- 커피 담당자는 캠퍼스당 정확히 1명이어야 하는가, 여러 명을 허용할 것인가?
- 사용자 직접 `PAID` 처리 후 운영자가 사후 정정하는 방식이 실제 운영에 충분한가?
- FCM 자동 알림의 정확한 발송 요일/시간은 누가 설정하는가?

자세한 질문은 [[open-questions]]에 둔다.
