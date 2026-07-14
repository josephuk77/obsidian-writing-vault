---
project: FaithLog
type: security-audit
issue: 157
status: done
created: 2026-07-12
tags:
  - FaithLog
  - security
  - threat-model
  - authorization
  - OWASP
---

# #157 위협 모델과 권한 행렬 보안 감사

## 1. 감사 배경

#156까지 책임 분리가 병합된 `origin/develop` `d9d9f250` 기준으로 보안 동작을 바꾸지 않고
인증·인가·tenant campus 경계를 읽기 전용으로 감사했다.

## 2. 감사 범위

- 21개 Controller, 80개 endpoint, application `permitAll` 4개, authenticated 76개
- service role USER/MANAGER/ADMIN
- campus role MINISTER/ELDER/CAMPUS_LEADER/MEMBER와 active COFFEE duty
- 모바일 앱, Cloud Run, Supabase PostgreSQL, Upstash Redis, Firebase FCM, Scheduler
- 7개 신뢰 경계, 11개 보호 자산 범주, 18개 객체 식별자 공격 표면
- JWT/tokenVersion/refresh rotation/logout blacklist/FCM ownership/account deletion

## 3. 결과

- Confirmed: Critical 0 / High 0 / Medium 1 / Low 0
- Medium: 마지막 active service ADMIN은 role 강등으로는 보호되지만 본인 탈퇴 경로에는 같은
  guard가 없어 active ADMIN 0명이 될 수 있다. 신뢰도 10/10, 독립 코드 검증 완료.
- False positive/의도된 정책: 7개
- LOW hardening 후보: non-root image, GitHub Actions SHA pin, repository secret scanner 3개
- 운영 콘솔 미확인 체크리스트: 12개

마지막 ADMIN 탈퇴는 유효 세션과 현재 비밀번호, 정확한 확인문구가 모두 필요하다. 성공하면
새 가입은 USER만 만들고 admin role 변경도 active ADMIN을 요구하므로 DB/운영자 개입 전까지
service 관리자 control plane이 잠긴다. campus manager의 제한된 기능은 유지될 수 있어 전체
서비스 중단이 아니라 관리자 plane 가용성 문제로 Medium 판정했다.

## 4. 현재 방어 확인

- JWT signature/type/JTI/sessionId/tokenVersion/expiration과 active DB version 검사
- Redis refresh allowlist/rotation과 access blacklist
- role 변경 시 tokenVersion 증가
- FCM `tokenId + userId` owner 삭제, token ownership 이전, stale 제외
- 주요 객체의 campus/parent/owner 결합 조회
- anonymous poll 결과의 respondent identity 숨김
- Scheduler Redis lock/dedup 장애 fail-closed

## 5. 기록과 검증

- 저장소 문서:
  - `docs/security/157-threat-model.md`
  - `docs/security/157-api-authorization-matrix.md`
  - `docs/security/157-audit-findings.md`
- secret 패턴은 값 없이 존재 여부/경로만 검사했고 실제 key 형식 후보는 0건이었다.
- `git diff --check`, 80개 endpoint 행 번호 대조, 문서 경로/링크 검증을 수행했다.
- 탈퇴·마지막 ADMIN 강등·role token invalidation·refresh 재사용·FCM owner focused 검증은
  5개 class, 19 tests / 0 failures / 0 errors / 0 skipped로 성공했다.
- 문서-only 감사라 Docker QA는 실행하지 않았다.
- 코드, config, DB, Flyway, 운영 인프라 변경 및 후속 Issue/PR 생성은 하지 않았다.

## 6. 후속 후보

- [ ] PM 승인 후 마지막 active ADMIN 탈퇴와 동시 최종 ADMIN 전이를 하나의 shared guard로 보호
- [ ] PM 승인 후 container/CI/secret scanner LOW hardening 묶음 검토
- [ ] Cloud Run/Supabase/Upstash/Firebase 운영 콘솔 체크리스트 수행
