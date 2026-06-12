## FaithLog ERD 설계

## 1. 서비스 개요

FaithLog는 교회 캠퍼스 단위로 사용하는 경건생활 체크, 수요예배 참여 투표, 토요 목자모임 참여 투표, 커피 주문, 벌 금/커피값 납부 관리를 위한 모바일 앱 서비스이다.

이 서비스에서 캠퍼스는 실제 운영 단위이다.

따라서 별도의 app_groups 테이블을 두지 않고, 모든 기능을 campuses 기준으로 관리한다.

초기 MVP에서는 점심 투표와 점심 정산 기능을 제외한다.

MVP에서는 경건생활 체크, 벌금 계산, 투표, 커피 주문, 납부 상태, 알림 기능에 집중한다.

## 2. 핵심 설계 방향

## 캠퍼스 중심 구조

기존에 고려했던 구조는 다음과 같았다.

```
campuses
app_groups
group_members
```

하지만 현재 서비스에서는 캠퍼스 자체가 실제 운영 단위이므로 아래처럼 단순화한다.

```
campuses
campus_members
```

모든 주요 데이터는 campus_id 를 기준으로 연결한다.

## campus_id 기준 데이터

- 구성원
- 경건생활 기록
- 벌금 규칙
- 커피 담당자
- 계좌
- 투표
- 청구 항목
- 알림

## 3. MVP 기능 범위

MVP 에서 구현할 기능은 다음과 같다.

```
회원가입 / 로그인
캠퍼스 가입
캠퍼스 구성원 관리
경권생활 하루별 체크
주간 경권생활 제출
벌금 자동 계산
수요예배 참여 투표
토요 목자모임 참여 투표
커피 주문 투표
투표 현황 조회
벌금/커피 청구 항목 생성
사용자 납부 완료 처리
FCM 알림
```

## 4. MVP에서 제외하는 기능

다음 기능은 초기 MVP에서 제외한다.

```
점심 투표
점심 공동 주문
점심 금액 배분
점심 담당자
점심 계좌
관리자 납부 승인
입금 인증 사진
결제 API
카카오톡 자동 연동
```

## 5. 권한과 담당자 구조

권한 역할과 운영 담당 역할은 분리한다.

## 권한 역할

권한 역할은 campus_members.role 에서 관리한다.

|값|설명|
|---|---|
|OWNER|캠퍼스 소유자|
|ADMIN|관리자|
|MEMBER|일반 구성원|

## 운영 담당 역할

운영 담당 역할은 campus_duty_assignments 에서 관리한다.

MVP에서는 커피 담당자만 둔다.

|값|설명|
|---|---|
|COFFEE|커피 담당|

커피 담당자는 커피 투표 생성, 커피 계좌 관리, 커피 주문 확인을 할 수 있다.

한 사용자가 일반 구성원이면서 커피 담당일 수 있으므로 campus_members.role 에 COFFEE 를 넣지 않고 별도 테이블로 분리한다.

## 6. 청구 구조

청구 항목은 charge_items 에서 관리한다.

MVP에서는 두 종류의 청구만 사용한다.

PENALTY COFFEE

## 벌금

벌금은 큐티, 기도, 말씀읽기, 지각을 각각 따로 청구하지 않는다.

한 주의 벌금을 모두 합산해서 PENALTY 청구 항목 한 줄로 생성한다.

예시:

|payment_category|title|reason|amount|status|
|---|---|---|---|---|
|PENALTY|2026년 6월 2주차 벌금|큐티 2회 부족, 지각 5분|2500|UNPAID|

## 커피

커피는 사용자가 커피 투표에서 메뉴를 선택하면 해당 메뉴 가격으로 COFFEE 청구 항목을 생성한다.

예시:

|payment_category|title|reason|amount|status|
|---|---|---|---|---|
|COFFEE|아이스 아메리카노|컴포즈커피 주문|1800|UNPAID|

## 납부 처리

사용자가 계좌이체 후 앱에서 “납부했어요”를 누르면 관리자 승인 없이 바로 납부 완료 처리한다.

```
charge_items.status = PAID
charge_items.paid_at = 현재 시간
```

## 7. 핵심 테이블 목록

|테이블명|역할|
|---|---|
|users|사용자 기본 정보|
|refresh_tokens|JWT Refresh Token 관리|
|campuses|캠퍼스 정보|
|campus_members|캠퍼스 구성원 및 권한|
|campus_duty_assignments|커피 담당자 지정|
|weekly_devotion_records|주간 경건생활 제출/합산 기록|
|devotion_daily_checks|하루별 경건생활 체크 기록|
|penalty_rules|벌금 규칙|
|payment_accounts|벌금/커피 계좌|
|poll_templates|반복 투표 템플릿|
|poll_template_options|반복 투표 템플릿 선택지|
|polls|실제 생성된 투표|
|poll_options|투표 선택지|
|poll_responses|사용자 투표 응답|
|charge_items|사용자별 청구 항목|
|user_fcm_tokens|사용자별 FCM 토큰|

|테이블명|역할|
|---|---|
|notification_logs|알림 발송 이력|

## 8. 주요 관계 오약

```
campuses 1 : N campus_members
users 1 : N campus_members
campuses 1 : N campus_duty_assignments
users 1 : N campus_duty_assignments
campuses 1 : N weekly_devotion_records
users 1 : N weekly_devotion_records
weekly_devotion_records 1 : N devotion_daily_checks
campuses 1 : N penalty_rules
campuses 1 : N payment_accounts
users 1 : N payment_accounts
campuses 1 : N poll_templates
poll_templates 1 : N poll_template_options
campuses 1 : N polls
polls 1 : N poll_options
polls 1 : N poll_responses
poll_options 1 : N poll_responses
users 1 : N poll_responses
campuses 1 : N charge_items
users 1 : N charge_items
payment_accounts 1 : N charge_items
users 1 : N user_fcm_tokens
users 1 : N notification_logs
campuses 1 : N notification_logs
```

## 9. Enum 설계

실제 구현에서는 PostgreSQL DB enum보다 Spring enum + DB varchar 저장 방식을 추천한다. dbdiagram.io에서는 보기 쉽게 Enum으로 표현한다. member_role

OWNER ADMIN MEMBER duty_type □ COFFEE member_status

```
ACTIVE
PENDING
INACTIVE
```

penalty_rule_type

```
QUIET_TIME
PRAYER
BIBLE_READING
SATURDAY_LATE
```

## penalty_calculation_type

```
MISSING_COUNT
LATE_MINUTE
```

```
payment_category
```

```
PENALTY
COFFEE
```

poll_type

```
WED_SERVICE
SATURDAY_LEADER
```

```
COFFEE
CUSTOM
```

selection_type

```
SINGLE
MULTIPLE
```

## charge_generation_type

```
NONE
OPTION_PRICE
```

## poll_status

```
SCHEDULED
OPEN
CLOSED
```

## charge_status

```
UNPAID
PAID
WAIVED
CANCELED
```

charge_source_type

```
DEVOTION_RECORD
POLL_RESPONSE
```

## notification_type

```
DEVOTION_REMINDER
DEVOTION_MISSING
WED_POLL_OPEN
WED_POLL_MISSING
SATURDAY_POLL_OPEN
SATURDAY_POLL_MISSING
COFFEE_POLL_OPEN
```

```
COFFEE_POLL_MISSING
PAYMENT_UNPAID
CUSTOM
```

## 10. 컴포즈커피 메뉴 관리 방식

컴포즈커피 메뉴는 DB enum으로 관리하지 않는다.

컴포즈커피 메뉴는 Spring enum으로 관리한다.

DB에는 compose_menu_code 라는 문자열 컬럼만 둔다.

실제 청구 금액은 poll_options.price_amount 를 기준으로 한다.

Spring enum의 가격은 기본값 역할만 한다.

커피 투표를 생성할 때 Spring enum의 기본 가격을 가져와 poll_options.price_amount 에 복사한다.

이렇게 해야 나중에 메뉴 가격이 바뀌어도 과거 투표와 과거 청구 금액이 변하지 않는다.

예시:

```
public enum TemperatureType {
    HOT,
    ICE,
    NONE
}
```

```java
public enum ComposeMenu {
    HOT_AMERICANO("따뜻한 아메리카노", TemperatureType.HOT, 1500),
    ICE_AMERICANO("아이스 아메리카노", TemperatureType.ICE, 1800),
    HOT_CAFE_LATTE("따뜻한 카페라떼", TemperatureType.HOT, 2900),
    ICE_CAFE_LATTE("아이스 카페라떼", TemperatureType.ICE, 2900),
    HOT_VANILLA_LATTE("따뜻한 바닐라라떼", TemperatureType.HOT, 3300),
    ICE_VANILLA_LATTE("아이스 바닐라라떼", TemperatureType.ICE, 3300),
    CUSTOM_MENU("직접 입력 메뉴", TemperatureType.NONE, 0);

    private final String displayName;
    private final TemperatureType temperatureType;
    private final int defaultPrice;
}
```

```java
ComposeMenu(String displayName, TemperatureType temperatureType, int defaultPrice) {
    this.displayName = displayName;
    this.temperatureType = temperatureType;
    this.defaultPrice = defaultPrice;
}

```

## 11. 테이블 설계

## users

사용자 기본 정보를 저장한다.

권한은 users 가 아니라 campus_members 에서 관리한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|name|varchar|사용자 이름|
|email|varchar|로그인 이메일|
|password_hash|varchar|암호화된 비밀번호|
|is_active|boolean|활성 여부|
|last_login_at|timestamptz|마지막 로그인 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
email unique
```

## refresh_tokens

JWT Refresh Token을 저장한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|user_id|bigint|사용자 ID|
|token_hash|varchar|Refresh Token 해시값|
|expires_at|timestamptz|만료 시간|
|revoked_at|timestamptz|폐기 시간|
|created_at|timestamptz|생성일|

## campuses

캠퍼스 정보를 저장한다.

FaithLog에서는 캠퍼스가 실제 운영 단위이다.

예를 들어 14 개 캠퍼스가 있다면 각 캠퍼스가 하나의 운영 단위가 된다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|name|varchar|캠퍼스 이름|
|region|varchar|지역|
|description|text|설명|
|invite_code|varchar|초대코드|
|is_active|boolean|활성 여부|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
invite_code unique
```

## campus_members

사용자의 캠퍼스 소속과 권한을 저장한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|user_id|bigint|사용자 ID|
|role|enum/varchar|OWNER, ADMIN, MEMBER|
|status|enum/varchar|ACTIVE, PENDING, INACTIVE|
|joined_at|timestamptz|가입일|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
campus_id + user_id unique
```

## campus_duty_assignments

커피 담당자를 저장한다.

시작일/종료일은 사용하지 않는다.

담당자가 바뀌면 기존 담당자를 비활성화하고 새 담당자를 활성화한다.

현재 커피 담당자는 is_active = true 인 사용자로 판단한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|user_id|bigint|담당자 사용자 ID|
|duty_type|enum/varchar|COFFEE|
|is_active|boolean|현재 활성 담당 여부|
|assigned_at|timestamptz|담당자로 지정된 시간|
|revoked_at|timestamptz|담당 해제 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

현재 커피 담당자 조회 기준:

```
campus_id = 현재 캠퍼스
duty_type = COFFEE
is_active = true
```

MVP 에서는 캠퍼스당 활성 커피 담당자 1 명을 권장한다.

## weekly_devotion_records

주간 경건생활 제출/합산 기록을 저장한다.

하루별 체크 데이터는 devotion_daily_checks 에 저장하고, 제출 시 합산 결과를 이 테이블에 저장한다.

이 테이블은 벌금 계산과 charge_items 생성의 기준이 된다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|user_id|bigint|사용자 ID|
|week_start_date|date|주차 시작일|
|week_end_date|date|주차 종료일|
|quiet_time_count|int|큐티 총 횟수|
|prayer_count|int|기도 총 횟수|
|bible_reading_count|int|말씀읽기 총 횟수|
|saturday_late_minutes|int|토요 목자모임 지각 시간|
|submitted_at|timestamptz|제출 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
campus_id + user_id + week_start_date unique
```

## devotion_daily_checks

하루별 경건생활 체크 기록을 저장한다.

프론트에서는 이 데이터를 캘린더 형식으로 보여줄 수 있다.

사용자는 날짜별로 큐티, 기도, 말씀읽기 여부를 체크한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|weekly_record_id|bigint|주간 기록 ID|
|record_date|date|체크 날짜|
|quiet_time_checked|boolean|큐티 체크 여부|
|prayer_checked|boolean|기도 체크 여부|
|bible_reading_checked|boolean|말씀읽기 체크 여부|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
weekly_record_id + record_date unique
```

## penalty_rules

캠퍼스별 벌금 규칙을 저장한다. 큐티, 기도, 말씀읽기는 부족 횟수 기준으로 계산한다. 토요 목자모임 지각은 지각 시간이 있을 때 기본 금액과 분당 금액을 기준으로 계산한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|rule_type|enum/varchar|QUIET_TIME, PRAYER, BIBLE_READING, SATURDAY_LATE|
|calculation_type|enum/varchar|MISSING_COUNT, LATE_MINUTE|
|required_count|int|기준 횟수|
|base_amount|int|기본 금액|
|amount_per_unit|int|부족 1 회당 금액 또는 지각 1 분당 금액|
|is_active|boolean|활성 여부|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

예시:

|rule_type|calculation_type|required_count|base_amount|amount_per_unit|
|---|---|---|---|---|
|QUIET_TIME|MISSING_COUNT|5|0|500|
|PRAYER|MISSING_COUNT|5|0|500|
|BIBLE_READING|MISSING_COUNT|5|0|300|
|SATURDAY_LATE|LATE_MINUTE|0|1000|100|

## payment_accounts

벌금 계좌와 커피 계좌를 저장한다.

시작일/종료일은 사용하지 않는다.

계좌가 바뀌면 기존 계좌를 비활성화하고 새 계좌를 활성화한다.

현재 사용하는 계좌는 is_active = true 인 계좌로 판단한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|account_type|enum/varchar|PENALTY, COFFEE|
|nickname|varchar|계좌 별칭|
|bank_name|varchar|은행명|
|account_number|varchar|계좌번호|
|account_holder|varchar|예금주|
|owner_user_id|bigint|계좌 담당자|
|is_active|boolean|현재 사용 여부|
|deactivated_at|timestamptz|비활성화 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

현재 벌금 계좌 조회:

```
campus_id = 현재 캠퍼스
account_type = PENALTY
is_active = true
```

현재 커피 계좌 조회:

```
campus_id = 현재 캠퍼스
account_type = COFFEE
is_active = true
```

계좌가 바뀌더라도 과거 청구 내역의 계좌 정보가 변하면 안 되므로 charge_items 에는 계좌 스냅샷을 저장한다.

## poll_templates

반복 투표 템플릿을 저장한다.

수요예배 참여 투표, 토요 목자모임 참여 투표처럼 매주 반복되는 투표에 사용한다.

커피 투표는 반복 템플릿으로 만들 수도 있고, 커피 담당자가 필요할 때마다 직접 만들 수도 있다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|title|varchar|템플릿 제목|
|poll_type|enum/varchar|WED_SERVICE, SATURDAY_LEADER, COFFEE, CUSTOM|
|start_day_of_week|int|시작 요일|
|start_time|time|시작 시간|
|end_day_of_week|int|마감 요일|
|end_time|time|마감 시간|
|is_active|boolean|활성 여부|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

요일 값:

```
1 = 월요일
2 = 화요일
3 = 수요일
4 = 목요일
5 = 금요일
6 = 토요일
7 = 일요일
```

## poll_template_options

반복 투표 템플릿의 선택지를 저장한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|template_id|bigint|반복 투표 템플릿 ID|
|content|varchar|선택지 내용|
|sort_order|int|정렬 순서|

예시:

수요예배 참여 투표

- 참여
- 미참여
- 미정

토요 목자모임 참여 투표

- 정시 참석
- 지각 예정
- 미정

## polls

실제로 생성된 투표를 저장한다.

수요예배 참여 투표, 토요 목자모임 참여 투표, 커피 주문 투표를 모두 이 테이블에서 관리한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|template_id|bigint|반복 템플릿 ID|
|title|varchar|투표 제목|
|poll_type|enum/varchar|WED_SERVICE, SATURDAY_LEADER, COFFEE, CUSTOM|
|selection_type|enum/varchar|SINGLE, MULTIPLE|
|is_anonymous|boolean|익명 여부|
|charge_generation_type|enum/varchar|NONE, OPTION_PRICE|
|payment_category|enum/varchar|PENALTY, COFFEE|
|payment_account_id|bigint|납부 계좌 ID|
|starts_at|timestamptz|시작 시간|
|ends_at|timestamptz|마감 시간|
|status|enum/varchar|SCHEDULED, OPEN, CLOSED|
|created_by|bigint|생성자 ID|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

예시:

|투표|charge_generation_type|payment_category|
|---|---|---|
|수요예배 참여 투표|NONE|null|
|토요 목자모임 참여 투표|NONE|null|
|컴포즈커피 주문|OPTION_PRICE|COFFEE|

## poll_options

투표 선택지를 저장한다.

커피 투표에서는 compose_menu_code , content , price_amount 를 사용한다.

수요예배와 토요 목자모임 참여 투표에서는 price_amount 를 0으로 둔다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|poll_id|bigint|투표 ID|
|content|varchar|선택지 내용|
|compose_menu_code|varchar|Spring ComposeMenu enum 코드|
|price_amount|int|선택지 금액|
|sort_order|int|정렬 순서|

예시 커피:

|content|compose_menu_code|price_amount|
|---|---|---|
|아이스 아메리카노|ICE_AMERICANO|1800|
|따뜻한 아메리카노|HOT_AMERICANO|1500|
|아이스 카페라떼|ICE_CAFE_LATTE|2900|
|직접 입력 메뉴|CUSTOM_MENU|3500|

예시 수요예배 투표:

|content|compose_menu_code|price_amount|
|---|---|---|
|참여|null|0|
|미참여|null|0|
|미정|null|0|

## poll_responses

사용자의 투표 응답을 저장한다.

초기 MVP에서는 한 사람이 한 투표에 하나의 선택지만 선택하는 구조로 설계한다.

커피 투표에서 사용자가 메뉴를 선택하면 poll_responses 가 저장되고, 선택한 poll_options.price_amount 를 기준으로 charge_items 에 커피 청구 항목이 생성된다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|poll_id|bigint|투표 ID|
|option_id|bigint|선택지 ID|
|user_id|bigint|사용자 ID|
|memo|text|응답 메모|
|responded_at|timestamptz|응답 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
poll_id + user_id unique
```

## charge_items

사용자가 실제로 납부해야 하는 청구 항목을 저장한다.

청구 항목은 벌금과 커피 두 가지만 관리한다.

벌금은 큐티, 기도, 말씀읽기, 지각을 각각 따로 저장하지 않고 주차별로 합산하여 하나의 PENALTY 청구 항목으로 저 장한다.

커피는 사용자가 커피 메뉴를 선택하면 하나의 COFFEE 청구 항목으로 저장한다.

관리자 승인 없이 사용자가 “납부했어요”를 누르면 status = PAID 로 변경된다.

계좌가 바뀌어도 과거 기록을 보존하기 위해 계좌 스냅샷을 저장한다.

계좌 스냅샷은 사진이 아니라 텍스트 복사본이다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|campus_id|bigint|캠퍼스 ID|
|user_id|bigint|사용자 ID|
|payment_category|enum/varchar|PENALTY, COFFEE|
|payment_account_id|bigint|납부 계좌 ID|
|bank_name_snapshot|varchar|당시 은행명|
|account_number_snapshot|varchar|당시 계좌번호|
|account_holder_snapshot|varchar|당시 예금주|
|source_type|enum/varchar|DEVOTION_RECORD, POLL_RESPONSE|
|source_id|bigint|원본 데이터 ID|
|title|varchar|청구 제목|
|reason|varchar|청구 사유|
|amount|int|청구 금액|
|status|enum/varchar|UNPAID, PAID, WAIVED, CANCELED|
|due_date|date|납부 기한|
|paid_at|timestamptz|납부 완료 처리 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

예시:

|payment_category|title|reason|amount|status|
|---|---|---|---|---|
|PENALTY|2026년 6월 2주차 벌금|큐티 2회 부족, 지각 5분|2500|UNPAID|
|COFFEE|아이스 아메리카노|컴포즈커피 주문|1800|UNPAID|

중복 방지 기준:

```
campus_id + user_id + payment_category + source_type + source_id unique
```

벌금의 경우:

```
payment_category = PENALTY
source_type = DEVOTION_RECORD
source_id = weekly_devotion_records.id
```

커피의 경우:

```
payment_category = COFFEE
source_type = POLL_RESPONSE
source_id = poll_responses.id
```

## user_fcm_tokens

사용자별 FCM 토큰을 저장한다.

한 사용자가 여러 기기를 사용할 수 있으므로 별도 테이블로 관리한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|user_id|bigint|사용자 ID|
|token|text|FCM 토큰|
|device_type|enum/varchar|ANDROID, IOS, WEB|
|is_active|boolean|활성 여부|
|last_used_at|timestamptz|마지막 사용 시간|
|created_at|timestamptz|생성일|
|updated_at|timestamptz|수정일|

제약 조건:

```
token unique
```

## notification_logs

푸시 알림 발송 이력을 저장한다.

배치는 정산 생성이 아니라 알림 발송에 사용한다.

|컬럼명|타입|설명|
|---|---|---|
|id|bigint|PK|
|user_id|bigint|수신 사용자 ID|
|campus_id|bigint|캠퍼스 ID|
|notification_type|enum/varchar|알림 유형|
|target_week_start_date|date|대상 주차|
|target_id|bigint|관련 대상 ID|
|title|varchar|알림 제목|
|body|text|알림 내용|
|send_status|enum/varchar|PENDING, SENT, FAILED, SKIPPED|
|failure_reason|text|실패 사유|
|sent_at|timestamptz|발송 시간|
|created_at|timestamptz|생성일|

## 12. 주요 기능별 데이터 흐름

## 경건생활 하루별 체크

사용자가 캘린더에서 날짜 선택 → 큐티, 기도, 말씀읽기 체크 → devotion_daily_checks 저장 또는 수정

프론트는 devotion_daily_checks 를 조회해서 캘린더 형식으로 보여준다.

## 주간 경건생활 제출과 벌금 생성

```
사용자가 주간 제출 버튼 클릭
-> devotion_daily_checks 합산
-> weekly_devotion_records에 count 저장
-> penalty_rules 기준으로 벌금 계산
-> 벌금 총액 합산
-> charge_items에 PENALTY 한 줄 생성 또는 갱신
```

예시:

```
큐티 2회 부족 = 1,000원
기도 부족 없음 = 0원
말씀읽기 부족 없음 = 0원
토요 목자모임 5분 지각 = 1,500원
총 벌금 = 2,500원
```

생성되는 청구 항목:

```
PENALTY / 2026년 6월 2주차 벌금 / 2,500원 / UNPAID
```

## 커피 투표 생성

COFFEE 담당자 또는 ADMIN/OWNER가 커피 투표 생성 → Spring ComposeMenu enum에서 메뉴 선택 → poll_options에 content, compose_menu_code, price_amount 저장

## 커피 주문과 청구 생성

사용자가 커피 메뉴 선택 → poll_responses 저장 → poll_options.price_amount 조회 → 금액이 0보다 크면 charge_items에 COFFEE 청구 생성

예시:

```
아이스 아메리카노 선택
-> COFFEE / 아이스 아메리카노 / 1,800원 / UNPAID
```

안 마셔요 처럼 price_amount $=0$ 인 선택지는 청구 항목을 생성하지 않는다.

## 납부 처리

사용자가 계좌이체 → 앱에서 “납부했어요” 클릭 → charge_items.status = PAID → charge_items.paid_at = 현재 시간

관리자 승인 과정은 없다.

## 계좌 변경

관리자가 새 계좌 등록 → 기존 같은 account_type의 계좌 is_active = false → 기존 계좌 deactivated_at = 현재 시간 → 새 계좌 is_active = true

현재 계좌 조회는 is_active = true 기준으로 한다.

## 커피 담당자 변경

관리자가 새 커피 담당자 지정 → 기존 COFFEE 담당자 is_active = false → 기존 담당자 revoked_at $=$ 현재 시간

→ 새 담당자 is_active = true → 새 담당자 assigned_at = 현재 시간

현재 담당자 조회는 is_active = true 기준으로 한다.

## 13. 투표 현황 조회 설계

현재 설계로 투표 현황 조회가 가능하다.

핵심 테이블은 다음과 같다.

```
polls
poll_options
poll_responses
users
campus_members
```

## 선택지별 투표 현황

```
SELECT
    po.id AS option_id,
    po.content AS option_name,
    po.price_amount,
    COUNT(pr.id) AS response_count
FROM poll_options po
LEFT JOIN poll_responses pr ON pr.option_id = po.id
WHERE po.poll_id = :pollId
GROUP BY po.id, po.content, po.price_amount
ORDER BY po.sort_order;
```

## 사용자별 응답 현황

```
SELECT
    u.id AS user_id,
    u.name AS user_name,
    po.content AS selected_option,
    po.price_amount,
    pr.responded_at
FROM poll_responses pr
JOIN users u ON u.id = pr.user_id
JOIN poll_options po ON po.id = pr.option_id
```

```
WHERE pr.poll_id = :pollId
ORDER BY pr.responded_at;
```

## 미응답자 조회

```
SELECT
    u.id,
    u.name
FROM campus_members cm
JOIN users u ON u.id = cm.user_id
LEFT JOIN poll_responses pr
    ON pr.user_id = cm.user_id
    AND pr.poll_id = :pollId
WHERE cm.campus_id = :campusld
AND cm.status = 'ACTIVE'
AND pr.id IS NULL;
```

## 투표 진행률 조회

```
SELECT
    COUNT(DISTINCT pr.user_id) AS responded_count,
    COUNT(DISTINCT cm.user_id) AS total_member_count
FROM campus_members cm
LEFT JOIN poll_responses pr
    ON pr.user_id = cm.user_id
    AND pr.poll_id = :pollId
WHERE cm.campus_id = :campusld
    AND cm.status = 'ACTIVE';
```

## 커피 주문 총액 조회

```
SELECT
    SUM(po.price_amount) AS total_price
FROM poll_responses pr
JOIN poll_options po ON po.id = pr.option_id
WHERE pr.poll_id = :pollId;
```

## 14. 배치 역할

배치는 정산 생성에 사용하지 않는다.

배치는 알림에만 사용한다.

```
일요일 경건생활 체크 알림
월요일 미체크자 알림
수요예배 투표 시작 알림
수요예배 투표 미응답자 알림
토요 목자모임 투표 시작 알림
토요 목자모임 투표 미응답자 알림
커피 투표 시작 알림
커피 투표 미응답자 알림
미납 charge_items 보유자 알림
```

## 미체크자 조회 기준

```
활성 campus_members 중
해당 week_start_date의 weekly_devotion_records가 없거나
submitted_at이 null인 사용자
```

## 미납자 조회 기준

```
charge_items.status = UNPAID
```

## 15. dbdiagram.io용 DBML 초안

```
Enum member_role {
  OWNER
  ADMIN
  MEMBER
}

Enum duty_type {
  COFFEE
}

Enum member_status {
  ACTIVE
  PENDING
  INACTIVE
}

Enum penalty_rule_type {
  QUIET_TIME
  PRAYER
  BIBLE_READING
  SATURDAY_LATE
}

Enum penalty_calculation_type {
  MISSING_COUNT
  LATE_MINUTE
}

Enum payment_category {
  PENALTY
  COFFEE
}

Enum poll_type {
  WED_SERVICE
  SATURDAY_LEADER
  COFFEE
  CUSTOM
}

Enum selection_type {
  SINGLE
  MULTIPLE
}

Enum charge_generation_type {
  NONE
  OPTION_PRICE
}

Enum poll_status {
  SCHEDULED
  OPEN
  CLOSED
}

Enum charge_status {
  UNPAID
  PAID
  WAIVED
  CANCELED
}

Enum charge_source_type {
  DEVOTION_RECORD
  POLL_RESPONSE
}

Enum device_type {
  ANDROID
  IOS
  WEB
}

Enum notification_type {
  DEVOTION_REMINDER
  DEVOTION_MISSING
  WED_POLL_OPEN
  WED_POLL_MISSING
  SATURDAY_POLL_OPEN
  SATURDAY_POLL_MISSING
  COFFEE_POLL_OPEN
  COFFEE_POLL_MISSING
  PAYMENT_UNPAID
  CUSTOM
}

Enum send_status {
  PENDING
  SENT
  FAILED
  SKIPPED
}

Table users {
  id bigint [pk, increment]
  name varchar(100) [not null]
  email varchar(255) [not null, unique]
  password_hash varchar(255) [not null]
  is_active boolean [not null, default: true]
  last_login_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table refresh_tokens {
  id bigint [pk, increment]
  user_id bigint [not null]
  token_hash varchar(255) [not null]
  expires_at timestamptz [not null]
  revoked_at timestamptz
  created_at timestamptz [not null]
}

Table campuses {
  id bigint [pk, increment]
  name varchar(100) [not null]
  region varchar(100)
  description text
  invite_code varchar(50) [not null, unique]
  is_active boolean [not null, default: true]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table campus_members {
  id bigint [pk, increment]
  campus_id bigint [not null]
  user_id bigint [not null]
  role member_role [not null, default: 'MEMBER']
  status member_status [not null, default: 'ACTIVE']
  joined_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]

  indexes {
    (campus_id, user_id) [unique]
  }
}

Table campus_duty_assignments {
  id bigint [pk, increment]
  campus_id bigint [not null]
  user_id bigint [not null]
  duty_type duty_type [not null]
  is_active boolean [not null, default: true]
  assigned_at timestamptz
  revoked_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table weekly_devotion_records {
  id bigint [pk, increment]
  campus_id bigint [not null]
  user_id bigint [not null]
  week_start_date date [not null]
  week_end_date date [not null]
  quiet_time_count int [not null, default: 0]
  prayer_count int [not null, default: 0]
  bible_reading_count int [not null, default: 0]
  saturday_late_minutes int [not null, default: 0]
  submitted_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]

  indexes {
    (campus_id, user_id, week_start_date) [unique]
  }
}

Table devotion_daily_checks {
  id bigint [pk, increment]
  weekly_record_id bigint [not null]
  record_date date [not null]
  quiet_time_checked boolean [not null, default: false]
  prayer_checked boolean [not null, default: false]
  bible_reading_checked boolean [not null, default: false]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]

  indexes {
    (weekly_record_id, record_date) [unique]
  }
}

Table penalty_rules {
  id bigint [pk, increment]
  campus_id bigint [not null]
  rule_type penalty_rule_type [not null]
  calculation_type penalty_calculation_type [not null]
  required_count int [not null, default: 0]
  base_amount int [not null, default: 0]
  amount_per_unit int [not null, default: 0]
  is_active boolean [not null, default: true]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table payment_accounts {
  id bigint [pk, increment]
  campus_id bigint [not null]
  account_type payment_category [not null]
  nickname varchar(100) [not null]
  bank_name varchar(100) [not null]
  account_number varchar(100) [not null]
  account_holder varchar(100) [not null]
  owner_user_id bigint
  is_active boolean [not null, default: true]
  deactivated_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table poll_templates {
  id bigint [pk, increment]
  campus_id bigint [not null]
  title varchar(200) [not null]
  poll_type poll_type [not null]
  start_day_of_week int [not null]
  start_time time [not null]
  end_day_of_week int [not null]
  end_time time [not null]
  is_active boolean [not null, default: true]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table poll_template_options {
  id bigint [pk, increment]
  template_id bigint [not null]
  content varchar(200) [not null]
  sort_order int [not null, default: 0]
}

Table polls {
  id bigint [pk, increment]
  campus_id bigint [not null]
  template_id bigint
  title varchar(200) [not null]
  poll_type poll_type [not null]
  selection_type selection_type [not null, default: 'SINGLE']
  is_anonymous boolean [not null, default: false]
  charge_generation_type charge_generation_type [not null, default: 'NONE']
  payment_category payment_category
  payment_account_id bigint
  starts_at timestamptz [not null]
  ends_at timestamptz [not null]
  status poll_status [not null, default: 'SCHEDULED']
  created_by bigint
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table poll_options {
  id bigint [pk, increment]
  poll_id bigint [not null]
  content varchar(200) [not null]
  compose_menu_code varchar(100)
  price_amount int [not null, default: 0]
  sort_order int [not null, default: 0]
}

Table poll_responses {
  id bigint [pk, increment]
  poll_id bigint [not null]
  option_id bigint [not null]
  user_id bigint [not null]
  memo text
  responded_at timestamptz [not null]
  created_at timestamptz [not null]
  updated_at timestamptz [not null]

  indexes {
    (poll_id, user_id) [unique]
  }
}

Table charge_items {
  id bigint [pk, increment]
  campus_id bigint [not null]
  user_id bigint [not null]
  payment_category payment_category [not null]
  payment_account_id bigint
  bank_name_snapshot varchar(100)
  account_number_snapshot varchar(100)
  account_holder_snapshot varchar(100)
  source_type charge_source_type [not null]
  source_id bigint
  title varchar(200) [not null]
  reason varchar(255)
  amount int [not null, default: 0]
  status charge_status [not null, default: 'UNPAID']
  due_date date
  paid_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]

  indexes {
    (campus_id, user_id, payment_category, source_type, source_id) [unique]
  }
}

Table user_fcm_tokens {
  id bigint [pk, increment]
  user_id bigint [not null]
  token text [not null, unique]
  device_type device_type [not null]
  is_active boolean [not null, default: true]
  last_used_at timestamptz
  created_at timestamptz [not null]
  updated_at timestamptz [not null]
}

Table notification_logs {
  id bigint [pk, increment]
  user_id bigint [not null]
  campus_id bigint
  notification_type notification_type [not null]
  target_week_start_date date
  target_id bigint
  title varchar(200) [not null]
  body text [not null]
  send_status send_status [not null, default: 'PENDING']
  failure_reason text
  sent_at timestamptz
  created_at timestamptz [not null]
}

Ref: refresh_tokens.user_id > users.id

Ref: campus_members.campus_id > campuses.id
Ref: campus_members.user_id > users.id

Ref: campus_duty_assignments.campus_id > campuses.id
Ref: campus_duty_assignments.user_id > users.id

Ref: weekly_devotion_records.campus_id > campuses.id
Ref: weekly_devotion_records.user_id > users.id

Ref: devotion_daily_checks.weekly_record_id > weekly_devotion_records.id

Ref: penalty_rules.campus_id > campuses.id

Ref: payment_accounts.campus_id > campuses.id
Ref: payment_accounts.owner_user_id > users.id

Ref: poll_templates.campus_id > campuses.id
Ref: poll_template_options.template_id > poll_templates.id

Ref: polls.campus_id > campuses.id
Ref: polls.template_id > poll_templates.id
Ref: polls.payment_account_id > payment_accounts.id
Ref: polls.created_by > users.id

Ref: poll_options.poll_id > polls.id

Ref: poll_responses.poll_id > polls.id
Ref: poll_responses.option_id > poll_options.id
Ref: poll_responses.user_id > users.id

Ref: charge_items.campus_id > campuses.id
Ref: charge_items.user_id > users.id
Ref: charge_items.payment_account_id > payment_accounts.id

Ref: user_fcm_tokens.user_id > users.id

Ref: notification_logs.user_id > users.id
Ref: notification_logs.campus_id > campuses.id
```

## 16. 최종 결론

이 설계에서는 캠퍼스가 곧 실제 운영 단위이다.

따라서 app_groups 는 제거하고, 모든 기능을 campus_id 기준으로 관리한다.

기존 group_members 는 campus_members 로 변경한다.

기존 group_duty_assignments 는 campus_duty_assignments 로 변경한다.

점심 기능은 MVP 에서 제외한다.

청구 항목은 PENALTY , COFFEE 두 가지만 사용한다.

벌금은 주차별로 합산해서 charge_items 에 PENALTY 한 줄로 저장한다.

커피는 투표 응답을 기준으로 charge_items 에 COFFEE 한 줄로 저장한다.

경건생활은 하루별 체크를 지원하기 위해 devotion_daily_checks 를 두고, 최종 제출과 벌금 계산 기준은 weekly_devotion_records 로 관리한다.

계좌와 커피 담당자는 시작일/종료일 없이 is_active 로 현재 사용 여부를 관리한다.

컴포즈커피 메뉴는 DB enum이 아니라 Spring enum으로 관리하고, DB에는 compose_menu_code, content, price_amount 만 저장한다.

투표 현황은 poll_options, poll_responses, users, campus_members 를 조인해서 선택지별 현황, 사용자별 응답, 미응답자, 진행률, 커피 총액을 조회할 수 있다.

이 구조가 현재 FaithLog MVP 기준으로 가장 단순하고 현실적인 설계이다.