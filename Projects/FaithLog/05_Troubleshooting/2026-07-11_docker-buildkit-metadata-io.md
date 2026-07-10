---
project: FaithLog
type: troubleshooting
created: 2026-07-11
tags:
  - FaithLog
  - troubleshooting
  - docker
---

# Docker BuildKit metadata DB I/O 오류

## 문제 상황

Issue #153 격리 Docker QA에서 `faithlog-qa-153-prayer` project의 clean app image를 build하던 중 BuildKit 내부 metadata DB 쓰기가 실패했다. QA 스크립트 trap은 같은 compose project를 volume 삭제 없이 down 처리했다.

## 에러 메시지

```text
write /var/lib/docker/buildkit/metadata_v2.db: input/output error
error getting build cache usage: failed to get usage for ...: write /var/lib/docker/buildkit/snapshots.db: input/output error
```

## 원인 분석

`docker info`는 daemon 정보를 반환했지만 `docker system df`가 동일 `snapshots.db` I/O 오류로 실패했다. Dockerfile 단계나 Spring application build가 아니라 Docker Desktop VM 내부 BuildKit metadata 저장소 상태 문제로 판단한다.

## 해결 방법

- 현재 작업에서는 다른 Docker 환경에 영향을 줄 수 있는 Docker Desktop 재시작을 사용자 승인 없이 수행하지 않았다.
- 재시작 승인 후 같은 격리 compose QA를 재실행한다.
- QA 성공 후 마지막 Docker 명령으로 `docker builder prune -f`만 실행하고 volume/system/image prune은 실행하지 않는다.

## 재발 방지

- 격리 QA 전 `docker info`와 BuildKit cache 조회 가능 여부를 확인한다.
- BuildKit metadata I/O 오류를 애플리케이션 build 실패와 구분해 기록한다.
- 기존 container/volume을 임의 삭제하거나 system-wide prune으로 우회하지 않는다.

## 관련 이슈

- #153
