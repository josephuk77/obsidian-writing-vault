---
tags:
  - type/project
  - area/backend
  - status/active
project: FaithLog
series: FaithLog 개발기
published: true
created: 2026-06-12
---

# [FaithLog 개발기 2] ERD 설계: 운영 흐름을 데이터 구조로 옮기기

## 들어가며

이전 글에서는 FaithLog를 기획하게 된 이유와 MVP 범위를 정리했다.

이번 글에서는 그 기획을 바탕으로 ERD를 설계한 과정을 정리해보려고 한다.

처음에는 단순히 사용자, 경건생활 기록, 투표, 벌금 정도만 저장하면 된다고 생각했다.
하지만 실제 운영 방식을 데이터 구조로 옮기다 보니 생각보다 고민할 부분이 많았다.

특히 다음 부분을 많이 고민했다.

* 사용자 권한과 커피 담당자를 같은 역할로 볼 것인가
* 경건생활을 주간 횟수로만 저장할 것인가, 하루별 체크로 저장할 것인가
* 벌금을 항목별로 저장할 것인가, 한 주 단위로 합산할 것인가
* 점심 기능을 MVP에 포함할 것인가
* 커피 메뉴를 DB enum으로 관리할 것인가
* 계좌와 담당자의 시작일/종료일을 관리할 것인가
* 투표 현황과 미응답자 조회가 가능한 구조인가

이번 글에서는 최종 테이블 구조뿐 아니라, 왜 그런 선택을 했는지도 함께 정리하려고 한다.

---

## MVP에서 제외한 기능

처음에는 토요일 점심 투표와 점심 정산 기능도 포함하려고 했다.

예를 들어 김치찜, 지코바, 치킨 같은 음식을 함께 주문하고, 총액을 사람별로 나눠서 청구하는 구조를 생각했다.

하지만 설계를 하다 보니 점심은 변수가 너무 많았다.

* 주문 총액이 매번 달라진다.
* 사람마다 먹는 양이 다를 수 있다.
* 중간에 참여자가 바뀔 수 있다.
* 동일 분배가 아닐 수 있다.
* 담당자가 수동으로 금액을 조정해야 할 수 있다.
* 주문 취소나 추가 주문이 생길 수 있다.

이 기능까지 MVP에 넣으면 프로젝트의 핵심이 흐려질 것 같았다.

그래서 초기 버전에서는 점심 기능을 제외하고, 다음 기능에 집중하기로 했다.

* 경건생활 체크
* 벌금 계산
* 수요예배 참여 투표
* 토요 목자모임 참여 투표
* 커피 주문 투표
* 벌금/커피 청구 항목 관리
* 납부 완료 처리
* FCM 알림

점심 기능은 나중에 서비스가 안정화된 뒤 확장 기능으로 추가하는 것이 더 현실적이라고 판단했다.

---

## 최종 테이블 목록

MVP 기준으로 설계한 테이블은 다음과 같다.

| 테이블명                    | 역할                   |
| ----------------------- | -------------------- |
| users                   | 사용자 기본 정보            |
| refresh_tokens          | JWT Refresh Token 관리 |
| campuses                | 캠퍼스 정보               |
| app_groups              | 그룹 정보                |
| group_members           | 그룹 구성원 및 권한          |
| group_duty_assignments  | 커피 담당자 지정            |
| weekly_devotion_records | 주간 경건생활 제출/합산 기록     |
| devotion_daily_checks   | 하루별 경건생활 체크 기록       |
| penalty_rules           | 벌금 규칙                |
| payment_accounts        | 벌금/커피 계좌             |
| poll_templates          | 반복 투표 템플릿            |
| poll_template_options   | 반복 투표 템플릿 선택지        |
| polls                   | 실제 생성된 투표            |
| poll_options            | 투표 선택지               |
| poll_responses          | 사용자 투표 응답            |
| charge_items            | 사용자별 청구 항목           |
| user_fcm_tokens         | 사용자별 FCM 토큰          |
| notification_logs       | 알림 발송 이력             |

---

## 전체 관계 요약

전체 구조는 그룹을 중심으로 연결된다.

하나의 캠퍼스에는 여러 그룹이 있을 수 있고, 사용자는 그룹에 소속된다.
경건생활 기록, 투표, 벌금 규칙, 계좌, 청구 항목, 알림도 모두 그룹 기준으로 관리한다.

주요 관계는 다음과 같다.

| 관계                                              | 설명                            |
| ----------------------------------------------- | ----------------------------- |
| campuses → app_groups                           | 하나의 캠퍼스는 여러 그룹을 가질 수 있다.      |
| users → group_members                           | 한 사용자는 여러 그룹에 속할 수 있다.        |
| app_groups → group_members                      | 한 그룹에는 여러 구성원이 있다.            |
| users → weekly_devotion_records                 | 사용자는 주차별 경건생활 기록을 가진다.        |
| weekly_devotion_records → devotion_daily_checks | 하나의 주간 기록은 여러 하루별 체크 기록을 가진다. |
| app_groups → penalty_rules                      | 그룹마다 벌금 규칙을 다르게 둘 수 있다.       |
| app_groups → payment_accounts                   | 그룹마다 벌금 계좌와 커피 계좌를 가진다.       |
| app_groups → polls                              | 그룹마다 투표를 생성할 수 있다.            |
| polls → poll_options                            | 하나의 투표는 여러 선택지를 가진다.          |
| polls → poll_responses                          | 하나의 투표는 여러 응답을 가진다.           |
| users → poll_responses                          | 사용자는 투표에 응답한다.                |
| users → charge_items                            | 사용자는 벌금 또는 커피 청구 항목을 가진다.     |
| payment_accounts → charge_items                 | 청구 항목은 납부 계좌와 연결된다.           |
| users → user_fcm_tokens                         | 사용자는 여러 기기의 FCM 토큰을 가질 수 있다.  |
| users → notification_logs                       | 사용자별 알림 발송 이력을 저장한다.          |

---

## 사용자와 그룹 구조

사용자는 `users` 테이블에 저장한다.

처음에는 사용자 테이블에 바로 role을 넣을까 고민했다.
하지만 FaithLog는 그룹 단위로 운영되는 서비스이기 때문에, 권한은 사용자 자체가 아니라 그룹 소속 기준으로 관리하는 것이 맞다고 판단했다.

예를 들어 한 사용자가 A그룹에서는 관리자이고, B그룹에서는 일반 구성원일 수도 있다.

그래서 사용자 기본 정보는 `users`에 저장하고, 그룹 내 권한은 `group_members`에서 관리한다.

### users

| 컬럼명           | 설명         |
| ------------- | ---------- |
| id            | 사용자 ID     |
| name          | 사용자 이름     |
| email         | 로그인 이메일    |
| password_hash | 암호화된 비밀번호  |
| is_active     | 활성 여부      |
| last_login_at | 마지막 로그인 시간 |
| created_at    | 생성일        |
| updated_at    | 수정일        |

### group_members

| 컬럼명        | 설명                        |
| ---------- | ------------------------- |
| id         | PK                        |
| group_id   | 그룹 ID                     |
| user_id    | 사용자 ID                    |
| role       | OWNER, ADMIN, MEMBER      |
| status     | ACTIVE, PENDING, INACTIVE |
| joined_at  | 가입일                       |
| created_at | 생성일                       |
| updated_at | 수정일                       |

`group_id + user_id`는 unique로 관리한다.

한 사용자가 같은 그룹에 중복 가입되는 것을 막기 위해서다.

---

## 권한과 담당자를 분리한 이유

역할을 설계하면서 가장 고민했던 부분 중 하나는 커피 담당자를 어떻게 표현할 것인가였다.

처음에는 역할을 다음처럼 생각했다.

| 값      | 설명     |
| ------ | ------ |
| OWNER  | 그룹 소유자 |
| ADMIN  | 관리자    |
| MEMBER | 일반 구성원 |
| COFFEE | 커피 담당  |

하지만 이렇게 하면 문제가 생긴다.

어떤 사용자는 일반 구성원이면서 커피 담당일 수 있다.
또 어떤 사용자는 관리자이면서 커피 담당일 수도 있다.

즉, `OWNER`, `ADMIN`, `MEMBER`는 권한에 가깝고, `COFFEE`는 운영 담당 역할에 가깝다.

그래서 권한 역할과 담당 역할을 분리했다.

권한은 `group_members.role`에서 관리한다.

| role   | 설명     |
| ------ | ------ |
| OWNER  | 그룹 소유자 |
| ADMIN  | 관리자    |
| MEMBER | 일반 구성원 |

커피 담당자는 `group_duty_assignments`에서 관리한다.

### group_duty_assignments

| 컬럼명         | 설명          |
| ----------- | ----------- |
| id          | PK          |
| group_id    | 그룹 ID       |
| user_id     | 담당자 사용자 ID  |
| duty_type   | COFFEE      |
| is_active   | 현재 활성 담당 여부 |
| assigned_at | 담당자로 지정된 시간 |
| revoked_at  | 담당 해제 시간    |
| created_at  | 생성일         |
| updated_at  | 수정일         |

처음에는 담당자에 시작일과 종료일을 둘까 고민했다.

하지만 실제 운영에서는 커피 담당 기간이 항상 규칙적으로 정해지는 것은 아니다.
그래서 시작일/종료일로 관리하기보다, 관리자가 현재 담당자를 직접 지정하고 해제하는 방식이 더 현실적이라고 판단했다.

현재 커피 담당자는 `duty_type = COFFEE`이고 `is_active = true`인 사용자로 조회한다.

---

## 경건생활 기록 구조

경건생활 체크는 처음에 주간 횟수만 저장하는 방식으로 생각했다.

예를 들어 다음처럼 저장하는 구조다.

| 항목   |  값 |
| ---- | -: |
| 큐티   | 3회 |
| 기도   | 5회 |
| 말씀읽기 | 4회 |

이 방식은 벌금 계산에는 편하다.

하지만 사용자 입장에서 보면 “내가 어느 날 체크했는지”를 확인하기 어렵다.
또 프론트에서 캘린더 형식으로 보여주려면 하루별 기록이 필요하다.

그래서 최종적으로는 두 테이블을 함께 사용하기로 했다.

| 테이블                     | 역할          |
| ----------------------- | ----------- |
| devotion_daily_checks   | 하루별 체크 기록   |
| weekly_devotion_records | 주간 제출/합산 기록 |

### devotion_daily_checks

하루별 경건생활 체크 기록을 저장한다.

| 컬럼명                   | 설명         |
| --------------------- | ---------- |
| id                    | PK         |
| weekly_record_id      | 주간 기록 ID   |
| record_date           | 체크 날짜      |
| quiet_time_checked    | 큐티 체크 여부   |
| prayer_checked        | 기도 체크 여부   |
| bible_reading_checked | 말씀읽기 체크 여부 |
| created_at            | 생성일        |
| updated_at            | 수정일        |

`weekly_record_id + record_date`는 unique로 관리한다.

한 주 안에서 같은 날짜의 체크 기록이 중복 생성되지 않게 하기 위해서다.

### weekly_devotion_records

주간 제출과 벌금 계산 기준이 되는 테이블이다.

| 컬럼명                   | 설명            |
| --------------------- | ------------- |
| id                    | PK            |
| group_id              | 그룹 ID         |
| user_id               | 사용자 ID        |
| week_start_date       | 주차 시작일        |
| week_end_date         | 주차 종료일        |
| quiet_time_count      | 큐티 총 횟수       |
| prayer_count          | 기도 총 횟수       |
| bible_reading_count   | 말씀읽기 총 횟수     |
| saturday_late_minutes | 토요 목자모임 지각 시간 |
| submitted_at          | 제출 시간         |
| created_at            | 생성일           |
| updated_at            | 수정일           |

사용자가 캘린더에서 하루별 체크를 하면 `devotion_daily_checks`에 저장된다.

그리고 주간 제출을 누르면 하루별 체크 데이터를 합산해서 `weekly_devotion_records`에 저장한다.

이후 `weekly_devotion_records`를 기준으로 벌금을 계산하고, `charge_items`에 벌금 청구 항목을 생성한다.

---

## 벌금 규칙 설계

벌금 규칙은 코드에 하드코딩하지 않고 `penalty_rules` 테이블로 분리했다.

현재 규칙은 다음과 같다.

| 항목         |    기준 |                  벌금 |
| ---------- | ----: | ------------------: |
| 큐티         |  주 5회 |         부족 1회당 500원 |
| 기도         |  주 5회 |         부족 1회당 500원 |
| 말씀읽기       |  주 5회 |         부족 1회당 300원 |
| 토요 목자모임 지각 | 지각 시간 | 기본 1,000원 + 분당 100원 |

큐티, 기도, 말씀읽기는 부족 횟수 기준으로 계산한다.

반면 지각은 지각 시간이 있을 때 기본 금액과 분당 금액을 함께 계산해야 한다.

그래서 벌금 계산 방식을 구분하기 위해 `calculation_type`을 두었다.

### penalty_rules

| 컬럼명              | 설명                                               |
| ---------------- | ------------------------------------------------ |
| id               | PK                                               |
| group_id         | 그룹 ID                                            |
| rule_type        | QUIET_TIME, PRAYER, BIBLE_READING, SATURDAY_LATE |
| calculation_type | MISSING_COUNT, LATE_MINUTE                       |
| required_count   | 기준 횟수                                            |
| base_amount      | 기본 금액                                            |
| amount_per_unit  | 부족 1회당 금액 또는 지각 1분당 금액                           |
| is_active        | 활성 여부                                            |
| created_at       | 생성일                                              |
| updated_at       | 수정일                                              |

예시는 다음과 같다.

| rule_type     | calculation_type | required_count | base_amount | amount_per_unit |
| ------------- | ---------------- | -------------: | ----------: | --------------: |
| QUIET_TIME    | MISSING_COUNT    |              5 |           0 |             500 |
| PRAYER        | MISSING_COUNT    |              5 |           0 |             500 |
| BIBLE_READING | MISSING_COUNT    |              5 |           0 |             300 |
| SATURDAY_LATE | LATE_MINUTE      |              0 |        1000 |             100 |

---

## 벌금은 왜 한 줄로 청구하는가

처음에는 벌금을 항목별로 `charge_items`에 저장하는 방식도 생각했다.

예를 들면 다음과 같다.

| payment_category | title         | amount | status |
| ---------------- | ------------- | -----: | ------ |
| PENALTY          | 큐티 2회 부족      |   1000 | UNPAID |
| PENALTY          | 토요 목자모임 5분 지각 |   1500 | UNPAID |

하지만 실제 사용자는 벌금을 항목별로 따로 납부하기보다, 한 주의 벌금을 한 번에 납부하는 방식이 더 자연스럽다.

그래서 벌금은 세부 항목을 계산만 하고, 실제 청구 항목은 주차별로 한 줄만 생성하기로 했다.

예를 들어 큐티 2회 부족과 지각 5분이 있다면 다음처럼 저장한다.

| payment_category | title           | reason          | amount | status |
| ---------------- | --------------- | --------------- | -----: | ------ |
| PENALTY          | 2026년 6월 2주차 벌금 | 큐티 2회 부족, 지각 5분 |   2500 | UNPAID |

세부 사유는 `reason`에 요약해서 남긴다.

나중에 벌금 상세 화면이 필요해지면 별도 상세 테이블을 추가할 수 있지만, MVP에서는 한 줄 청구 구조가 더 단순하다고 판단했다.

---

## 청구 항목 설계

`charge_items`는 사용자가 실제로 납부해야 하는 항목을 저장한다.

MVP에서는 청구 항목을 두 가지로만 관리한다.

| payment_category | 설명  |
| ---------------- | --- |
| PENALTY          | 벌금  |
| COFFEE           | 커피값 |

점심 기능은 MVP에서 제외했기 때문에 `LUNCH`는 넣지 않았다.

### charge_items

| 컬럼명                     | 설명                             |
| ----------------------- | ------------------------------ |
| id                      | PK                             |
| group_id                | 그룹 ID                          |
| user_id                 | 사용자 ID                         |
| payment_category        | PENALTY, COFFEE                |
| payment_account_id      | 납부 계좌 ID                       |
| bank_name_snapshot      | 당시 은행명                         |
| account_number_snapshot | 당시 계좌번호                        |
| account_holder_snapshot | 당시 예금주                         |
| source_type             | DEVOTION_RECORD, POLL_RESPONSE |
| source_id               | 원본 데이터 ID                      |
| title                   | 청구 제목                          |
| reason                  | 청구 사유                          |
| amount                  | 청구 금액                          |
| status                  | UNPAID, PAID, WAIVED, CANCELED |
| due_date                | 납부 기한                          |
| paid_at                 | 납부 완료 처리 시간                    |
| created_at              | 생성일                            |
| updated_at              | 수정일                            |

`source_type`과 `source_id`를 둔 이유는 청구 항목이 어디서 발생했는지 추적하기 위해서다.

벌금은 `weekly_devotion_records`에서 발생한다.

커피값은 `poll_responses`에서 발생한다.

중복 생성을 막기 위해 `group_id`, `user_id`, `payment_category`, `source_type`, `source_id` 조합은 unique로 관리한다.

---

## 계좌 설계

벌금과 커피는 납부 계좌가 다를 수 있다.

그래서 계좌는 `payment_accounts`에서 관리한다.

처음에는 계좌에 시작일과 종료일을 둘까 고민했다.

하지만 실제 운영에서는 계좌가 정해진 기간에 맞춰 규칙적으로 바뀐다기보다, 관리자가 필요할 때 바꾸는 방식에 가깝다.

그래서 `effective_from`, `effective_to` 같은 기간 컬럼은 두지 않았다.

대신 현재 사용하는 계좌는 `is_active = true`로 판단한다.

계좌가 바뀌면 기존 계좌를 비활성화하고 새 계좌를 등록한다.

### payment_accounts

| 컬럼명            | 설명              |
| -------------- | --------------- |
| id             | PK              |
| group_id       | 그룹 ID           |
| account_type   | PENALTY, COFFEE |
| nickname       | 계좌 별칭           |
| bank_name      | 은행명             |
| account_number | 계좌번호            |
| account_holder | 예금주             |
| owner_user_id  | 계좌 담당자          |
| is_active      | 현재 사용 여부        |
| deactivated_at | 비활성화 시간         |
| created_at     | 생성일             |
| updated_at     | 수정일             |

`charge_items`에는 계좌 스냅샷을 저장한다.

계좌가 나중에 바뀌어도 과거 청구 항목의 납부 계좌 정보가 바뀌면 안 되기 때문이다.

---

## 투표 설계

FaithLog의 MVP에는 세 종류의 투표가 있다.

| 투표 종류           | 설명            |
| --------------- | ------------- |
| WED_SERVICE     | 수요예배 참여 투표    |
| SATURDAY_LEADER | 토요 목자모임 참여 투표 |
| COFFEE          | 커피 주문 투표      |

수요예배와 토요 목자모임 투표는 금액이 발생하지 않는다.

반면 커피 주문 투표는 사용자가 선택한 메뉴의 가격으로 청구 항목이 생성된다.

그래서 투표에는 `charge_generation_type`을 두었다.

| charge_generation_type | 설명             |
| ---------------------- | -------------- |
| NONE                   | 청구 금액 없음       |
| OPTION_PRICE           | 선택지 가격으로 청구 생성 |

수요예배와 토요 목자모임 투표는 `NONE`을 사용한다.

커피 주문 투표는 `OPTION_PRICE`를 사용한다.

### poll_templates

반복 투표 템플릿을 저장한다.

수요예배 참여 투표와 토요 목자모임 참여 투표는 매주 반복되기 때문에 템플릿으로 관리한다.

| 컬럼명               | 설명                                           |
| ----------------- | -------------------------------------------- |
| id                | PK                                           |
| group_id          | 그룹 ID                                        |
| title             | 템플릿 제목                                       |
| poll_type         | WED_SERVICE, SATURDAY_LEADER, COFFEE, CUSTOM |
| start_day_of_week | 시작 요일                                        |
| start_time        | 시작 시간                                        |
| end_day_of_week   | 마감 요일                                        |
| end_time          | 마감 시간                                        |
| is_active         | 활성 여부                                        |
| created_at        | 생성일                                          |
| updated_at        | 수정일                                          |

### poll_template_options

반복 투표 템플릿의 선택지를 저장한다.

| 컬럼명         | 설명           |
| ----------- | ------------ |
| id          | PK           |
| template_id | 반복 투표 템플릿 ID |
| content     | 선택지 내용       |
| sort_order  | 정렬 순서        |

### polls

실제로 생성된 투표를 저장한다.

| 컬럼명                    | 설명                                           |
| ---------------------- | -------------------------------------------- |
| id                     | PK                                           |
| group_id               | 그룹 ID                                        |
| template_id            | 반복 템플릿 ID                                    |
| title                  | 투표 제목                                        |
| poll_type              | WED_SERVICE, SATURDAY_LEADER, COFFEE, CUSTOM |
| selection_type         | SINGLE, MULTIPLE                             |
| is_anonymous           | 익명 여부                                        |
| charge_generation_type | NONE, OPTION_PRICE                           |
| payment_category       | PENALTY, COFFEE                              |
| payment_account_id     | 납부 계좌 ID                                     |
| starts_at              | 시작 시간                                        |
| ends_at                | 마감 시간                                        |
| status                 | SCHEDULED, OPEN, CLOSED                      |
| created_by             | 생성자 ID                                       |
| created_at             | 생성일                                          |
| updated_at             | 수정일                                          |

### poll_options

투표 선택지를 저장한다.

| 컬럼명               | 설명                         |
| ----------------- | -------------------------- |
| id                | PK                         |
| poll_id           | 투표 ID                      |
| content           | 선택지 내용                     |
| compose_menu_code | Spring ComposeMenu enum 코드 |
| price_amount      | 선택지 금액                     |
| sort_order        | 정렬 순서                      |

커피 투표에서는 `compose_menu_code`, `content`, `price_amount`를 사용한다.

수요예배나 토요 목자모임 투표에서는 `price_amount`를 0으로 둔다.

### poll_responses

사용자의 투표 응답을 저장한다.

| 컬럼명          | 설명     |
| ------------ | ------ |
| id           | PK     |
| poll_id      | 투표 ID  |
| option_id    | 선택지 ID |
| user_id      | 사용자 ID |
| memo         | 응답 메모  |
| responded_at | 응답 시간  |
| created_at   | 생성일    |
| updated_at   | 수정일    |

MVP에서는 한 사람이 한 투표에 하나의 선택지만 고르는 구조로 설계했다.

그래서 `poll_id + user_id`는 unique로 관리한다.

---

## 투표 현황 조회

투표는 단순히 응답을 저장하는 것뿐 아니라, 현황 조회도 가능해야 한다.

현재 구조에서는 `polls`, `poll_options`, `poll_responses`, `users`, `group_members`를 조합해서 다음 정보를 조회할 수 있다.

* 선택지별 응답 수
* 사용자별 응답 내역
* 미응답자 목록
* 전체 응답률
* 커피 주문 총액

특히 미응답자 조회는 `poll_responses`가 아니라 `group_members`를 기준으로 해야 한다.

활성 구성원 전체를 기준으로 두고, 특정 투표에 대한 응답이 없는 사용자를 찾는 방식이다.

이 구조를 통해 투표 마감 전 미응답자에게만 FCM 알림을 보낼 수 있다.

---

## 커피 메뉴는 왜 DB enum으로 만들지 않았나

커피 메뉴는 처음에 DB enum으로 관리할지 고민했다.

하지만 메뉴는 시간이 지나면서 바뀔 수 있고, 가격도 바뀔 수 있다.

또 HOT/ICE에 따라 가격이 달라질 수 있다.

반대로 메뉴를 DB 테이블로 따로 만들면, 메뉴 관리 화면까지 필요해질 수 있어 MVP 범위가 커진다.

그래서 타협안으로 Spring enum을 사용하기로 했다.

커피 메뉴 목록과 기본 가격은 Spring enum으로 관리한다.

DB에는 enum 이름을 문자열로 저장한다.

| 컬럼명               | 설명             |
| ----------------- | -------------- |
| compose_menu_code | Spring enum 코드 |
| content           | 화면에 보여준 메뉴명    |
| price_amount      | 실제 투표에서 사용한 가격 |

중요한 점은 실제 청구 금액은 Spring enum이 아니라 `poll_options.price_amount`를 기준으로 한다는 것이다.

Spring enum의 가격은 기본값일 뿐이다.

투표 생성 시점에 enum의 기본 가격을 `poll_options.price_amount`에 복사한다.

이렇게 하면 나중에 메뉴 가격이 바뀌어도 과거 투표와 청구 금액이 변하지 않는다.

---

## 알림 설계

배치는 정산 생성에 사용하지 않는다.

정산은 사용자의 행동에 따라 생성된다.

배치는 알림 발송 용도로만 사용한다.

알림 예시는 다음과 같다.

* 일요일 경건생활 체크 알림
* 월요일 미체크자 알림
* 수요예배 투표 시작 알림
* 수요예배 투표 미응답자 알림
* 토요 목자모임 투표 시작 알림
* 토요 목자모임 투표 미응답자 알림
* 커피 투표 시작 알림
* 커피 투표 미응답자 알림
* 미납 항목 알림

### user_fcm_tokens

한 사용자가 여러 기기를 사용할 수 있기 때문에 FCM 토큰은 사용자 테이블에 직접 넣지 않았다.

| 컬럼명          | 설명                |
| ------------ | ----------------- |
| id           | PK                |
| user_id      | 사용자 ID            |
| token        | FCM 토큰            |
| device_type  | ANDROID, IOS, WEB |
| is_active    | 활성 여부             |
| last_used_at | 마지막 사용 시간         |
| created_at   | 생성일               |
| updated_at   | 수정일               |

### notification_logs

알림 발송 이력은 별도 테이블에 저장한다.

중복 발송을 막고, 실패 원인을 추적하기 위해서다.

| 컬럼명                    | 설명                             |
| ---------------------- | ------------------------------ |
| id                     | PK                             |
| user_id                | 수신 사용자 ID                      |
| group_id               | 그룹 ID                          |
| notification_type      | 알림 유형                          |
| target_week_start_date | 대상 주차                          |
| target_id              | 관련 대상 ID                       |
| title                  | 알림 제목                          |
| body                   | 알림 내용                          |
| send_status            | PENDING, SENT, FAILED, SKIPPED |
| failure_reason         | 실패 사유                          |
| sent_at                | 발송 시간                          |
| created_at             | 생성일                            |

---

## 최종 ERD 정리

최종적으로 FaithLog MVP의 ERD는 다음 흐름을 중심으로 설계했다.

1. 사용자는 그룹에 소속된다.
2. 그룹 안에서 사용자는 OWNER, ADMIN, MEMBER 권한을 가진다.
3. 커피 담당자는 권한과 별도로 `group_duty_assignments`에서 관리한다.
4. 경건생활은 하루별로 체크하고, 주간 제출 시 합산한다.
5. 벌금은 주간 경건생활 기록을 기준으로 계산한다.
6. 벌금은 항목별이 아니라 주차별 한 줄로 청구한다.
7. 커피는 투표 응답을 기준으로 청구한다.
8. 청구 항목은 `charge_items`에서 관리한다.
9. 납부는 사용자가 직접 “납부했어요”를 눌러 완료 처리한다.
10. 배치는 정산 생성이 아니라 알림 발송에만 사용한다.

---

## 마무리

이번 ERD 설계에서 가장 많이 고민한 부분은 테이블을 많이 만드는 것이 아니라, 실제 운영 방식에 맞게 어디까지 단순화할 것인지였다.

처음에는 점심 기능까지 포함하려고 했지만 MVP에서는 제외했다.

처음에는 벌금을 항목별로 저장하려고 했지만, 실제 납부 흐름에 맞게 주차별 한 줄 청구로 바꾸었다.

처음에는 경건생활을 주간 횟수로만 저장하려고 했지만, 사용자 경험을 고려해 하루별 체크 테이블을 추가했다.

처음에는 커피 메뉴를 DB enum으로 관리하려고 했지만, 가격 변경과 유지보수를 고려해 Spring enum과 가격 스냅샷 구조로 바꾸었다.

처음에는 계좌와 담당자에 시작일/종료일을 두려고 했지만, 실제 운영이 규칙적이지 않을 수 있어 `is_active` 기반으로 단순화했다.

이런 과정을 거치면서 ERD는 단순히 테이블을 나누는 작업이 아니라, 실제 서비스 운영 방식을 데이터 구조로 옮기는 과정이라는 것을 느꼈다.

다음 글에서는 이 ERD를 바탕으로 API를 어떻게 나눌지 정리해볼 예정이다.

특히 다음 흐름을 중심으로 API를 설계할 예정이다.

* 경건생활 하루별 체크
* 주간 제출과 벌금 계산
* 수요예배/토요 목자모임 투표
* 커피 투표 생성과 응답
* 투표 현황 조회
* 청구 항목 조회
* 납부 완료 처리
* 알림 발송
