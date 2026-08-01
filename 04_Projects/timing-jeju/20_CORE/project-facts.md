# project-facts

---
tags:
  - type/project
  - status/active
---

## One-line Summary

- 제주 관련 서비스 기획을 실제 프로젝트로 만들기 위한 핵심 사실 저장소입니다.

## Confirmed Facts

| Fact | Evidence | Source |
| --- | --- | --- |
| 백엔드 로컬 저장소가 있다. | `/Users/josephuk77/Tour-API`에서 초기 품질 게이트 통과 | [[REPO_LINKS]] |
| GitHub 원격 저장소는 `Timing-Jeju/jeju_BE`다. | Issue #1과 작업 브랜치 push 완료 | [[REPO_LINKS]] |
| 백엔드는 Spring API와 FastAPI MCP를 한 저장소에서 관리하는 모노레포다. | `82fb3df` 구조 전환과 전체 품질 게이트 성공 | [[2026-07-28-backend-initial-setup-log]] |
| Spring API는 `services/spring-api`에 있고 FastAPI MCP는 `services/fastapi-mcp`에 둔다. | 모노레포 구조 테스트 5개 성공 | [[2026-07-28-backend-initial-setup-log]] |
| 백엔드는 Java 21과 Spring Boot 4.1.0을 사용한다. | Gradle build와 Docker smoke test 성공 | [[2026-07-28-backend-initial-setup-log]] |
| 기본 패키지는 `com.timingjeju.api`다. | 애플리케이션과 Architecture 테스트 확인 | [[2026-07-28-backend-initial-setup-log]] |
| 현재 상태는 active다. | 백엔드 초기 개발 환경과 모노레포 경계 구축 | [[INDEX]] |
| Notion 원문은 아직 수집되지 않았다. | Raw Source manifest 비어 있음 | [[_MANIFEST]] |

## Users

- 

## Problem

- Notion 원문 수집 후 확정합니다.

## Value Proposition

- 

## Scope Boundary

- In:
- Out:

## Links

- [[project-brief]]
- [[requirements]]
- [[REPO_LINKS]]
