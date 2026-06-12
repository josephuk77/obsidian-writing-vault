# core-data

---
tags:
  - type/project
  - status/planning
---

## 실제 필요한 데이터

| Data | Why needed | Source | Status |
| --- | --- | --- | --- |
| 사용자 | 로그인, 권한, 청구/투표/알림 대상 | [[ERD설계]] | confirmed |
| Refresh Token | 쿠키 기반 인증 재발급 | [[API 명세서]] | confirmed |
| 캠퍼스 | 실제 운영 단위 | [[ERD설계]] | confirmed |
| 캠퍼스 멤버 | 사용자와 캠퍼스의 다대다 관계, 내부 역할 | [[ERD설계]] | confirmed |
| 커피 담당자 | 권한과 별도인 운영 담당 지정 | [[ERD설계]] | confirmed |
| 주간 경건생활 기록 | 제출 여부, 주간 합산, 벌금 생성 기준 | [[ERD설계]], [[API 명세서]] | confirmed |
| 하루별 경건생활 체크 | 캘린더형 체크와 주간 합산 원천 | [[ERD설계]], [[API 명세서]] | confirmed |
| 벌금 규칙 | 캠퍼스별 벌금 산정 | [[ERD설계]] | confirmed |
| 납부 계좌 | 벌금/커피 계좌 및 snapshot 생성 | [[ERD설계]] | confirmed |
| 반복 투표 템플릿 | 수요예배/토요 목자모임 반복 생성 | [[API 명세서]] | confirmed |
| 투표/선택지/응답 | 투표 참여, 결과, 미응답자 조회 | [[ERD설계]], [[API 명세서]] | confirmed |
| 투표 댓글 | 투표별 질의/공지/대댓글과 삭제 상태 관리 | [[ERD설계]] | confirmed |
| 청구 항목 | 벌금과 커피비 통합 납부 흐름 | [[ERD설계]], [[API 명세서]] | confirmed |
| FCM 토큰 | 사용자별 푸시 알림 대상 | [[API 명세서]] | confirmed |
| 알림 로그 | 중복 방지, 실패 원인 추적 | [[ERD설계]], [[API 명세서]] | confirmed |

## 핵심 Enum

| Enum | Values |
| --- | --- |
| `user_role` | `USER`, `MANAGER`, `ADMIN` |
| `campus_role` | `MINISTER`, `ELDER`, `CAMPUS_LEADER`, `MEMBER` |
| `duty_type` | `COFFEE` |
| `member_status` | `ACTIVE`, `INACTIVE` |
| `penalty_rule_type` | `QUIET_TIME`, `PRAYER`, `BIBLE_READING`, `SATURDAY_LATE` |
| `penalty_calculation_type` | `MISSING_COUNT`, `LATE_MINUTE` |
| `payment_category` | `PENALTY`, `COFFEE` |
| `poll_type` | `WED_SERVICE`, `SATURDAY_LEADER`, `COFFEE`, `CUSTOM` |
| `selection_type` | `SINGLE`, `MULTIPLE` |
| `charge_generation_type` | `NONE`, `OPTION_PRICE` |
| `poll_status` | `SCHEDULED`, `OPEN`, `CLOSED` |
| `charge_status` | `UNPAID`, `PAID`, `WAIVED`, `CANCELED` |
| `charge_source_type` | `DEVOTION_RECORD`, `POLL_RESPONSE` |
| `device_type` | `ANDROID`, `IOS`, `WEB` |
| `notification_type` | `DEVOTION_REMINDER`, `DEVOTION_MISSING`, `WED_POLL_OPEN`, `WED_POLL_MISSING`, `SATURDAY_POLL_OPEN`, `SATURDAY_POLL_MISSING`, `COFFEE_POLL_OPEN`, `COFFEE_POLL_MISSING`, `PAYMENT_UNPAID`, `CUSTOM` |
| `send_status` | `PENDING`, `SENT`, `FAILED`, `SKIPPED` |

## 벌금 기본값

| 항목 | 계산 방식 | 기준 |
| --- | --- | --- |
| 큐티 | 부족 횟수 | 주 5회 기준, 부족 1회당 500원 |
| 기도 | 부족 횟수 | 주 5회 기준, 부족 1회당 500원 |
| 말씀읽기 | 부족 횟수 | 주 5회 기준, 부족 1회당 300원 |
| 토요 목자모임 지각 | 지각 시간 | 기본 1,000원 + 1분당 100원 |

## 중복 방지 키

| 대상 | Unique 기준 |
| --- | --- |
| 캠퍼스 멤버 | `campus_id + user_id` |
| 주간 경건생활 기록 | `campus_id + user_id + week_start_date` |
| 하루별 경건생활 체크 | `weekly_record_id + record_date` |
| 투표 응답 | `poll_id + user_id` |
| 투표 응답 선택지 | `response_id + option_id` |
| 청구 항목 | `campus_id + user_id + payment_category + source_type + source_id` |
| FCM 토큰 | `token` |

## DBML 반영 메모

- `poll_templates`는 반복 투표의 시간 규칙을 저장하고, `poll_template_options`는 반복 생성 시 사용할 기본 선택지를 저장한다.
- `polls.payment_account_id`와 `payment_category`는 투표 응답에서 청구를 만들 때 어느 계좌/분류로 청구할지 결정한다.
- `poll_options.compose_menu_code`는 커피 메뉴 코드용이며, 가격 변경에 대비해 `price_amount` snapshot을 함께 저장한다.
- `poll_comments`는 투표별 댓글과 대댓글을 지원하며, 삭제는 `is_deleted/deleted_at`로 처리한다.
- `charge_items`는 계좌 snapshot(`bank_name_snapshot`, `account_number_snapshot`, `account_holder_snapshot`)을 저장해 과거 청구가 계좌 변경에 흔들리지 않게 한다.
- `notification_logs.target_week_start_date`와 `target_id`는 주차/대상별 알림 중복 방지와 실패 추적에 사용한다.

## 실제 필요한 정보

| Information | Decision/use | Source | Status |
| --- | --- | --- | --- |
| MVP 포함 범위 | 개발 전 범위 고정 | [[project-brief]], [[requirements]] | confirmed |
| 제외 범위 | 과도한 기능 확장 방지 | [[project-brief]] | confirmed |
| 납부 처리 기준 | 청구 API와 상태 enum 구현 | [[ERD설계]], [[API 명세서]] | confirmed for MVP |
| 주차 시작 요일 | 경건생활 제출/알림 기준 | [[open-questions]] | open |
| 커피 담당자 수 제한 | DB 제약 또는 앱 정책 결정 | [[open-questions]] | open |
| 자동 알림 시각 | Scheduler 구현 기준 | [[open-questions]] | open |

## 확인 필요

- [[open-questions]]
- [[research-queue]]
