# roadmap

---
tags:
  - type/project
  - status/planning
---

## 기획 단계

- [x] Notion 원문을 `10_RAW_SOURCE/notion/`에 보존
- [x] 원문 기반으로 MVP 범위 정리
- [x] 최신 ERD/API 기준과 구 기획서 충돌사항 정리
- [x] `20_WIKI` 설명형 문서 갱신
- [x] `20_CORE` 핵심 기준 문서 갱신
- [ ] 실제 개발 레포 생성 후 [[REPO_LINKS]] 갱신
- [ ] API 우선순위를 GitHub Issues 또는 작업 티켓으로 분해

## MVP 단계

### 1. Backend Foundation

- Spring Boot 프로젝트 생성
- Supabase PostgreSQL 연결
- 공통 응답/예외 포맷
- 사용자/Refresh Token/Campus/CampusMember Entity
- Spring Security + JWT + HttpOnly Cookie

### 2. Campus & Permission

- 캠퍼스 생성/조회/수정
- 초대코드 발급/재발급/가입
- 캠퍼스 멤버 목록/역할 변경/비활성화
- 전역 권한과 캠퍼스 내부 역할 guard

### 3. Devotion & Penalty

- 하루별 경건생활 체크 API
- 주간 경건생활 조회/저장/제출 API
- 벌금 규칙 조회/생성/수정
- 제출 시 `PENALTY` 청구 생성/갱신
- 관리자 주차별 제출 현황/미제출자 조회

### 4. Charges & Accounts

- 납부 계좌 조회/생성/비활성화
- 내 청구 항목/요약 조회
- 사용자 직접 `PAID` 처리
- 관리자 청구 목록/회원별 상세/상태 변경
- 계좌 snapshot 응답 검증

### 5. Polls & Coffee

- 반복 투표 템플릿 생성/조회
- 투표 생성/진행 중 목록/상세/응답
- 투표 결과/미참여자 조회
- 커피 담당 등록/해제/조회
- 커피 투표 응답 시 `COFFEE` 청구 생성/갱신

### 6. Notifications & Dashboard

- FCM 토큰 등록/비활성화
- 미제출자 알림, 투표 미참여자 알림, 커스텀 알림
- 알림 로그 조회
- Scheduler 기반 반복 알림
- 캠퍼스 관리자 대시보드

## 앱 개발 단계

- 로그인/회원가입/로그아웃
- 캠퍼스 선택 및 가입
- 일반 구성원 홈
- 경건생활 캘린더/주간 제출 화면
- 투표 목록/상세/응답 화면
- 내 청구/납부 완료 화면
- 관리자 대시보드
- 관리자 멤버/투표/청구/알림 화면

## 배포 단계

- 백엔드 Dockerfile 작성
- GitHub Actions 빌드/테스트
- 배포 플랫폼 선택: Render, Railway, Fly.io, EC2, 개인 서버 중 결정
- HTTPS 적용
- Firebase 프로젝트 설정
- Swagger/OpenAPI 문서 공개 범위 결정

## 운영 단계

- 실제 캠퍼스 파일럿 운영
- 경건생활 제출/투표 응답/청구 생성/알림 발송 로그 점검
- 중복 청구와 중복 알림 여부 확인
- 운영자 피드백으로 대시보드와 알림 정책 조정
- 점심 기능, 납부 승인 플로우, 입금 인증 등 보류 기능 재평가
