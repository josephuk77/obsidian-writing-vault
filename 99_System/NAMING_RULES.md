# NAMING_RULES

---
tags:
  - type/project
  - status/active
---

## 폴더명

- 최상위 폴더는 `숫자_영문` 형식을 유지한다.
- 프로젝트 폴더명은 `kebab-case`를 사용한다.
- 프로젝트 내부 구조는 `_Project_Template/`를 기준으로 만든다.

## 파일명

- 일반 문서는 소문자 `kebab-case.md`를 권장한다.
- 날짜 문서는 `YYYY-MM-DD-title.md` 형식을 사용한다.
- ADR은 `ADR-0001-title.md` 형식을 사용한다.
- 에러 기록은 `ERR-0001-title.md` 형식을 사용한다.
- 프로젝트 핵심 스키마 문서는 기존 규칙에 맞춰 `INDEX.md`, `LOG.md`, `PROJECT_RULES.md`, `REPO_LINKS.md`를 사용한다.

## 링크명

- 가능한 한 Obsidian 내부 링크 `[[문서명]]`을 사용한다.
- 동일 이름 문서가 여러 프로젝트에 있을 수 있으므로 필요하면 경로 링크를 사용한다.
- 외부 링크는 링크 목적과 접속 날짜를 함께 기록한다.
