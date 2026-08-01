# ai-brief

---
tags:
  - type/project
  - status/active
---

## Project Snapshot

- `timing-jeju`는 로컬 백엔드 저장소가 연결된 active 단계 프로젝트입니다.
- 백엔드는 Java 21, Spring Boot 4.1.0, Gradle 9.5.1, PostgreSQL/PostGIS를 사용합니다.
- 저장소는 공통 루트와 `services/spring-api`, `services/fastapi-mcp`로 나뉜 모노레포입니다.
- GitHub 원격 저장소는 `Timing-Jeju/jeju_BE`이며 초기 환경 작업은 Issue #1로 관리합니다.

## What AI Should Remember

- Raw Source는 수정하지 않습니다.
- 확정된 핵심 정보는 `20_CORE/`에 정리합니다.
- 상세 설명형 문서는 `20_WIKI/`에 둡니다.
- 실행 서비스 코드는 루트가 아니라 `services/{service}`에 둡니다.

## Current Working Context

- 백엔드 초기 환경과 모노레포 전환을 작업 단위별 커밋 6개로 구성해 `chore/1-backend-initial-setup`에 push했습니다.
- 최신 원격 HEAD는 `82fb3df`입니다.
- 다음 단계는 Issue #1의 Reviewer 검토와 `develop` 대상 PR입니다.

## Do Not Assume

- 해결할 제주 사용자 문제와 MVP 범위는 Notion 원문 수집 전까지 확정하지 않습니다. 가짜 비즈니스 도메인을 만들지 않습니다.
- FastAPI 원본 저장소가 제공되기 전에는 가짜 MCP 구현을 만들지 않습니다.

## Links

- [[INDEX]]
- [[project-facts]]
- [[open-questions]]
