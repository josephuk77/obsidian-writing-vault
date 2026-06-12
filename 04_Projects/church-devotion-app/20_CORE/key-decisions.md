# key-decisions

---
tags:
  - type/decision
  - status/planning
---

프로젝트 진행에 직접 영향을 주는 중요한 결정의 현재 요약입니다. 정식 기록이 필요하면 `30_DECISIONS/ADR-0001-title.md`로 남깁니다.

## Key Decisions

| Date | Decision | Reason | Evidence | ADR |
| --- | --- | --- | --- | --- |
| 2026-06-12 | 서비스 전체 권한은 `users.role`, 캠퍼스 내부 역할은 `campus_members.campus_role`로 분리한다. | 전역 권한과 캠퍼스별 운영 권한의 책임 범위가 다르기 때문 | [[ERD설계]], [[API 명세서]] |  |
| 2026-06-12 | `campus_members.status`는 `ACTIVE`, `INACTIVE`만 사용한다. | 가입 대기 상태를 MVP 권한/멤버십 흐름에서 제외하고 단순화하기 위함 | [[ERD설계]] |  |
| 2026-06-12 | 캠퍼스가 실제 운영 단위이며 `app_groups`는 만들지 않는다. | MVP 운영 단위가 캠퍼스이고 그룹 테이블은 현재 기능에 비해 과하다 | [[ERD설계]] |  |
| 2026-06-12 | 커피 담당은 `campus_members.campus_role`에 넣지 않고 `campus_duty_assignments`로 분리한다. | 한 사용자가 일반 멤버이면서 커피 담당일 수 있고, 담당은 권한이 아니라 업무이기 때문 | [[ERD설계]] |  |
| 2026-06-12 | MVP 청구 항목은 `PENALTY`, `COFFEE` 두 종류만 사용한다. | 벌금과 커피비가 실제 MVP 납부 흐름의 전부이기 때문 | [[ERD설계]], [[API 명세서]] |  |
| 2026-06-12 | 벌금은 주차별 합산 후 `charge_items`에 `PENALTY` 한 줄로 저장한다. | 항목별 청구를 만들면 납부/조회/중복 방지가 복잡해진다 | [[ERD설계]] |  |
| 2026-06-12 | 커피는 투표 응답을 기준으로 `charge_items`에 `COFFEE` 한 줄로 저장한다. | 선택한 메뉴 가격이 곧 커피 청구 금액이기 때문 | [[ERD설계]], [[API 명세서]] |  |
| 2026-06-12 | 사용자 직접 납부 완료 처리를 MVP 기준으로 한다. | 최신 ERD/API가 관리자 승인 없는 `UNPAID -> PAID` 흐름을 기준으로 한다 | [[ERD설계]], [[API 명세서]] |  |
| 2026-06-12 | 점심 기능은 MVP에서 제외한다. | 최신 ERD 결론에서 점심 투표/정산/계좌/담당자를 제외했다 | [[ERD설계]] |  |
| 2026-06-12 | 컴포즈커피 메뉴는 DB enum이 아니라 Spring enum으로 관리하고, DB에는 메뉴 코드와 가격 snapshot을 저장한다. | 메뉴 가격 변경이 과거 투표/청구 금액을 바꾸면 안 되기 때문 | [[ERD설계]] |  |
| 2026-06-12 | 배치는 정산 생성이 아니라 알림 발송에 사용한다. | 청구 생성은 경건생활 제출과 투표 응답 이벤트에서 발생한다 | [[ERD설계]] |  |
| 2026-06-12 | 반복 투표의 기본 선택지는 `poll_template_options`에 저장하고 생성 시 `poll_options`로 복사한다. | 반복 생성된 실제 투표가 템플릿 변경에 흔들리지 않게 하기 위함 | DBML 수정본 |  |
| 2026-06-12 | 투표 댓글은 `poll_comments`로 응답과 분리한다. | 투표 선택 데이터와 논의/질문 데이터를 섞지 않기 위함 | DBML 수정본 |  |
| 2026-06-12 | 커피 청구 투표는 `polls.payment_account_id`와 `payment_category = COFFEE`를 함께 사용한다. | 청구 생성 시점에 어떤 계좌로 납부해야 하는지 고정하기 위함 | DBML 수정본 |  |

## Pending Decisions

| Decision needed | Options | Needed by | Link |
| --- | --- | --- | --- |
| 주차 시작 요일 | 월요일 시작 / 일요일 시작 / 캠퍼스별 설정 | 경건생활 API 구현 전 | [[open-questions]] |
| 제출 후 수정 정책 | 마감 전 수정 / 제출 후 관리자만 수정 / 항상 수정 가능 | 주간 제출 구현 전 | [[open-questions]] |
| 직접 `PAID` 처리의 운영 적합성 | 직접 처리 유지 / 승인 플로우 추가 / 사후 정정만 허용 | 청구 API 구현 전 | [[open-questions]] |
| 커피 담당자 수 제한 | 앱에서 1명 권장 / DB 제약 강제 / 여러 명 허용 | 커피 담당 API 구현 전 | [[open-questions]] |
| 자동 알림 시각 | 코드 상수 / 캠퍼스 설정 / 관리자 수동 | Scheduler 구현 전 | [[open-questions]] |
