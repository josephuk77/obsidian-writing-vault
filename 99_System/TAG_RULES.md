# TAG_RULES

---
tags:
  - type/project
  - status/active
---

## 작성 위치

태그는 YAML frontmatter에 작성합니다.

```yaml
---
tags:
  - type/project
  - status/planning
---
```

## Type 태그

- `type/project`
- `type/raw-source`
- `type/decision`
- `type/error`
- `type/template`

## Status 태그

- `status/planning`
- `status/active`
- `status/paused`
- `status/archived`

## Area 태그

- `area/backend`
- `area/frontend`
- `area/infra`
- `area/ai`
- `area/career`
- `area/study`

## 규칙

- 하나의 문서에는 최소 하나의 `type/` 태그를 둔다.
- 프로젝트 문서에는 가능하면 하나의 `status/` 태그를 둔다.
- 주제성이 분명한 학습/리소스 문서에는 `area/` 태그를 둔다.
