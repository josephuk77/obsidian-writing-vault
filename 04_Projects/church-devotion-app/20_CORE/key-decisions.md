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
| 2026-06-12 | 서비스 전체 권한은 `users.role`, 캠퍼스 내부 역할은 `campus_members.campus_role`로 분리한다. | 전역 권한과 캠퍼스별 운영 권한의 책임 범위가 다르기 때문 | [[ERD설계]] |  |
| 2026-06-12 | `campus_members.status`는 `ACTIVE`, `INACTIVE`만 사용한다. | 가입 대기 상태를 MVP 권한/멤버십 흐름에서 제외하고 단순화하기 위함 | [[ERD설계]] |  |

## Pending Decisions

| Decision needed | Options | Needed by | Link |
| --- | --- | --- | --- |
|  |  |  | [[open-questions]] |
