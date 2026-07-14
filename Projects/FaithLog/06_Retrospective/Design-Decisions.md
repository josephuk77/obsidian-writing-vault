# FaithLog Design Decisions

## 2026-07-13 - 관리자 PAID와 경건 벌금 취소 재제출

### 배경

Notion Billing 기획은 관리자 `PAID` 전환을 금지했고, 경건 벌금 취소와 source weekly record 재오픈 및 CANCELED 청구 재사용 계약을 정의하지 않았다. Issue #190에서 사용자가 최신 동작을 명시적으로 확정했다.

### 선택지

1. 기존 Notion대로 관리자 PAID를 금지하고 취소된 경건 제출을 닫힌 상태로 유지한다.
2. 별도 관리자 납부 API와 새 재제출 charge row를 만든다.
3. 기존 관리자 status API와 source charge row를 확장하고 Billing application port로 Devotion 재오픈을 연결한다.

### 결정

3안을 적용한다. 관리 가능한 `UNPAID` 청구는 기존 관리자 status API에서 `PAID`로 전환하고 서버 현재 시각을 `paidAt`으로 저장한다. `UNPAID PENALTY + DEVOTION_RECORD -> CANCELED`이면 같은 Billing transaction에서 source weekly `submittedAt`만 null로 만들고 daily checks는 보존한다. 재제출 벌금이 양수이면 기존 CANCELED row를 같은 ID로 `UNPAID` 재사용하고, 0원이면 CANCELED row를 유지한다.

### 이유

기존 API·unique source·권한 경계를 유지하면서 잘못된 제출을 수정할 수 있고, 취소·재오픈·재제출·청구 갱신을 원자적으로 보장할 수 있다. Billing Entity와 Devotion Entity의 직접 결합도 피한다.

### 영향 범위

- Billing status policy/command와 Devotion reopen application port/adapter
- `ChargeItem` CANCELED row 재활성화와 weekly `submittedAt` 재오픈
- 관리자 PAID 및 cancel/reopen REST Docs
- 같은 청구의 사용자·관리자 상태 변경과 PENALTY/COFFEE 기존 source charge 갱신·재활성화는 동일 row write lock으로 직렬화해 뒤 요청이 커밋된 상태를 다시 읽고 기존 상태별 전이 규칙을 적용
- DB/Flyway/dependency/API path/request-response DTO는 변경 없음

### 관련 이슈

- #190
