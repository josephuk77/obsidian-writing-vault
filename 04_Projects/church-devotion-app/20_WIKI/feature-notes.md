# feature-notes

---
tags:
  - type/project
  - status/planning
---

## Feature List

| Feature | 사용자 가치 | 상태 | 관련 요구사항 |
| --- | --- | --- | --- |
| 인증/로그인 | 앱 접근과 권한 판단의 시작점 | planning | [[requirements]] |
| 캠퍼스 가입 | 초대코드로 실제 운영 단위에 들어간다 | planning | [[requirements]] |
| 캠퍼스 멤버 관리 | 운영자가 구성원과 역할을 관리한다 | planning | [[requirements]] |
| 커피 담당 관리 | 일반 권한과 운영 담당을 분리한다 | planning | [[requirements]] |
| 하루별 경건생활 체크 | 사용자가 매일 또는 주간에 체크할 수 있다 | planning | [[requirements]] |
| 주간 경건생활 제출 | 제출 시점과 벌금 계산 기준을 만든다 | planning | [[requirements]] |
| 벌금 규칙 관리 | 캠퍼스별 벌금 기준을 바꿀 수 있다 | planning | [[requirements]] |
| 청구 항목 관리 | 벌금과 커피비를 한 흐름에서 본다 | planning | [[requirements]] |
| 사용자 납부 완료 처리 | 구성원이 직접 납부 상태를 반영한다 | planning | [[requirements]] |
| 반복 투표 템플릿 | 수요예배/토요 목자모임 투표를 반복 생성한다 | planning | [[requirements]] |
| 커피 투표 | 메뉴 선택과 커피비 청구를 연결한다 | planning | [[requirements]] |
| 투표 결과/미응답자 조회 | 운영자가 누락자를 바로 찾는다 | planning | [[requirements]] |
| FCM 토큰/알림 | 미제출/미응답/공지 알림을 보낸다 | planning | [[requirements]] |
| 관리자 대시보드 | 주차별 운영 상태를 한 화면에서 본다 | planning | [[requirements]] |

## 핵심 화면 메모

### 일반 구성원 홈

- 이번 주 경건생활 제출 상태
- 진행 중 투표 목록
- 미납 청구 요약
- 최근 알림 또는 해야 할 일

### 경건생활 화면

- 월요일부터 일요일까지 7일 체크
- 큐티/기도/말씀읽기 체크박스
- 토요 목자모임 지각 시간 입력
- 제출 전 벌금 미리보기
- 제출 후 수정 가능 여부는 정책 결정 필요

### 투표 화면

- 진행 중 투표 목록
- 투표 상세와 내 응답
- 커피 투표의 경우 메뉴명, 온도, 금액 표시
- 응답 수정 시 기존 청구 항목도 갱신되어야 한다

### 내 청구 화면

- 총액, 미납액, 납부액 요약
- 벌금/커피 카테고리 필터
- 청구별 계좌 snapshot 표시
- `납부했어요` 버튼은 `UNPAID` 상태에서만 노출

### 관리자 대시보드

- 활성/비활성 멤버 수
- 주차별 경건생활 제출률
- 청구 총액/미납액/납부액/면제액
- 진행 중 투표와 미응답자 수
- 대상자에게 알림 보내기 진입점

## Feature Notes

### 경건생활

기획서에는 “주간 일수 입력”으로 설명되어 있지만, 최신 API/ERD는 하루별 체크와 주간 제출을 모두 지원한다. 구현 기준은 하루별 체크 데이터를 저장하고, 제출 시 주간 합산 결과를 `weekly_devotion_records`에 저장하는 방식이다.

### 벌금

벌금은 큐티, 기도, 말씀읽기, 지각을 각각 청구하지 않는다. 한 주의 결과를 합산하여 `PENALTY` 청구 항목 하나로 만든다.

### 커피

커피는 점심 기능이 아니다. MVP에는 커피 투표와 커피비 청구가 포함된다. 메뉴는 Spring enum으로 관리하되, 투표 생성 시 `poll_options.compose_menu_code`와 `poll_options.price_amount`에 메뉴 코드와 가격 snapshot을 복사한다. 커피 투표는 `polls.payment_category = COFFEE`, `polls.charge_generation_type = OPTION_PRICE`, `polls.payment_account_id`를 함께 사용한다.

### 투표 댓글

투표 응답은 `poll_responses/poll_response_options`에 저장하고, 투표에 대한 질문/공지/대댓글은 `poll_comments`에 저장한다. 댓글 삭제는 `is_deleted`, `deleted_at` 기반 soft delete로 처리한다.

### 납부

최신 ERD/API 기준에서는 사용자가 직접 `PAID` 처리한다. 기획서의 “납부 요청 -> 관리자 승인/반려” 흐름은 보류한다.

### 알림

배치는 정산 생성이 아니라 알림 발송에 사용한다. 정산/청구 생성은 사용자의 제출 또는 투표 응답 이벤트에서 발생한다.
