# LOG

---
tags:
  - type/project
  - status/planning
---

프로젝트 작업 기록입니다. 세션이 끊겨도 이 문서와 [[INDEX]]를 읽으면 맥락을 복구할 수 있게 작성합니다.

## 2026-06-12

### Task

- users와 campus_members 역할 구조 변경을 Notion/Obsidian 문서에 반영

### Changed

- [[ERD설계]]에서 `user_role`, `campus_role`, `users.role`, `campus_members.campus_role` 기준으로 수정했다.
- Notion `대학부 앱 개발 > ERD 설계 > FaithLog ERD 설계` 문서의 권한 설명, 테이블 설명, DBML을 같은 기준으로 수정했다.
- [[key-decisions]]와 [[project-facts]]에 권한 분리 결정을 추가했다.

### Evidence

- 서비스 전체 권한: `USER`, `MANAGER`, `ADMIN`
- 캠퍼스 내부 역할: `MINISTER`, `ELDER`, `CAMPUS_LEADER`, `MEMBER`
- 멤버 상태: `ACTIVE`, `INACTIVE`

### Decisions

- 전역 권한은 `users.role`에서 관리한다.
- 캠퍼스별 운영 역할은 `campus_members.campus_role`에서 관리한다.
- 커피 담당은 `campus_members.campus_role`에 넣지 않고 `campus_duty_assignments`로 분리한다.

### Errors

- 없음

### Next

- API 구현 시 `role`과 `campusRole` 응답 필드가 이 분리 기준을 따르는지 확인한다.

## 2026-06-12

### Task

- 프로젝트 내부 문서 공간을 사용자 문서, AI 맥락, 핵심 정보로 분리

### Changed

- `15_MY_DOCUMENTS/`를 추가했다.
- `16_AI_CONTEXT/`를 추가했다.
- `20_CORE/`를 추가했다.
- [[INDEX]]와 [[PROJECT_RULES]]를 새 구조에 맞게 갱신했다.

### Evidence

- 기존 `20_WIKI/`, `30_DECISIONS/`, `40_ERRORS/`는 유지했다.

### Decisions

- 사용자가 직접 쓴 프로젝트 문서는 `15_MY_DOCUMENTS/`에 둔다.
- AI 작업 가정과 조사 큐는 `16_AI_CONTEXT/`에 둔다.
- 실제 진행 기준 정보는 `20_CORE/`에 둔다.

### Errors

- 없음

### Next

- Notion 원문 수집 후 [[project-facts]], [[core-data]], [[current-plan]]을 갱신한다.

## 2026-06-12

### Task

- 프로젝트 기획 허브 초기 구조 생성

### Changed

- `_Project_Template` 기준으로 프로젝트 폴더 구조와 기본 문서를 생성했다.

### Evidence

- 아직 실제 개발 레포는 연결하지 않았다.
- Notion 원문은 아직 추가하지 않았다.

### Decisions

- Raw Source는 `10_RAW_SOURCE/notion/`에 원문 그대로 보존한다.
- Codex 정리본은 `20_WIKI/`에 저장한다.

### Errors

- 없음

### Next

- Notion 기획 원문을 `10_RAW_SOURCE/notion/`에 추가한다.
- [[project-brief]], [[requirements]], [[roadmap]], [[open-questions]]를 실제 기획 내용으로 갱신한다.

## 2026-06-12

### Task

- Notion 원문 기반 FaithLog MVP 기획, 위키, 코어 기준 문서 갱신

### Changed

- [[project-brief]]에 FaithLog의 문제 정의, 대상 사용자, MVP 범위, 제외 범위, 성공 기준을 정리했다.
- [[requirements]]에 인증, 캠퍼스, 경건생활, 청구, 투표, 커피, 알림, 대시보드 요구사항을 정리했다.
- [[architecture-memo]]에 React Native, Spring Boot, Supabase PostgreSQL, FCM 구조와 핵심 데이터 흐름을 정리했다.
- [[feature-notes]], [[domain-notes]], [[roadmap]], [[open-questions]]를 Notion 원문 기반으로 갱신했다.
- [[project-facts]], [[core-data]], [[key-decisions]], [[current-plan]], [[solved-issues]]를 현재 구현 기준으로 갱신했다.
- [[INDEX]]의 현재 상태를 Notion 원문 수집 완료로 바꿨다.

### Evidence

- Raw Source: [[기획서]], [[API 명세서]], [[ERD설계]]
- 최신 MVP 기준: `campuses/campus_members`, `charge_items`, `weekly_devotion_records`, `devotion_daily_checks`, `polls`, `poll_responses`, `notification_logs`

### Decisions

- 캠퍼스가 실제 운영 단위이며 `app_groups`는 만들지 않는다.
- 점심 기능은 MVP에서 제외한다.
- 납부 흐름은 사용자 직접 `PAID` 처리 기준으로 정리한다.
- 벌금과 커피비는 `charge_items`에서 `PENALTY`, `COFFEE`로 통합 관리한다.
- 커피 담당은 `campus_duty_assignments`로 분리한다.

### Errors

- gstack autoplan 전체 프리플라이트는 telemetry/gbrain sync 가능성 때문에 실행하지 않았다. 로컬 파일 읽기와 문서 작성 중심으로 진행했다.

### Next

- 실제 개발 레포를 생성하고 [[REPO_LINKS]]를 갱신한다.
- [[open-questions]]에서 주차 기준, 제출 후 수정 정책, 납부 처리 정책을 먼저 확정한다.

## 2026-06-12 DBML 수정본 기획 반영

### Context

- 사용자가 최신 DBML을 제공했다.
- 디자인은 그대로 두고, 기획/요구사항/아키텍처 문서만 최신 DB 구조에 맞췄다.

### Updated

- [[core-data]]: `notification_type`, `poll_template_options`, `poll_response_options`, `poll_comments`, `payment_account_id`, 계좌 snapshot 메모 반영
- [[requirements]]: 반복 투표 선택지, 단일/다중 선택, 투표 상태, 커피 계좌 연결, 투표 댓글, 세분화된 알림 유형 반영
- [[architecture-memo]]: 반복 투표 생성, 투표 댓글, 커피 청구 생성, 알림 로그 흐름 보강
- [[project-brief]]: 투표 댓글/대댓글과 DB 수정 기준 반영
- [[project-facts]]: DBML 수정본 기준 핵심 사실 추가
- [[current-plan]]: 투표 템플릿, 커피 청구, 투표 댓글 순서로 실행 계획 세분화
- [[key-decisions]]: 반복 투표 선택지 복사, 투표 댓글 분리, 커피 청구 계좌 연결 결정 추가
- [[feature-notes]], [[domain-notes]]: 커피 투표/댓글 도메인 설명 보강

### Decisions

- 밥/식사/점심 기능은 계속 MVP 제외다.
- 커피는 MVP에 남기되, `polls.payment_account_id`, `payment_category = COFFEE`, `charge_generation_type = OPTION_PRICE` 기준으로 청구와 연결한다.
- 투표 응답과 투표 댓글은 분리한다.
