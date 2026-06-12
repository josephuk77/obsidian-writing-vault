# solved-issues

---
tags:
  - type/project
  - status/planning
---

프로젝트 진행 중 해결한 중요한 문제를 요약합니다. 상세 에러 기록이 필요하면 `40_ERRORS/ERR-0001-title.md`로 남깁니다.

## Solved Issues

| Date | Issue | Resolution | Evidence | Detail |
| --- | --- | --- | --- | --- |
| 2026-06-12 | 기획서에는 그룹 구조가 남아 있고 ERD는 캠퍼스 중심 구조를 제안한다. | 최신 기준은 `campuses/campus_members`로 확정하고 `app_groups`는 제거한다. | [[ERD설계]] | [[architecture-memo]] |
| 2026-06-12 | 기획서에는 점심 투표가 포함되어 있지만 ERD는 MVP 제외로 정리한다. | MVP에서는 점심 기능을 제외하고 커피 투표만 포함한다. | [[ERD설계]] | [[project-brief]] |
| 2026-06-12 | 납부 흐름이 “납부 요청/관리자 승인”과 “사용자 직접 PAID”로 충돌한다. | MVP 기준은 최신 ERD/API의 사용자 직접 `PAID` 처리로 정리한다. | [[ERD설계]], [[API 명세서]] | [[key-decisions]] |
| 2026-06-12 | 경건생활 입력 방식이 “주간 일수 입력”과 “하루별 체크 + 주간 제출”로 다르게 표현된다. | 최신 API/ERD 기준으로 하루별 체크를 저장하고 제출 시 주간 합산한다. | [[API 명세서]], [[ERD설계]] | [[requirements]] |
| 2026-06-12 | 커피 담당을 캠퍼스 역할로 넣을지 운영 담당으로 분리할지 혼동될 수 있다. | `campus_duty_assignments`로 분리한다. | [[ERD설계]] | [[key-decisions]] |

## Reusable Lessons

- 원문 기획서보다 최신 ERD/API가 더 구현에 가까운 기준 문서다.
- 구상 문서에 남은 확장 기능은 MVP 기준 문서에서 명시적으로 제외해야 한다.
- 운영 담당과 권한 역할은 분리해야 나중에 예외 권한이 덜 생긴다.
- 청구는 원인별 테이블을 나누기보다 `charge_items`로 합치는 편이 MVP 구현에 맞다.
