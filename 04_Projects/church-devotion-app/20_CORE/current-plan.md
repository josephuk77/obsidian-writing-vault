# current-plan

---
tags:
  - type/project
  - status/planning
---

## Current Goal

- Notion 원문을 기준으로 FaithLog MVP 기획, 요구사항, 아키텍처, 핵심 결정을 확정하고 실제 개발 레포 생성 전 기준 문서로 사용한다.

## Current Product Direction

FaithLog MVP는 “캠퍼스 운영 자동화 앱”이다. 묵상 콘텐츠 앱이 아니라, 경건생활 제출, 예배/모임 일정 투표, 커피 당번/커피비, 벌금/청구, 납부 상태, 알림을 줄이는 운영 도구로 만든다. 밥/식사/점심 기능은 MVP에서 제외하고 이후 확장으로 분리한다.

## Execution Order

| Priority | Action | Owner | Status |
| --- | --- | --- | --- |
| 1 | 개발 레포 생성 및 [[REPO_LINKS]] 갱신 | user/Codex | open |
| 2 | Spring Boot 백엔드 프로젝트 생성 | Codex | open |
| 3 | Supabase PostgreSQL 연결과 기본 Entity 작성 | Codex | open |
| 4 | 인증/쿠키/JWT/Refresh Token hash 구현 | Codex | open |
| 5 | 캠퍼스/멤버/권한 API 구현 | Codex | open |
| 6 | 경건생활 하루 체크/주간 제출/벌금 청구 구현 | Codex | open |
| 7 | 투표/커피비/청구 통합 구현. 단, 밥/식사 기능은 제외 | Codex | open |
| 8 | FCM 토큰/알림/대시보드 구현 | Codex | open |
| 9 | React Native 앱 구현 | Codex | open |

## This Week

- 레포 생성 여부 결정
- 백엔드부터 시작할지, API 문서/DBML을 더 고정할지 결정
- [[open-questions]] 중 주차 기준, 제출 후 수정 정책, 납부 처리 정책을 먼저 확정

## Blockers

- 실제 개발 레포 미연결
- 주차 시작 요일 미확정
- 제출 후 수정 정책 미확정
- 사용자 직접 `PAID` 처리의 실제 운영 적합성 검증 필요
- 자동 알림 발송 시각 미확정

## Not in Scope Now

- 밥/식사/점심 기능 전체. MVP에서는 만들지 않고, 추후 별도 확장으로 검토
- 카카오톡 자동 연동
- 결제 API
- QR/GPS 출석 인증
- AI 묵상 분석
- 포인트/랭킹/캐릭터 성장

## Links

- [[PROJECT_DASHBOARD]]
- [[project-brief]]
- [[requirements]]
- [[architecture-memo]]
- [[roadmap]]
- [[open-questions]]
