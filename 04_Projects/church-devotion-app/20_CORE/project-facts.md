# project-facts

---
tags:
  - type/project
  - status/planning
---

## One-line Summary

- FaithLog는 교회 캠퍼스의 경건생활 체크, 예배/모임 투표, 커피 주문, 벌금/커피 청구, 납부 상태, 알림을 통합 관리하는 모바일 앱 서비스이다.

## Confirmed Facts

| Fact | Evidence | Source |
| --- | --- | --- |
| 아직 실제 개발 레포는 없다. | `00_SCHEMA/REPO_LINKS.md`가 미연결 상태 | [[REPO_LINKS]] |
| 현재 상태는 planning이다. | vault 문서 frontmatter와 INDEX 상태 | [[INDEX]] |
| Notion 원문 기획서, ERD 설계, API 명세서가 Raw Source에 있다. | `10_RAW_SOURCE/notion/`에 3개 원문 보관 | [[기획서]], [[ERD설계]], [[API 명세서]] |
| 앱은 React Native로 개발한다. | 서비스 구조 문서화 | [[기획서]] |
| 백엔드는 Spring Boot REST API 서버로 개발한다. | 서비스 구조 문서화 | [[기획서]], [[API 명세서]] |
| 데이터베이스는 Supabase PostgreSQL을 사용한다. | DB 설계 방향 명시 | [[기획서]], [[ERD설계]] |
| 앱은 Supabase DB에 직접 접근하지 않는다. | 모든 요청은 Spring Boot API를 통해 처리 | [[기획서]] |
| 푸시 알림은 Firebase Cloud Messaging을 사용한다. | FCM 토큰/API/로그 설계 존재 | [[API 명세서]], [[ERD설계]] |
| 서비스 전체 권한은 `USER`, `MANAGER`, `ADMIN`이다. | `users.role`에 `user_role` 적용 | [[ERD설계]], [[API 명세서]] |
| 캠퍼스 내부 역할은 `MINISTER`, `ELDER`, `CAMPUS_LEADER`, `MEMBER`이다. | `campus_members.campus_role`에 `campus_role` 적용 | [[ERD설계]], [[API 명세서]] |
| 커피 담당은 권한 역할이 아니라 별도 운영 담당이다. | `campus_duty_assignments` 사용 | [[ERD설계]] |
| 캠퍼스가 실제 운영 단위다. | `app_groups` 제거 결론 | [[ERD설계]] |
| 청구 항목은 MVP에서 `PENALTY`, `COFFEE` 두 종류만 사용한다. | `charge_items` 통합 설계 | [[ERD설계]], [[API 명세서]] |
| 점심 기능은 MVP에서 제외한다. | 최신 ERD 결론에 제외 명시 | [[ERD설계]] |
| 반복 투표의 기본 선택지는 `poll_template_options`에 저장한다. | 템플릿 기반 투표 생성 시 실제 `poll_options`로 복사 | DBML 수정본 |
| 투표 응답 선택지는 `poll_response_options`에 저장한다. | 단일/다중 선택을 같은 구조로 처리 | DBML 수정본 |
| 투표 댓글은 `poll_comments`로 관리한다. | 응답 데이터와 논의/질문 데이터를 분리 | DBML 수정본 |
| 커피 청구 투표는 `polls.payment_account_id`로 납부 계좌를 연결한다. | 청구 생성 시 계좌 snapshot을 고정하기 위함 | DBML 수정본 |

## Users

- 일반 구성원: 경건생활 체크, 투표 응답, 커피 주문, 청구 확인, 납부 완료 처리
- 캠퍼스 운영자: 멤버/역할/투표/벌금/청구/알림/대시보드 관리
- 커피 담당자: 커피 투표 생성, 커피 계좌 관리, 커피 주문 확인
- 서비스 관리자: 전역 사용자 권한과 캠퍼스 생성 권한 관리

## Problem

- 캠퍼스 운영자는 매주 경건생활 미제출자, 투표 미응답자, 벌금/커피 미납자를 수동으로 확인한다.
- 구성원은 입력, 투표, 납부를 놓치기 쉽다.
- 벌금 계산과 커피 주문 금액 정산이 분리되어 반복 업무가 생긴다.
- 알림 발송 이력이 없으면 같은 사람에게 같은 요청을 중복 발송하기 쉽다.

## Value Proposition

- 구성원은 해야 할 입력과 납부를 앱에서 빠르게 끝낸다.
- 운영자는 누락자를 자동으로 찾고 필요한 대상에게 바로 알림을 보낸다.
- 벌금과 커피비를 하나의 청구 모델로 관리한다.
- 초기에는 한 캠퍼스에서 바로 쓸 수 있고, 나중에 여러 캠퍼스로 확장할 수 있다.

## Scope Boundary

### In

- 인증, 캠퍼스, 멤버/권한, 커피 담당
- 경건생활 하루 체크와 주간 제출
- 벌금 규칙과 PENALTY 청구
- 투표 템플릿, 실제 투표, 투표 응답, 미응답자 조회
- 투표 댓글/대댓글
- 커피 투표와 COFFEE 청구
- 납부 계좌, 청구 조회, 사용자 직접 납부 완료 처리
- FCM 토큰, 알림 발송, 알림 로그
- 관리자 대시보드

### Out

- 점심 투표/정산
- 결제 API
- 카카오톡 자동 연동
- QR/GPS 출석 인증
- AI 묵상 분석
- 포인트/랭킹/캐릭터 성장
- Supabase 클라이언트 직접 연동
- 관리자 납부 승인/반려 전용 플로우

## Links

- [[project-brief]]
- [[requirements]]
- [[architecture-memo]]
- [[roadmap]]
- [[REPO_LINKS]]
