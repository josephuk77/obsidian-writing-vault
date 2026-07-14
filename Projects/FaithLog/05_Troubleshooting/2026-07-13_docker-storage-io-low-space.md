---
project: FaithLog
type: troubleshooting
created: 2026-07-13
tags:
  - FaithLog
  - troubleshooting
  - docker
---

# Docker Desktop storage I/O 오류와 낮은 host 여유 공간

## 문제 상황

#188 feature Docker 시도에서 공개 PostgreSQL/Redis image pull과 Docker 내부 Gradle `bootJar`는 성공했지만 image layer 전환 단계에서 Docker Desktop backend가 중지됐다.

## 에러 메시지

- overlay2 intermediate root filesystem 제거: `input/output error`
- containerd metadata: `meta.db: input/output error`
- Docker Desktop backend status: `stopped`
- host available space: 561MiB

## 원인 분석

애플리케이션 compile 또는 bootJar 실패가 아니라 Docker Desktop storage layer에서 발생한 I/O 오류다. host 여유 공간이 매우 낮은 상태도 함께 관찰됐다. 데이터 삭제 없는 restart로 backend가 복구되지 않았다.

## 해결 방법

사용자 승인 없이 cache, worktree build, Docker image/volume을 삭제하지 않았다. 최신 사용자 결정에 따라 feature 세션의 Docker QA를 중단하고 세 feature 통합 이후 `integration/188-190-devotion-meal-billing`에서 한 번 수행하도록 이관했다.

## 재발 방지

- integration Docker QA 전에 host 여유 공간을 사용자 승인 절차로 확보
- 격리 compose project만 사용하고 QA 후 `down`으로 종료
- `down -v`, named volume 삭제, system/image/volume prune 금지
- 모든 Docker 작업의 마지막 명령은 `docker builder prune -f`

## 관련 이슈

- #188
- #189
- #190
