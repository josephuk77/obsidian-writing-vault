# FaithLog API 명세서

## 1. 프로젝트 개요

FaithLog는 교회 캠퍼스 단위로 경건생활 체크, 벌금 관리, 커피 주문 투표, 알림 발송을 관리하는 웹 서비스이다.

기존에는 카카오톡 메시지와 수기 정산으로 운영되던 경건생활 체크와 벌금 관리를 웹 서비스로 전환하여, 사용자는 자신의 경건생활 기록과 납부 상태를 확인하고, 관리자는 캠퍼스별 구성원, 벌금 규칙, 투표, 알림을 통합 관리할 수 있도록 설계하였다.

---

## 2. API 설계 방향

### 2.1 핵심 설계 기준

- 서비스 전체 권한과 캠퍼스 내부 역할을 분리한다.
    
- 사용자는 여러 캠퍼스에 소속될 수 있다.
    
- 캠퍼스별로 벌금 규칙, 납부 계좌, 투표, 알림을 독립적으로 관리한다.
    
- 경건생활은 하루 단위 체크와 주간 일괄 제출을 모두 지원한다.
    
- 벌금과 커피비는 `charge_items`로 통합 관리한다.
    
- 사용자는 본인의 청구 항목을 직접 납부 완료 처리할 수 있다.
    
- 관리자는 투표별 미참여자를 조회하고 알림을 발송할 수 있다.
    
- Access Token과 Refresh Token은 HttpOnly Cookie로 관리한다.
    

---

## 3. 공통 규칙

### Base URL

```http
/api/v1
```

### 인증 방식

로그인 성공 시 Access Token과 Refresh Token을 HttpOnly Cookie로 내려준다.

```http
Set-Cookie: accessToken=...; HttpOnly; Secure; SameSite=Lax; Path=/api/v1; Max-Age=1800
Set-Cookie: refreshToken=...; HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth/refresh; Max-Age=1209600
```

Refresh Token은 토큰 재발급 API에만 전송되도록 Cookie Path를 제한한다.

```http
Path=/api/v1/auth/refresh
```

### 공통 성공 응답

```json
{
  "success": true,
  "data": {},
  "message": "요청이 성공했습니다."
}
```

### 공통 실패 응답

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "요청 권한이 없습니다."
  }
}
```

---

## 4. 권한 정책

### 4.1 서비스 전체 권한

|Role|설명|
|---|---|
|`USER`|일반 사용자|
|`MANAGER`|캠퍼스 생성 가능|
|`ADMIN`|전체 관리자, 사용자 권한 변경 가능|

### 4.2 캠퍼스 내부 역할

|Campus Role|설명|
|---|---|
|`MINISTER`|전도사님|
|`ELDER`|엘더|
|`CAMPUS_LEADER`|캠장|
|`MEMBER`|일반 캠퍼스원|

### 4.3 권한 기준

|기능|허용 권한|
|---|---|
|회원가입|전체|
|캠퍼스 가입|로그인 사용자|
|캠퍼스 생성|`MANAGER`, `ADMIN`|
|서비스 전체 권한 변경|`ADMIN`|
|캠퍼스 정보 수정|`ADMIN`, `MINISTER`, `ELDER`, `CAMPUS_LEADER`|
|캠퍼스 내부 역할 변경|`ADMIN`, `MINISTER`, `ELDER`, `CAMPUS_LEADER`|
|커피 담당 관리|`ADMIN`, `MINISTER`, `ELDER`, `CAMPUS_LEADER`|
|벌금 규칙 관리|`ADMIN`, `MINISTER`, `ELDER`, `CAMPUS_LEADER`|
|투표 생성 및 결과 조회|`ADMIN`, `MINISTER`, `ELDER`, `CAMPUS_LEADER`|
|본인 경건생활 체크|캠퍼스 소속 사용자|
|본인 청구 항목 납부 완료 처리|청구 항목 소유자|

---

## 5. 인증 API

## 5.1 회원가입

```http
POST /auth/signup
```

### Request

```json
{
  "name": "이승욱",
  "email": "user@example.com",
  "password": "1234"
}
```

### Response

```json
{
  "id": 1,
  "name": "이승욱",
  "email": "user@example.com",
  "role": "USER",
  "isActive": true
}
```

---

## 5.2 로그인

```http
POST /auth/login
```

### Request

```json
{
  "email": "user@example.com",
  "password": "1234"
}
```

### Response Body

```json
{
  "id": 1,
  "name": "이승욱",
  "email": "user@example.com",
  "role": "USER",
  "isActive": true,
  "campusMemberships": [
    {
      "campusMemberId": 1,
      "campusId": 1,
      "campusName": "1캠",
      "region": "분당",
      "campusRole": "MEMBER",
      "status": "ACTIVE"
    }
  ]
}
```

### Set-Cookie

```http
Set-Cookie: accessToken=access-token; HttpOnly; Secure; SameSite=Lax; Path=/api/v1; Max-Age=1800
Set-Cookie: refreshToken=refresh-token; HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth/refresh; Max-Age=1209600
```

---

## 5.3 토큰 재발급

```http
POST /auth/refresh
```

### Request

Request Body 없음. Refresh Token은 Cookie로 전달된다.

### Response

```json
{
  "message": "토큰이 재발급되었습니다."
}
```

### Set-Cookie

```http
Set-Cookie: accessToken=new-access-token; HttpOnly; Secure; SameSite=Lax; Path=/api/v1; Max-Age=1800
Set-Cookie: refreshToken=new-refresh-token; HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth/refresh; Max-Age=1209600
```

### 처리 기준

1. Cookie에서 refreshToken을 조회한다.
    
2. DB에는 원본 토큰이 아닌 `token_hash`를 저장한다.
    
3. 유효기간과 `revoked_at` 여부를 검증한다.
    
4. Access Token을 재발급한다.
    
5. Refresh Token Rotation을 적용하는 경우 Refresh Token도 재발급한다.
    

---

## 5.4 로그아웃

```http
POST /auth/logout
```

### Response

```json
{
  "message": "로그아웃되었습니다."
}
```

### Set-Cookie

```http
Set-Cookie: accessToken=; HttpOnly; Secure; SameSite=Lax; Path=/api/v1; Max-Age=0
Set-Cookie: refreshToken=; HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth/refresh; Max-Age=0
```

---

# 6. 사용자 API

## 6.1 내 정보 조회

```http
GET /users/me
```

### Response

```json
{
  "id": 1,
  "name": "이승욱",
  "email": "user@example.com",
  "role": "USER",
  "isActive": true,
  "lastLoginAt": "2026-06-12T10:30:00",
  "campusMemberships": [
    {
      "campusMemberId": 1,
      "campusId": 1,
      "campusName": "1캠",
      "region": "분당",
      "campusRole": "MEMBER",
      "status": "ACTIVE"
    }
  ]
}
```

---

## 6.2 관리자 - 사용자 전체 권한 변경

```http
PATCH /admin/users/{userId}/role
```

### 권한

```text
ADMIN
```

### Request

```json
{
  "role": "MANAGER"
}
```

### Response

```json
{
  "userId": 3,
  "name": "김OO",
  "email": "kim@example.com",
  "role": "MANAGER"
}
```

### 처리 기준

- 일반 사용자의 서비스 전체 권한 변경은 `ADMIN`만 가능하다.
    
- `MANAGER`는 캠퍼스 생성 권한을 가진다.
    
- 캠퍼스 내부 역할 변경과 서비스 전체 권한 변경은 별도의 API로 분리한다.
    

---

# 7. 캠퍼스 API

## 7.1 캠퍼스 생성

```http
POST /campuses
```

### 권한

```text
MANAGER, ADMIN
```

### Request

```json
{
  "name": "1캠",
  "region": "분당",
  "description": "분당 1캠퍼스"
}
```

### Response

```json
{
  "id": 1,
  "name": "1캠",
  "region": "분당",
  "description": "분당 1캠퍼스",
  "inviteCode": "BD-1CAMP-A8F2",
  "isActive": true
}
```

### 처리 기준

1. 로그인 사용자의 `users.role`을 확인한다.
    
2. `MANAGER` 또는 `ADMIN`이면 캠퍼스를 생성한다.
    
3. `invite_code`를 자동 생성한다.
    
4. 생성자를 해당 캠퍼스의 `CAMPUS_LEADER`로 등록한다.
    

---

## 7.2 캠퍼스 목록 조회

```http
GET /campuses
```

### Query Parameters

|이름|설명|
|---|---|
|`name`|캠퍼스 이름|
|`region`|지역|
|`isActive`|활성 여부|

### Example

```http
GET /campuses?region=분당
GET /campuses?name=1캠
GET /campuses?region=분당&name=1캠
```

### Response

```json
[
  {
    "id": 1,
    "name": "1캠",
    "region": "분당",
    "description": "분당 1캠퍼스",
    "isActive": true
  }
]
```

---

## 7.3 내 캠퍼스 목록 조회

```http
GET /campuses/me
```

### Response

```json
[
  {
    "campusMemberId": 1,
    "campusId": 1,
    "campusName": "1캠",
    "region": "분당",
    "campusRole": "CAMPUS_LEADER",
    "status": "ACTIVE"
  }
]
```

---

## 7.4 캠퍼스 상세 조회

```http
GET /campuses/{campusId}
```

### Response

```json
{
  "id": 1,
  "name": "1캠",
  "region": "분당",
  "description": "분당 1캠퍼스",
  "inviteCode": "BD-1CAMP-A8F2",
  "isActive": true,
  "createdAt": "2026-06-12T10:30:00",
  "updatedAt": "2026-06-12T10:30:00"
}
```

---

## 7.5 캠퍼스 수정

```http
PATCH /campuses/{campusId}
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Request

```json
{
  "name": "1캠",
  "region": "분당",
  "description": "분당 청년부 1캠퍼스",
  "isActive": true
}
```

---

## 7.6 초대코드 재발급

```http
POST /campuses/{campusId}/invite-code/refresh
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Response

```json
{
  "campusId": 1,
  "inviteCode": "BD-1CAMP-K92A"
}
```

---

## 7.7 초대코드로 캠퍼스 가입

```http
POST /campuses/join
```

### Request

```json
{
  "inviteCode": "BD-1CAMP-A8F2"
}
```

### Response

```json
{
  "campusMemberId": 10,
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "campusRole": "MEMBER",
  "status": "ACTIVE",
  "joinedAt": "2026-06-12T10:30:00"
}
```

### 처리 기준

1. `invite_code`로 캠퍼스를 조회한다.
    
2. 사용자가 이미 해당 캠퍼스에 가입되어 있는지 확인한다.
    
3. 가입되어 있지 않다면 `campus_members`를 생성한다.
    
4. 기본 `campusRole`은 `MEMBER`로 설정한다.
    
5. 가입 승인 없이 바로 `ACTIVE` 상태로 등록한다.
    

---

# 8. 캠퍼스 멤버 API

## 8.1 관리자 - 캠퍼스 멤버 전체 조회

```http
GET /admin/campus-members
```

### Query Parameters

|이름|설명|
|---|---|
|`campusName`|캠퍼스 이름|
|`region`|지역|
|`campusRole`|캠퍼스 내부 역할|
|`status`|멤버 상태|
|`keyword`|이름 또는 이메일 검색|

### Example

```http
GET /admin/campus-members?campusName=1캠
GET /admin/campus-members?region=분당
GET /admin/campus-members?campusName=1캠&campusRole=ELDER
```

### Response

```json
[
  {
    "campusMemberId": 1,
    "campusId": 1,
    "campusName": "1캠",
    "region": "분당",
    "userId": 1,
    "name": "이승욱",
    "email": "user@example.com",
    "userRole": "USER",
    "campusRole": "MEMBER",
    "status": "ACTIVE",
    "joinedAt": "2026-06-12T10:30:00"
  }
]
```

---

## 8.2 관리자 - 특정 캠퍼스 멤버 조회

```http
GET /admin/campuses/{campusId}/members
```

### Query Parameters

|이름|설명|
|---|---|
|`campusRole`|캠퍼스 내부 역할|
|`status`|멤버 상태|
|`keyword`|이름 또는 이메일 검색|

### Response

```json
[
  {
    "campusMemberId": 1,
    "userId": 1,
    "name": "이승욱",
    "email": "user@example.com",
    "userRole": "USER",
    "campusRole": "MEMBER",
    "status": "ACTIVE",
    "joinedAt": "2026-06-12T10:30:00"
  }
]
```

---

## 8.3 관리자 - 캠퍼스 내부 역할 변경

```http
PATCH /admin/campuses/{campusId}/members/{campusMemberId}/campus-role
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Request

```json
{
  "campusRole": "ELDER"
}
```

### Response

```json
{
  "campusMemberId": 10,
  "userId": 3,
  "name": "김OO",
  "campusId": 1,
  "campusName": "1캠",
  "campusRole": "ELDER",
  "status": "ACTIVE"
}
```

---

## 8.4 관리자 - 캠퍼스 멤버 비활성화

```http
PATCH /admin/campuses/{campusId}/members/{campusMemberId}/inactive
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Response

```json
{
  "campusMemberId": 10,
  "status": "INACTIVE"
}
```

---

# 9. 커피 담당 API

## 9.1 캠퍼스 커피 담당 조회

```http
GET /campuses/{campusId}/duty-assignments
```

### Query Parameters

|이름|설명|
|---|---|
|`dutyType`|담당 유형|
|`isActive`|활성 여부|

### Example

```http
GET /campuses/1/duty-assignments?dutyType=COFFEE&isActive=true
```

### Response

```json
[
  {
    "id": 1,
    "campusId": 1,
    "campusName": "1캠",
    "region": "분당",
    "userId": 3,
    "name": "김OO",
    "email": "coffee@example.com",
    "dutyType": "COFFEE",
    "isActive": true,
    "assignedAt": "2026-06-01T09:00:00",
    "revokedAt": null
  }
]
```

---

## 9.2 관리자 - 커피 담당 등록

```http
POST /admin/campuses/{campusId}/duty-assignments
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Request

```json
{
  "userId": 3,
  "dutyType": "COFFEE"
}
```

### Response

```json
{
  "id": 1,
  "campusId": 1,
  "userId": 3,
  "name": "김OO",
  "dutyType": "COFFEE",
  "isActive": true,
  "assignedAt": "2026-06-12T10:30:00"
}
```

---

## 9.3 관리자 - 커피 담당 해제

```http
PATCH /admin/duty-assignments/{assignmentId}/revoke
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Response

```json
{
  "id": 1,
  "isActive": false,
  "revokedAt": "2026-06-12T10:30:00"
}
```

---

# 10. 경건생활 API

## 10.1 내 이번 주 경건생활 조회

```http
GET /campuses/{campusId}/devotions/me/current-week
```

### Response

```json
{
  "weeklyRecordId": 1,
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "userId": 1,
  "weekStartDate": "2026-06-08",
  "weekEndDate": "2026-06-14",
  "quietTimeCount": 3,
  "prayerCount": 4,
  "bibleReadingCount": 2,
  "saturdayLateMinutes": 5,
  "submittedAt": null,
  "dailyChecks": [
    {
      "id": 1,
      "recordDate": "2026-06-08",
      "quietTimeChecked": true,
      "prayerChecked": true,
      "bibleReadingChecked": false
    }
  ]
}
```

---

## 10.2 내 특정 주 경건생활 조회

```http
GET /campuses/{campusId}/devotions/me/weeks/{weekStartDate}
```

### Example

```http
GET /campuses/1/devotions/me/weeks/2026-06-08
```

---

## 10.3 하루 경건생활 체크

```http
PUT /campuses/{campusId}/devotions/me/days/{recordDate}
```

### Example

```http
PUT /campuses/1/devotions/me/days/2026-06-08
```

### Request

```json
{
  "quietTimeChecked": true,
  "prayerChecked": true,
  "bibleReadingChecked": false
}
```

### Response

```json
{
  "weeklyRecordId": 1,
  "recordDate": "2026-06-08",
  "quietTimeChecked": true,
  "prayerChecked": true,
  "bibleReadingChecked": false,
  "quietTimeCount": 1,
  "prayerCount": 1,
  "bibleReadingCount": 0,
  "submittedAt": null
}
```

### 처리 기준

1. `recordDate` 기준으로 `weekStartDate`를 계산한다.
    
2. `weekly_devotion_records`가 없으면 생성한다.
    
3. `devotion_daily_checks`에 해당 날짜 row가 없으면 생성한다.
    
4. 이미 있으면 수정한다.
    
5. 주간 count를 재계산한다.
    
6. 하루 체크 API에서는 `submitted_at`을 변경하지 않는다.
    
7. 하루 체크 API에서는 `charge_items`를 생성하지 않는다.
    

---

## 10.4 주간 경건생활 일괄 저장 및 제출

```http
PUT /campuses/{campusId}/devotions/me/weeks/{weekStartDate}
```

### Request

```json
{
  "dailyChecks": [
    {
      "recordDate": "2026-06-08",
      "quietTimeChecked": true,
      "prayerChecked": true,
      "bibleReadingChecked": false
    },
    {
      "recordDate": "2026-06-09",
      "quietTimeChecked": true,
      "prayerChecked": false,
      "bibleReadingChecked": true
    }
  ],
  "saturdayLateMinutes": 5,
  "submit": true
}
```

### Response

```json
{
  "weeklyRecordId": 1,
  "weekStartDate": "2026-06-08",
  "weekEndDate": "2026-06-14",
  "quietTimeCount": 2,
  "prayerCount": 1,
  "bibleReadingCount": 1,
  "saturdayLateMinutes": 5,
  "submittedAt": "2026-06-12T22:00:00",
  "generatedCharges": [
    {
      "id": 1,
      "paymentCategory": "PENALTY",
      "sourceType": "DEVOTION_RECORD",
      "sourceId": 1,
      "title": "큐티 미달 벌금",
      "reason": "필수 5회 중 2회 제출",
      "amount": 1500,
      "status": "UNPAID"
    }
  ]
}
```

### 처리 기준

1. `weekly_devotion_records`를 생성 또는 수정한다.
    
2. 월요일부터 일요일까지 7일치 `devotion_daily_checks` row를 생성 또는 수정한다.
    
3. 요청에 없는 날짜는 `false` 기본값으로 생성한다.
    
4. `quiet_time_count`, `prayer_count`, `bible_reading_count`를 재계산한다.
    
5. `saturday_late_minutes`를 저장한다.
    
6. `submit = true`이면 `submitted_at`을 갱신한다.
    
7. `submit = true`이면 `penalty_rules` 기준으로 `charge_items`를 생성 또는 갱신한다.
    

---

## 10.5 내 월간 경건생활 통계 조회

```http
GET /campuses/{campusId}/devotions/me/monthly-summary
```

### Query Parameters

|이름|설명|
|---|---|
|`year`|조회 연도|
|`month`|조회 월|

### Example

```http
GET /campuses/1/devotions/me/monthly-summary?year=2026&month=6
```

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "userId": 1,
  "name": "이승욱",
  "year": 2026,
  "month": 6,
  "devotion": {
    "quietTimeCount": 18,
    "prayerCount": 20,
    "bibleReadingCount": 15,
    "saturdayLateMinutes": 12
  },
  "weeklyRecords": [
    {
      "weeklyRecordId": 1,
      "weekStartDate": "2026-06-01",
      "weekEndDate": "2026-06-07",
      "quietTimeCount": 4,
      "prayerCount": 5,
      "bibleReadingCount": 3,
      "saturdayLateMinutes": 0,
      "submittedAt": "2026-06-07T22:00:00"
    }
  ]
}
```

---

# 11. 관리자 경건생활 API

## 11.1 주차별 경건생활 현황 조회

```http
GET /admin/campuses/{campusId}/devotions/weeks/{weekStartDate}
```

### Query Parameters

|이름|설명|
|---|---|
|`submitted`|제출 여부|
|`keyword`|이름 또는 이메일 검색|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "weekStartDate": "2026-06-08",
  "weekEndDate": "2026-06-14",
  "records": [
    {
      "weeklyRecordId": 1,
      "userId": 1,
      "name": "이승욱",
      "email": "user@example.com",
      "quietTimeCount": 3,
      "prayerCount": 4,
      "bibleReadingCount": 2,
      "saturdayLateMinutes": 5,
      "submitted": true,
      "submittedAt": "2026-06-12T22:00:00",
      "totalPenaltyAmount": 4500
    }
  ]
}
```

---

## 11.2 주차별 경건생활 미제출자 조회

```http
GET /admin/campuses/{campusId}/devotions/weeks/{weekStartDate}/missing
```

### Response

```json
[
  {
    "userId": 2,
    "name": "김OO",
    "email": "kim@example.com",
    "campusMemberId": 5,
    "campusName": "1캠",
    "region": "분당"
  }
]
```

### 조회 기준

```text
campus_members.status = ACTIVE 인 사용자 중
weekly_devotion_records가 없거나 submitted_at이 null인 사용자
```

---

## 11.3 관리자 - 특정 회원 월간 통계 조회

```http
GET /admin/campuses/{campusId}/members/{userId}/monthly-summary
```

### Query Parameters

|이름|설명|
|---|---|
|`year`|조회 연도|
|`month`|조회 월|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "userId": 1,
  "name": "이승욱",
  "email": "user@example.com",
  "year": 2026,
  "month": 6,
  "devotion": {
    "quietTimeCount": 18,
    "prayerCount": 20,
    "bibleReadingCount": 15,
    "saturdayLateMinutes": 12
  },
  "charges": {
    "totalPaidAmount": 43000,
    "monthlyTotalChargeAmount": 11500,
    "monthlyPaidAmount": 8500,
    "monthlyUnpaidAmount": 3000
  }
}
```

---

# 12. 벌금 규칙 API

## 12.1 캠퍼스 벌금 규칙 조회

```http
GET /campuses/{campusId}/penalty-rules
```

### Response

```json
[
  {
    "id": 1,
    "ruleType": "QUIET_TIME",
    "calculationType": "MISSING_COUNT",
    "requiredCount": 5,
    "baseAmount": 0,
    "amountPerUnit": 500,
    "isActive": true
  },
  {
    "id": 4,
    "ruleType": "SATURDAY_LATE",
    "calculationType": "LATE_MINUTE",
    "requiredCount": 0,
    "baseAmount": 1000,
    "amountPerUnit": 100,
    "isActive": true
  }
]
```

---

## 12.2 관리자 - 벌금 규칙 생성

```http
POST /admin/campuses/{campusId}/penalty-rules
```

### Request

```json
{
  "ruleType": "QUIET_TIME",
  "calculationType": "MISSING_COUNT",
  "requiredCount": 5,
  "baseAmount": 0,
  "amountPerUnit": 500
}
```

---

## 12.3 관리자 - 벌금 규칙 수정

```http
PATCH /admin/penalty-rules/{ruleId}
```

### Request

```json
{
  "requiredCount": 5,
  "baseAmount": 0,
  "amountPerUnit": 500,
  "isActive": true
}
```

---

# 13. 납부 계좌 API

## 13.1 캠퍼스 납부 계좌 조회

```http
GET /campuses/{campusId}/payment-accounts
```

### Query Parameters

|이름|설명|
|---|---|
|`accountType`|`PENALTY`, `COFFEE`|
|`isActive`|활성 여부|

### Response

```json
[
  {
    "id": 1,
    "accountType": "PENALTY",
    "nickname": "1캠 벌금 계좌",
    "bankName": "카카오뱅크",
    "accountNumber": "3333-00-0000000",
    "accountHolder": "이승욱",
    "ownerUserId": 1,
    "isActive": true
  }
]
```

---

## 13.2 관리자 - 납부 계좌 생성

```http
POST /admin/campuses/{campusId}/payment-accounts
```

### Request

```json
{
  "accountType": "PENALTY",
  "nickname": "1캠 벌금 계좌",
  "bankName": "카카오뱅크",
  "accountNumber": "3333-00-0000000",
  "accountHolder": "이승욱",
  "ownerUserId": 1
}
```

---

## 13.3 관리자 - 납부 계좌 비활성화

```http
PATCH /admin/payment-accounts/{accountId}/deactivate
```

---

# 14. 투표 템플릿 API

## 14.1 관리자 - 투표 템플릿 생성

```http
POST /admin/campuses/{campusId}/poll-templates
```

### Request

```json
{
  "title": "수요예배 참석 투표",
  "pollType": "WED_SERVICE",
  "startDayOfWeek": 1,
  "startTime": "09:00:00",
  "endDayOfWeek": 3,
  "endTime": "18:00:00",
  "options": [
    {
      "content": "참석",
      "sortOrder": 1
    },
    {
      "content": "불참",
      "sortOrder": 2
    }
  ]
}
```

---

## 14.2 관리자 - 투표 템플릿 목록 조회

```http
GET /admin/campuses/{campusId}/poll-templates
```

---

# 15. 투표 API

## 15.1 진행 중인 투표 목록 조회

```http
GET /campuses/{campusId}/polls/active
```

### Response

```json
[
  {
    "id": 1,
    "title": "6월 12일 수요예배 참석 투표",
    "pollType": "WED_SERVICE",
    "selectionType": "SINGLE",
    "isAnonymous": false,
    "chargeGenerationType": "NONE",
    "paymentCategory": null,
    "startsAt": "2026-06-10T09:00:00",
    "endsAt": "2026-06-12T18:00:00",
    "status": "OPEN",
    "responded": true
  }
]
```

---

## 15.2 투표 상세 조회

```http
GET /campuses/{campusId}/polls/{pollId}
```

### Response

```json
{
  "id": 1,
  "title": "6월 12일 수요예배 참석 투표",
  "pollType": "WED_SERVICE",
  "selectionType": "SINGLE",
  "isAnonymous": false,
  "chargeGenerationType": "NONE",
  "paymentCategory": null,
  "startsAt": "2026-06-10T09:00:00",
  "endsAt": "2026-06-12T18:00:00",
  "status": "OPEN",
  "options": [
    {
      "id": 1,
      "content": "참석",
      "composeMenuCode": null,
      "priceAmount": 0,
      "sortOrder": 1
    },
    {
      "id": 2,
      "content": "불참",
      "composeMenuCode": null,
      "priceAmount": 0,
      "sortOrder": 2
    }
  ],
  "myResponse": {
    "responseId": 1,
    "optionId": 1,
    "content": "참석",
    "memo": null,
    "respondedAt": "2026-06-12T10:00:00"
  }
}
```

---

## 15.3 투표 응답

```http
PUT /campuses/{campusId}/polls/{pollId}/responses/me
```

### Request

```json
{
  "optionId": 1,
  "memo": "참석합니다"
}
```

### Response

```json
{
  "responseId": 1,
  "pollId": 1,
  "optionId": 1,
  "content": "참석",
  "memo": "참석합니다",
  "respondedAt": "2026-06-12T10:00:00"
}
```

### 처리 기준

1. 사용자가 해당 캠퍼스의 `ACTIVE` 멤버인지 확인한다.
    
2. 투표가 `OPEN` 상태인지 확인한다.
    
3. 기존 응답이 없으면 생성한다.
    
4. 기존 응답이 있으면 선택지를 수정한다.
    
5. 커피 투표처럼 `chargeGenerationType = OPTION_PRICE`인 경우 선택한 옵션 가격으로 `charge_items`를 생성 또는 갱신한다.
    

---

## 15.4 관리자 - 투표 생성

```http
POST /admin/campuses/{campusId}/polls
```

### Request

```json
{
  "templateId": 1,
  "title": "6월 12일 수요예배 참석 투표",
  "pollType": "WED_SERVICE",
  "selectionType": "SINGLE",
  "isAnonymous": false,
  "chargeGenerationType": "NONE",
  "paymentCategory": null,
  "paymentAccountId": null,
  "startsAt": "2026-06-10T09:00:00",
  "endsAt": "2026-06-12T18:00:00",
  "options": [
    {
      "content": "참석",
      "sortOrder": 1
    },
    {
      "content": "불참",
      "sortOrder": 2
    }
  ]
}
```

---

## 15.5 관리자 - 커피 투표 생성

```http
POST /admin/campuses/{campusId}/polls
```

### Request

```json
{
  "title": "6월 12일 커피 투표",
  "pollType": "COFFEE",
  "selectionType": "SINGLE",
  "isAnonymous": false,
  "chargeGenerationType": "OPTION_PRICE",
  "paymentCategory": "COFFEE",
  "paymentAccountId": 2,
  "startsAt": "2026-06-12T09:00:00",
  "endsAt": "2026-06-12T11:00:00",
  "options": [
    {
      "content": "아메리카노",
      "composeMenuCode": "ICE_AMERICANO",
      "priceAmount": 2000,
      "sortOrder": 1
    },
    {
      "content": "안 먹어요",
      "composeMenuCode": "NONE",
      "priceAmount": 0,
      "sortOrder": 2
    }
  ]
}
```

---

## 15.6 관리자 - 투표 결과 조회

```http
GET /admin/campuses/{campusId}/polls/{pollId}/results
```

### Response

```json
{
  "pollId": 1,
  "title": "6월 12일 수요예배 참석 투표",
  "pollType": "WED_SERVICE",
  "status": "OPEN",
  "targetMemberCount": 30,
  "respondedCount": 25,
  "notRespondedCount": 5,
  "optionResults": [
    {
      "optionId": 1,
      "content": "참석",
      "count": 20,
      "priceAmount": 0,
      "totalAmount": 0
    },
    {
      "optionId": 2,
      "content": "불참",
      "count": 5,
      "priceAmount": 0,
      "totalAmount": 0
    }
  ]
}
```

---

## 15.7 관리자 - 투표 미참여자 조회

```http
GET /admin/campuses/{campusId}/polls/{pollId}/missing-members
```

### Query Parameters

|이름|설명|
|---|---|
|`keyword`|이름 또는 이메일 검색|
|`campusRole`|캠퍼스 내부 역할|

### Response

```json
{
  "pollId": 3,
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "title": "6월 12일 수요예배 참석 투표",
  "pollType": "WED_SERVICE",
  "status": "OPEN",
  "targetMemberCount": 30,
  "respondedCount": 24,
  "missingCount": 6,
  "missingMembers": [
    {
      "campusMemberId": 10,
      "userId": 5,
      "name": "김OO",
      "email": "kim@example.com",
      "campusRole": "MEMBER",
      "status": "ACTIVE"
    }
  ]
}
```

### 조회 기준

```text
campus_members.status = ACTIVE 인 사용자 중
poll_responses에 해당 poll_id, user_id 조합이 없는 사용자
```

---

# 16. 청구 및 납부 API

## 16.1 내 청구 항목 조회

```http
GET /campuses/{campusId}/charges/me
```

### Query Parameters

|이름|설명|
|---|---|
|`paymentCategory`|`PENALTY`, `COFFEE`|
|`status`|`UNPAID`, `PAID`, `WAIVED`, `CANCELED`|
|`startDate`|조회 시작일|
|`endDate`|조회 종료일|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "summary": {
    "totalAmount": 8500,
    "unpaidAmount": 6500,
    "paidAmount": 2000,
    "waivedAmount": 0,
    "canceledAmount": 0
  },
  "items": [
    {
      "id": 1,
      "paymentCategory": "PENALTY",
      "title": "큐티 미달 벌금",
      "reason": "필수 5회 중 3회 제출",
      "amount": 1000,
      "status": "UNPAID",
      "dueDate": "2026-06-16",
      "paidAt": null,
      "account": {
        "paymentAccountId": 1,
        "bankName": "카카오뱅크",
        "accountNumber": "3333-00-0000000",
        "accountHolder": "이승욱"
      },
      "source": {
        "sourceType": "DEVOTION_RECORD",
        "sourceId": 1
      }
    }
  ]
}
```

### 응답 설계 기준

DB에는 `bank_name_snapshot`, `account_number_snapshot`, `account_holder_snapshot`으로 저장하지만, API 응답에서는 프론트에서 사용하기 쉽도록 `account` 객체로 묶어서 반환한다.

---

## 16.2 내 납부 요약 조회

```http
GET /campuses/{campusId}/charges/me/summary
```

### Query Parameters

|이름|설명|
|---|---|
|`year`|조회 연도|
|`month`|조회 월|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "userId": 1,
  "name": "이승욱",
  "totalPaidAmount": 43000,
  "monthlyPaidAmount": 8500,
  "monthlyUnpaidAmount": 3000,
  "monthlyTotalChargeAmount": 11500,
  "monthlyByCategory": [
    {
      "paymentCategory": "PENALTY",
      "paidAmount": 6500,
      "unpaidAmount": 3000,
      "totalAmount": 9500
    },
    {
      "paymentCategory": "COFFEE",
      "paidAmount": 2000,
      "unpaidAmount": 0,
      "totalAmount": 2000
    }
  ]
}
```

---

## 16.3 내 청구 항목 납부 완료 처리

```http
PATCH /campuses/{campusId}/charges/me/{chargeItemId}/paid
```

### 권한

```text
해당 캠퍼스의 ACTIVE 멤버
본인의 chargeItem만 변경 가능
```

### Request

```json
{
  "paidAt": "2026-06-12T12:30:00"
}
```

`paidAt`을 보내지 않으면 서버 시간을 기준으로 처리한다.

### Response

```json
{
  "id": 1,
  "campusId": 1,
  "userId": 1,
  "paymentCategory": "PENALTY",
  "title": "큐티 미달 벌금",
  "reason": "필수 5회 중 3회 제출",
  "amount": 1000,
  "status": "PAID",
  "paidAt": "2026-06-12T12:30:00"
}
```

### 처리 기준

1. 로그인 사용자를 확인한다.
    
2. `charge_items.id`를 조회한다.
    
3. `charge_items.user_id`가 로그인 사용자와 같은지 확인한다.
    
4. `charge_items.campus_id`가 요청 `campusId`와 같은지 확인한다.
    
5. 현재 상태가 `UNPAID`인지 확인한다.
    
6. `status = PAID`로 변경한다.
    
7. `paid_at = 요청 paidAt 또는 now()`로 저장한다.
    

### 예외

|상황|HTTP Status|
|---|---|
|본인 청구 항목이 아님|403|
|이미 PAID 상태|409|
|WAIVED 또는 CANCELED 상태|409|
|존재하지 않는 청구 항목|404|

---

## 16.4 관리자 - 캠퍼스 청구 항목 전체 조회

```http
GET /admin/campuses/{campusId}/charges
```

### Query Parameters

|이름|설명|
|---|---|
|`paymentCategory`|`PENALTY`, `COFFEE`|
|`status`|`UNPAID`, `PAID`, `WAIVED`, `CANCELED`|
|`userId`|사용자 ID|
|`keyword`|이름 또는 이메일 검색|
|`startDate`|조회 시작일|
|`endDate`|조회 종료일|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "summary": {
    "totalAmount": 96000,
    "unpaidAmount": 54000,
    "paidAmount": 30000,
    "waivedAmount": 12000,
    "canceledAmount": 0
  },
  "members": [
    {
      "userId": 1,
      "name": "이승욱",
      "email": "user@example.com",
      "totalAmount": 8500,
      "unpaidAmount": 6500,
      "paidAmount": 2000,
      "waivedAmount": 0,
      "canceledAmount": 0
    }
  ]
}
```

---

## 16.5 관리자 - 회원별 청구 상세 조회

```http
GET /admin/campuses/{campusId}/members/{userId}/charges
```

---

## 16.6 관리자 - 청구 상태 변경

```http
PATCH /admin/charges/{chargeItemId}/status
```

### 권한

```text
ADMIN
또는 해당 캠퍼스의 MINISTER, ELDER, CAMPUS_LEADER
```

### Request

```json
{
  "status": "PAID",
  "paidAt": "2026-06-12T12:00:00"
}
```

### 가능한 상태

|Status|설명|
|---|---|
|`UNPAID`|미납|
|`PAID`|납부 완료|
|`WAIVED`|면제|
|`CANCELED`|취소|

---

# 17. FCM 토큰 API

## 17.1 내 FCM 토큰 등록

```http
POST /users/me/fcm-tokens
```

### Request

```json
{
  "token": "fcm-token-value",
  "deviceType": "WEB"
}
```

### Response

```json
{
  "message": "FCM 토큰이 등록되었습니다."
}
```

---

## 17.2 내 FCM 토큰 비활성화

```http
DELETE /users/me/fcm-tokens
```

### Request

```json
{
  "token": "fcm-token-value"
}
```

### Response

```json
{
  "message": "FCM 토큰이 비활성화되었습니다."
}
```

---

# 18. 알림 API

## 18.1 관리자 - 경건생활 미제출자 알림 발송

```http
POST /admin/campuses/{campusId}/notifications/devotion-missing
```

### Request

```json
{
  "targetWeekStartDate": "2026-06-08",
  "title": "경건생활 미제출 알림",
  "body": "아직 이번 주 경건생활을 제출하지 않았습니다."
}
```

---

## 18.2 관리자 - 투표 미참여자 알림 발송

```http
POST /admin/campuses/{campusId}/notifications/poll-missing
```

### Request

```json
{
  "pollId": 1,
  "notificationType": "WED_POLL_MISSING",
  "title": "수요예배 투표 미참여 알림",
  "body": "아직 수요예배 참석 투표를 하지 않았습니다."
}
```

---

## 18.3 관리자 - 커스텀 알림 발송

```http
POST /admin/campuses/{campusId}/notifications/custom
```

### Request

```json
{
  "targetUserIds": [1, 2, 3],
  "title": "공지",
  "body": "이번 주 모임 장소가 변경되었습니다."
}
```

---

## 18.4 관리자 - 알림 로그 조회

```http
GET /admin/campuses/{campusId}/notification-logs
```

### Query Parameters

|이름|설명|
|---|---|
|`notificationType`|알림 유형|
|`sendStatus`|발송 상태|
|`targetWeekStartDate`|대상 주차|
|`targetId`|대상 ID|
|`startDate`|조회 시작일|
|`endDate`|조회 종료일|

---

# 19. 대시보드 API

## 19.1 캠퍼스 대시보드 조회

```http
GET /admin/campuses/{campusId}/dashboard
```

### Query Parameters

|이름|설명|
|---|---|
|`weekStartDate`|조회 주차 시작일|

### Response

```json
{
  "campusId": 1,
  "campusName": "1캠",
  "region": "분당",
  "weekStartDate": "2026-06-08",
  "members": {
    "activeCount": 30,
    "inactiveCount": 5
  },
  "devotion": {
    "submittedCount": 24,
    "missingCount": 6,
    "submitRate": 80.0
  },
  "charges": {
    "totalAmount": 96000,
    "unpaidAmount": 54000,
    "paidAmount": 30000,
    "waivedAmount": 12000
  },
  "polls": [
    {
      "pollId": 1,
      "title": "6월 12일 수요예배 참석 투표",
      "pollType": "WED_SERVICE",
      "status": "OPEN",
      "respondedCount": 25,
      "notRespondedCount": 5
    }
  ]
}
```

---

# 20. 최종 API 목록

## 인증

```http
POST   /auth/signup
POST   /auth/login
POST   /auth/refresh
POST   /auth/logout
```

## 사용자

```http
GET    /users/me
PATCH  /admin/users/{userId}/role
```

## 캠퍼스

```http
POST   /campuses
GET    /campuses
GET    /campuses/me
GET    /campuses/{campusId}
PATCH  /campuses/{campusId}
POST   /campuses/{campusId}/invite-code/refresh
POST   /campuses/join
```

## 캠퍼스 멤버

```http
GET    /admin/campus-members
GET    /admin/campuses/{campusId}/members
PATCH  /admin/campuses/{campusId}/members/{campusMemberId}/campus-role
PATCH  /admin/campuses/{campusId}/members/{campusMemberId}/inactive
```

## 커피 담당

```http
GET    /campuses/{campusId}/duty-assignments
POST   /admin/campuses/{campusId}/duty-assignments
PATCH  /admin/duty-assignments/{assignmentId}/revoke
```

## 경건생활

```http
GET    /campuses/{campusId}/devotions/me/current-week
GET    /campuses/{campusId}/devotions/me/weeks/{weekStartDate}
PUT    /campuses/{campusId}/devotions/me/days/{recordDate}
PUT    /campuses/{campusId}/devotions/me/weeks/{weekStartDate}
GET    /campuses/{campusId}/devotions/me/monthly-summary
```

## 관리자 경건생활

```http
GET    /admin/campuses/{campusId}/devotions/weeks/{weekStartDate}
GET    /admin/campuses/{campusId}/devotions/weeks/{weekStartDate}/missing
GET    /admin/campuses/{campusId}/members/{userId}/monthly-summary
```

## 벌금 규칙

```http
GET    /campuses/{campusId}/penalty-rules
POST   /admin/campuses/{campusId}/penalty-rules
PATCH  /admin/penalty-rules/{ruleId}
```

## 납부 계좌

```http
GET    /campuses/{campusId}/payment-accounts
POST   /admin/campuses/{campusId}/payment-accounts
PATCH  /admin/payment-accounts/{accountId}/deactivate
```

## 투표 템플릿

```http
POST   /admin/campuses/{campusId}/poll-templates
GET    /admin/campuses/{campusId}/poll-templates
```

## 투표

```http
GET    /campuses/{campusId}/polls/active
GET    /campuses/{campusId}/polls/{pollId}
PUT    /campuses/{campusId}/polls/{pollId}/responses/me
POST   /admin/campuses/{campusId}/polls
GET    /admin/campuses/{campusId}/polls/{pollId}/results
GET    /admin/campuses/{campusId}/polls/{pollId}/missing-members
```

## 청구 및 납부

```http
GET    /campuses/{campusId}/charges/me
GET    /campuses/{campusId}/charges/me/summary
PATCH  /campuses/{campusId}/charges/me/{chargeItemId}/paid
GET    /admin/campuses/{campusId}/charges
GET    /admin/campuses/{campusId}/members/{userId}/charges
PATCH  /admin/charges/{chargeItemId}/status
```

## FCM 토큰

```http
POST   /users/me/fcm-tokens
DELETE /users/me/fcm-tokens
```

## 알림

```http
POST   /admin/campuses/{campusId}/notifications/devotion-missing
POST   /admin/campuses/{campusId}/notifications/poll-missing
POST   /admin/campuses/{campusId}/notifications/custom
GET    /admin/campuses/{campusId}/notification-logs
```

## 대시보드

```http
GET    /admin/campuses/{campusId}/dashboard
```

---

# 21. 이력서에 어필할 수 있는 설계 포인트

## 권한 분리

서비스 전체 권한과 캠퍼스 내부 역할을 분리하여, 전역 관리자와 캠퍼스 운영자의 책임 범위를 명확히 분리하였다.

## 멀티 캠퍼스 구조

사용자가 여러 캠퍼스에 소속될 수 있도록 `users`, `campuses`, `campus_members`를 분리하여 다대다 관계를 설계하였다.

## 쿠키 기반 인증

Access Token과 Refresh Token을 HttpOnly Cookie로 관리하고, Refresh Token의 Cookie Path를 재발급 API로 제한하여 토큰 노출 범위를 줄였다.

## 경건생활 기록 정규화

주간 요약 데이터와 일별 체크 데이터를 분리하여, 사용자가 매일 체크하거나 주간에 한 번에 제출해도 일관된 데이터 구조로 저장되도록 설계하였다.

## 청구 항목 통합 관리

경건생활 벌금과 커피 주문 금액을 `charge_items`로 통합 관리하여, 서로 다른 발생 원인을 하나의 납부 흐름으로 처리할 수 있게 설계하였다.

## 계좌 Snapshot 저장

청구 항목 생성 시점의 계좌 정보를 snapshot으로 저장하여, 납부 계좌가 변경되어도 과거 청구 내역의 정합성이 유지되도록 설계하였다.

## 투표 미참여자 추적

투표별 미참여자 조회 API를 분리하여, 관리자가 미응답자를 확인하고 FCM 알림을 발송할 수 있도록 설계하였다.

## 사용자 직접 납부 처리

사용자가 본인의 청구 항목을 직접 `PAID` 상태로 변경할 수 있도록 하되, 본인 소유의 청구 항목만 수정 가능하도록 권한 검증 기준을 설계하였다.