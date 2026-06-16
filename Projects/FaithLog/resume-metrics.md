# FaithLog Resume Metrics Log

FaithLog를 운영 가능한 프로젝트로 만들면서 이력서에 사용할 수 있는 정량 지표, 테스트 결과, 트러블슈팅 내역을 누적 기록한다.

## 기록 원칙

- 가능한 모든 개선은 수치로 남긴다.
- 테스트가 필요하다고 판단되면 테스트 항목, 이유, 기대 지표를 먼저 적는다.
- 장애, 버그, 성능 저하, 설정 문제는 원인, 해결, 재발 방지, 전후 수치를 함께 기록한다.
- 이력서에 쓸 수 있는 문장 후보는 별도로 남긴다.

## 핵심 지표 후보

| 영역 | 지표 | 측정 방법 | 최신값 | 목표 |
| --- | --- | --- | --- | --- |
| 품질 | 테스트 통과율 | `./gradlew test` | 100% (2026-06-16) | 100% |
| 품질 | 테스트 코드 파일 수 | `rg --files src/test` | 1 test source, 1 test resource | 증가 추적 |
| 안정성 | 빌드 성공 여부 | `./gradlew build` | 성공 (2026-06-16) | 성공 |
| API | 응답 시간 | 로컬/운영 부하 테스트 | TBD | TBD |
| 운영 | 헬스체크 성공률 | `/health` 또는 배포 플랫폼 상태 | TBD | 99%+ |
| 유지보수 | 주요 모듈 수 | 패키지/도메인 기준 | TBD | 추적 |
| 데이터 | DB 마이그레이션 수 | `src/main/resources/db/migration` | 1 | 추적 |

## Daily Monitoring Notes

### 2026-06-16

- 자동화 목표: 매일 오전 6시에 프로젝트 상태를 확인하고, 수치화 가능한 변경과 개선 포인트를 보고한다.
- 기록 위치: 이 파일. Obsidian Vault 경로를 받으면 Vault 내부 문서로 옮기거나 동기화한다.
- 다음 테스트 후보:
  - `./gradlew test`로 기본 테스트 통과율 확보
  - `./gradlew build`로 배포 전 빌드 안정성 확보
  - 헬스체크 엔드포인트 기준 운영 상태 지표 정의
- 기준선 수치:
  - `./gradlew test`: 성공, 18초, 5개 Gradle task up-to-date
  - `./gradlew build`: 성공, 3초, 8개 Gradle task up-to-date
  - 테스트 코드 파일: 1개 (`FaithLogApplicationTests.java`)
  - 테스트 리소스 파일: 1개 (`application-test.yml`)
  - DB 마이그레이션: 1개 (`V1__init_schema.sql`)

## Troubleshooting Log

| 날짜 | 문제 | 원인 | 해결 | 전후 수치 | 재발 방지 |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

## Test Runs

| 날짜 | 명령/방법 | 결과 | 주요 수치 | 후속 조치 |
| --- | --- | --- | --- | --- |
| 2026-06-16 | `./gradlew test` | 성공 | 18초, 5개 task up-to-date, 테스트 통과율 100% | 기능별 테스트 수 확대 |
| 2026-06-16 | `./gradlew build` | 성공 | 3초, 8개 task up-to-date, 빌드 성공률 기준선 100% | 배포 전 빌드 체크 유지 |

## Resume Bullet Candidates

- Spring Boot 기반 FaithLog 프로젝트의 테스트 기준선을 수립하고, `./gradlew test` 기준 테스트 통과율 100%를 확보.
- `./gradlew build` 기준 빌드 성공 상태를 확보해 배포 전 안정성 검증 기준선을 수립.
