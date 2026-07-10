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

- 승인된 Docker Desktop 재시작은 별도 Android Emulator의 QEMU 프로세스가 실행 중이라 stop 단계에서 실패했다. 범위 밖 Android Emulator는 종료하지 않았다.
- Docker Desktop 앱을 다시 열어 daemon을 복구했지만, 격리 QA 2차 실행은 호스트 데이터 볼륨 가용 공간 116MiB·100% 사용 상태에서 buildx activity 임시 파일을 만들지 못해 `no space left on device`로 중단됐다.
- 두 QA 실행 모두 같은 compose project를 volume 삭제 없이 down 처리했다.
- 마지막 Docker 명령으로 `docker builder prune -f`만 실행했으나 가용 공간은 116MiB로 변하지 않았다. `docker system prune`, image/volume prune, named volume 삭제는 실행하지 않았다.
- 사용자가 호스트 디스크 공간을 확보한 뒤 같은 격리 compose QA를 다시 실행해야 한다.

## 재발 방지

- 격리 QA 전 `docker info`와 BuildKit cache 조회 가능 여부를 확인한다.
- BuildKit metadata I/O 오류를 애플리케이션 build 실패와 구분해 기록한다.
- 기존 container/volume을 임의 삭제하거나 system-wide prune으로 우회하지 않는다.
- QA 전 호스트 데이터 볼륨에 image layer와 build context를 기록할 충분한 여유 공간이 있는지 확인한다.

## 관련 이슈

- #153
