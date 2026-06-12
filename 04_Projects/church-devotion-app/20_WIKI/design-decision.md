# design-decision

---
tags:
  - type/project
  - status/planning
  - area/design
---

## 최종 디자인 기준

FaithLog 모바일 디자인은 Figma 파일 `FaithLog 모바일 와이어프레임 v2`의 원본 페이지 `FaithLog Mobile Wireframes v2` 하단에 있는 최종 세트를 기준으로 한다.

사용자가 “맨 밑에 있는 세트”를 최종 디자인 기준으로 선택했다. 따라서 이전에 만든 `Warm Campus Notebook v1` 페이지는 참고용 디자인 탐색물로만 둔다.

## Figma 링크

- [FaithLog 모바일 와이어프레임 v2](https://www.figma.com/design/RBpxs4ixQBwFUFHKg9ngh6/FaithLog-%EB%AA%A8%EB%B0%94%EC%9D%BC-%EC%99%80%EC%9D%B4%EC%96%B4%ED%94%84%EB%A0%88%EC%9E%84-v2?node-id=0-1&p=f&t=Sx80fhdYngGlQt38-0)
- 기준 page/node: `0:1`

## 기준 세트

Figma에서 가장 아래쪽에 배치된 세트는 상태/피드백 화면까지 포함한 최종 모바일 흐름이다.

### 최하단 상태 세트

- `Status 01 App Loading`
- `Status 02 Devotion Submit Loading`
- `Status 03 Devotion Submit Complete`
- `Status 04 Poll Response Loading`
- `Status 05 Poll Response Complete`
- `Status 06 Payment Mark Loading`
- `Status 07 Payment Mark Complete`
- `Status 08 Notification Sending`
- `Status 09 Notification Sent`
- `Status 10 Poll Create Loading`
- `Status 11 Poll Create Complete`
- `Status 12 Save Failed`
- `Poll UX DB 반영 메모`

### 같은 하단 디자인 흐름에 포함되는 관리자 세트

- `Admin 01 Home`
- `Admin 06 Poll Manage`
- `Admin 07 Poll Create`
- `Admin 08 Poll Result`
- `Admin 09 Poll Missing`
- `Admin 10 Settlement`
- `Admin 11 Charge Detail`
- `Admin 12 Notification Confirm`
- `Admin 13 Campus Settings`
- `Style Guide - Tokens & Components`

## 구현 반영 원칙

- 개발 구현은 `FaithLog Mobile Wireframes v2` 페이지 하단 세트를 우선 기준으로 삼는다.
- `Warm Campus Notebook v1`은 색감/톤 탐색 기록으로만 사용한다.
- 화면 구조, 상태 처리, 로딩/완료/실패 피드백은 하단 `Status` 세트를 따른다.
- 관리자 화면은 하단 `Admin` 세트와 `Style Guide - Tokens & Components`를 우선 기준으로 삼는다.
- MVP에서는 밥/식사/점심 기능을 만들지 않는다.
- 커피 기능은 MVP에 포함하되, DBML 수정본 기준으로 `polls.payment_account_id`, `payment_category = COFFEE`, `charge_generation_type = OPTION_PRICE`와 연결한다.

## 구현 시 주의

- Figma 상단/중간의 과거 시안은 기능 참고용으로만 본다.
- 같은 기능이 여러 세트에 있으면 더 아래쪽 세트를 최신 기준으로 본다.
- 디자인 문구에 식사/밥/점심이 남아 있어도 MVP 구현 범위에는 포함하지 않는다.
- 최종 구현 전에는 하단 세트의 화면명을 기준으로 프론트엔드 작업 단위를 쪼갠다.

## 결정 기록

| Date | Decision | Source |
| --- | --- | --- |
| 2026-06-12 | Figma 최하단 세트를 FaithLog 모바일 최종 디자인 기준으로 사용한다. | 사용자 결정 |
| 2026-06-12 | `Warm Campus Notebook v1`은 참고용 탐색물로만 둔다. | 사용자 결정 |
| 2026-06-12 | 최종 디자인 기준 Figma 링크를 `node-id=0-1`로 고정한다. | 사용자 제공 링크 |
