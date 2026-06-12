# domain-notes

---
tags:
  - type/project
  - status/planning
  - area/study
---

## 도메인 개념

| 개념 | 의미 | 구현 기준 |
| --- | --- | --- |
| 캠퍼스 | 실제 운영 단위 | `campuses` |
| 캠퍼스 멤버 | 사용자의 캠퍼스 소속과 내부 역할 | `campus_members` |
| 서비스 전체 권한 | 서비스 전체에서의 권한 | `users.role` |
| 캠퍼스 내부 역할 | 특정 캠퍼스 안에서의 운영 권한 | `campus_members.campus_role` |
| 운영 담당 | 권한이 아니라 특정 업무 담당 | `campus_duty_assignments` |
| 경건생활 | 큐티, 기도, 말씀읽기 체크 | `devotion_daily_checks`, `weekly_devotion_records` |
| 주간 제출 | 벌금 계산 기준이 되는 제출 이벤트 | `weekly_devotion_records.submitted_at` |
| 벌금 규칙 | 캠퍼스별 벌금 산정 기준 | `penalty_rules` |
| 청구 항목 | 사용자가 납부해야 할 금액 | `charge_items` |
| 반복 투표 템플릿 | 매주 반복 생성되는 투표 설정 | `poll_templates` |
| 반복 투표 선택지 | 반복 투표 생성 시 복사되는 기본 선택지 | `poll_template_options` |
| 실제 투표 | 사용자가 응답하는 투표 인스턴스 | `polls` |
| 커피 투표 | 선택지 금액으로 커피 청구가 생성되는 투표 | `poll_type = COFFEE` |
| 투표 응답 선택지 | 단일/다중 선택 결과 | `poll_response_options` |
| 투표 댓글 | 투표 상세의 질문, 공지, 대댓글 | `poll_comments` |
| 알림 로그 | 푸시 알림 발송 이력 | `notification_logs` |

## 사용자 언어

- “경건생활 제출했어?” -> `weekly_devotion_records.submitted_at` 존재 여부
- “이번 주 큐티 몇 번 했어?” -> `quiet_time_count`
- “토요 목자모임 지각 몇 분?” -> `saturday_late_minutes`
- “벌금 얼마야?” -> `charge_items.payment_category = PENALTY`
- “커피값 냈어?” -> `charge_items.payment_category = COFFEE`
- “납부했어요” -> 본인 청구 항목을 `PAID`로 변경
- “수요예배 투표 안 한 사람” -> 해당 poll에 `poll_responses`가 없는 활성 멤버
- “투표에서 어떤 선택지를 골랐어?” -> `poll_response_options`
- “투표 댓글 남겼어?” -> `poll_comments`
- “커피 담당” -> `campus_duty_assignments`의 활성 `COFFEE` 담당자

## 중요한 도메인 결정

- 캠퍼스가 곧 운영 단위다. `app_groups`는 만들지 않는다.
- 한 사용자는 여러 캠퍼스에 속할 수 있다.
- `COFFEE`는 권한 역할이 아니다. 담당 업무다.
- 청구 항목은 MVP에서 `PENALTY`, `COFFEE` 두 종류만 사용한다.
- 경건생활 청구는 제출 시점에만 만든다.
- 커피 청구는 커피 투표 응답 시점에 만든다.
- 커피 청구 투표는 `polls.payment_account_id`로 커피 계좌를 연결한다.
- 반복 투표 템플릿의 선택지는 실제 투표 생성 시 `poll_options`로 복사한다.
- 투표 댓글은 응답 데이터와 분리해서 `poll_comments`에 저장한다.
- 사용자 직접 `PAID` 처리가 MVP 기준이다.

## 헷갈리기 쉬운 표현

| 표현 | 주의 |
| --- | --- |
| 그룹 | 최신 ERD에서는 제거됨. 캠퍼스로 통일 |
| 점심 투표 | MVP 제외. 커피 투표와 섞지 말 것 |
| 납부 요청 | 최신 API에는 별도 요청 상태가 없음 |
| 관리자 승인 | 최신 ERD/API에서는 MVP 제외 |
| 정산 | 현재 설계에서는 별도 settlement 테이블보다 `charge_items` 중심 |

## 참고자료

- [[기획서]]
- [[API 명세서]]
- [[ERD설계]]
- [[project-brief]]
- [[requirements]]
- [[architecture-memo]]
