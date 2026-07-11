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
| 품질 | 테스트 통과율 | `./gradlew test` | 100% of executed tests (2026-07-11 #153, 355 tests / 0 failures / 0 errors / 1 skipped) | 100% |
| 품질 | 테스트 코드 파일 수 | `rg --files src/test/java | rg '\.java$'` | 70 test files (2026-07-11 #153) | 증가 추적 |
| 품질 | 인증/문서 스니펫 묶음 수 | `find build/generated-snippets -mindepth 1 -maxdepth 1 -type d` | 57 snippet groups (2026-07-10, checked-out branch) | 증가 추적 |
| 안정성 | 빌드 성공 여부 | `./gradlew build` | 성공 (2026-07-11 #153) | 성공 |
| API | 응답 시간 | 로컬/운영 부하 테스트 | 측정 보류 (2026-06-17) | TBD |
| 운영 | 헬스체크 성공률 | `/health` 또는 배포 플랫폼 상태 | 측정 보류 (2026-06-17) | 99%+ |
| 유지보수 | 주요 모듈 수 | 패키지/도메인 기준 | 10 top-level modules, 559 Java sources including tests (2026-07-11 #153) | 추적 |
| 데이터 | DB 마이그레이션 수 | `src/main/resources/db/migration` | 6 (Flyway V1-V6, 2026-07-10 #152) | 추적 |

## Daily Monitoring Notes

### 2026-07-11

- #153 Prayer 유스케이스 책임 분리:
  - 기준: 최신 `origin/develop` `f6e3c2e`, 별도 worktree, `chore/153-prayer-usecase-separation`.
  - TDD: production 수정 전 구조 테스트 5건을 추가해 5/5 RED를 확인하고 책임 이동 후 5/5 GREEN. PM 리뷰에서 다중 제출 서비스명을 새 이름 기준으로 먼저 바꿔 다시 5/5 RED를 확인하고 production rename 후 GREEN. 기존 Prayer service/동시성/REST Docs characterization 유지.
  - 분리: 11개 public 유스케이스를 season command/query, group command/query, board query, 조별/본인 submission command의 7개 전용 Service로 분리. `PrayerGroupSubmissionCommandService`는 일반 ACTIVE 멤버의 자기 활성 조 다중 입력과 관리자 전체 조 입력을 모두 포함하는 권한 범위를 표현한다. 권한·대상 조원·보드 조립은 3개 package-private support에 응집.
  - 줄 수: `PrayerService` 606→90(-516, -85.1%). 추출 class를 포함한 전체 코드 감소가 아니라 compatibility facade 책임 축소 수치.
  - 검증: PM 리뷰 rename 이후 Prayer focused 23/23, Campus+Billing/Devotion/Poll/Prayer/Batch 260/260, 전체 355 tests / 0 failures / 0 errors / 1 skipped, build/asciidoctor 성공. PM 세션의 독립 Gradle 실행과 같은 worktree `build/classes` 경합으로 발생한 삭제/쓰기 실패 및 손상 class/XML 결과는 코드 실패에서 분리했고, worker 0개 확인과 `./gradlew clean` 후 단독 test/build 재실행으로 최종 수치를 확정했다. Docker QA는 BuildKit metadata DB I/O 오류와 호스트 가용 공간 116MiB·100% 사용 상태의 no-space 오류로 image/health 확인 미완료. volume/system/image prune과 named volume 삭제는 수행하지 않았고 마지막 Docker 명령은 `docker builder prune -f`였다.
  - 무변경: API/DTO/ErrorCode/Entity/DB/Flyway/repository/의존성 변경 0건, Swagger annotation 추가 0건, Controller Entity import 0건, 서비스 순환 의존 0건.
  - 이력서 후보: `Prayer의 11개 유스케이스를 조별 다중 제출을 포함한 7개 응집 Service와 3개 package-private support로 분리해 606줄 통합 Service를 90줄 호환 facade로 85.1% 축소하고, 5개 구조 회귀 테스트·355개 전체 테스트·260개 연관 도메인 테스트로 API·DB·권한·optimistic locking·all-or-nothing 동작 무변경을 보장했다.`


### 2026-07-11 Daily Monitor (checked-out branch)

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중이다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/chore/145-ddd-mvc-package-structure`, `origin/chore/147-campus-admin-usecase-separation`, `origin/chore/148-billing-command-usecase-separation`, `origin/chore/149-billing-query-aggregation-separation`, `origin/chore/150-devotion-usecase-separation`, `origin/chore/151-poll-core-usecase-separation`, `origin/chore/152-poll-template-coffee-settlement-separation`, `origin/chore/165-devotion-test-isolation` 원격 ref가 정리됐다.
  - `git status --short`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 브랜치 divergence: `git rev-list --left-right --count origin/develop...HEAD` 기준 현재 브랜치 ahead 4, behind 134
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1777 insertions(+), 8 deletions(-)
  - 지난 자동화 실행 시각(`2026-07-09T21:01:14.351Z`) 이후 현재 체크아웃 브랜치 새 커밋: 0건
  - 같은 기간 `origin/develop` 비-merge 실변경 커밋: 38건. 최근 묶음은 `#146` DDD 패키지 구조 정리, `#147` Campus Admin 책임 분리, `#148` Billing 명령 책임 분리, `#149` Billing 조회 책임 분리, `#150` Devotion 책임 분리, `#151` Poll core 책임 분리, `#152` Poll template/coffee settlement 책임 분리, `#165` 테스트 DB 격리 보강이다.
  - 같은 기간 `origin/develop` 누적 변경량: 546 unique files changed, 7496 insertions(+), 3979 deletions(-)
  - 변경 영역: `admin`, `batch`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `prayer`, `user`
  - 의존성/CI 파일 변경: 관찰된 범위에서 없음
  - DB 마이그레이션 신규 변경: 현재 체크아웃 브랜치 0, 로컬 `origin/develop` snapshot 6
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: 8 top-level modules, 231 Java sources, 28 test Java sources, 1 test resource, 57 snippet groups, 2 GitHub Actions workflows, DB 마이그레이션 0개
  - 로컬 `origin/develop` tree snapshot: 479 Java sources, 69 test Java sources, DB 마이그레이션 6개
- 검증 신호:
  - `./gradlew test --warning-mode all --console=plain`: 성공, 14초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all --console=plain`: 성공, 17초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐다.
  - build problems report: `build/reports/problems/problems-report.html` 갱신 (`2026-07-11 06:03:50 +0900`, 129,871 bytes)
  - 테스트 HTML 리포트: `build/reports/tests/test/index.html`은 rerun이 `UP-TO-DATE`로 끝나 `2026-06-20 06:03:15 +0900`, 10,574 bytes 상태를 유지했다.
- 운영/배포 신호:
  - `docker ps --format '{{.Names}}'`: 현재 세션에서 `EOF`로 실패해 실행 중 컨테이너 수를 확인하지 못했다.
  - health/latency 측정은 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope`, `2026-07-08 - Daily Monitor Local Runtime Startup Scope`, `2026-07-10 - Daily Monitor Upstream Revalidation Branch-Switch Scope` pending question이 남아 있어 오늘도 보류했다.
- 오늘 리스크/관찰:
  - 현재 체크아웃 브랜치 기준 신규 앱 코드 변경은 없고 로컬 검증 성공도 docs branch 기준이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `ahead 4 / behind 134`까지 벌어져 checked-out branch 검증값을 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - 최신 upstream에는 Java 소스 479개, 테스트 Java 소스 69개, 마이그레이션 6개가 있지만 현재 체크아웃 브랜치에는 각각 231개, 28개, 0개라 최신 통합선 품질을 직접 재검증하지 못했다.
  - Gradle deprecated 경고는 오늘도 동일하게 1건 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다.
  - Docker 운영 신호는 오늘 `EOF` 실패로 비어 있다.
  - 운영 리스크 집계: 5건(브랜치 격차, upstream 미재검증, Gradle deprecated 경고 지속, Docker 운영 신호 부재, untracked 파일 `0`)
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 checked-out docs branch 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: develop 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.campus.service.CampusUseCaseServiceStructureTest --tests com.faithlog.billing.service.BillingCommandUseCaseServiceStructureTest --tests com.faithlog.billing.service.BillingQueryUseCaseServiceStructureTest --tests com.faithlog.devotion.service.DevotionUseCaseServiceStructureTest --tests com.faithlog.poll.service.PollUseCaseServiceStructureTest --tests com.faithlog.poll.service.PollTemplateSettlementServiceStructureTest`
  - 이유: 지난 실행 이후 최신 upstream 핵심 실변경이 책임 분리 구조 회귀(`#147`~`#152`)에 집중돼 있기 때문이다.
  - 기대 지표: 구조 분리 회귀 테스트 pass/fail, 패키지 경계 유지 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.support.TestDatabaseIsolationConfigTest`
  - 이유: 지난 실행 이후 최신 upstream 핵심 수정 중 하나가 테스트 DB 격리 보강(`#165`)이기 때문이다.
  - 기대 지표: 테스트 컨텍스트 격리 회귀 pass/fail
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘도 직접 재확인하지 못했다.
  - 기대 지표: develop 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 Asciidoctor/Grolifant 계열 플러그인 경로가 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test --warning-mode all`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-10과 2026-07-11 모두 테스트/빌드 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인
  - 미해결 관찰 2: 운영 측정 신호 미확보.
  - 문제: `docker ps --format '{{.Names}}'`가 `EOF`로 실패해 컨테이너 상태와 `/api/v1/health` 측정 대상을 확인하지 못했다.
  - 원인: 현재 세션의 Docker daemon 접근 상태 또는 응답 경로가 불안정한 것으로 관찰되지만, 자동으로 환경을 변경하거나 재기동하는 범위는 승인되지 않았다.
  - 조치 현황: 오늘은 실패 사실만 기록하고 Docker 재기동이나 런타임 시작은 수행하지 않았다.
  - 전후 지표: 2026-07-11 컨테이너 수 미확인 / health 미측정
  - 재발 방지 후보: Docker 접근 경로 또는 로컬 런타임 기동 허용 범위를 사용자 승인으로 먼저 확정해야 한다.
- 오늘 이력서 bullet 후보:
  - checked-out branch 기준 신규 구현 성과 없음.
  - upstream observed candidate: 지난 실행 이후 `origin/develop`에는 책임 분리/테스트 격리 중심 비-merge 커밋 38건이 누적됐고, 10개 앱 영역에 걸쳐 546개 파일과 7496 insertions가 관찰됐다. 단, 현재 브랜치 재검증 전까지는 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-10

- #152 Poll 템플릿과 커피 정산 책임 분리:
  - 기준: 최신 `origin/develop` `d7ae1d6`, 별도 worktree, `chore/152-poll-template-coffee-settlement-separation`.
  - TDD: production 수정 전 구조 테스트 6건을 추가해 6/6 RED를 확인하고 책임 이동 후 6/6 GREEN. 자동 생성 snapshot 전체 필드와 비활성 auto template 제외 characterization 추가.
  - 분리: template command 3개/query 2개를 `PollTemplateCommandService`/`PollTemplateQueryService`, option snapshot을 `PollTemplateOptionSupport`, 자동 복사를 `ScheduledPollFactory`, settlement transaction/Billing orchestration을 `CoffeePollSettlementCommandService`, eligibility/response-option 조립을 `CoffeePollSettlementSupport`로 분리. `CoffeeCatalogService`는 변경하지 않음.
  - 줄 수: `PollTemplateService` 218→42(-80.7%), `PollAutomationService` 207→121(-41.5%), `CoffeePollSettlementService` 130→17(-86.9%). 추출 class를 포함한 전체 코드 감소가 아니라 facade/orchestrator 책임 축소 수치.
  - 검증: focused 62/62, 4-domain 204/204, 전체 350 tests / 0 failures / 0 errors / 1 skipped, build/asciidoctor 성공, 격리 Docker image build + PostgreSQL/Redis healthy + backend `data.status=UP` + volume 삭제 없는 down. GitHub CI는 PR/push 금지로 미실행.
  - 무변경: API/DTO/ErrorCode/Entity/DB/Flyway/repository/scheduler/의존성 변경 0건, Swagger annotation 추가 0건, Controller Entity import 0건, 서비스 순환 의존 0건.
  - 이력서 후보: `Poll template의 5개 command/query와 자동 생성·커피 정산 책임을 전용 Service/Support/Factory로 분리해 기존 통합 Service를 최대 86.9% 축소하고, 6개 구조 회귀 테스트·350개 전체 테스트·204개 4-domain 테스트·격리 Docker health 검증으로 API·DB·권한·스케줄·정산 동작 무변경을 보장했다.`

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중이다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/main`이 `904135a`로 갱신됐고 `origin/fix/139-timezone-config`, `origin/fix/142-poll-status-time-sync-dev` 원격 ref는 정리됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 브랜치 divergence: `git rev-list --left-right --count origin/develop...HEAD` 기준 현재 브랜치 ahead 4, behind 95
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1695 insertions(+), 8 deletions(-)
  - 지난 자동화 실행 시각(`2026-07-08T21:16:35.441Z`) 이후 현재 체크아웃 브랜치 새 커밋: 0건
  - 같은 기간 `origin/develop` 비-merge 실변경 커밋: 3건 (`77f0822`, `b2dde4a`, `354ee68`)
  - 같은 기간 `origin/main` 비-merge 커밋: 2건 (`b2dde4a`, `904135a`)
  - develop 비-merge 실변경 중 code/config 영향 커밋: 2건 (`#140`, `#143`), 합계 8 unique files changed, 262 insertions(+), 8 deletions(-)
  - 변경 영역: `global`, `poll`, `deploy`, `config`, `docs`
  - 의존성/CI 파일 변경: 0건
  - DB 마이그레이션 신규 변경: 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: 8 top-level modules, 231 Java sources, 28 test Java sources, 1 test resource, 57 snippet groups, 2 GitHub Actions workflows, DB 마이그레이션 0개
  - 로컬 `origin/develop` tree snapshot: 437 Java sources, 59 test Java sources, DB 마이그레이션 6개
- 검증 신호:
  - `./gradlew test --warning-mode all --console=plain`: 성공, 1분 8초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all --console=plain`: 성공, 2초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐다.
  - build problems report: `build/reports/problems/problems-report.html` 갱신 (`2026-07-10 06:05:41 +0900`, 129,871 bytes)
  - 테스트 HTML 리포트: `build/reports/tests/test/index.html`은 rerun이 `UP-TO-DATE`로 끝나 `2026-06-20 06:03:15 +0900`, 10,574 bytes 상태를 유지했다.
- 최신 통합선 변경 관찰:
  - `origin/develop` 최신 ref는 `1bc3578` (`release: #142 main 변경사항을 develop에 병합`)이다.
  - `77f0822`는 `#140 서버 DB 세션 시간대 설정 정리`로 5 files changed, 96 insertions(+), `ApplicationTimeZoneConfig`, `application.yml`, `TimeZoneConfigurationTest`를 추가해 UTC JVM 환경에서 날짜 저장 밀림을 방지하는 방향의 코드/테스트 증거를 남겼다.
  - `354ee68`은 `#143 투표 조회 상태 시간 동기화`로 5 files changed, 166 insertions(+), 8 deletions(-)이며 `PollService`, `PollServiceTest`, `docs/wiki/engineering/2026-07-09-poll-status-time-sync.md`를 갱신했다.
  - `b2dde4a`와 `904135a`는 각각 `main` 반영/배포 release 커밋으로 관찰됐지만, 오늘 모니터는 dirty worktree를 바꾸지 않고 현재 브랜치에 머물렀으므로 최신 통합선 직접 재검증은 하지 않았다.
- 운영/배포 신호:
  - `docker ps`: 성공. 실행 중 컨테이너 0개.
  - health/latency 측정은 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope`와 `2026-07-08 - Daily Monitor Local Runtime Startup Scope` pending question이 남아 있고 앱 컨테이너도 없어 오늘도 보류했다.
- 오늘 리스크/관찰:
  - 현재 체크아웃 브랜치 기준 신규 앱 코드 변경은 없고 로컬 검증 성공도 docs branch 기준이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `ahead 4 / behind 95`까지 벌어져 checked-out branch 검증값을 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - 최신 upstream에는 Java 소스 437개, 테스트 Java 소스 59개, 마이그레이션 6개가 있지만 현재 체크아웃 브랜치에는 각각 231개, 28개, 0개라 최신 통합선 품질을 직접 재검증하지 못했다.
  - Gradle deprecated 경고는 오늘도 동일하게 1건 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다.
  - 운영 리스크 집계: 5건(브랜치 격차, upstream 미재검증, Gradle deprecated 경고 지속, 실행 중 컨테이너 부재, dirty worktree로 인한 branch-switch 검증 미실시)
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 checked-out docs branch 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: develop 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && TZ=UTC ./gradlew test --tests com.faithlog.deploy.TimeZoneConfigurationTest`
  - 이유: 지난 실행 이후 최신 upstream 핵심 실변경 중 하나가 UTC 환경 날짜 저장 보강(`#140`)이기 때문이다.
  - 기대 지표: UTC 환경 날짜 저장 회귀 pass/fail, 시간대 설정 계약 검증 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.poll.application.PollServiceTest`
  - 이유: 지난 실행 이후 최신 upstream 핵심 실변경 중 하나가 투표 조회 상태 시간 동기화(`#143`)이기 때문이다.
  - 기대 지표: poll 상태 계산 회귀 테스트 pass/fail
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘도 직접 재확인하지 못했다.
  - 기대 지표: develop 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 Asciidoctor/Grolifant 계열 플러그인 경로가 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test --warning-mode all`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-09와 2026-07-10 모두 테스트/빌드 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인
  - 미해결 관찰 2: 운영 측정 대상 미기동.
  - 문제: `docker ps`는 성공했지만 실행 중 컨테이너가 0개라 `/api/v1/health`나 응답 시간 측정을 수행할 대상이 없었다.
  - 원인: 현재 세션에서 로컬 FaithLog 런타임이 시작되지 않았고, 자동 기동 허용 범위도 승인되지 않았다.
  - 조치 현황: 오늘은 런타임 자동 기동을 추측하지 않고 컨테이너 0개 사실만 기록했다.
  - 전후 지표: 2026-07-09와 2026-07-10 모두 `docker ps` 성공 / 실행 중 컨테이너 0개
  - 재발 방지 후보: 모니터링이 로컬 런타임을 자동으로 올려도 되는지 사용자 승인 범위를 먼저 확정해야 한다.
- 오늘 이력서 bullet 후보:
  - checked-out branch 기준 신규 구현 성과 없음.
  - upstream observed candidate: 2026-07-09 기준 최신 통합선에는 UTC 환경 날짜 저장 보강(`#140`)과 투표 조회 상태 시간 동기화(`#143`)가 추가돼 8개 고유 파일, 262 insertions, 2개 핵심 앱 영역(`global`, `poll`)과 회귀 테스트 2종 이상 영향이 관찰됐다. 단, 현재 브랜치 재검증 전까지는 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-09

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중이다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 브랜치 divergence: `git rev-list --left-right --count origin/develop...HEAD` 기준 현재 브랜치 ahead 4, behind 89
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1625 insertions(+), 8 deletions(-)
  - 지난 자동화 실행 시각(`2026-07-07T21:14:47.750Z`) 이후 현재 체크아웃 브랜치 새 커밋: 0건
  - 같은 기간 `origin/develop` 비-merge 실변경 커밋: 2건 (`3edb1df`, `de2a227`), `origin/main` release 커밋: 1건 (`e742dc6`)
  - 최근 upstream 실변경 묶음: 30 unique files, 1129 insertions, 16 deletions, 8개 앱 모듈(`batch`, `billing`, `campus`, `devotion`, `notification`, `poll`, `prayer`, `user`) + config/docs 영향
  - 의존성/CI 파일 변경: 0건
  - DB 마이그레이션 신규 변경: 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: 8 top-level modules, 231 Java sources, 28 test Java sources, 1 test resource, 57 snippet groups, 2 GitHub Actions workflows, DB 마이그레이션 0개
  - 로컬 `origin/develop` tree snapshot: 437 Java sources, 59 test Java sources, DB 마이그레이션 6개
- 검증 신호:
  - `./gradlew test --warning-mode all`: 성공, 1분 6초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 2초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐다.
  - build problems report: `build/reports/problems/problems-report.html` 갱신 (`2026-07-09 09:07:50 +0900`, 129,871 bytes)
  - 테스트 HTML 리포트: `build/reports/tests/test/index.html`은 현재 rerun이 `UP-TO-DATE`로 끝나 `2026-06-20 06:03:15 +0900`, 10,574 bytes 상태를 유지했다.
- 최신 통합선 변경 관찰:
  - `origin/develop` 최신 ref는 `993d6ee` (`2026-07-08`, `Merge branch 'main' into develop`)이며, 실질적인 새 기능/개선 근거는 `3edb1df`와 `de2a227`이다.
  - `3edb1df`는 `#134 1000명 조회 성능 최적화`로 9 files changed, 197 insertions(+), 7 deletions(-)이며 `poll`, `prayer`, `user`, `campus` 경로와 테스트 2종을 함께 갱신했다.
  - `de2a227`은 `#136 운영 데이터 정리 배치 구현`으로 22 files changed, 932 insertions(+), 9 deletions(-)이며 `batch` 정리 서비스/스케줄러, 여러 repository 조회 메서드, `application.yml`, 테스트 4종을 추가·보강했다.
  - 위 upstream 구현값은 현재 체크아웃 브랜치에서 직접 checkout 재검증하지 않았으므로 계속 "upstream observed evidence"로만 취급해야 한다.
- 운영/배포 신호:
  - `docker ps`: 성공. 실행 중 컨테이너 0개.
  - health/latency 측정은 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope`와 `2026-07-08 - Daily Monitor Local Runtime Startup Scope` pending question이 남아 있어 오늘도 보류했다.
- 오늘 리스크/관찰:
  - 현재 체크아웃 브랜치는 오늘도 문서 변경만 있고 신규 앱 코드 검증 근거는 없다.
  - 현재 브랜치와 `origin/develop`의 격차가 `ahead 4 / behind 89`까지 벌어져 checked-out branch 검증값을 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - 최신 upstream에는 Java 소스 437개, 테스트 Java 소스 59개, 마이그레이션 6개가 있지만 현재 체크아웃 브랜치에는 각각 231개, 28개, 0개라 최신 통합선 품질을 직접 재검증하지 못했다.
  - Gradle deprecated 경고는 오늘도 동일하게 1건 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다.
  - 운영 리스크 집계: 4건(브랜치 격차, upstream 미재검증, Gradle deprecated 경고 지속, 실행 중 컨테이너 부재)
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 checked-out docs branch 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: develop 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.batch.application.DataRetentionCleanupServiceTest --tests com.faithlog.batch.scheduler.FaithLogSchedulerConfigTest --tests com.faithlog.user.presentation.AuthLogoutFcmPersistenceTest --tests com.faithlog.poll.application.PollServiceTest --tests com.faithlog.prayer.application.PrayerServiceTest`
  - 이유: 지난 실행 이후 최신 upstream 실변경이 #134 조회 최적화와 #136 데이터 정리 배치 구현이기 때문이다.
  - 기대 지표: batch/poll/prayer/user 회귀 테스트 pass/fail, 신규 정리 배치 계약 회귀 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘도 직접 재확인하지 못했다.
  - 기대 지표: develop 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 Asciidoctor/Grolifant 계열 플러그인 경로가 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test --warning-mode all`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-08과 2026-07-09 모두 테스트/빌드 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인
  - 미해결 관찰 2: 운영 측정 대상 미기동.
  - 문제: `docker ps`는 성공했지만 실행 중 컨테이너가 0개라 `/api/v1/health`나 응답 시간 측정을 수행할 대상이 없었다.
  - 원인: 현재 세션에서 로컬 FaithLog 런타임이 시작되지 않았고, 자동 기동 허용 범위도 승인되지 않았다.
  - 조치 현황: 오늘은 런타임 자동 기동을 추측하지 않고 컨테이너 0개 사실만 기록했다.
  - 전후 지표: 2026-07-08과 2026-07-09 모두 `docker ps` 성공 / 실행 중 컨테이너 0개
  - 재발 방지 후보: 모니터링이 로컬 런타임을 자동으로 올려도 되는지 사용자 승인 범위를 먼저 확정해야 한다.
- 오늘 이력서 bullet 후보:
  - checked-out branch 기준 신규 구현 성과 없음.
  - upstream observed candidate: `origin/develop`에는 지난 실행 이후 #134 1000명 조회 최적화와 #136 운영 데이터 정리 배치 구현이 추가돼 30개 파일, 8개 앱 모듈, 테스트 6종 이상 영향이 관찰됐다. 단, 현재 브랜치 재검증 전까지는 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-08

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중이다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. fetch 후에도 로컬 `origin/develop` 최신 ref는 `e52459f`(2026-07-06, `Merge branch 'main' into develop`), `origin/main` 최신 ref는 `31bdad1`(2026-07-06, `[Release] develop 변경사항 main 병합 (#133)`)로 유지됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 지난 자동화 실행 시각(`2026-07-06T21:01:05.561Z`) 이후 현재 체크아웃 브랜치, 로컬 `origin/develop`, 로컬 `origin/main`에서 새 커밋은 관찰되지 않았다.
  - `git rev-list --left-right --count origin/develop...HEAD`: `85 4`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1547 insertions(+), 8 deletions(-)
  - 지난 실행 이후 새 upstream 실변경: 0건
  - 지난 실행 이후 브랜치 고유 앱 코드 변경: 0건
  - 지난 실행 이후 브랜치 고유 테스트 코드 변경: 0건
  - 지난 실행 이후 의존성/CI 파일 변경: 0건
  - 지난 실행 이후 DB 마이그레이션 변경: 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개, Java 소스 231개
  - 현재 체크아웃 브랜치: 테스트 Java 소스 28개, 테스트 리소스 1개, REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 435개, 테스트 Java 소스 57개, DB 마이그레이션 6개
- 검증 신호:
  - `./gradlew test --warning-mode all`: 성공, 9초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 3초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-08 08:09:43 +0900`, 129,871 bytes)
  - 테스트 HTML 리포트: `build/reports/tests/test/index.html`은 현재 rerun이 `UP-TO-DATE`로 끝나 `2026-06-20 06:03:15 +0900`, 10,574 bytes 상태를 유지했다.
- 최신 통합선 변경 관찰:
  - 지난 실행 이후 로컬 `origin/develop`와 `origin/main`에 새 커밋은 없었다.
  - 최신 통합선의 마지막 실변경 관찰값은 전일과 동일하다. `origin/develop` 최신 ref `e52459f`는 `b498356` 회원 탈퇴/계정 소프트 삭제 구현을 반영한 merge 결과다.
  - `b498356`은 20 files changed, 632 insertions(+), 8 deletions(-)이며 `user` 도메인 중심 앱 코드 11개 수정/추가, `V6__add_user_deleted_at.sql` 추가, `UserDeletionControllerTest` 신규 추가, `AuthApiRestDocsTest`와 `PostgresFlywayMigrationTest` 보강을 포함한다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 계속 "upstream documented evidence"로만 취급해야 한다.
- 운영/배포 신호:
  - `docker ps`: 성공. 실행 중 컨테이너 0개로 확인됐다.
  - health/latency 측정 대상은 여전히 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending decision 상태이며, 현재 실행 중 앱 컨테이너도 없어 새 수치를 추가하지 않았다.
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 앱 코드 성과는 없고, 오늘 새 근거는 checked-out branch 품질 재검증과 운영 신호 공백 재확인이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `85 4`로 유지돼, checked-out branch 검증값을 최신 통합선 품질로 인용하면 과대해석 위험이 크다.
  - 최신 upstream에는 DB 마이그레이션 6개와 테스트 Java 소스 57개가 있지만 현재 체크아웃 브랜치에는 각각 0개, 28개라서 통합선 품질을 직접 재검증하지 못했다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-08까지 연속 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다.
  - 운영 리스크 집계: 4건(브랜치 격차, upstream 미재검증, Gradle deprecated 경고 지속, 실행 중 컨테이너 부재)
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.user.presentation.UserDeletionControllerTest --tests com.faithlog.user.presentation.AuthApiRestDocsTest --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: 최신 통합선에서 마지막으로 관찰된 실변경이 회원 탈퇴/계정 소프트 삭제와 `V6` migration 추가다.
  - 기대 지표: user deletion 회귀 테스트 pass/fail, REST Docs 계약 pass/fail, Flyway migration test pass/fail
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘도 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 Asciidoctor/Grolifant 계열 플러그인 경로가 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test --warning-mode all`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-07과 2026-07-08 모두 빌드 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인
  - 미해결 관찰 2: 운영 측정 대상 미기동.
  - 문제: `docker ps`는 성공했지만 실행 중 컨테이너가 0개라 `/api/v1/health`나 응답 시간 측정을 수행할 대상이 없었다.
  - 원인: 현재 세션에서 로컬 FaithLog 런타임이 시작되지 않았다.
  - 조치 현황: 오늘은 런타임 자동 기동을 추측하지 않고, 컨테이너 0개 사실만 기록했다.
  - 전후 지표: 2026-07-07 Docker socket 미확인 -> 2026-07-08 `docker ps` 성공 / 실행 중 컨테이너 0개
  - 재발 방지 후보: 모니터링이 로컬 런타임을 자동으로 올려도 되는지 사용자 승인 범위를 먼저 확정해야 한다.
- 오늘 이력서 bullet 후보:
  - 신규 구현 개선이 없어 오늘은 추가 후보 없음.

### 2026-07-07

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중이다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop`는 `e52459f`(2026-07-06, `Merge branch 'main' into develop`)로, `origin/main`은 `31bdad1`(2026-07-06, `[Release] develop 변경사항 main 병합 (#133)`)로 갱신됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 지난 자동화 실행 시각(`2026-07-05T21:00:15.920Z`) 이후 현재 체크아웃 브랜치 새 커밋은 없고, `origin/develop`에는 `b498356`(2026-07-06, `[Feat] 회원 탈퇴와 계정 소프트 삭제 구현 (#132)`)와 merge commit `e52459f`가 추가됐다.
  - `git rev-list --left-right --count origin/develop...HEAD`: `85 4`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1433 insertions(+), 8 deletions(-)
  - 지난 실행 이후 최신 upstream 실변경 누적: 20 files changed, 632 insertions(+), 8 deletions(-)
  - upstream 변경 구성: 문서 3개, AsciiDoc index 1개, 앱 코드 11개, DB 마이그레이션 1개, 테스트 4개
  - 지난 실행 이후 최신 upstream 기준 의존성/CI 파일 변경: 0건
  - 지난 실행 이후 최신 upstream 기준 DB 마이그레이션 변경: `V6__add_user_deleted_at.sql` 1건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개, Java 소스 231개
  - 현재 체크아웃 브랜치: 테스트 Java 소스 28개, 테스트 리소스 1개, REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 435개, 테스트 Java 소스 57개, DB 마이그레이션 6개
- 검증 신호:
  - `./gradlew test`: 성공, 7초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 2초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-07 06:02:41 +0900`)
- 최신 통합선 변경 관찰:
  - `origin/develop` 최신 ref `e52459f`는 실질적으로 `b498356` 회원 탈퇴/계정 소프트 삭제 구현을 반영한 merge 결과다.
  - `b498356`은 20 files changed, 632 insertions(+), 8 deletions(-)이며 `user` 도메인 중심 앱 코드 11개 수정/추가, `V6__add_user_deleted_at.sql` 추가, `UserDeletionControllerTest` 신규 추가, `AuthApiRestDocsTest`와 `PostgresFlywayMigrationTest` 보강을 포함한다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 계속 "upstream documented evidence"로만 취급해야 한다.
- 운영/배포 신호:
  - `docker ps`: 실패. `unix:///Users/josephuk77/.docker/run/docker.sock` 미존재로 Docker daemon/runtime 상태를 확인하지 못했다.
  - health/latency 측정 대상은 여전히 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending decision 상태라 새 수치를 추가하지 않았다.
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 앱 코드 성과는 없고, 오늘 새 근거는 checked-out branch 품질 재검증과 latest upstream 회원 탈퇴 구현 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `85 4`로 더 벌어져, checked-out branch 검증값을 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - 최신 upstream에는 DB 마이그레이션 6개와 테스트 Java 소스 57개가 있지만 현재 체크아웃 브랜치에는 각각 0개, 28개라서 통합선 품질을 직접 재검증하지 못했다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-07까지 연속 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.user.presentation.UserDeletionControllerTest --tests com.faithlog.user.presentation.AuthApiRestDocsTest --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: 지난 실행 이후 최신 upstream 핵심 실변경이 회원 탈퇴/계정 소프트 삭제와 `V6` migration 추가다.
  - 기대 지표: user deletion 회귀 테스트 pass/fail, REST Docs 계약 pass/fail, Flyway migration test pass/fail
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 Asciidoctor/Grolifant 계열 플러그인 경로가 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-06과 2026-07-07 모두 빌드 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인
  - 미해결 관찰 2: Docker 운영 신호 수집 불가.
  - 문제: `docker ps`가 Docker API socket 미존재로 실패했다.
  - 원인: 현재 세션에서 `/Users/josephuk77/.docker/run/docker.sock` 경로를 찾을 수 없었다.
  - 조치 현황: 오늘은 실패 사실만 기록하고 런타임 측정은 보류했다.
  - 전후 지표: 컨테이너 상태 미확인, `/api/v1/health` 측정 미실시
  - 재발 방지 후보: Docker daemon 가동 여부와 모니터링 실행 환경의 socket 경로를 먼저 확인해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: 회원 탈퇴/계정 소프트 삭제 구현이 앱 코드 11개 수정·추가, `V6__add_user_deleted_at.sql` 1개 추가, user/Flyway 테스트 3종 보강과 함께 `origin/develop`에 반영됐다. 단, `origin/develop` 직접 체크아웃 재검증 전까지는 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-06

- 브랜치/작업트리:
  - 기준 문서 확인: repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고, 기존 승인 결정대로 `AGENTS.md`를 단일 Agent 규칙 파일로 취급했다.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - 지난 자동화 실행 시각(`2026-07-04T21:09:36.805Z`) 이후 현재 체크아웃 브랜치와 로컬 `origin/develop`, `origin/main` ref에서 새 커밋은 관찰되지 않았다.
  - 최근 가시 커밋 기준: `HEAD`는 `fc366d7` (`docs: #38 투표 결과 조회와 커피 카탈로그 기준 반영`), 로컬 `origin/develop` 최신 ref는 `0abafe8` (`fix: #128 FCM 토큰 upsert 무결성 보강 (#129)`).
- 변경 범위 수치:
  - `git rev-list --left-right --count origin/develop...HEAD`: `81 4`
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1332 insertions(+), 8 deletions(-)
  - `git show --stat -n 1 HEAD`: 문서 3개, 34 insertions(+)
  - `git show --stat -n 1 origin/develop`: 13 files changed, 154 insertions(+), 19 deletions(-), 앱 코드 5개 + DB 마이그레이션 1개 + 테스트 4개 + 문서 3개
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개, Java 소스 231개
  - 현재 체크아웃 브랜치: 테스트 Java 소스 28개, 테스트 리소스 1개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개
  - DB 마이그레이션 수: 현재 체크아웃 브랜치 0개, 로컬 `origin/develop` ref 5개
- 검증 신호:
  - `./gradlew test`: 성공, 10초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 10초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` 경고 1건이 계속 출력됐고 `BuildFeatures.configurationCache.requested` 전환 요구가 유지됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-06 06:01:20 +0900`)
- 최신 통합선 변경 관찰:
  - 오늘 새 upstream 커밋은 없었고, 로컬 `origin/develop` 최신 ref는 계속 `0abafe8`다.
  - `0abafe8`은 `FcmTokenService`, `FcmTokenResult`, `FcmTokenResponse`, `UserFcmTokenRepository`, `UserFcmToken` 수정과 `V5__fix_fcm_token_active_uniqueness.sql`, notification/Flyway 테스트 4종 보강을 포함한다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 계속 "upstream documented evidence"로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했다.
  - health/latency 측정 대상은 여전히 `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending decision 상태라 새 수치를 추가하지 않았다.
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 앱 코드 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 로컬 `origin/develop` 최신 ref 유지 확인이다.
  - 현재 브랜치와 `origin/develop`의 격차가 여전히 `81 4`라서, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 크다.
  - 현재 체크아웃 브랜치에는 DB 마이그레이션 디렉터리가 없지만 로컬 `origin/develop` ref에는 5개 migration이 보여, 통합선 마이그레이션 체인을 현재 브랜치에서 재검증하지 못했다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-06까지 연속 재현됐다.
  - 루트의 미추적 빈 파일 `0`이 계속 남아 있다. 현재 모니터링 범위에서는 생성 의도와 보존 필요성을 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.notification.application.FcmTokenServiceTest --tests com.faithlog.notification.presentation.FcmTokenControllerTest --tests com.faithlog.notification.presentation.NotificationApiRestDocsTest --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: 현재 확인 가능한 최신 통합선 핵심 실변경이 FCM token upsert 무결성과 V5 migration 추가다.
  - 기대 지표: notification 회귀 테스트 pass/fail, Flyway migration test pass/fail, FCM 중복/활성 토큰 회귀 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 기준 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 현재 build 구성의 Asciidoctor/Grolifant 계열 플러그인 경로에서 deprecated API를 호출하는 것으로 계속 관찰된다.
  - 조치 현황: 오늘은 `./gradlew test`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 재확인했다.
  - 전후 지표: 2026-07-05와 2026-07-06 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: FCM 토큰 upsert 무결성 보강이 앱 코드 5개 수정, V5 migration 1개 추가, notification/Flyway 테스트 4종 보강으로 로컬 `origin/develop` 최신 ref에 유지되고 있다. 단, `origin/develop` 직접 체크아웃 재검증 전까지는 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-05

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `0abafe8`, `origin/main` 최신 tip은 `1f8aedb`로 갱신됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - `git log --since='2026-07-03T21:01:24.391Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-07-03T21:01:24.391Z' origin/develop`: 새 커밋 1건 (`0abafe8`)
  - `git log --since='2026-07-03T21:01:24.391Z' origin/main`: 새 커밋 1건 (`1f8aedb`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `81 4`로 `origin/develop`이 현재 브랜치보다 81커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `0abafe8`, `afeb47e`, `a88def5`, `ade0d87`, `65dcdb8`
  - `origin/main` 최근 5커밋: `1f8aedb`, `f2d3ba9`, `ade0d87`, `04b9d01`, `61571d4`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1249 insertions(+), 8 deletions(-)
  - 지난 실행 이후 최신 upstream 실변경 누적 파일은 13개이며, 구성은 `docs` 3개, `notification` 앱 코드 5개, DB 마이그레이션 1개, 테스트 4개다.
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - 최신 upstream 기준 의존성 파일 변경 0건, 배포/CI 파일 변경 0건
  - 최신 upstream 기준 DB 마이그레이션 변경 1건: `V5__fix_fcm_token_active_uniqueness.sql`
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 430개, 테스트 Java 소스 56개, GitHub Actions workflow 2개, DB 마이그레이션 5개
- 검증 신호:
  - `./gradlew test`: 성공, 25초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 25초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고 Gradle이 `BuildFeatures.configurationCache.requested` 전환을 요구했다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-05 08:14:57 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋 1건이 추가됐고 현재 체크아웃 브랜치에는 새 커밋이 없었다.
  - `0abafe8`는 13 files changed, 154 insertions(+), 19 deletions(-)이며 `notification` 도메인에서 FCM token upsert 무결성 보강, `UserFcmTokenRepository` 조회 조건 보정, `FcmTokenService`/`FcmTokenResult`/`FcmTokenResponse` 수정, `PostgresFlywayMigrationTest`와 notification 테스트 3종 보강, `V5__fix_fcm_token_active_uniqueness.sql` 추가를 포함한다.
  - `1f8aedb`는 위 develop 변경을 main에 반영한 release 커밋이다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docker ps`는 Docker API socket 미연결로 실패했다. 현재 로컬 런타임 컨테이너 상태는 확인하지 못했다.
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 upstream notification/Flyway 변경 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `81 4`로 더 벌어져, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - `origin/develop` tree snapshot의 테스트 Java 소스는 56개, DB 마이그레이션은 5개지만 현재 브랜치에는 각각 28개, 0개라서 통합선 품질을 직접 재검증하지 않으면 이력서 근거로 승격할 수 없다.
  - 최신 upstream는 FCM 토큰 활성 유니크니스 보강을 위해 V5 마이그레이션을 추가했지만 현재 체크아웃 브랜치에는 해당 파일이 없어 마이그레이션 누적 상태를 로컬에서 재검증하지 못했다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-05까지 연속 재현됐고 source 교정은 아직 미완료다.
  - 루트에 미추적 빈 파일 `0`이 계속 남아 있다. 현재 모니터링 범위에서는 생성 의도와 보존 필요성을 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.notification.application.FcmTokenServiceTest --tests com.faithlog.notification.presentation.FcmTokenControllerTest --tests com.faithlog.notification.presentation.NotificationApiRestDocsTest --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: 지난 실행 이후 새 upstream 실변경 중심이 FCM token upsert 무결성과 V5 migration 추가다.
  - 기대 지표: notification 회귀 테스트 pass/fail, Flyway migration test pass/fail, FCM 중복/활성 토큰 회귀 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에 notification 테스트와 migration 검증이 추가됐지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - 승인된 단일 대상에서 Docker daemon 가동 확인 후 `docker compose up -d postgres redis app`
  - 이유: 현재는 Docker API socket 미연결로 런타임 상태를 확인하지 못했고, health/latency 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, 컨테이너 상태, 이후 `/api/v1/health` 측정 가능 여부
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰 1: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 `./gradlew test`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 다시 확인하고 기록했다.
  - 전후 지표: 2026-07-04와 2026-07-05 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
  - 미해결 관찰 2: Docker 운영 신호 수집 불가.
  - 문제: `docker ps`가 Docker API socket 미연결로 실패해 컨테이너 상태를 확인하지 못했다.
  - 원인: 현재 세션에서 `/Users/josephuk77/.docker/run/docker.sock`에 연결할 수 없었다.
  - 조치 현황: 오늘은 실패 사실만 기록하고 런타임 측정은 보류했다.
  - 전후 지표: 컨테이너 수 0건으로 확정할 수 없음, `/api/v1/health` 측정 미실시
  - 재발 방지 후보: Docker daemon 가동 여부와 모니터링 실행 환경의 socket 접근 가능 여부를 먼저 확인해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: FCM 토큰 upsert 무결성 보강이 `notification` 앱 코드 5개 수정, `V5__fix_fcm_token_active_uniqueness.sql` 추가, notification/Flyway 테스트 4종 보강과 함께 `origin/develop`에 반영됐다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-04

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `afeb47e`, `origin/main` 최신 tip은 `f2d3ba9`로 유지됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - `git log --since='2026-07-02T21:01:51.309Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-07-02T21:01:51.309Z' origin/develop`: 새 커밋 0건
  - `git log --since='2026-07-02T21:01:51.309Z' origin/main`: 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `80 4`로 `origin/develop`이 현재 브랜치보다 80커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `afeb47e`, `a88def5`, `ade0d87`, `65dcdb8`, `f680dc6`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1174 insertions(+), 8 deletions(-)
  - 최신 upstream 실변경 누적 파일은 12개이며, 구성은 `docs` 4개, `billing` 앱 코드 3개, `billing` 테스트 5개다.
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - 최신 upstream 기준 의존성 파일 변경 0건, 배포/CI 파일 변경 0건, DB 마이그레이션 변경 0건
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 430개, 테스트 Java 소스 56개, GitHub Actions workflow 2개, DB 마이그레이션 4개
- 검증 신호:
  - `./gradlew test`: 성공, 13초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 14초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고 Gradle이 `BuildFeatures.configurationCache.requested` 전환을 요구했다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-04 06:02:30 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋이 추가되지 않았고 현재 체크아웃 브랜치에도 새 커밋이 없었다.
  - 기준 remote tip은 전일과 동일하게 billing 정산 조회 정책과 계좌 활성 전환 계약 보강 커밋(`a88def5`, `f680dc6`)을 포함한 상태다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 브랜치 격차 지속 확인이다.
  - 현재 브랜치와 `origin/develop`의 격차가 여전히 `80 4`라서, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 크다.
  - `origin/develop` tree snapshot의 테스트 Java 소스는 56개, DB 마이그레이션은 4개지만 현재 브랜치에는 각각 28개, 0개라서 통합선 품질을 직접 재검증하지 않으면 이력서 근거로 승격할 수 없다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-04까지 연속 재현됐고 source 교정은 아직 미완료다.
  - 루트에 미추적 빈 파일 `0`이 계속 남아 있다. 현재 모니터링 범위에서는 생성 의도와 보존 필요성을 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에 billing 회귀 테스트와 마이그레이션 누적이 반영돼 있지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.billing.application.BillingQueryServiceTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.billing.application.BillingServiceUnitTest --tests com.faithlog.billing.presentation.BillingControllerTest`
  - 이유: 현재 확인 가능한 최신 통합선 실변경 중심이 billing 정산 조회 정책과 활성 계좌 전환 계약이다.
  - 기대 지표: 핵심 billing 회귀 테스트 pass/fail, 기능별 회귀 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: `origin/develop`에 `V3`, `V4` 마이그레이션이 누적됐지만 현재 브랜치에서는 실행 근거가 없다.
  - 기대 지표: Flyway migration test pass/fail, 누적 migration 적용 가능 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 기존 누적 기록 기준 `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 `./gradlew test`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 다시 확인하고 기록했다.
  - 전후 지표: 2026-07-03과 2026-07-04 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: billing 정산 조회 정책과 계좌 활성 전환 계약 보강이 `BillingQueryService`/`BillingService` 수정, billing 테스트 4종 보강, `BillingServiceUnitTest` 신규 추가와 함께 유지되고 있다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-03

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `afeb47e`, `origin/main` 최신 tip은 `f2d3ba9`로 확인됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - `git log --since='2026-07-01T21:00:38.611Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-07-01T21:00:38.611Z' origin/develop`: 새 커밋 5건 (`afeb47e`, `a88def5`, `ade0d87`, `65dcdb8`, `f680dc6`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `80 4`로 `origin/develop`이 현재 브랜치보다 80커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `afeb47e`, `a88def5`, `ade0d87`, `65dcdb8`, `f680dc6`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 1073 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 430개, 테스트 Java 소스 56개, GitHub Actions workflow 2개, DB 마이그레이션 4개
- 검증 신호:
  - `./gradlew test`: 성공, 11초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 11초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고 Gradle이 `BuildFeatures.configurationCache.requested` 전환을 요구했다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-03 06:03:11 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋 5건이 추가됐고 현재 체크아웃 브랜치에는 새 커밋이 없었다.
  - `a88def5`는 4 files changed, 185 insertions(+), 9 deletions(-)이며 `BillingService` 수정, `PaymentAccountRepositoryPort` 변경, `BillingServiceUnitTest` 153줄 추가를 포함한다.
  - `f680dc6`는 10 files changed, 284 insertions(+), 25 deletions(-)이며 `BillingQueryService`, `BillingService`, `BillingQueryServiceTest`, `BillingServiceTest`, `BillingControllerTest`, `BillingApiRestDocsTest` 보강을 포함한다.
  - `afeb47e`, `ade0d87`, `65dcdb8`는 release merge 계열 커밋이며 위 billing 변경과 문서 변경을 `develop`/`main`에 반영했다.
  - 지난 실행 이후 확인된 upstream 실변경 범위는 billing 모듈과 관련 테스트/REST Docs 중심이며, 새 설정 파일이나 의존성 파일 변경은 관찰되지 않았다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 upstream 5커밋 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `80 4`까지 벌어져, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - `origin/develop` tree snapshot의 테스트 Java 소스는 56개, DB 마이그레이션은 4개지만 현재 브랜치에는 각각 28개, 0개라서 통합선 품질을 직접 재검증하지 않으면 이력서 근거로 승격할 수 없다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-03까지 연속 재현됐고 source 교정은 아직 미완료다.
  - 루트에 미추적 빈 파일 `0`이 계속 남아 있다. 현재 모니터링 범위에서는 생성 의도와 보존 필요성을 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에 billing 회귀 테스트가 추가됐지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.billing.application.BillingQueryServiceTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.billing.application.BillingServiceUnitTest --tests com.faithlog.billing.presentation.BillingControllerTest`
  - 이유: 지난 실행 이후 새 upstream 실코드/테스트 변화의 중심이 billing 정산 조회 정책과 활성 계좌 전환 계약이다.
  - 기대 지표: 핵심 billing 회귀 테스트 pass/fail, 기능별 회귀 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: `origin/develop`에 `V3`, `V4` 마이그레이션이 누적됐지만 현재 브랜치에서는 실행 근거가 없다.
  - 기대 지표: Flyway migration test pass/fail, 누적 migration 적용 가능 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 직전 재현 기록 기준 `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 `./gradlew test`와 `./gradlew build --warning-mode all`를 재실행해 경고 지속 여부만 다시 확인하고 기록했다.
  - 전후 지표: 2026-07-02와 2026-07-03 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: billing 정산 조회 정책과 계좌 활성 전환 계약 보강이 `BillingQueryService`/`BillingService` 수정, billing 테스트 4종 보강, `BillingServiceUnitTest` 신규 추가와 함께 진행됐다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-02

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `bc521bb`, `origin/main` 최신 tip은 `04b9d01`로 갱신됐고 삭제된 remote ref 5건이 정리됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - `git log --since='2026-06-30T21:01:49.186Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-30T21:01:49.186Z' origin/develop`: 새 커밋 7건 (`bc521bb`, `4c5a21a`, `61571d4`, `863877a`, `8f36f9d`, `b6d0a61`, `76b669f`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `74 4`로 `origin/develop`이 현재 브랜치보다 74커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `bc521bb`, `4c5a21a`, `61571d4`, `863877a`, `8f36f9d`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 969 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 430개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 4개
- 검증 신호:
  - `./gradlew test`: 성공, 7초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 2초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고 Gradle이 `BuildFeatures.configurationCache.requested` 전환을 요구했다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋 7건이 추가됐고 현재 체크아웃 브랜치에는 새 커밋이 없었다.
  - `76b669f`는 28 files changed, 1106 insertions(+), 124 deletions(-)이며 계좌 기준 관리자 정산 조회, 커피 투표 권한 정책 정리, `BillingQueryService` 161줄 증분, `PollServiceTest` 283줄 증분을 포함한다.
  - `b6d0a61`과 `61571d4`는 release merge 계열 커밋이며 `develop`에 billing/poll/devotion 계좌 정책과 문서 변경을 재반영했다.
  - `4c5a21a`는 2 files changed, 152 insertions(+)이며 `BillingControllerTest` 회귀 테스트 144줄 추가와 `docs/resume-metrics.md` 8줄 갱신을 포함한다.
  - `bc521bb`는 release merge commit이며 `PollAccessService.java` 10줄, `BillingApiRestDocsTest.java` 17줄이 `develop`에 병합됐다.
  - 직전 upstream 실변경 기준 `863877a`는 15 files changed, 673 insertions(+), 51 deletions(-)로 `V4__add_payment_account_soft_delete.sql`, `BillingService`, `BillingQueryService`, `PaymentAccount` soft delete/활성화 정책과 관련 REST Docs/테스트를 추가했다.
  - 직전 upstream 실변경 기준 `8f36f9d`는 19 files changed, 423 insertions(+), 79 deletions(-)로 `V3__split_active_coffee_payment_account_owner_scope.sql`, 사용자별 커피 계좌 범위 정리, 커피투표 정산 권한 정책 보강, `PollServiceTest` 182줄 증분을 포함한다.
  - `c2762ec..origin/develop` 누적 diff는 현재 확인 기준 32 files changed, 2299 insertions(+), 172 deletions(-)이며 실코드 변경 모듈은 `billing` 11개, `poll` 4개, `global` 1개 파일이고 테스트 변경 모듈은 `billing` 4개, `poll` 2개, `batch` 1개, `campus` 1개 파일이다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 upstream 7커밋 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `74 4`까지 벌어져, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - `origin/develop` tree snapshot의 DB 마이그레이션 수는 4개까지 증가했지만 현재 브랜치에는 0개라서, Flyway 재도입 해석은 기존 pending decision 없이는 확정할 수 없다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-02까지 연속 재현됐고 source 교정은 아직 미완료다.
  - 루트에 미추적 빈 파일 `0`이 남아 있다. 현재 모니터링 범위에서는 생성 의도와 보존 필요성을 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에 `billing` 회귀 테스트와 계좌 정책 변경이 누적됐지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.poll.application.PollServiceTest`
  - 이유: 지난 실행 이후 새 upstream 실코드/테스트 변화의 중심이 billing 계좌 정책과 coffee poll 권한 정책이다.
  - 기대 지표: 핵심 회귀 테스트 pass/fail, 기능별 회귀 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: `origin/develop`에 `V3`, `V4` 마이그레이션이 누적됐지만 현재 브랜치에서는 실행 근거가 없다.
  - 기대 지표: Flyway migration test pass/fail, 누적 migration 적용 가능 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: `./gradlew build --warning-mode all --stacktrace` 기준 `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 `./gradlew test`, `./gradlew build --warning-mode all`, `./gradlew build --warning-mode all --stacktrace`를 재실행해 source까지 다시 확인하고 기록만 수행했다.
  - 전후 지표: 2026-07-01과 2026-07-02 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: 경고 source를 다시 stacktrace까지 포함해 특정한 뒤 plugin 업그레이드 또는 설정 교체 가능성을 검토해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: 사용자별 커피 계좌 범위 분리와 벌금 계좌 soft delete/활성화 정책 추가가 `V3`, `V4` 마이그레이션, Billing/Poll 테스트 보강과 함께 진행됐다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-07-01

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `c2762ec`로 전진했다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`), 미추적 빈 파일 1건 (`0`)
  - `git log --since='2026-06-29T21:00:59.829Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-29T21:00:59.829Z' origin/develop`: 새 커밋 9건 (`4537801`, `c9436e3`, `576126f`, `04b5fb9`, `ac869ae`, `b3d40ed`, `2d1e191`, `7102981`, `c2762ec`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `67 4`로 `origin/develop`이 현재 브랜치보다 67커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c2762ec`, `7102981`, `2d1e191`, `b3d40ed`, `ac869ae`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 897 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 430개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 2개
- 검증 신호:
  - `./gradlew test`: 성공, 18초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 19초, 8 actionable tasks up-to-date
  - `./gradlew build --warning-mode all --stacktrace`: 성공, 3초
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고, stacktrace 기준 발생 경로가 `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`까지 다시 확인됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-07-01 06:03:39 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋 9건이 추가됐고 현재 체크아웃 브랜치에는 새 커밋이 없었다.
  - `7102981`은 7 files changed, 126 insertions(+), 20 deletions(-)이며 `DevotionService` 0원 벌금 청구 생성 방지와 `DevotionServiceTest` 78줄, `DevotionApiRestDocsTest` 27줄 보강을 포함한다.
  - `ac869ae`는 24 files changed, 857 insertions(+), 25 deletions(-)이며 기도 운영 기간/기도조 관리 API 보강과 `PrayerServiceTest` 269줄, `PrayerApiRestDocsTest` 140줄 보강을 포함한다.
  - `04b5fb9`는 11 files changed, 383 insertions(+), 32 deletions(-)이며 커피 담당자 정산 흐름 보강과 `PollServiceTest` 101줄, `PollApiRestDocsTest` 145줄 보강을 포함한다.
  - `c624be5..origin/develop` 누적 diff는 실코드 기준 `prayer` 20개, `poll` 7개, `devotion` 3개, `global` 1개 파일 변경을 포함한다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 upstream 9커밋 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `67 4`까지 벌어져, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-07-01까지 연속 재현됐고 source 특정은 됐지만 교정은 아직 미완료다.
  - 루트에 미추적 빈 파일 `0`이 남아 있어 작업트리 위생상 확인이 필요하다. 생성 의도는 오늘 검증 범위에서 확인하지 못했다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에 기도/투표/경건생활 테스트 보강이 누적됐지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.prayer.application.PrayerServiceTest --tests com.faithlog.poll.application.PollServiceTest --tests com.faithlog.devotion.application.DevotionServiceTest`
  - 이유: 지난 실행 이후 새 upstream 실코드 변경이 가장 크게 누적된 회귀 포인트가 prayer, poll, devotion 모듈이다.
  - 기대 지표: 핵심 회귀 테스트 pass/fail, 기능별 회귀 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: stacktrace 기준 `org.asciidoctor.gradle` 계열 plugin 초기화 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 경고 발생 경로를 다시 재현하고 기록만 수행했으며 수정은 하지 않았다.
  - 전후 지표: 2026-06-30과 2026-07-01 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: 기도 운영 기간/기도조 관리 API 보강과 커피 담당자 정산 흐름, 0원 벌금 청구 방지까지 이어지는 연속 변경에서 prayer/poll/devotion 테스트 보강이 함께 진행됐다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-06-30

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md`, `docs/prompts/daily-resume-monitor.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 성공. `origin/develop` 최신 tip은 `c624be5`로 전진했고, 삭제된 remote ref 2건(`origin/feat/100-coffee-duty-access`, `origin/feat/97-poll-close-user-option`)이 정리됐다.
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-28T21:00:26.119Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-28T21:00:26.119Z' origin/develop`: 새 커밋 3건 (`c624be5`, `af83734`, `0eb1e95`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `57 4`로 `origin/develop`이 현재 브랜치보다 57커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c624be5`, `af83734`, `0eb1e95`, `c46266d`, `e1190e1`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 816 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 426개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 2개, `performance/k6` 파일 3개
- 검증 신호:
  - `./gradlew test`: 성공, 4초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 9초, 8 actionable tasks up-to-date
  - `./gradlew build --warning-mode all --stacktrace`: 성공, 19초
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 계속 출력됐고, stacktrace 기준 발생 경로가 `org.asciidoctor.gradle` plugin 적용 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`까지 좁혀졌다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-06-30 09:04:37 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각 이후 `origin/develop`에는 새 커밋 3건이 추가됐고 현재 체크아웃 브랜치에는 새 커밋이 없었다.
  - `0eb1e95`는 36 files changed, 912 insertions(+), 18 deletions(-)이며 투표 종료/사용자 항목 추가, `src/main/resources/db/migration/V2__add_poll_user_option_fields.sql`, `PollServiceTest` 232줄 보강, `PollApiRestDocsTest` 165줄 보강을 포함한다.
  - `c624be5`는 26 files changed, 949 insertions(+), 33 deletions(-)이며 커피 담당자 전용 권한, 내 담당 상태 조회 DTO/서비스/컨트롤러, `Billing*`, `Campus*`, `Poll*`, `AuthService` 보강과 관련 REST Docs/테스트 추가를 포함한다.
  - `af83734`는 `main` 변경사항을 `develop`에 병합한 release merge commit이다.
  - `c46266d..origin/develop` 누적 diff는 55 files changed, 1851 insertions(+), 41 deletions(-)이며 앱 코드 변경 모듈 6개(`batch`, `billing`, `campus`, `global`, `poll`, `user`), 테스트 변경 모듈 8개(`admin`, `batch`, `billing`, `campus`, `deploy`, `notification`, `poll`, `user`)를 포함한다.
  - 위 upstream 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급해야 한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치 기준 신규 구현 성과는 없고, 오늘 새 근거는 문서 브랜치 품질 재검증과 upstream 3커밋 관찰이다.
  - 현재 브랜치와 `origin/develop`의 격차가 `57 4`로 더 벌어져, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 더 커졌다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-06-30까지 연속 재현됐고 source 특정 또는 교정은 아직 미완료다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에는 새 테스트/REST Docs/migration 변경이 누적됐지만 coverage 산출 여부는 오늘 직접 재확인하지 못했다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.poll.application.PollServiceTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.campus.presentation.CampusControllerTest`
  - 이유: 새 upstream 기능 중 직접 영향 범위가 큰 #97 Poll 기능과 #101 coffee-duty/billing/campus 권한 검증 회귀 포인트다.
  - 기대 지표: 핵심 회귀 테스트 pass/fail, 관련 모듈 회귀 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: `origin/develop`에 `V2__add_poll_user_option_fields.sql`가 추가되어 마이그레이션 검증 신호가 새로 필요하다.
  - 기대 지표: Flyway migration test pass/fail, V2 적용 가능 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고 지속.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: stacktrace 기준 `org.asciidoctor.gradle` plugin 초기화 중 `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`가 deprecated API를 호출한다.
  - 조치 현황: 오늘은 source 후보를 plugin 경로까지 특정하고 재현만 수행했으며 수정은 하지 않았다.
  - 전후 지표: 2026-06-29와 2026-06-30 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: Asciidoctor/Grolifant plugin 버전 검토 또는 대체 설정 확인으로 deprecated 호출 제거 여부를 점검해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음.
  - upstream documented candidate: 투표 종료 및 사용자 직접 항목 추가 범위에서 `V2` 마이그레이션 1건과 Poll/Billing/Campus/User 모듈 테스트 보강이 함께 진행됐다. 단, 이 문장은 `origin/develop` 직접 체크아웃 재검증 전까지 로컬 검증 완료 성과로 승격하면 안 된다.

### 2026-06-29

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, `Projects/FaithLog/decision-log.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch`: 성공. `origin/develop` 최신 tip은 계속 `c46266d`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-27T21:01:08.057Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-27T21:01:08.057Z' origin/develop`: 최신 통합선 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `53 4`로 `origin/develop`이 현재 브랜치보다 53커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c46266d`, `dd32bff`, `6965dbb`, `0c036ef`, `6e9a205`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 719 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 422개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 1개, `performance/k6` 파일 3개
- 검증 신호:
  - `./gradlew test`: 성공, 12초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 13초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 다시 출력됐고 `BuildFeatures.configurationCache.requested` 전환 필요 메시지가 유지됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-06-29 06:01:58 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 실행 시각인 `2026-06-27T21:01:08.057Z` 이후 현재 브랜치와 `origin/develop` 모두 새 커밋은 관찰되지 않았다.
  - 현재 브랜치 고유 diff는 여전히 문서 3파일뿐이라, 오늘 검증 성공은 기능 추가가 아니라 문서 브랜치 상태 재확인으로 해석해야 한다.
  - 원격 ref를 다시 가져온 뒤에도 `origin/develop` tip은 `c46266d`로 유지됐고, 오늘 새 코드/설정/의존성/마이그레이션 변화는 확인되지 않았다.
  - 최신 통합선의 직전 의미 있는 코드/설정 변화 기록은 그대로 유지된다: `c46266d`는 `performance/k6/seed-cloud-run-perf-data.mjs` 추가와 `RoleTokenInvalidationIntegrationTest` 7줄 보강을 포함했고, `dd32bff`는 `build.gradle.kts` JaCoCo 관련 변경 11줄과 `CampusMembershipRow`, `CampusService`, `CampusServiceTest`, `performance/k6/read-baseline.js` 추가/보강을 포함한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - `docs/decision-log.md`의 `2026-06-17 - Daily Health And Response-Time Measurement Scope` pending question이 아직 열려 있어 health/latency 새 수치를 추가하지 않음
  - decision log에는 오늘 새 승인 결정이나 새 pending question 추가가 없었다.
- 오늘 리스크/관찰:
  - 2026년 6월 27일 이후 새 커밋 근거가 없어서 resume bullet로 승격 가능한 신규 기능 성과는 확인되지 않았다.
  - 현재 브랜치와 `origin/develop`의 격차가 계속 `53 4`라서, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 있다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-06-29까지 연속 재현됐고 source 특정 또는 교정은 아직 미완료다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 로컬 문서 브랜치에서는 coverage 산출 여부를 확인할 수 없고, 최신 통합선 문서에만 JaCoCo 근거가 남아 있다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest`
  - 이유: 최신 통합선의 코드성 변화 중 직접 확인 가능한 회귀 포인트는 여전히 역할 변경 후 토큰 무효화 테스트 보강이다.
  - 기대 지표: 해당 통합 테스트 pass/fail, 역할 변경 후 토큰 버전 무효화 회귀 여부
  - `./gradlew build --warning-mode all --stacktrace`
  - 이유: deprecated 경고 source를 특정하지 못해 같은 관찰이 누적되고 있다.
  - 기대 지표: 경고 발생 경로 식별 가능 여부, plugin/script 원인 후보 수
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고가 지속된다.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 공식 경고 메시지상 `BuildFeatures.configurationCache.requested`로 전환되지 않은 script 또는 plugin 경로가 남아 있으나 source는 아직 특정하지 못했다.
  - 조치 현황: 오늘은 재현과 기록만 수행했고 수정은 하지 않았다.
  - 전후 지표: 2026-06-28과 2026-06-29 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: `./gradlew build --warning-mode all --stacktrace` 또는 관련 plugin/script 분리 점검으로 경고 source를 특정해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 품질 재검증 유지와 upstream 관찰값/로컬 검증값 분리 기록 중심.

### 2026-06-28

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 새 remote ref 변화 없음. `origin/develop` 최신 tip은 계속 `c46266d`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-26T21:01:17.078Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-26T21:01:17.078Z' origin/develop`: 최신 통합선 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `53 4`로 `origin/develop`이 현재 브랜치보다 53커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c46266d`, `dd32bff`, `6965dbb`, `0c036ef`, `6e9a205`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 628 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 422개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 1개, `performance/k6` 파일 3개
- 검증 신호:
  - `./gradlew test`: 성공, 6초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 24 XML files, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 2초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested` deprecation 경고 1건이 다시 출력됐고 `BuildFeatures.configurationCache.requested` 전환 필요 메시지가 유지됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성/갱신됨 (`2026-06-28 06:02:58 +0900`)
- 최신 통합선 변경 관찰:
  - 지난 자동화 이후 현재 브랜치와 `origin/develop` 모두 새 커밋은 관찰되지 않았다.
  - 현재 브랜치 고유 diff는 여전히 문서 3파일뿐이라, 오늘 검증 성공은 기능 추가가 아니라 문서 브랜치 상태 재확인으로 해석해야 한다.
  - `c46266d` 기준 변경량은 `6 files changed, 562 insertions(+), 15 deletions(-)`이며 `performance/k6/seed-cloud-run-perf-data.mjs` 신규 추가와 `RoleTokenInvalidationIntegrationTest` 7줄 보강이 포함된다.
  - 직전 upstream 코드/설정성 변화로 남아 있는 `dd32bff`는 `build.gradle.kts` JaCoCo 관련 변경 11줄, `CampusMembershipRow` 추가, `CampusService` 조회 최적화, `CampusServiceTest` 보강, `performance/k6/read-baseline.js` 신설을 포함한다.
  - 위 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - health/latency 측정 대상은 `docs/decision-log.md`의 pending decision 상태라 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 오늘 새 커밋 근거가 없어서 resume bullet로 승격 가능한 신규 기능 성과는 확인되지 않았다.
  - 현재 브랜치와 `origin/develop`의 격차가 계속 `53 4`라서, 문서 브랜치 검증값을 저장소 최신 통합선 품질로 인용하면 과대해석 위험이 있다.
  - Gradle deprecated 경고는 2026-06-25부터 2026-06-28까지 연속 재현됐고 source 특정 또는 교정은 아직 미완료다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 오늘 성공값은 문서 브랜치 기준이며, 최신 통합선 품질은 직접 재검증하지 못했다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 로컬 문서 브랜치에서는 coverage 산출 여부를 확인할 수 없고, 최신 통합선 문서에만 JaCoCo 근거가 남아 있다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고가 지속된다.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 원인: 공식 경고 메시지상 `BuildFeatures.configurationCache.requested`로 전환되지 않은 script 또는 plugin 경로가 남아 있으나 source는 아직 특정하지 못했다.
  - 조치 현황: 오늘은 재현과 기록만 수행했고 수정은 하지 않았다.
  - 전후 지표: 2026-06-27과 2026-06-28 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: `./gradlew build --warning-mode all --stacktrace` 또는 관련 plugin/script 분리 점검으로 경고 source를 특정해야 한다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 품질 재검증 유지와 upstream 관찰값/로컬 검증값 분리 기록 중심.

### 2026-06-27

- 브랜치/작업트리:
  - 기준 문서 확인: repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 새 remote ref 변화 없음. `origin/develop` 최신 tip은 계속 `c46266d`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-25T21:00:29.620Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-25T21:00:29.620Z' origin/develop`: 최신 통합선 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `53 4`로 `origin/develop`이 현재 브랜치보다 53커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c46266d`, `dd32bff`, `6965dbb`, `0c036ef`, `6e9a205`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 553 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 422개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 1개, `performance/k6` 파일 3개
- 검증 신호:
  - `./gradlew test`: 성공, 1분 21초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 1분 22초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 오늘도 동일하게 출력됐고 `BuildFeatures.configurationCache.requested` 전환 필요 메시지가 유지됐다.
  - build problems report: `build/reports/problems/problems-report.html` 생성됨 (`2026-06-27 06:04:18 +0900`)
- 최신 통합선 변경 관찰:
  - 오늘 새 local commit 관찰은 없고, `origin/develop` tip `c46266d` 관찰값도 어제와 동일하다.
  - `c46266d` 기준 변경량은 `6 files changed, 562 insertions(+), 15 deletions(-)`이며 `performance/k6/seed-cloud-run-perf-data.mjs` 신규 추가와 `RoleTokenInvalidationIntegrationTest` 보강이 포함된다.
  - 직전 upstream 코드/설정성 변화로 남아 있는 `dd32bff`는 `build.gradle.kts`에 JaCoCo 관련 변경 11줄을 추가했고 `CampusService` 조회 최적화 및 `CampusServiceTest` 보강, `performance/k6/read-baseline.js` 신설을 포함한다.
  - 위 수치는 현재 브랜치에서 체크아웃/재실행하지 않았으므로 여전히 upstream documented evidence로만 취급한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 재측정은 수행하지 않음
  - health/latency 측정 대상은 `docs/decision-log.md`의 pending decision 상태라 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 지난 모니터링 이후 현재 브랜치와 `origin/develop` 모두 새 커밋이 없어서, 오늘의 새 근거는 재검증 성공과 누적 문서 diff 증가뿐이다.
  - 현재 브랜치 고유 차이는 여전히 문서 3파일뿐이라, 오늘의 테스트/빌드 성공을 기능 진전으로 해석하면 과대기재 위험이 있다.
  - `origin/develop`과의 격차는 계속 `53 4`이며 최신 통합선 품질과 현재 문서 브랜치 품질을 분리해서 적어야 한다.
  - Gradle deprecated 경고는 오늘도 재현됐고 발생 source 특정 또는 수정은 아직 미완료다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 최신 통합선 기준 품질 신호를 오늘도 직접 재현하지 못했고, 현재 성공값은 문서 브랜치 기준이다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에는 JaCoCo/k6 기반 문서가 있으나 현재 브랜치에서는 coverage 산출 여부를 확인할 수 없다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest`
  - 이유: 최신 통합선의 코드성 변화 중 직접 확인 가능한 회귀 포인트가 역할 변경 후 토큰 무효화 테스트 보강이다.
  - 기대 지표: 해당 통합 테스트 pass/fail, 역할 변경 후 토큰 버전 무효화 회귀 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure/build 시작 단계 deprecated 경고가 지속된다.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 반복 노출된다.
  - 조치 현황: 오늘은 재현과 기록만 수행했고 수정은 하지 않았다.
  - 전후 지표: 2026-06-26과 2026-06-27 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: 경고 source를 특정할 수 있는 별도 추적 실행(`--stacktrace`, 관련 plugin/script 분리 점검)이 필요하다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 품질 재검증 유지와 upstream 관찰값/로컬 검증값 분리 기록 중심.
  - 최신 통합선을 직접 체크아웃해 검증이 끝나면 후보 문장: "Cloud Run 성능 기준선 문서와 역할 변경 후 토큰 무효화 통합 테스트를 분리 검증해 운영 수치와 로컬 검증 수치를 혼동하지 않도록 품질 근거를 관리했다."

### 2026-06-26

- 브랜치/작업트리:
  - 기준 문서 확인: repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: 새 remote ref 변화 없음. `origin/develop` 최신 tip은 계속 `c46266d`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-24T21:01:50.868Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-24T21:01:50.868Z' origin/develop`: 최신 통합선 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `53 4`로 `origin/develop`이 현재 브랜치보다 53커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `HEAD` 최근 5커밋: `fc366d7`, `4131fcc`, `3ecd177`, `b766520`, `93bc1f7`
  - `origin/develop` 최근 5커밋: `c46266d`, `dd32bff`, `6965dbb`, `0c036ef`, `6e9a205`
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 428 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 422개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 1개, `performance/k6` 파일 3개
- 검증 신호:
  - `./gradlew test`: 성공, 1분 9초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 1분 10초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 Gradle 10.0 제거 예정, `BuildFeatures.configurationCache.requested` 전환 필요
  - build problems report: `build/reports/problems/problems-report.html` 생성됨
- 최신 통합선 변경 관찰:
  - 오늘 새 upstream 커밋은 없고, 최신 local `origin/develop` tip `c46266d`는 계속 `performance/k6/README.md`, `performance/k6/read-baseline.js`, `performance/k6/seed-cloud-run-perf-data.mjs`, `RoleTokenInvalidationIntegrationTest`, `docs/decision-log.md`, `docs/resume-metrics.md`를 포함한다.
  - `c46266d`의 로컬 관찰 기준 변경량은 `6 files changed, 562 insertions(+), 15 deletions(-)`다.
  - `RoleTokenInvalidationIntegrationTest`에는 서비스 역할 변경, 캠퍼스 역할 변경, 로그아웃 블랙리스트 이후 재발급 토큰 거부를 검증하는 테스트 3건이 포함돼 있다.
  - 위 성능 문서/k6/통합 테스트 보강은 현재 브랜치에서 직접 체크아웃하거나 실행하지 않았으므로, 오늘 모니터링에서는 "upstream에 존재하는 관찰값"으로만 기록한다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 원격 ref 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, Cloud Run 재측정은 수행하지 않음
  - health/latency 측정 대상은 여전히 `decision-log.md`의 pending decision 상태라 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 지난 모니터링 이후 현재 브랜치와 `origin/develop` 모두 새 커밋이 없어서, 오늘의 새 근거는 재검증 성공과 미커밋 문서 변경량 증가뿐이다.
  - 현재 브랜치 고유 차이는 여전히 문서 3파일뿐이라, 로컬 테스트/빌드 성공을 제품 기능 진전으로 해석하면 과대기재 위험이 있다.
  - `origin/develop`과의 격차가 계속 `53 4`로 유지돼 최신 통합선 품질과 현재 문서 브랜치 품질을 분리해 적어야 한다.
  - Gradle deprecated 경고는 오늘도 동일하게 재현됐고 source 특정 또는 교정은 아직 완료되지 않았다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 최신 통합선 기준 품질 신호를 오늘도 직접 재현하지 못했고, 현재 성공값은 문서 브랜치 기준이다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에는 성능/커버리지 기반 정리와 k6 문서가 있으나 현재 브랜치에서는 coverage 산출 여부를 확인할 수 없다.
  - 기대 지표: 통합선 기준 테스트 수, coverage HTML/XML 생성 성공 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest`
  - 이유: 최신 통합선의 코드성 변화 중 직접 확인 가능한 회귀 포인트가 역할 변경 후 토큰 무효화 테스트 보강이다.
  - 기대 지표: 해당 통합 테스트 pass/fail, 역할 변경 후 토큰 버전 무효화 회귀 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 런타임 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 트러블슈팅:
  - 신규 해결 항목 없음.
  - 미해결 관찰: Gradle configure 단계 deprecated 경고가 지속된다.
  - 문제: `StartParameter.isConfigurationCacheRequested` 사용 경고가 Gradle 10.0 제거 예정 API로 반복 노출된다.
  - 추정 원인 아님: 공식 경고 메시지상 `BuildFeatures.configurationCache.requested`로의 전환이 필요한 코드 또는 플러그인 경로가 남아 있다.
  - 조치 현황: 오늘은 재현과 기록만 수행했고 수정은 하지 않았다.
  - 전후 지표: 2026-06-25와 2026-06-26 모두 `./gradlew build --warning-mode all` 성공, deprecated 경고 1건 지속
  - 재발 방지 후보: 경고 source를 특정할 수 있는 별도 추적 실행(`--stacktrace`, 관련 plugin/script 분리 점검)이 필요하다.
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 품질 재검증 유지와 upstream 관찰값/로컬 검증값 분리 기록 중심.
  - 최신 통합선을 직접 체크아웃해 검증이 끝나면 후보 문장: "역할 변경 후 기존 Access/Refresh Token 무효화 통합 테스트와 Cloud Run read baseline 문서를 정리해 권한 변경 회귀와 배포 후 성능 기준선을 함께 추적했다."

### 2026-06-25

- 브랜치/작업트리:
  - 기준 문서 확인: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune`: `origin/develop`가 `dd32bff -> c46266d`로 1커밋 전진했고, `origin/perf/94-cloud-run-performance-tuning` 원격 브랜치는 삭제됨
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-23T21:02:02.261Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-23T21:02:02.261Z' origin/develop`: 최신 통합선 새 커밋 1건 (`c46266d`, `[Perf] Cloud Run 실서버 성능 측정과 기준 정리 (#95)`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `53 4`로 `origin/develop`이 현재 브랜치보다 53커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `origin/develop` 최근 5커밋: `c46266d` (#95 Cloud Run 실서버 성능 측정 정리), `dd32bff` (#90 성능 테스트와 커버리지 측정 기반 정리), `6965dbb` (#25 main 배포 브랜치 기준 develop 동기화), `0c036ef` (#25 Cloud Build Trigger 기준 CD 정리), `6e9a205` (#25 투표 상태 테스트 날짜 의존성 제거)
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 375 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 리소스 1개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: Java 소스 422개, 테스트 Java 소스 55개, GitHub Actions workflow 2개, DB 마이그레이션 1개
- 검증 신호:
  - `./gradlew test`: 성공, 40초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 41초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 Gradle 10.0 제거 예정, `BuildFeatures.configurationCache.requested` 전환 필요
  - build problems report: `build/reports/problems/problems-report.html` 생성됨
- 최신 통합선 변경 관찰:
  - `c46266d`는 `docs/resume-metrics.md`, `docs/decision-log.md`, `performance/k6/README.md`, `performance/k6/read-baseline.js`, `performance/k6/seed-cloud-run-perf-data.mjs`, `RoleTokenInvalidationIntegrationTest`를 수정했다.
  - `c46266d` 문서 기준 관찰값: Cloud Run steady-state read baseline은 `VUS=30`, `DURATION=5m`에서 throughput `124.67 req/s`, failure `0.00%`, p95 `285.97ms`, p99 `446.20ms`로 기록돼 있다.
  - 위 Cloud Run 수치는 현재 체크아웃 브랜치에서 로컬 재실행하거나 운영 환경에서 재검증하지 않았으므로, 오늘 모니터링에서는 "upstream 문서에 기록된 근거"로만 취급하고 현재 브랜치의 검증 완료 성과로 일반화하지 않는다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 원격 ref 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, Cloud Run 재측정은 수행하지 않음
  - health/latency 측정 대상은 여전히 `decision-log.md`의 pending decision 상태라 새 수치를 추가하지 않음
- 오늘 리스크/관찰:
  - 현재 브랜치에는 새 커밋이 없고, 오늘 변화는 upstream 성능 커밋 1건 유입과 검증 재실행 중심이다.
  - `origin/develop`과의 격차가 `52 4`에서 `53 4`로 더 벌어져, 현재 브랜치 기준 테스트/빌드 성공을 저장소 최신 통합 상태의 품질로 인용하면 과대해석 위험이 크다.
  - 최신 통합선에는 Cloud Run 성능 기준선, k6 seed 스크립트, 추가 테스트 변경이 들어갔지만 현재 브랜치에서는 그 변경을 직접 체크아웃하거나 실행하지 않았다.
  - Gradle deprecated 경고는 오늘도 재현됐고 현재 브랜치 기준으로는 경고 source 특정이 끝나지 않았다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 최신 통합선에 #95 성능 문서와 테스트 변경이 추가됐지만 오늘 검증은 문서 브랜치에서만 수행됐다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선 문서에는 243 tests와 JaCoCo coverage 기준선이 기록돼 있지만 현재 브랜치에서는 재현할 수 없다.
  - 기대 지표: 통합선 기준 테스트 수, line/branch/class/method coverage 재현 가능 여부
  - `git switch develop && ./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest`
  - 이유: 최신 통합선의 유일한 신규 코드성 변경이 해당 통합 테스트 보강이라 회귀 여부를 분리 확인할 가치가 있다.
  - 기대 지표: 역할 변경 토큰 무효화 관련 테스트 pass/fail
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 오늘도 runtime/health 기준선은 비어 있고, 기존 pending decision상 측정 대상 확정이 필요하다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 local 품질 신호 유지 확인과 upstream 성능 기준선 커밋 분리 기록 중심.
  - 최신 통합선이 체크아웃되거나 병합된 뒤 재검증되면 후보 문장: "Cloud Run steady-state read baseline을 k6 VUS 30/5분 기준으로 정리해 124.67 req/s, failure 0.00%, p95 285.97ms, p99 446.20ms 운영 기준선을 문서화했다."

### 2026-06-24

- 브랜치/작업트리:
  - 기준 문서 확인: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-22T21:00:14.146Z' HEAD`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-22T21:00:14.146Z' origin/develop`: 최신 통합선 새 커밋 5건
  - `git rev-list --left-right --count origin/develop...HEAD`: `52 4`로 `origin/develop`이 현재 브랜치보다 52커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `origin/develop` 최근 5커밋: `dd32bff` (#90 성능 테스트와 커버리지 측정 기반 정리), `6965dbb` (#25 main 배포 브랜치 기준 develop 동기화), `0c036ef` (#25 Cloud Build Trigger 기준 CD 정리), `6e9a205` (#25 투표 상태 테스트 날짜 의존성 제거), `201c7b7` (#25 Cloud Run CD와 v0.1.0 배포 버전 명시)
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 319 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 Java 소스 28개, 테스트 파일 총 29개, 테스트 결과 XML 24개
  - 현재 체크아웃 브랜치: REST Docs snippet groups 57개, GitHub Actions workflow 2개, DB 마이그레이션 0개
  - 최신 통합선 tree snapshot 참고: `build.gradle.kts`, `docker-compose.yml`, `src/main/resources/application-*.yml`, `src/main/resources/db/migration/V1__initial_schema.sql`, `src/main/resources/seed/compose-coffee-menu-2026.csv`가 존재
- 검증 신호:
  - `./gradlew test`: 성공, 13초, 5 actionable tasks up-to-date
  - `build/test-results/test/*.xml` 집계: 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build --warning-mode all`: 성공, 14초, 8 actionable tasks up-to-date
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 Gradle 10.0 제거 예정, `BuildFeatures.configurationCache.requested` 전환 필요
  - build problems report: `build/reports/problems/problems-report.html` 생성됨
- 최신 통합선 변경 관찰:
  - `201c7b7`, `0c036ef`: `origin/develop`에는 `main` push 기반 `Deploy Cloud Run` workflow와 Cloud Build/Cloud Run CD 정리가 추가되어 배포 자동화 기준이 바뀌었다.
  - `201c7b7`: `build.gradle.kts` 버전이 `0.1.0`으로 상향됐다.
  - `dd32bff`: `jacoco` 플러그인, `jacocoTestReport` HTML/XML 산출, `performance/k6/read-baseline.js`, `performance/k6/README.md`가 추가됐고, 캠퍼스 목록 조회 쿼리 수를 줄이기 위한 `CampusService`/repository 경로 최적화 테스트가 들어갔다.
  - 현재 체크아웃 브랜치에서는 위 통합선 변경을 직접 체크아웃하지 않았으므로, 오늘의 성공 신호를 최신 통합선 전체 품질로 일반화하면 안 된다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 git tree 비교만 수행했고 Docker 기동, `/api/v1/health` 반복 측정, 배포 환경 확인은 재실행하지 않음
  - health/latency 측정 대상은 `docs/decision-log.md`의 pending decision 상태라 계속 보류
- 오늘 리스크/관찰:
  - 마지막 모니터링 이후 현재 브랜치에는 새 커밋이 없고, 오늘 지표 변화는 검증 재실행과 upstream drift 확대 확인이 중심이다.
  - `origin/develop`과의 격차가 `16 4`에서 `52 4`로 더 벌어져 현재 브랜치 기준 테스트/빌드 성공을 저장소 최신 통합 상태의 품질로 인용하면 과대해석 위험이 크다.
  - 최신 통합선에는 배포 workflow, 버전 상향, JaCoCo, k6 스캐폴드, Flyway migration이 포함되지만 현재 브랜치에서는 그 변경을 실행 검증하지 않았다.
  - Gradle deprecated 경고는 오늘도 재현됐고 현재 브랜치 기준으로는 경고 source 특정이 끝나지 않았다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
  - 이유: 최신 통합선에 #25, #90 관련 배포/성능/테스트 변경이 누적됐지만 오늘 검증은 문서 브랜치에서만 수행됐다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, deprecated 경고 지속 여부
  - `git switch develop && ./gradlew test jacocoTestReport`
  - 이유: 최신 통합선에는 JaCoCo 리포트 생성이 추가됐지만 현재 브랜치에서는 coverage 산출 여부를 확인할 수 없다.
  - 기대 지표: coverage HTML/XML 생성 성공 여부, 측정 가능한 커버리지 기준선 확보 가능 여부
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/api/v1/health` 반복 측정
  - 이유: 현재 통합선에는 Cloud Run/CD와 Flyway 변화가 누적됐지만 health/latency 기준선은 여전히 비어 있고 측정 대상 승인도 필요하다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 이력서 bullet 후보:
  - 현재 체크아웃 브랜치 기준 신규 구현 성과 없음. 오늘 업데이트는 품질 신호 유지 확인과 upstream drift/검증 공백 분리 기록 중심.
  - 최신 통합선이 병합된 뒤 검증되면 후보 문장: "JaCoCo HTML/XML coverage 리포트와 k6 read-baseline 스캐폴드를 도입하고, 캠퍼스 목록 조회의 per-membership lookup을 제거해 N+1 리스크를 낮춤."

### 2026-06-23

- 브랜치/작업트리:
  - 기준 문서 확인: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git fetch --all --prune` 후 기준 비교 수행
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-21T21:01:06Z'`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git log --since='2026-06-21T21:01:06Z' origin/develop`: 최신 통합선 새 커밋 9건
  - `git rev-list --left-right --count origin/develop...HEAD`: `16 4`로 `origin/develop`이 현재 브랜치보다 16커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `git merge-base origin/develop HEAD`: `93bc1f7` (`[Feat] 서비스 ADMIN 유저와 캠퍼스 관리 구현 (#63)`)
  - `origin/develop` 최근 5커밋: `8db64ec` (#87 Flyway 마이그레이션 + Supabase 배포 DB 설정), `310c778` (#85 QA Docker Compose 격리 실행 정리), `cbef63d` (#83 테스트 deprecation 경고 정리), `aab95a2` (#80 투표 목록 응답 여부 조회 N+1 개선), `33aa68c` (#78 역할 변경 Access Token 무효화)
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 236 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 현재 브랜치 0건, `origin/develop` tree snapshot 1건 (`V1__initial_schema.sql`)
- 코드베이스 구조 수치:
  - 현재 체크아웃 브랜치: `src/main/java/com/faithlog` top-level 모듈 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - 현재 체크아웃 브랜치: Java 소스 231개, 테스트 소스 28개, 테스트 리소스 1개
  - 현재 체크아웃 브랜치: 테스트 결과 XML 24개, REST Docs snippet groups 57개, GitHub Actions workflow 2개
  - 최신 통합선 tree snapshot 참고: Java 소스 421개, 테스트 Java 소스 55개, DB 마이그레이션 1개
- 검증 신호:
  - `./gradlew test`: 성공, 22초, 5 actionable tasks up-to-date, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build`: 성공, 21초, 8 actionable tasks up-to-date
  - `./gradlew build --warning-mode all`: 성공, 22초, configure phase deprecated 경고 1건
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 Gradle 10.0 제거 예정, `BuildFeatures.configurationCache.requested` 전환 필요
- 통합선 변경 관찰:
  - `8db64ec` 기준 최신 통합선에는 `.env.*.example`, `application-docker.yml`, `application-prod.example.yml`, `docker-compose.yml`, `build.gradle.kts`, `V1__initial_schema.sql`, Flyway migration 테스트 2개가 추가 또는 정리되어 있다.
  - 현재 체크아웃 브랜치에서는 위 통합선 변경을 직접 실행 검증하지 않았으므로, 오늘의 성공 신호를 최신 통합선 전체 품질로 일반화하면 안 된다.
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증과 원격 ref 확인만 수행했고 Docker 기동, 앱 healthcheck, 배포 환경 측정은 재실행하지 않음
  - 로컬/배포 응답 시간 지표는 승인된 측정 대상이 아직 없어 계속 보류
- 오늘 리스크/관찰:
  - 마지막 모니터링 이후 현재 브랜치에는 새 커밋이 없고, 신규 수치 변화는 검증 재실행과 upstream drift 확인 중심이다.
  - `origin/develop`이 9개의 새 커밋을 쌓았고 그 안에 DB migration, 배포 설정, QA 스크립트, 보안 변경이 포함되어 있어 문서 브랜치 기준 검증 결과를 최신 저장소 상태로 인용하면 과대해석 위험이 크다.
  - Gradle deprecated 경고는 여전히 재현됐고, 현재 브랜치 기준으로는 경고 source 분리가 끝나지 않았다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test && ./gradlew build`
  - 이유: 최신 통합선에 #78, #80, #83, #85, #87이 누적되었지만 오늘 검증은 문서 브랜치에서만 수행됐다.
  - 기대 지표: 통합선 기준 테스트 통과율, 빌드 성공 여부, 현재 브랜치 대비 회귀 유무
  - `git switch develop && ./gradlew test --tests com.faithlog.deploy.FlywayMigrationContractTest --tests com.faithlog.deploy.PostgresFlywayMigrationTest`
  - 이유: 최신 통합선에 Flyway migration과 배포 DB 설정이 추가됐지만 문서 브랜치에서는 해당 테스트를 실행할 수 없다.
  - 기대 지표: migration contract pass/fail, Postgres migration pass/fail
  - `./gradlew build --warning-mode all --stacktrace`
  - 이유: deprecated 경고는 재현됐지만 발생 source가 아직 특정되지 않았다.
  - 기대 지표: 경고 source 추적 가능 여부, Gradle 9/10 호환성 backlog 후보
  - 승인된 단일 대상에서 `docker compose up -d postgres redis app` 후 `/health` 반복 측정
  - 이유: 오늘도 runtime/health 기준선은 비어 있고, 기존 pending decision상 측정 대상 확정이 필요하다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
- 오늘 이력서 bullet 후보:
  - 신규 구현 성과 없음. 오늘 업데이트는 품질 신호 유지 확인과 최신 통합선 drift 리스크 분리 기록 중심.

### 2026-06-22

- 브랜치/작업트리:
  - 기준 문서 확인: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git status --short --branch`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git log --since='2026-06-20 21:00:22 +0000'`: 현재 체크아웃 브랜치 새 커밋 0건
  - `git rev-list --left-right --count origin/develop...HEAD`: `7 4`로 `origin/develop`이 현재 브랜치보다 7커밋 앞서고, 현재 브랜치는 문서 커밋 4개를 별도로 보유
  - `git merge-base origin/develop HEAD`: `93bc1f7` (`[Feat] 서비스 ADMIN 유저와 캠퍼스 관리 구현 (#63)`)
  - `origin/develop` 최근 3커밋: `ab4a5ad` (#68 Redis 알림 중복 방지와 알림 락), `00e242a` (#69 배치와 스케줄러), `77dd745` (#70 조별 기도제목 조회와 입력)
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop...HEAD`: 3 files changed, 104 insertions(+)
  - `git diff --shortstat`: 워크트리 미커밋 변경 4 files changed, 161 insertions(+), 8 deletions(-)
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 0건
- 코드베이스 구조 수치:
  - `src/main/java/com/faithlog` top-level 모듈: 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - Java 소스 파일: 231개
  - 테스트 소스 파일: 28개
  - 테스트 리소스 파일: 1개
  - 테스트 결과 XML 수: 24개
  - REST Docs snippet groups: 57개
  - `build/docs/asciidoc/index.html`: 434,854 bytes
  - DB 마이그레이션 파일: 0개
  - GitHub Actions workflow 파일: 2개
- 검증 신호:
  - `./gradlew test`: 성공, 7초, 5 actionable tasks up-to-date, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build`: 성공, 1초, 8 actionable tasks up-to-date
  - `./gradlew build --warning-mode all`: 성공, 2초, configure phase deprecated 경고 1건
  - deprecated 경고 상세: `StartParameter.isConfigurationCacheRequested`는 Gradle 10.0 제거 예정, `BuildFeatures.configurationCache.requested` 전환 필요
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증만 재실행했고 Docker 기동, 앱 healthcheck, 배포 환경 측정은 재실행하지 않음
  - 로컬/배포 응답 시간 지표는 승인된 측정 대상이 아직 없어 계속 보류
- 오늘 리스크/관찰:
  - 마지막 모니터링 이후 현재 브랜치에는 새 커밋이 없고, 수치 변화도 테스트/빌드 재검증 위주라 이력서용 "신규 구현 성과"로 과대해석하면 안 된다.
  - `origin/develop`이 #68, #69, #70까지 앞서 있어 현재 브랜치 검증 결과를 저장소 최신 통합 상태 전체로 일반화하면 정확하지 않다.
  - Gradle deprecated 경고는 오늘도 재현됐고 저장소 직접 사용처 추적 결과가 없는 상태라, 플러그인/공통 빌드 로직 원인 분리가 남아 있다.
- 오늘 테스트 후보:
  - `git switch develop && ./gradlew test`
  - 이유: 오늘 지표는 문서 브랜치 기준이며, 저장소 최신 통합선인 `origin/develop`과 분리되어 있다.
  - 기대 지표: 최신 통합 브랜치 기준 테스트 통과율, 현재 브랜치 대비 회귀 유무
  - `docker compose up -d postgres redis app` 후 승인된 단일 대상에 대해 `curl /api/v1/health` 반복 측정
  - 이유: 오늘도 runtime/health 기준선은 비어 있고, 기존 pending decision상 측정 대상 확정이 필요하다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
  - `./gradlew build --warning-mode all --stacktrace`
  - 이유: deprecated 경고는 재현됐지만 발생 source가 아직 특정되지 않았다.
  - 기대 지표: 경고 source 추적 가능 여부, Gradle 9/10 호환성 backlog 후보
- 오늘 이력서 bullet 후보:
  - 신규 구현 성과 없음. 오늘 업데이트는 검증 신호 유지와 브랜치 기준선 리스크 명시 중심.

### 2026-06-21

- 브랜치/작업트리:
  - 기준 문서 확인: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git status --short`: 워크트리 변경 4건 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`)
  - `git rev-list --left-right --count origin/develop...HEAD`: `4 4`로 `origin/develop`과 상호 4커밋씩 갈라진 상태
  - `git merge-base origin/develop HEAD`: `93bc1f7` (`[Feat] 서비스 ADMIN 유저와 캠퍼스 관리 구현 (#63)`)
  - 현재 브랜치 최근 커밋 4개: `b766520`, `3ecd177`, `4131fcc`, `fc366d7`
  - `origin/develop` 최신 커밋: `2dc07be` (`[Feat] FCM 토큰 등록과 알림 발송 로그 구현 (#67)`)
- 변경 범위 수치:
  - `git diff --name-only origin/develop...HEAD`: 현재 브랜치 고유 변경 파일 3개, 모두 문서 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - `git diff --shortstat origin/develop..HEAD`: tip-to-tip 기준 154 files changed, 13 insertions, 9,995 deletions
  - 해석 주의: 위 154파일 diff는 현재 브랜치가 `origin/develop`보다 뒤처진 4커밋까지 함께 반영한 결과이며, 이번 브랜치가 그 파일들을 실제로 삭제했다는 뜻으로 해석하면 안 된다.
  - 브랜치 고유 앱 코드 변경 파일: 0개
  - 브랜치 고유 테스트 코드 변경 파일: 0개
  - 브랜치 고유 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 0건
- 코드베이스 구조 수치:
  - `src/main/java/com/faithlog` top-level 모듈: 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - Java 소스 파일: 231개
  - 테스트 소스 파일: 28개
  - 테스트 리소스 파일: 1개
  - 테스트 결과 XML 수: 24개
  - REST Docs snippet groups: 57개
  - 빌드 산출물 JAR 수: 2개
  - DB 마이그레이션 파일: 0개
  - GitHub Actions workflow 파일: 2개
- 검증 신호:
  - `./gradlew test`: 성공, 8초, 5 actionable tasks up-to-date, 138 tests / 0 failures
  - `./gradlew build --warning-mode all`: 성공, 2초, 8 actionable tasks up-to-date
  - build configure phase deprecated 경고 1건: `StartParameter.isConfigurationCacheRequested`
  - `./gradlew asciidoctor`: 최초 샌드박스 실행은 `~/.gradle/...zip.lck` lock 접근 실패, 권한 상승 재실행 후 성공, 2초, 6 actionable tasks up-to-date
  - `build/docs/asciidoc/index.html`: 434,854 bytes
  - `rg -n "isConfigurationCacheRequested|configurationCache\\.requested|configurationCacheRequested|configurationCache" .`: 저장소 직접 사용처는 기존 기록 외 새 검색 결과 0건
- 운영/배포 신호:
  - 오늘은 로컬 Gradle 검증만 재실행했고 Docker 기동, 앱 healthcheck, 배포 환경 측정은 재실행하지 않음
  - 로컬/배포 응답 시간 지표는 승인된 측정 대상이 아직 없어 계속 보류
- 오늘 리스크/관찰:
  - `origin/develop`과 현재 브랜치가 4커밋씩 갈라져 있어 비교 기준을 명시하지 않으면 "문서-only 브랜치"와 "develop 대비 대규모 삭제"를 혼동할 위험이 있다.
  - `origin/develop` 최신 #67 FCM/알림 로그 구현이 현재 브랜치 tip에는 아직 포함되지 않아, 현재 브랜치 기준 검증 결과를 저장소 전체 최신 상태로 일반화하면 과대해석이 된다.
  - Gradle deprecated 경고는 build 경로에서도 재현됐고, 저장소 직접 사용처 검색은 여전히 0건이라 외부 플러그인 또는 공통 빌드 로직 추적이 추가로 필요하다.
- 오늘 테스트 후보:
  - `docker compose up -d postgres redis app` 후 승인된 단일 대상에 대해 `curl /api/v1/health` 반복 측정
  - 이유: 오늘은 Docker/runtime 검증을 재실행하지 않았고, 일별 health/응답시간 기준선은 여전히 비어 있다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
  - `./gradlew build --warning-mode all --stacktrace`
  - 이유: deprecated 경고가 build 경로에서도 재현됐지만 소스 위치가 아직 특정되지 않았다.
  - 기대 지표: 경고 발생 source 추적 가능 여부, Gradle 9 호환성 backlog 후보
  - `git switch develop && ./gradlew test`
  - 이유: 현재 보고서는 체크아웃된 브랜치 기준이며, 저장소 최신 통합 상태와 분리되어 있다.
  - 기대 지표: `develop` 기준 테스트 통과율, 브랜치 간 회귀 여부
  - 주의: 브랜치 전환은 사용자 승인된 비교 기준이 있어야 일일 지표 해석이 일관된다.

### 2026-06-20

- 브랜치/작업트리:
  - 기준 문서 확인: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md` 확인 후 진행. 저장소에는 `AGENT.md`가 없고 `AGENTS.md` 단일 규칙만 유지 중.
  - 현재 브랜치: `docs/37-poll-template-planning-sync`
  - `git status --short --branch`: 워크트리 변경 0건
  - `origin/develop` 대비 최근 커밋: 4개 (`b766520`, `3ecd177`, `4131fcc`, `fc366d7`)
- 변경 범위 수치:
  - `git diff --stat origin/develop..HEAD`: 3 files changed, 104 insertions, 0 deletions
  - 변경 파일: `docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`
  - 앱 코드 변경 파일: 0개
  - 테스트 코드 변경 파일: 0개
  - 설정/의존성 변경 파일: 0개
  - DB 마이그레이션 변경: 0건
  - 변경 모듈: 0개
- 문서 계약 동기화:
  - #37 커피 카탈로그 기준: MVP 커피 주문 브랜드를 Compose Coffee 1개로 제한하고, `coffee_brands`, `coffee_menu_catalog`, 공식 메뉴 소스 기반 seed 정책을 정책 문서에 반영.
  - #37 API 계약: `GET /api/v1/coffee-brands`, `GET /api/v1/coffee-brands/{brandId}/menus` 경로를 policy/Hook/decision log에 동기화.
  - #38 결과 조회 계약: `GET /api/v1/campuses/{campusId}/polls/{pollId}/results` 단일 poll-level API, 익명 결과 집계-only, 일반 사용자 3일 / 관리자 7일 visibility window를 정책 문서에 반영.
- 코드베이스 구조 수치:
  - `src/main/java/com/faithlog` top-level 모듈: 8개 (`admin`, `billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - Java 소스 파일: 231개
  - 테스트 소스 파일: 28개
  - 테스트 리소스 파일: 1개
  - DB 마이그레이션 파일: 0개
  - GitHub Actions workflow 파일: 2개
- 검증 신호:
  - `./gradlew test`: 성공, 50초, 24 test suites, 138 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew build`: 성공, 1초, 8 tasks up-to-date
  - `./gradlew asciidoctor`: 샌드박스 lock 실패 후 권한 상승 재실행 성공, 4초, 57 snippet groups, `build/docs/asciidoc/index.html` 434,854 bytes
  - `./gradlew test --warning-mode all`: 성공, configure phase에서 `StartParameter.isConfigurationCacheRequested` deprecated 경고 1건 확인
  - `rg -n "isConfigurationCacheRequested|configurationCacheRequested|configurationCache" .`: 저장소 직접 사용 0건
- 운영/배포 신호:
  - 오늘은 문서 브랜치 기준 검증만 수행했고 Docker 기동, 앱 healthcheck, 배포 환경 측정은 재실행하지 않음
  - 로컬/배포 응답 시간 지표는 승인된 측정 대상이 아직 없어 계속 보류
- 오늘 리스크/관찰:
  - 현재 브랜치는 문서-only 상태라 기능 회귀는 없지만, #37 구현 착수 전 공식 Compose Coffee 메뉴 소스 확보가 선행되지 않으면 seed 데이터와 청구 금액을 확정할 수 없다.
  - Gradle deprecated 경고는 여전히 남아 있고, 저장소 내부 직접 사용처가 검색되지 않아 외부 플러그인 또는 빌드 로직 원인 추적이 추가로 필요하다.
- 오늘 테스트 후보:
  - `docker compose up -d postgres redis app` 후 `curl /api/v1/health` 반복 측정
  - 이유: 오늘은 문서 브랜치라 런타임 검증을 재실행하지 않았고, 일별 health/응답시간 기준선은 아직 비어 있다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)
  - `./gradlew build --warning-mode all`
  - 이유: 오늘 `test --warning-mode all`로 deprecation source key는 확인했지만 build 경로까지 같은 원인인지 분리되지 않았다.
  - 기대 지표: deprecation 경고 발생 경로 수, build 전용 경고 존재 여부, Gradle 9 호환성 backlog 후보

### 2026-06-19

- #61 서비스 ADMIN 유저와 캠퍼스 관리 구현:
  - 브랜치: `feat/61-service-admin-user-campus-management`
  - 구현 API: `GET /api/v1/admin/users`, `GET /api/v1/admin/users/{userId}`, `PATCH /api/v1/admin/users/{userId}/role`, `GET /api/v1/admin/campuses`, `POST /api/v1/admin/campuses/{campusId}/members`, 기존 `GET/PATCH /api/v1/admin/campuses/{campusId}/members...`, `PATCH /api/v1/campuses/{campusId}` 권한 회귀 검증.
  - 확정 계약: 사용자 목록/상세 응답 필드, 캠퍼스 목록 응답 필드, sort 허용 필드, 마지막 ADMIN 판정 기준(`users.role = ADMIN` and `users.is_active = true`), 이미 ACTIVE 소속 직접 추가 시 `CAMPUS_ALREADY_JOINED` 400.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.admin.presentation.AdminManagementControllerTest`가 새 관리자 endpoint 미구현으로 4 tests / 4 failed 실패.
  - 구현 구조: `admin` application/presentation 패키지를 추가하고 `AdminAccessPolicy`, 검색 criteria, result DTO, repository port를 분리. Controller는 Entity를 반환하지 않고 request/response DTO와 `PageResponse`를 사용.
  - 검증 범위: `ADMIN` 전용 `/api/v1/admin/**`, `USER`/`MANAGER` 접근 거부, 멤버십 없는 서비스 `ADMIN` 전체 조회/수정, 사용자 검색/role/page/size/sort, 사용자 상세 캠퍼스 소속 상태, `users.role` 단독 변경, 마지막 ADMIN 강등 차단, 캠퍼스 검색/운영상태 필터/page/size/sort, `is_active` 기반 `ACTIVE`/`PAUSED`, 직접 멤버 추가, `INACTIVE` 재활성화, ACTIVE 중복 추가 실패, 캠퍼스 역할 same-level 정책 유지, 캠퍼스 수정 권한.
  - REST Docs 결과: `admin-users-list-success`, `admin-user-detail-success`, `admin-user-role-change-success`, `admin-campuses-list-success`, `admin-campus-member-add-success`, `campus-update-success` snippets 추가, 전체 snippet group 57개.
  - 재검증: `AdminManagementServiceTest`, `AdminManagementControllerTest`, `AdminManagementApiRestDocsTest` 성공, `./gradlew test` 성공(138 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - Docker 검증: `docker compose build app` 2회 시도 모두 `eclipse-temurin:21-jdk-alpine`/`21-jre-alpine` 베이스 이미지 metadata 조회 단계에서 `DeadlineExceeded: context deadline exceeded`로 실패. 컨테이너는 시작되지 않았고 `docker ps` 실행 결과 running container 0개.
  - 제외 범위 준수: audit log 저장/조회, `INVITED` 캠퍼스 상태, 신규 DB schema/enum, Swagger 문서화 어노테이션 추가 없음.
  - 코드베이스 수치: Java 소스 231개, 테스트 파일 28개.
- #57 내 월간 경건생활 통계 조회 구현:
  - 브랜치: `feat/57-my-monthly-devotion-summary`
  - 구현 API: `GET /api/v1/campuses/{campusId}/devotions/me/monthly-summary?year={year}&month={month}`
  - 구현 흐름: 현재 로그인한 사용자의 ACTIVE 캠퍼스 멤버십을 검증한 뒤, 선택 월의 첫날부터 마지막 날까지 `devotion_daily_checks.record_date` 기준으로 월간 합계와 주차별 부분 집계를 계산.
  - 구현 서비스/DTO: `DevotionMonthlySummaryQueryService`, `GetMyMonthlyDevotionSummaryQuery`, `MyMonthlyDevotionSummaryResult`, `MyMonthlyDevotionSummaryResponse`.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`가 `DevotionMonthlySummaryQueryService`, `GetMyMonthlyDevotionSummaryQuery`, `MyMonthlyDevotionSummaryResult`, `DEVOTION_INVALID_YEAR_MONTH` 부재로 `compileTestJava` 실패.
  - 검증 범위: `year/month` 검증, 비멤버 접근 거부, 본인 데이터만 조회, 월 경계 주차의 선택 월 날짜만 부분 집계, 토요일 날짜가 선택 월에 포함될 때만 `saturdayLateMinutes` 포함, 공통 `ApiResponse` envelope, Controller Entity 미반환.
  - REST Docs 결과: `devotion-my-monthly-summary-success`, `devotion-invalid-year-month` snippets 추가, 전체 snippet group 51개.
  - 재검증: #57 대상 테스트 묶음 성공, `./gradlew test` 성공(130 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - Docker 검증: `docker compose up -d --build postgres redis app` 성공, postgres/redis healthy, app started, 컨테이너 내부 `GET /api/v1/health` 응답 `status=UP` 확인, `docker compose down` 성공. 호스트 `curl localhost:8080`은 현재 세션 네트워크에서 연결 실패했지만 컨테이너 내부 health는 정상.
  - 제외 범위 준수: #31 하루 체크/주간 제출 구현, #32 벌금 규칙/계산, #33 벌금 청구 자동 생성, 관리자 경건생활 집계 API, 신규 DB 스키마, Swagger 문서화 어노테이션 변경 없음.
  - 코드베이스 수치: Java 소스 207개, 테스트 파일 26개.
- #57 PM 리뷰 보강 - 월간 경건생활 연도 검증:
  - 문제: Docker QA에서 `GET /api/v1/campuses/10/devotions/me/monthly-summary?year=0&month=6` 요청이 `200 OK`로 성공하고 `year: 0`, 합계 0 응답을 반환하는 입력 검증 누락 확인.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest`가 27 tests / 2 failed로 실패. 서비스는 `year=0` 또는 음수 year 요청을 `DEVOTION_INVALID_YEAR_MONTH`로 거부하지 않았고, 컨트롤러도 `year=0&month=6` 요청을 400으로 반환하지 못함.
  - 수정: `DevotionMonthlySummaryQueryService.yearMonth()`에서 `year <= 0`을 먼저 검증해 `DEVOTION_INVALID_YEAR_MONTH` 400 계약을 적용하고, `month < 1 || month > 12`는 기존 `YearMonth.of` 검증으로 동일 에러 코드를 유지.
  - 추가 테스트: 서비스 `year=0`, 음수 year 실패 케이스, 컨트롤러 `year=0` 400 케이스, REST Docs query parameter 설명의 `year` 1 이상 및 `month` 1~12 범위 명시.
  - 재검증: 대상 테스트 묶음 성공. 병렬 Gradle 실행 중 test result writer의 `build/test-results/test/TEST-*.xml` 파일 쓰기 충돌이 있었으나, daemon 중지 후 `./gradlew --no-daemon test` 성공. `./gradlew --no-daemon build`, `./gradlew --no-daemon asciidoctor`, `git diff --check` 성공.
- #33 경건생활 제출 시 벌금 청구 자동 생성 구현:
  - 브랜치: `feat/33-devotion-penalty-charge-automation`
  - 구현 흐름: `PUT /api/v1/campuses/{campusId}/devotions/me/weeks/{weekStartDate}` 첫 `submit=true`에서 주간 요약 저장 후 `PENALTY` 청구 1건 자동 생성.
  - 청구 기준: `paymentCategory=PENALTY`, `sourceType=DEVOTION_RECORD`, `sourceId=weekly_devotion_records.id`, `status=UNPAID`, 활성 PENALTY 계좌 및 계좌 snapshot 저장.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest`가 12 tests / 2 failed로 실패. 첫 제출 청구 미생성과 활성 계좌 없음 요청이 제출/일별 저장을 진행하는 문제를 확인. 중복 제출 에러 테스트는 `DEVOTION_WEEKLY_ALREADY_SUBMITTED` 부재로 `compileTestJava` 실패를 먼저 확인.
  - 수정: Devotion 애플리케이션 계층에 `DevotionPenaltyChargePort`/command를 두고 Billing 어댑터가 기존 `BillingService.createPenaltyCharge`를 호출하도록 분리. Devotion 도메인은 Billing Entity를 직접 참조하지 않는다.
  - 검증 범위: 첫 제출 청구 생성, `submit=false` 청구 미생성/미갱신, 제출 후 `submit=false` 저장 실패, 중복 `submit=true` 실패, 활성 PENALTY 계좌 없음 전체 실패 및 row 미생성, `weekly_devotion_records.id` sourceId 검증, account snapshot 검증, 음수 `saturdayLateMinutes` 차단 유지.
  - API 에러 계약: 계좌 없음 `BILLING_REQUIRED_PAYMENT_ACCOUNT_MISSING` 400 `관리자에게 문의하세요`, 중복 제출 `DEVOTION_WEEKLY_ALREADY_SUBMITTED` 409 `이미 제출된 주간 경건생활은 수정할 수 없습니다.`
  - API 응답 계약: `PUT /api/v1/campuses/{campusId}/devotions/me/weeks/{weekStartDate}` 성공 응답은 기존 `WeeklyDevotionResponse` 구조를 유지하고, `generatedCharges` 같은 청구 요약 필드는 추가하지 않음. 생성된 청구 확인은 기존 청구 조회 API를 사용.
  - REST Docs 결과: `devotion-missing-penalty-account`, `devotion-weekly-already-submitted` snippets 추가, 전체 snippet group 48개.
  - 재검증: `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest` 성공, `./gradlew test --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest` 성공, `./gradlew test` 성공(121 tests / 0 failures / 0 errors / 0 skipped).
  - 코드베이스 수치: Java 소스 203개, 테스트 파일 26개.
- #33 PM 리뷰 보강 - 제출 완료 주차 일별 체크 차단:
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`가 32 tests / 3 failed로 실패. 서비스/컨트롤러/REST Docs가 제출 완료 주차 일별 체크를 아직 허용하는 문제를 확인.
  - 수정: `updateDailyCheck`에서 해당 `recordDate`의 주차 weekly row를 먼저 조회하고 `submittedAt`이 있으면 `DEVOTION_WEEKLY_ALREADY_SUBMITTED`로 차단한 뒤, 미제출 주차에만 weekly/daily row를 생성 또는 수정하도록 변경.
  - 검증 범위: 주간 제출 후 같은 주차 일별 체크 실패, 기존 daily row/weekly summary/charge count 불변, HTTP 409와 error code 계약, REST Docs 에러 snippet.
  - 재검증: 대상 테스트 묶음 성공, `./gradlew cleanTest test --no-parallel --max-workers=1` 성공(124 tests / 0 failures / 0 errors / 0 skipped), `./gradlew test` 성공, `./gradlew build` 성공, `./gradlew asciidoctor` 성공.
  - REST Docs 결과: `devotion-daily-check-already-submitted-week` snippet 추가, 전체 snippet group 49개.
- #32 경건생활 벌금 규칙과 벌금 계산 구현:
  - 브랜치: `feat/32-devotion-penalty-rules`
  - 구현 API: `GET /api/v1/campuses/{campusId}/penalty-rules`, `POST /api/v1/admin/campuses/{campusId}/penalty-rules`, `PATCH /api/v1/admin/penalty-rules/{ruleId}`
  - 구현 모델/서비스: `PenaltyRule`, `PenaltyRuleType`, `PenaltyCalculationType`, `PenaltyRuleRepository`, `PenaltyRuleService`, `DevotionFineCalculator`, 벌금 계산 input/item/result records.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests 'com.faithlog.devotion.domain.DevotionFineCalculatorTest' --tests 'com.faithlog.devotion.application.PenaltyRuleServiceTest' --tests 'com.faithlog.devotion.presentation.PenaltyRuleApiRestDocsTest'`가 `PenaltyRule`, enum, repository, service, calculator, #32 error code 부재로 `compileTestJava` 실패. 구현 후 최초 runtime 검증에서 계산 테스트 기대값 산술 오류(3,100원 기대)를 발견하고 승인된 공식 기준에 맞춰 3,400원으로 테스트를 보정.
  - 검증 범위: 큐티/기도/말씀 부족 일수 `max(requiredCount - checkedCount, 0)`, `MISSING_COUNT` 금액, 토요 지각 0분 0원, 1분 이상 `baseAmount + minutes * amountPerUnit`, inactive rule 계산 제외, 같은 campus/ruleType ACTIVE 자동 교체, 수정/비활성화, 잘못된 rule/calculation 조합 400, 음수 기준값/금액 400, 관리자 권한, Controller DTO 응답.
  - 제외 범위 준수: #31 하루 체크/주간 제출 흐름 변경 없음, #33 `PENALTY charge_items` 생성/갱신 연결 없음, #34/#35 청구/계좌 상태 변경 없음, #57 월간 통계 및 벌금 미리보기 API/관리자 수동 청구 API/Flyway migration 추가 없음.
  - 재검증: #32 대상 테스트 묶음 성공, `./gradlew test` 성공(114 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공.
  - Docker 검증: `docker compose up -d --build postgres redis app` 성공, `GET /api/v1/health` 200 `status=UP`, Docker Postgres QA 계정 1건을 `MANAGER`로 바꿔 캠퍼스 생성 후 #32 POST/GET/PATCH API 성공, `docker compose down` 성공.
  - REST Docs 결과: `penalty-rule-create-success`, `penalty-rule-list-success`, `penalty-rule-update-success`, `penalty-rule-invalid-type-pair`, `penalty-rule-invalid-negative-value` snippets 생성, 전체 snippet group 46개.
  - 코드베이스 수치: Java 소스 200개, 테스트 파일 25개.
- #31 주간 경건생활 제출과 일별 체크 구현:
  - 브랜치: `feat/31-weekly-devotion-daily-check`
  - 구현 API: `PUT /api/v1/campuses/{campusId}/devotions/me/days/{recordDate}`, `PUT /api/v1/campuses/{campusId}/devotions/me/weeks/{weekStartDate}`, `GET /api/v1/campuses/{campusId}/devotions/me/weeks/{weekStartDate}`, `GET /api/v1/admin/campuses/{campusId}/devotions/missing?weekStartDate={weekStartDate}`
  - 구현 모델/서비스: `WeeklyDevotionRecord`, `DevotionDailyCheck`, `DevotionService`, Command/Result DTO, member/admin devotion controllers
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest`가 devotion 도메인/서비스/리포지토리 클래스 부재로 `compileTestJava` 실패.
  - 검증 범위: 하루 체크 daily/weekly row 생성 및 수정, 하루 체크의 `submittedAt`/청구 미변경, 주간 PUT 7일치 생성/수정, `dailyChecks` 필드, 제출 시 누락 날짜 false 기본값, 월요일 검증 400, `submit=true` 제출시각/요약값 갱신, 본인 주간 조회, 관리자 미제출자 조회 `submittedAt` 기준, ACTIVE 캠퍼스 멤버 권한, 캠퍼스 관리자 권한.
  - 제외 범위: 월간 경건생활 통계는 #57, 실제 `PENALTY charge_items` 생성/갱신은 #33으로 유지. #31 테스트는 `charge_items`가 생성되지 않음을 검증.
  - 재검증: #31 서비스/컨트롤러/REST Docs 테스트 성공, `./gradlew test` 성공(92 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - Docker 검증: `docker compose build app` 성공, `docker compose up -d postgres redis app` 성공, postgres/redis healthy, app started, 컨테이너 내부 `GET /api/v1/health` 응답 `status=UP` 확인, `docker compose down` 성공. 호스트 `curl localhost:8080`은 현재 세션에서 연결 실패했지만 컨테이너 내부 health는 정상.
  - REST Docs 결과: devotion snippets 5개 묶음 추가(`devotion-daily-check-success`, `devotion-weekly-save-submit-success`, `devotion-my-week-success`, `devotion-admin-missing-success`, `devotion-invalid-week-start-date`), 전체 snippet group 37개.
  - 코드베이스 수치: Java 소스 183개, 테스트 파일 22개.
- #31 PM 리뷰 입력 검증 보강:
  - TDD 실패 확인: 검증 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`가 새 `DEVOTION_*` ErrorCode 부재로 `compileTestJava` 실패.
  - 수정: 주간 PUT에서 `dailyChecks[].recordDate`가 `weekStartDate`부터 6일 뒤까지만 허용되도록 검증하고, `saturdayLateMinutes < 0` 요청을 도메인 에러 코드로 400 처리.
  - 추가 에러 코드: `DEVOTION_DAILY_CHECK_DATE_OUT_OF_WEEK`, `DEVOTION_INVALID_SATURDAY_LATE_MINUTES`.
  - 추가 테스트: 서비스 검증 2개, 컨트롤러 400 응답 2개, REST Docs 에러 계약 2개.
  - 재검증: 대상 테스트 묶음 성공, `./gradlew test --rerun-tasks` 성공(98 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공.
  - REST Docs 결과: `devotion-daily-check-date-out-of-week`, `devotion-invalid-saturday-late-minutes` snippet 추가, 전체 snippet group 39개.
- #31 빈 주간 경건생활 조회 기본 응답 결정 반영:
  - 문서 결정 포함: `origin/docs/31-devotion-planning-sync`의 `52b82b2 docs: #31 빈 주간 경건생활 조회 기본값 결정 기록`을 개발 브랜치에 병합.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`가 19 tests / 3 failed로 실패. 서비스는 기존 `DEVOTION_WEEKLY_RECORD_NOT_FOUND` 예외를 던졌고 HTTP/REST Docs는 기본 응답 기대에서 실패.
  - 수정: 본인 주간 조회에서 weekly row가 없으면 DB row를 생성하지 않고 월요일-일요일 7일치 false 기본 응답을 반환. `weeklyRecordId`, `submittedAt`, `dailyChecks[].id`는 null로 응답에 포함.
  - 추가 테스트: 서비스 기본 조회/DB 미생성 1개, 컨트롤러 200 기본 응답/DB count 불변 1개, REST Docs 기본 성공 계약 1개.
  - 재검증: 대상 테스트 묶음 성공, `./gradlew test --rerun-tasks` 성공(101 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공.
  - REST Docs 결과: `devotion-my-week-default-success` snippet 추가, 전체 snippet group 40개.
- #31 Docker QA 부분 주간 조회 7일 합성 수정:
  - QA 증거: 빈 주간 조회는 7일 기본 응답과 DB row 미생성을 만족했지만, 하루 체크 후 주간 조회가 저장된 1일치(`2026-06-17`)만 반환.
  - TDD 실패 확인: 구현 전 `./gradlew test --tests com.faithlog.devotion.application.DevotionServiceTest --tests com.faithlog.devotion.presentation.DevotionControllerTest --tests com.faithlog.devotion.presentation.DevotionApiRestDocsTest`가 22 tests / 3 failed로 실패. 부분 주간 조회가 7일이 아니라 저장된 daily row만 반환하는 문제 확인.
  - 수정: 본인 주간 조회 결과 생성 시 weekly row가 있어도 월요일-일요일 7일치 `dailyChecks`를 합성. 저장된 날짜는 DB id/체크값을 사용하고, 누락 날짜는 `id = null`, false 기본값으로 반환. 조회 중 누락 daily row는 생성하지 않음.
  - 추가 테스트: 서비스 부분 주간 조회/DB 미생성 1개, 컨트롤러 부분 주간 7일 응답 1개, REST Docs 부분 주간 성공 계약 1개.
  - 재검증: 대상 devotion 테스트 묶음 성공, `./gradlew test --rerun-tasks` 성공(104 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공.
  - REST Docs 결과: `devotion-my-week-partial-success` snippet 추가, 전체 snippet group 41개.
- #55 공통 에러 코드와 요청 검증 구조 리팩토링:
  - 브랜치: `refactor/55-error-validation-structure`
  - TDD 실패 확인: 세부 error code, 잘못된 `page`/`size`/`sort` 400 응답, Bean Validation 실패 code, billing/campus/auth 주요 예외 code, REST Docs 대표 에러 응답 계약 테스트를 먼저 추가. 구현 전 대상 테스트 묶음은 28 tests / 12 failed로 실패.
  - 수정: 글로벌 `ErrorCode`를 `AUTH_*`, `CAMPUS_*`, `BILLING_*`, `GLOBAL_*` 세부 code로 확장하고, `BusinessException`/`GlobalExceptionHandler`/Security entry point가 세부 code를 응답하도록 정리. `PageSortRequestValidator` 공통 컴포넌트로 page/size/sort 검증을 분리해 잘못된 값 자동 보정을 제거. `CampusRolePolicy`, `BillingAccessPolicy`, `ChargeStatusPolicy`로 비즈니스 규칙 검증을 분리.
  - 추가 운영 장치: `.githooks/commit-msg`를 추가해 `<분류>: #<이슈번호> <한국어 작업 요약>` 커밋 메시지 형식을 강제하고, 잘못된 메시지 실패/올바른 메시지 성공을 수동 검증.
  - 재검증: 수정된 테스트 묶음 44 tests 성공, `./gradlew test` 성공(82 tests / 0 failures / 0 errors / 0 skipped), `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - REST Docs 결과: 대표 에러 응답 snippet `error-response-detailed-code` 추가, 전체 snippet group 32개.
- #36 PM 재검토 sort 허용 목록 버그 수정:
  - 문제: 관리자 캠퍼스 청구 회원별 집계 조회에서 `sort=amount`, `sort=status`, `sort=paymentCategory` 같은 charge item 전용 정렬 필드가 유효 요청처럼 통과했지만 실제 정렬은 `latestChargeCreatedAt` default로 처리될 수 있었다.
  - TDD 실패 확인: `BillingControllerTest`에 `sort=amount,asc`는 `400 Bad Request`와 `지원하지 않는 정렬 기준입니다.`를 반환하고, `sort=unpaidAmount,desc`는 정상 동작해야 하는 테스트를 먼저 추가. 구현 수정 전 `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest`가 8 tests / 1 failed로 실패.
  - 수정: `BillingPageRequests.adminMembers()` 허용 정렬 목록을 실제 회원 집계 comparator가 지원하는 `createdAt`, `userId`, `name`, `email`, `totalAmount`, `unpaidAmount`, `paidAmount`, `waivedAmount`, `canceledAmount`로 제한. 내 청구/관리자 회원별 상세 charge item 목록 정렬 허용 목록은 유지.
  - 재검증: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor는 샌드박스 wrapper lock 실패 후 권한 상승 재실행으로 성공.
- #36 PM 재검토 sort direction 검증 보강:
  - 문제: `sort=name,wrong`, `sort=createdAt,ascending`, `sort=unpaidAmount,foo` 같은 잘못된 direction 값이 조용히 `DESC`로 처리될 수 있었다.
  - TDD 실패 확인: `sort=unpaidAmount,wrong`과 `sort=createdAt,ascending`이 `400 Bad Request`와 `지원하지 않는 정렬 방향입니다.`를 반환해야 하는 컨트롤러 테스트를 먼저 추가. 구현 수정 전 `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest`가 8 tests / 1 failed로 실패.
  - 수정: `BillingPageRequests.sort()`에서 direction이 없으면 기본 `DESC`를 유지하고, direction이 있으면 `asc` 또는 `desc`만 허용하도록 검증을 추가. 검증 로직은 page request helper 안에 유지.
  - 재검증: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor는 샌드박스 wrapper lock 실패 후 권한 상승 재실행으로 성공.
- #36 PM 재검토 sort 형식 검증 보강:
  - 문제: `sort=createdAt,desc,extra`, `sort=unpaidAmount,asc,ignored`처럼 `property,direction`보다 긴 malformed sort가 앞의 두 토큰만 사용되어 정상처럼 처리될 수 있었다.
  - TDD 실패 확인: malformed sort가 `400 Bad Request`와 `지원하지 않는 정렬 형식입니다.`를 반환해야 하는 컨트롤러 테스트를 먼저 추가. 구현 수정 전 `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest`가 8 tests / 1 failed로 실패.
  - 수정: `BillingPageRequests.sort()`에서 comma token이 2개를 초과하면 `INVALID_REQUEST`로 차단. `sort=createdAt`, `sort=createdAt,asc`, `sort=createdAt,desc` 정상 동작은 유지.
  - 재검증: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor는 샌드박스 wrapper lock 실패 후 권한 상승 재실행으로 성공.

### 2026-06-18

- #36 청구 목록 조회와 캠퍼스별 집계 구현 검증:
  - 브랜치: `feat/36-charge-list-campus-summary`
  - 구현 API: `GET /api/v1/campuses/{campusId}/charges/me`, `GET /api/v1/campuses/{campusId}/charges/me/summary`, `GET /api/v1/admin/campuses/{campusId}/charges`, `GET /api/v1/admin/campuses/{campusId}/members/{userId}/charges`
  - 구현 모델/서비스: `BillingQueryService`, `ChargeSearchCriteria`, 조회 Query/Result records, 목록 전용 `ChargeListItemResponse`, 관리자 campus/member response DTO
  - 확정 계약: `startDate`/`endDate` 제거, 백엔드는 전체 이력 보존 + pagination/sort/filter 조회, 앱 기본 화면에서 최근 납부 항목 노출 UX 처리. 월별 요약은 `monthlyPaidAmount = paidAt 기준`, `monthlyUnpaidAmount/monthlyTotalChargeAmount/monthlyByCategory = createdAt 기준`.
  - TDD 실패 확인:
    - `./gradlew test --tests com.faithlog.billing.application.BillingQueryServiceTest` 실패: `BillingQueryService`, `MyChargeListQuery`, `MyChargesResult`, admin query/result records 부재로 `compileTestJava` 실패.
    - `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest` 실패: 새 `GET /api/v1/campuses/{campusId}/charges/me` endpoint 미구현으로 기대 200 assertion 실패.
  - 테스트 결과: `./gradlew test --tests com.faithlog.billing.application.BillingQueryServiceTest` 성공, `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest` 성공, `./gradlew test --tests com.faithlog.billing.presentation.BillingApiRestDocsTest` 성공, `./gradlew test` 성공(77 tests / 0 failures / 0 errors / 0 skipped)
  - 빌드/문서 결과: `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - Docker 검증: `docker compose build app` 성공, `docker compose up -d postgres redis app` 성공, postgres/redis healthy, app started, 컨테이너 내부 `GET /api/v1/health` 응답 `status=UP` 확인, `docker compose down` 성공. 호스트 `curl localhost:8080`은 현재 세션 네트워크에서 연결 실패했지만 컨테이너 내부 health는 정상.
  - REST Docs 결과: charge query snippets 4개 묶음 추가(`charge-my-list-success`, `charge-my-summary-success`, `charge-admin-campus-summary-success`, `charge-admin-member-detail-success`), 전체 snippet group 31개.
  - 검증 범위: 본인 ACTIVE 캠퍼스 멤버 청구 목록/요약, item `account` snapshot 객체와 `source` 객체, `paymentCategory`/`status` 필터, page/size/sort 기본값, 관리자 campus `summary + members[]` 집계만 반환, 관리자 회원별 상세 대상 회원 `userId/name/email`, 전역 `ADMIN` 허용, 서비스 `MANAGER` 단독 권한 거부, 일반 `MEMBER` 관리자 조회 거부.
  - 코드베이스 수치: Java 소스 157개, 테스트 파일 20개.
  - 금지어 검사: 실제 소스/테스트/API 문서에서 금지어 위반 0건. Swagger 문서화 어노테이션 추가 0건.
  - PM 재검증 보강: 관리자 캠퍼스 청구 조회 `status=UNPAID` 필터 회귀 테스트를 추가해 미납 청구가 있는 회원만 `members[]`에 포함되고, paid/waived/canceled만 있는 회원은 제외되며, 개별 `items`는 반환되지 않는 계약을 고정.
  - PM 재검증 문서화: GitHub Issue #36, Notion `16.1`, `16.4`, `16.5`, `API 설계`, `FaithLog 통합 기획서·ERD·API 설계`를 `startDate`/`endDate` 미사용 정책과 `summary + members`/회원별 상세 분리 기준으로 동기화.
  - PM 재검증 결과: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(78 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor는 샌드박스 wrapper lock 실패 후 권한 상승 재실행으로 성공.

- #35 청구 납부 완료, 면제, 취소 상태 관리 구현 검증:
  - 브랜치: `feat/35-charge-paid-waive-cancel`
  - 구현 API: `PATCH /api/v1/campuses/{campusId}/charges/me/{chargeItemId}/paid`, `PATCH /api/v1/admin/charges/{chargeItemId}/status`
  - 구현 모델/서비스: `ChargeItem.markPaid(Instant)`, `ChargeItem.waive`, `ChargeItem.cancel`, `ChargeItem.reopenAsUnpaid`, `BillingService.completeMyChargePayment`, `BillingService.changeChargeStatus`
  - TDD 실패 확인: 구현 전 `./gradlew test --tests 'com.faithlog.billing.*'`가 `CompleteChargePaymentCommand`, `ChangeChargeStatusCommand`, `paidAt`, 상태 전이 메서드 부재로 `compileTestJava` 실패.
  - 테스트 결과: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공, 67 tests / 0 failures / 0 errors / 0 skipped
  - 빌드 결과: `./gradlew build` 성공
  - 문서 렌더 결과: `./gradlew asciidoctor` 성공. 최초 샌드박스 실행은 Gradle wrapper lock 파일 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - REST Docs 결과: charge status snippets 2개 묶음 추가 (`charge-my-paid-success`, `charge-admin-status-change-success`), 전체 snippet group 27개
  - 검증 범위: 본인 `UNPAID` 청구 즉시 `PAID`, `paidAt` 요청값 저장, `paidAt` 생략 시 서버 시간 저장, body 생략/빈 JSON 허용, 타인 청구/다른 캠퍼스/비활성 멤버 거부, terminal 청구 재납부 `409`, 관리자 `UNPAID -> WAIVED/CANCELED`, `PAID/WAIVED/CANCELED -> UNPAID`, `PAID -> UNPAID` 시 `paidAt` null, 관리자 `PAID` 처리 금지, 일반 `MEMBER`와 서비스 `MANAGER` 단독 권한 거부.
  - 코드베이스 수치: Java 소스 134개, 실구현 Java 파일 107개, 테스트 파일 19개.
  - 금지어 검사: 실제 소스/테스트/API 문서에서 금지어 위반 0건. 단수 API 필드 `optionId` 검색은 Hook 문서의 검사 예시 1건만 확인.
  - 범위 분리: 경건생활 자동 청구 연결은 #33, 커피 자동 청구 연결은 #39로 유지.
  - PM 리뷰 테스트 보강:
    - 추가 범위: 전역 `ADMIN`의 캠퍼스 멤버십 없는 관리자 청구 상태 변경 성공, `ELDER`/`CAMPUS_LEADER`의 관리자 청구 상태 변경 성공, `INACTIVE` 멤버의 본인 청구 납부 완료 API `403`.
    - 재검증: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(70 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공.

- #34 계좌와 청구 항목 관리 구현 검증:
  - 브랜치: `feat/34-payment-account-charge-item`
  - 구현 API: `GET /api/v1/campuses/{campusId}/payment-accounts`, `POST /api/v1/admin/campuses/{campusId}/payment-accounts`, `PATCH /api/v1/admin/payment-accounts/{accountId}/deactivate`
  - 구현 모델/서비스: `PaymentAccount`, `ChargeItem`, `PaymentCategory(PENALTY/COFFEE)`, `ChargeSourceType(DEVOTION_RECORD/POLL_RESPONSE)`, `ChargeStatus(UNPAID/PAID/WAIVED/CANCELED)`, `BillingService.createPenaltyCharge`
  - TDD 실패 확인: 구현 전 `./gradlew test --tests 'com.faithlog.billing.*'`가 billing 도메인/서비스/리포지토리 클래스 부재로 `compileTestJava` 실패. terminal 상태 보강 전 `markWaived`, `markCanceled` 부재 실패도 별도 확인.
  - 테스트 결과: `./gradlew test` 성공, 56 tests / 0 failures / 0 errors / 0 skipped
  - 빌드 결과: `./gradlew build` 성공
  - 문서 렌더 결과: `./gradlew asciidoctor` 성공. 최초 샌드박스 실행은 Gradle wrapper lock 파일 권한 문제로 실패했고, 권한 상승 재실행으로 성공.
  - Docker 검증: `docker compose build app` 시도 중 Docker daemon 응답 `Docker Desktop is unable to start`로 중단. 앱 이미지 빌드 전 로컬 Docker Desktop 상태 문제이며 코드 검증으로 완료하지 못함.
  - REST Docs 결과: payment account snippets 3개 묶음 추가 (`payment-account-create-success`, `payment-account-list-success`, `payment-account-deactivate-success`), 전체 snippet group 25개
  - 검증 범위: 캠퍼스별 accountType 활성 계좌 1개 정책, 새 활성 계좌 등록 시 기존 활성 계좌 자동 비활성화, ACTIVE 멤버 조회 허용, 비멤버/INACTIVE 멤버 조회 거부, 계좌 등록/비활성화 관리자 권한, 계좌번호 전체 노출, 일반 멤버 응답의 관리용 메타데이터 미노출, UNPAID 청구 재연결/snapshot 갱신, PAID/WAIVED/CANCELED snapshot 유지, 활성 PENALTY 계좌 누락 시 `관리자에게 문의하세요`, 계좌 누락 시 charge row 미생성, 청구 생성 시 snapshot 저장, 중복 청구 unique 제약.
  - 코드베이스 수치: Java 소스 129개, 실구현 Java 파일 102개, 테스트 파일 19개.
  - 금지어 검사: 실제 소스/README에서 금지어 및 단수 API 필드 `optionId` 위반 0건. Swagger 문서화 어노테이션 추가 0건.
  - 범위 분리: 실제 경건생활 제출 PENALTY 연결은 #33, 커피 투표 응답 COFFEE 연결은 #39로 유지.
  - PM 리뷰 수정:
    - 실패 확인: `./gradlew test --tests 'com.faithlog.billing.*'`가 4건 실패. 서비스 ADMIN 계좌 조회가 `BusinessException`/HTTP assertion failure로 실패했고, 같은 source의 `createPenaltyCharge` 재실행 2건이 unique constraint `DataIntegrityViolationException`으로 실패.
    - 수정 내용: 서비스 `ADMIN`의 계좌 조회 허용, 기존 `UNPAID` PENALTY 청구 create-or-update, 최신 active PENALTY 계좌 snapshot/title/reason/amount/dueDate 갱신. terminal 청구 재제출 정책은 아직 사용자 확정 전이므로 #34 foundation에서는 데이터 훼손 방지용 구현 가드로 덮어쓰기를 막고 명확한 예외를 반환.
    - 재검증: `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(59 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공.
    - Docker 재검증: `docker compose build app`가 Docker daemon 응답 `Docker Desktop is unable to start`로 동일하게 중단.

- #30 캠퍼스 멤버 역할/커피 담당자 관리 구현 검증:
  - 브랜치: `feat/30-campus-member-role-duty-assignment`
  - 구현 API: `GET /api/v1/admin/campuses/{campusId}/members`, `PATCH /api/v1/admin/campuses/{campusId}/members/{campusMemberId}/campus-role`, `GET /api/v1/admin/campuses/{campusId}/duty-assignments`, `PUT /api/v1/admin/campuses/{campusId}/duty-assignments/coffee`, `DELETE /api/v1/admin/campuses/{campusId}/duty-assignments/coffee/{assignmentId}`
  - 테스트 결과: `./gradlew test` 성공, 47 tests / 0 failures / 0 errors / 0 skipped
  - 빌드 결과: `./gradlew build` 성공
  - REST Docs 결과: `./gradlew asciidoctor` 성공, Spring REST Docs snippet group 22개 생성, admin campus snippets 5개 추가
  - 역할 변경 검증: `MINISTER`/`ELDER`/`CAMPUS_LEADER`의 same-level assignment, 상위 역할 변경/부여 거부, `MEMBER` 권한 없음, 전역 `ADMIN` 전체 변경 허용, 전역 `MANAGER` 단독 권한 없음, 마지막 관리 역할 `MEMBER` downgrade 허용.
  - 커피 담당자 검증: `CampusDutyAssignment + DutyType.COFFEE`로 분리, 새 담당자 지정 시 기존 활성 담당자 inactive 처리, 활성 담당자 목록 1명 유지, 해제 시 inactive/revoked 처리, non-`MEMBER` 캠퍼스 역할 및 전역 `ADMIN` 관리 허용.
  - 동시성 보강: concurrent `PUT /duty-assignments/coffee` 상황을 재현하는 `CampusDutyAssignmentConcurrencyTest` 추가. 구현 전에는 active row 중복으로 `NonUniqueResultException` 실패를 확인했고, 캠퍼스 row `PESSIMISTIC_WRITE` lock 적용 후 동시 12개 지정 요청에서도 active coffee assignment 1개 유지 검증.
  - 코드베이스 수치: Java 소스 110개, 실구현 Java 파일 83개, 테스트 소스 14개, 테스트 리소스 1개.
  - Docker 검증: `docker compose build app` 성공, `docker compose up -d postgres redis app` 성공, postgres/redis healthy, app container started, `GET /api/v1/health` 응답 `status=UP` 확인.
  - 문서 동기화: `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/backend-implementation-policy.md`, GitHub Issue #30, Notion role/coffee/API 통합 문서를 same-level assignment 기준으로 갱신.
  - 금지어 검사: 실제 소스/테스트/API 문서에서 금지어 및 단수 API 필드 `optionId` 위반 0건. 허용된 정책 문서 예시만 검색됨.
  - 제품/아키텍처 결정 기록: same-level campus role assignment와 coffee duty non-`MEMBER` permission을 `docs/decision-log.md`에 기록.

- #29 캠퍼스 생성/초대코드 가입 구현 검증:
  - 브랜치: `feat/29-campus-create-join`
  - 구현 API: `POST /api/v1/campuses`, `POST /api/v1/campuses/join`, `GET /api/v1/campuses/me`, `GET /api/v1/campuses/{campusId}`, `DELETE /api/v1/campuses/{campusId}/members/{membershipId}`
  - 테스트 결과: `./gradlew test` 성공, 37 tests / 0 failures / 0 errors / 0 skipped
  - 빌드 결과: `./gradlew build` 성공
  - REST Docs 결과: `./gradlew asciidoctor` 성공, Spring REST Docs snippet group 17개 생성
  - 캠퍼스 관련 신규/변경 테스트 파일: 3개 (`CampusControllerTest`, `CampusServiceTest`, `CampusApiRestDocsTest`)
  - 캠퍼스 멤버 삭제 검증: 일반 `MEMBER` 삭제 거부, `ELDER` 삭제 허용, 서비스 `ADMIN` 캠퍼스 미가입 삭제 허용, 삭제 시 `INACTIVE` 전이, 삭제 후 초대코드 재가입 시 기존 멤버십 `ACTIVE + MEMBER` 재활성화.
  - Java 소스 수: 96개, 실구현 Java 파일 69개, `package-info.java` 27개
  - Docker PostgreSQL 검증: `docker compose up -d postgres redis app` 이미지 빌드와 postgres/redis healthcheck 성공. 기존 로컬 Docker volume의 `faithlog` role 비밀번호가 compose 네트워크 접속 기준과 어긋난 상태를 `ALTER USER faithlog WITH PASSWORD 'faithlog'`로 정리한 뒤, `docker compose up -d --force-recreate app` 및 `GET /api/v1/health` 200 검증 완료.
  - 금지어 검사: 실제 소스/테스트/API 문서에서 금지어 및 단수 API 필드 `optionId` 위반 0건. `CampusRole` 검사 결과는 최종 enum 값 `MINISTER`, `ELDER`, `CAMPUS_LEADER`, `MEMBER` 구조로 정상.
  - 제품/아키텍처 결정 기록: 캠퍼스 생성은 `PaymentAccount`와 `penalty_rules`를 만들지 않으며, `GET /campuses/me`와 상세 조회 응답 계약/오류 메시지를 `docs/decision-log.md`에 기록.

- 브랜치/작업트리:
  - 현재 브랜치: `feat/28-auth-refresh-logout-redis`
  - `git status --short --branch`: `docs/resume-metrics.md`와 wiki 문서 변경/추가가 남아 있던 상태에서 검증했고, 이 중 `docs/resume-metrics.md`는 별도 docs 커밋 대상으로 정리
  - `develop` 대비 추가 커밋: 6개 (`0b7cc7a`, `f14ffb7`, `ea5bd3d`, `59d89b0`, `3885808`, `9a910ba`)
- 변경 범위 수치:
  - `git diff --stat origin/develop..HEAD`: 33 files changed, 1,099 insertions, 12 deletions
  - 앱 코드 변경 파일: 22개
  - 테스트 코드 변경 파일: 7개
  - 프로젝트 문서 변경 파일: 3개 (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`)
  - API 문서 변경 파일: 1개 (`src/docs/asciidoc/index.adoc`)
  - 변경 모듈: 2개 (`global`, `user`)
  - 의존성/DB 마이그레이션 변경: 0건
- 코드베이스 구조 수치:
  - `src/main/java/com/faithlog` top-level 모듈: 7개 (`billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - Java 소스 파일: 74개
  - 실구현 Java 파일(`package-info.java` 제외): 47개
  - `package-info.java`: 27개
  - 테스트 소스 파일: 11개
  - 테스트 리소스 파일: 1개
  - 테스트 스위트: 7개
  - 테스트 케이스: 21개
  - DB 마이그레이션 파일: 0개 (Flyway deferred)
- 검증 신호:
  - `./gradlew test --rerun-tasks`: 성공, 20초, 5 tasks executed, 21 tests / 0 failures / 0 errors / 0 skipped
  - `./gradlew asciidoctor --rerun-tasks`: 성공, 39초, 6 tasks executed, REST Docs snippets 재생성
  - `./gradlew build`: 성공, 5초, 3 tasks executed / 5 tasks up-to-date
  - 빌드 아티팩트: `build/libs/faithlog-backend-0.0.1-SNAPSHOT.jar`, `build/libs/faithlog-backend-0.0.1-SNAPSHOT-plain.jar`
  - Spring REST Docs 스니펫 묶음: 10개
  - 생성 문서 확인: `build/docs/asciidoc/index.html` 91,078 bytes
- 운영/문서 신호:
  - 인증 상세 계약 문서 파일 유지: `src/docs/asciidoc/index.adoc`
  - 코드상 헬스 엔드포인트 존재: `GET /api/v1/health`
  - 응답 시간/헬스 성공률은 측정 대상 환경이 승인되지 않아 오늘도 수치 미기록
- 오늘 리스크/관찰:
  - Gradle 실행은 성공했지만 deprecated feature 경고가 남아 있어 Gradle 9 업그레이드 전에 원인 정리가 필요하다.
  - 현재 브랜치 변경은 인증(`user`, `global`)에 집중되어 있고 나머지 5개 top-level 모듈은 이번 브랜치에서 직접 변경되지 않았다.
  - #40의 실제 FCM port 구현이 추가될 때 NoOp FCM adapter가 충돌하거나 우선 사용되지 않도록 `@ConditionalOnMissingBean(CurrentDeviceFcmTokenDeactivationPort.class)` 기반 configuration bean으로 정리했다.
- 오늘 테스트 후보:
  - `./gradlew test --warning-mode all`
  - 이유: 오늘 `test`/`build` 모두 Gradle deprecated feature 경고를 출력했지만 원인 플러그인/스크립트가 식별되지 않았다.
  - 기대 지표: 경고 발생 항목 수, 소유 위치(빌드 스크립트/플러그인), Gradle 9 호환성 정리 backlog
  - `docker compose up -d postgres redis app` 후 `curl /api/v1/health` 반복 측정
  - 이유: 헬스 엔드포인트는 존재하지만 승인된 일일 측정 대상이 아직 없다.
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)

### 2026-06-17

- 브랜치/작업트리:
  - 현재 브랜치: `chore/codex-hook-dev-rules`
  - `git status --short --branch`: 워크트리 변경 0건
  - `develop` 대비 최근 커밋: 4개 (`9e0a6b0`, `65c6ba0`, `6845738`, `a5289e4`)
- 변경 범위 수치:
  - `develop..HEAD` diff: 파일 6개, 추가 1,179라인, 삭제 0라인
  - 앱 코드 변경 파일: 0개
  - 문서/운영 규칙 변경 파일: 6개 (`AGENTS.md`, `README.md`, `docs/*`)
- 코드베이스 구조 수치:
  - `src/main/java/com/faithlog` top-level 모듈: 7개 (`billing`, `campus`, `devotion`, `global`, `notification`, `poll`, `user`)
  - Java 소스 파일: 36개
  - 실구현 Java 파일(`package-info.java` 제외): 9개
  - `package-info.java`: 27개
  - 테스트 파일: 1개
  - 테스트 리소스 파일: 1개
  - DB 마이그레이션 파일: 0개 (Flyway deferred)
- 의존성/설정 관찰:
  - `build.gradle.kts`에서 Flyway 런타임 의존성 제거
  - 핵심 런타임 의존성 유지: Spring Boot 3.5.0, Java 21, JPA, Redis, Security, PostgreSQL, Firebase Admin, JWT
  - Netty override 유지: `4.1.135.Final`
- 운영 신호:
  - 코드상 헬스 엔드포인트 존재: `GET /api/v1/health`
  - GitHub Actions workflow 파일: 2개 (`ci.yml`, `project-docs-check.yml`)
  - `ci.yml` 로컬 기준 품질 게이트 job: 2개 (`spring-boot`, `docker`)
  - Docker Compose 로컬 서비스: 5개 (`postgres`, `redis`, `pgadmin`, `redis-commander`, `app`)
  - Docker Compose 명시 healthcheck: 2개 (`postgres`, `redis`)
  - 응답 시간/헬스 성공률은 측정 대상 환경이 승인되지 않아 오늘 수치 미기록
- 오늘 테스트 후보:
  - `docker compose up -d postgres redis` 후 앱 기동 + `curl /api/v1/health` 측정
  - 이유: 현재 엔드포인트는 존재하지만 승인된 런타임 기준의 일별 헬스/지연시간 기준선이 없다
  - 기대 지표: 앱 기동 성공 여부, HTTP 200 여부, 응답 시간(ms), 연속 성공률(%)

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
  - DB 마이그레이션: 0개 (Flyway deferred)
- 기획 정합성 보정 수치:
  - 핵심 정책 반영 이슈: 7개 (#21, #27, #28, #31, #38, #39, #40)
  - 수동 `칸반 상태:` 제거 이슈: 21개 범위 검증 중 14개 직접 정리, 최종 잔여 0개
  - 코드 충돌 확인: `refresh_tokens` 테이블/Entity 없음, 현 시점 삭제 작업 불필요
- Project Board 정합성 보정 수치:
  - GitHub Project Board 필드 수정: 24개
  - #39 Priority: P1 -> P0
  - #16 Kanban Status: Code Review -> Done
  - #23~#26 누락된 Priority/Estimate/Work Type/Epic/Release/Domain 필드 보강
  - #23, #24 Domain은 single-select 제약과 혼합 도메인 표기 때문에 pending decision으로 남김
- Codex Hook 세팅 수치:
  - GitHub Issue 생성: 1개 (#43)
  - GitHub Project 카드 연결: 1개
  - Project 카드 상태: In Progress
  - 개발 규칙 문서 추가: 1개 (`docs/codex/FAITHLOG_CODEX_HOOK.md`)
  - README Codex Hook 링크 추가: 1개
  - 금지어 검색 결과: 허용 문서 외 0건
- Agent 규칙 정리 수치:
  - Agent 규칙 파일 단일화: 2개(`AGENT.md`, `AGENTS.md`) -> 1개(`AGENTS.md`)
  - 문서 우선순위 명시: 사용자 최신 결정 > decision-log > Notion > Hook > backend policy > 기존 코드
  - 단수 `optionId` 검사 기준 추가: 1개 명령 패턴
  - `AGENT.md` 활성 로딩 참조: 0건
- 투표 템플릿 정책 정리 수치:
  - 기본 제공 템플릿: 1개(커피)
  - 관리자 생성 템플릿 범주: 3개(수요예배, 토요목자모임, 커스텀)
  - 반영 대상: #37 투표 템플릿/투표 생성 기획
- 투표 자동 생성 정책 정리 수치:
  - 자동 생성 설정 가능 대상: 관리자 생성 PollTemplate
  - 실행 담당 이슈: #24 Scheduler/Batch
  - 중복 방지 기준: campus + template + week 단위 필요
- 커피 투표 시간 설정 정책 수치:
  - 커피 담당자가 설정하는 시간 필드: 2개(자동 생성 시간, 마감 시간)
  - 적용 대상: 기본 커피 PollTemplate
  - 칼럼명 기준: Notion ERD

## Troubleshooting Log

| 날짜 | 문제 | 원인 | 해결 | 전후 수치 | 재발 방지 |
| --- | --- | --- | --- | --- | --- |
| 2026-06-20 | 샌드박스에서 `./gradlew asciidoctor` 재실행 실패 | `~/.gradle/wrapper` 락 파일이 샌드박스 쓰기 범위 밖에 있어 `.zip.lck` 파일을 열 수 없었음 | 권한 상승으로 동일 명령 재실행 후 성공 | 전: 즉시 `FileNotFoundException`, 후: 4초 성공 + snippet group 57개 확인 | Gradle 문서 생성 검증은 샌드박스 lock 실패 시 즉시 권한 상승 재시도 |
| 2026-06-19 | #33 전체 테스트 XML 결과 파일 쓰기 실패 | 기본 전체 테스트 실행 중 일부 `build/test-results/test/TEST-*.xml`이 0바이트로 남아 Gradle 테스트 결과 XML 작성이 실패 | `cleanTest` 후 단일 워커(`--no-parallel --max-workers=1`)로 전체 테스트를 재실행하고, 이후 요청 명령 `./gradlew test`를 다시 실행해 성공 확인 | 전: `./gradlew test` 코드 실패 없이 XML write error, 후: 124 tests / 0 failures / 0 errors / 0 skipped 및 `./gradlew test` 성공 | 동일 증상 재발 시 산출물 정리 후 단일 워커 전체 테스트로 검증 |
| 2026-06-18 | 샌드박스에서 `./gradlew asciidoctor` 실행 실패 | `~/.gradle/wrapper` 락 파일이 샌드박스 쓰기 범위 밖에 있어 Gradle wrapper가 `.zip.lck` 파일을 열지 못함 | 권한 상승으로 동일 명령 재실행 후 성공 | 전: `./gradlew asciidoctor` 즉시 실패, 후: 3초 성공 + `build/docs/asciidoc/index.html` 생성 확인 | Gradle 기반 문서 생성 검증은 샌드박스 실패 시 권한 상승 재시도 |
| 2026-06-17 | 샌드박스에서 Gradle wrapper lock 파일 접근 실패 | `~/.gradle/wrapper` 락 파일이 샌드박스 쓰기 범위 밖에 있어 `./gradlew test`가 `FileNotFoundException`으로 중단 | 권한 상승으로 동일 명령 재실행 후 성공 | 전: 테스트 실행 실패, 후: `./gradlew test` 21.29초 성공 / `./gradlew build` 7.58초 성공 | 자동화 리포트에서 Gradle 검증은 필요 시 권한 상승 재시도 |
| TBD | TBD | TBD | TBD | TBD | TBD |

## Test Runs

| 날짜 | 명령/방법 | 결과 | 주요 수치 | 후속 조치 |
| --- | --- | --- | --- | --- |
| 2026-06-20 | Branch monitoring audit | 성공 | `origin/develop` 대비 4커밋, 3파일, +104/-0, 앱 코드 0파일, 테스트 코드 0파일, 설정/의존성 0건, DB migration 0개 | 문서 결정은 동기화됐고, 런타임 health 측정 대상 승인 필요 |
| 2026-06-20 | `./gradlew test` | 성공 | 50초, 24 test suites, 138 tests / 0 failures / 0 errors / 0 skipped, 테스트 통과율 100% | 문서 브랜치 기준 baseline 유지 확인 |
| 2026-06-20 | `./gradlew build` | 성공 | 1초, 8 tasks up-to-date, 빌드 성공률 기준선 100% | 앱 코드 변경 브랜치에서 다시 비교 필요 |
| 2026-06-20 | `./gradlew asciidoctor` | 성공 | 4초, 57 snippet groups, HTML 434,854 bytes, 샌드박스 lock 실패 후 권한 상승 재실행 성공 | 새 poll API 구현 시 snippets 증가량 추적 |
| 2026-06-20 | `./gradlew test --warning-mode all` | 성공 | configure phase deprecated 경고 1건(`StartParameter.isConfigurationCacheRequested`), 저장소 직접 사용 검색 0건 | 외부 플러그인/빌드 로직 원인 추적 필요 |
| 2026-06-19 | #61 TDD 실패 확인 | 실패 확인 | 구현 전 `./gradlew test --tests com.faithlog.admin.presentation.AdminManagementControllerTest`가 4 tests / 4 failed로 실패. 서비스 ADMIN 관리 endpoint와 role 변경 PATCH 미구현 확인 | admin application/presentation/port 계층 구현 |
| 2026-06-19 | #61 focused admin tests | 성공 | `AdminManagementServiceTest`, `AdminManagementControllerTest`, `AdminManagementApiRestDocsTest` 성공. 사용자/캠퍼스 검색, 마지막 ADMIN 보호, 직접 멤버 추가/재활성화, REST Docs 계약 검증 | 전체 회귀 테스트로 확대 |
| 2026-06-19 | #61 full regression/build/docs | 성공 | `./gradlew test` 성공(138 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공, REST Docs snippet group 57개 | PM 리뷰 요청 |
| 2026-06-19 | #61 Docker validation | 실패 | `docker compose build app` 2회 모두 Docker Hub metadata 조회 단계에서 `DeadlineExceeded` 실패. `docker ps` 기준 running container 0개 | Docker 네트워크/registry 접근 가능 상태에서 재시도 필요 |
| 2026-06-19 | #33 PM review daily check submitted-week guard | 성공 | 구현 전 대상 테스트 32 tests / 3 failed 확인. 수정 후 대상 테스트 성공, `./gradlew cleanTest test --no-parallel --max-workers=1` 성공(124 tests / 0 failures / 0 errors / 0 skipped), `./gradlew test` 성공, `./gradlew build` 성공, `./gradlew asciidoctor` 성공, REST Docs snippet group 49개 | PM 검증 요청 |
| 2026-06-18 | #36 TDD 실패 확인 | 실패 확인 | Query service 테스트는 missing class 15개로 `compileTestJava` 실패, Controller 테스트는 새 조회 endpoint 미구현으로 HTTP 200 assertion 실패 | 조회 Query Service, Result/Response DTO, Controller endpoint 구현 |
| 2026-06-18 | #36 focused query/controller/docs tests | 성공 | `BillingQueryServiceTest`, `BillingControllerTest`, `BillingApiRestDocsTest` 각각 성공 | 전체 테스트로 확대 |
| 2026-06-18 | #36 full regression/build/docs/docker | 성공 | `./gradlew test` 성공, 77 tests / 0 failures / 0 errors / 0 skipped; `./gradlew build` 성공; `./gradlew asciidoctor` 성공; Docker compose app 내부 health `UP` | PM 리뷰 전 브랜치 push 여부 확인 필요 |
| 2026-06-18 | #36 PM revalidation unpaid filter/docs sync | 성공 | 관리자 캠퍼스 조회 `status=UNPAID` 회귀 테스트 추가. 구현 변경 전 `BillingControllerTest` 성공으로 기존 동작이 계약을 이미 만족함을 확인. 최종 `./gradlew test` 성공, 78 tests / 0 failures / 0 errors / 0 skipped; `./gradlew build` 성공; `./gradlew asciidoctor` 성공 | PM 재검토 후 push/PR 여부 확인 필요 |
| 2026-06-19 | #36 PM re-review admin member summary sort guard | 성공 | 구현 수정 전 `BillingControllerTest` 실패 확인(8 tests / 1 failed). 수정 후 `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공 | PM 재검토 후 push/PR 여부 확인 필요 |
| 2026-06-19 | #36 PM re-review sort direction guard | 성공 | 구현 수정 전 `BillingControllerTest` 실패 확인(8 tests / 1 failed). 수정 후 `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공 | PM 재검토 후 push/PR 여부 확인 필요 |
| 2026-06-19 | #36 PM re-review malformed sort token guard | 성공 | 구현 수정 전 `BillingControllerTest` 실패 확인(8 tests / 1 failed). 수정 후 `./gradlew test --tests 'com.faithlog.billing.*'` 성공, `./gradlew test` 성공(79 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew asciidoctor` 성공 | PM 재검토 후 push/PR 여부 확인 필요 |
| 2026-06-18 | #35 PM review permission regression tests | 성공 | 전역 `ADMIN` 무멤버십 상태 변경, `ELDER`/`CAMPUS_LEADER` 상태 변경, `INACTIVE` 멤버 본인 납부 `403` 테스트 추가 | PR 전 권한 회귀 테스트 유지 |
| 2026-06-18 | #35 PM review focused tests | 성공 | `./gradlew test --tests 'com.faithlog.billing.*'` 성공 | 전체 테스트로 확대 |
| 2026-06-18 | #35 PM review full regression/build | 성공 | `./gradlew test` 성공, 70 tests / 0 failures / 0 errors / 0 skipped; `./gradlew build` 성공 | PR 생성 전 최종 확인 |
| 2026-06-18 | #35 TDD 실패 확인 | 실패 확인 | `./gradlew test --tests 'com.faithlog.billing.*'` 실패: `CompleteChargePaymentCommand`, `ChangeChargeStatusCommand`, `paidAt`, 상태 전이 메서드 부재로 `compileTestJava` 실패 | 청구 상태 전이 도메인/서비스/API 최소 구현 |
| 2026-06-18 | #35 billing 집중 테스트 | 성공 | `./gradlew test --tests 'com.faithlog.billing.*'` 성공, billing 테스트 20개 통과 | 전체 테스트로 확대 |
| 2026-06-18 | #35 full regression | 성공 | `./gradlew test` 성공, 67 tests / 0 failures / 0 errors / 0 skipped | build/asciidoctor 확인 |
| 2026-06-18 | #35 build/docs | 성공 | `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패 후 권한 상승 재실행 성공 | PR 전 동일 검증 유지 |
| 2026-06-18 | `./gradlew test --rerun-tasks` | 성공 | 20초, 5 tasks executed, 21 tests / 0 failures / 0 errors / 0 skipped, 테스트 통과율 100% | `--warning-mode all`로 deprecated feature 원인 식별 필요 |
| 2026-06-18 | #30 TDD 실패 확인 | 실패 확인 | `./gradlew test --tests com.faithlog.campus.application.CampusServiceTest --tests com.faithlog.campus.presentation.CampusControllerTest --tests com.faithlog.campus.presentation.CampusApiRestDocsTest`가 구현 전 `DutyType`, `ChangeCampusRoleCommand`, `AssignCoffeeDutyCommand`, `DutyAssignmentResult`, 서비스 메서드 부재로 `compileTestJava` 실패 | 최소 구현 후 동일 테스트 통과 |
| 2026-06-18 | #30 커피 담당자 동시 지정 실패 확인 | 실패 확인 | `./gradlew test --tests com.faithlog.campus.application.CampusDutyAssignmentConcurrencyTest`가 구현 전 active row 중복으로 `NonUniqueResultException` 실패 | 캠퍼스 row pessimistic lock 적용 후 동일 테스트 통과 |
| 2026-06-18 | #30 집중 테스트 | 성공 | `CampusServiceTest`, `CampusControllerTest`, `CampusApiRestDocsTest` 통과 | 전체 테스트로 확대 |
| 2026-06-18 | #30 `./gradlew test` | 성공 | 47 tests / 0 failures / 0 errors / 0 skipped, 테스트 통과율 100% | Docker 검증 완료 |
| 2026-06-18 | #30 `./gradlew build` | 성공 | bootJar/build 성공, Gradle deprecated feature 경고 유지 | Gradle 9 호환성 경고는 별도 정리 |
| 2026-06-18 | #30 `./gradlew asciidoctor` | 성공 | REST Docs snippet group 22개, admin campus snippets 5개 추가, 샌드박스 Gradle wrapper lock 실패 후 권한 상승 재실행 성공 | 신규 관리자 API마다 REST Docs 테스트 유지 |
| 2026-06-18 | #30 Docker validation | 성공 | `docker compose build app` 성공, `docker compose up -d postgres redis app` 성공, postgres/redis healthy, app started, `curl http://localhost:8080/api/v1/health` 성공 | 컨테이너는 검증 후 실행 상태 유지 |
| 2026-06-18 | #34 TDD 실패 확인 | 실패 확인 | 구현 전 billing 도메인/서비스/리포지토리 부재로 `./gradlew test --tests 'com.faithlog.billing.*'` `compileTestJava` 실패. terminal 상태 보강 전 `markWaived`, `markCanceled` 부재 실패 확인 | 최소 구현 및 terminal 상태 전이 추가 후 동일 범위 통과 |
| 2026-06-18 | #34 billing 집중 테스트 | 성공 | `./gradlew test --tests 'com.faithlog.billing.*'` 성공, billing service/controller/REST Docs 테스트 통과 | 전체 테스트로 확대 |
| 2026-06-18 | #34 `./gradlew test` | 성공 | 56 tests / 0 failures / 0 errors / 0 skipped, 테스트 통과율 100% | `./gradlew build`, `asciidoctor` 추가 확인 |
| 2026-06-18 | #34 `./gradlew build` | 성공 | bootJar/build 성공, Gradle deprecated feature 경고 유지 | Docker 검증 시도 |
| 2026-06-18 | #34 `./gradlew asciidoctor` | 성공 | payment account snippets 3개 묶음, 전체 snippet group 25개, 샌드박스 Gradle wrapper lock 실패 후 권한 상승 재실행 성공 | 신규 billing API 문서 include 유지 |
| 2026-06-18 | #34 Docker validation | 실패 | `docker compose build app`가 Docker daemon 응답 `Docker Desktop is unable to start`로 중단 | Docker Desktop 실행 가능 상태에서 재시도 필요 |
| 2026-06-18 | #34 PM review failure tests | 실패 확인 | `./gradlew test --tests 'com.faithlog.billing.*'` 실패: service ADMIN 계좌 조회 403 계열 실패, HTTP ADMIN 조회 assertion 실패, penalty charge rerun 2건 unique constraint 실패 | 관리자 조회 권한과 UNPAID 청구 create-or-update 구현 |
| 2026-06-18 | #34 PM review focused tests | 성공 | `./gradlew test --tests 'com.faithlog.billing.*'` 성공, billing 테스트 12개 통과 | 전체 테스트로 확대 |
| 2026-06-18 | #34 PM review full regression | 성공 | `./gradlew test` 성공, 59 tests / 0 failures / 0 errors / 0 skipped | build/asciidoctor 확인 |
| 2026-06-18 | #34 PM review build/docs | 성공 | `./gradlew build` 성공, `./gradlew asciidoctor` 성공. asciidoctor 최초 샌드박스 실행은 Gradle wrapper lock 권한 문제로 실패 후 권한 상승 재실행 성공 | Docker Desktop 상태 복구 후 Docker 재검증 필요 |
| 2026-06-18 | #29 `./gradlew test` | 성공 | 31 tests / 0 failures / 0 errors / 0 skipped, 테스트 통과율 100% | 캠퍼스 멤버 관리 이슈에서 권한 테스트 추가 |
| 2026-06-18 | #29 `./gradlew build` | 성공 | bootJar/build 성공, Gradle deprecated feature 경고 유지 | Gradle 9 호환성 경고는 별도 정리 |
| 2026-06-18 | #29 `./gradlew asciidoctor` | 성공 | REST Docs snippet group 16개, 캠퍼스 API snippets 6개 추가 | 신규 API마다 REST Docs 테스트 유지 |
| 2026-06-18 | #29 Docker PostgreSQL validation | 성공 | `docker compose up -d postgres redis app` 이미지 빌드 성공, postgres/redis healthy, 기존 로컬 Docker volume의 `faithlog` role password 재설정 후 app 기동 및 `GET /api/v1/health` 200 확인 | Docker volume을 삭제하지 않고 credential mismatch를 복구하는 절차를 troubleshooting에 유지 |
| 2026-06-18 | `./gradlew asciidoctor --rerun-tasks` | 성공 | 39초, 6 tasks executed, REST Docs 스니펫 10개, HTML 1개 생성 | 새 API 추가 시 문서 스니펫 수와 HTML 생성 여부 비교 |
| 2026-06-18 | `./gradlew build` | 성공 | 5초, 3 tasks executed / 5 tasks up-to-date, 빌드 성공률 기준선 100%, JAR 2개 유지 | 앱 코드 변경이 생기면 오늘 수치와 비교 |
| 2026-06-18 | Branch monitoring audit | 성공 | `origin/develop` 대비 6커밋, 33파일, +1,099/-12, 앱 코드 22파일, 테스트 코드 7파일, DB migration 0개 | 헬스/응답시간 측정 대상 환경 결정 필요 |
| 2026-06-16 | `./gradlew test` | 성공 | 18초, 5개 task up-to-date, 테스트 통과율 100% | 기능별 테스트 수 확대 |
| 2026-06-16 | `./gradlew build` | 성공 | 3초, 8개 task up-to-date, 빌드 성공률 기준선 100% | 배포 전 빌드 체크 유지 |
| 2026-06-16 | GitHub issue policy audit | 성공 | #17~#41 `칸반 상태:` 잔여 0개, 핵심 이슈 7개 정책 반영 | Project Board 조회에는 `read:project` scope 필요 |
| 2026-06-16 | GitHub Project Board audit | 성공 | Project Board 필드 24개 수정, #39 P0 반영, #16 상태 필드 일치 | #23/#24 Domain 결정 필요 |
| 2026-06-16 | Codex Hook validation | 성공 | `./gradlew test` 13초 성공, 금지어 검색 0건, AGENTS/Hook 문서 존재 확인 | 문서-only 작업이라 신규 테스트 없음 |
| 2026-06-16 | Agent rule consolidation validation | 성공 | `AGENT.md` 활성 로딩 참조 0건, `AGENTS.md` 단일 기준화, 단수 `optionId` 검사 명령 결과 Hook 문서 예시 1건만 확인 | Obsidian 최종 경로 결정 필요 |
| 2026-06-16 | PR readiness validation | 성공 | `./gradlew test` 4초 성공, 5개 task up-to-date | 문서-only PR로 기능 테스트 추가 없음 |
| 2026-06-16 | Poll template planning validation | 성공 | 기본 템플릿 1개, 관리자 생성 템플릿 범주 3개로 정책 확정 | #37 구현 시 seed/admin 생성 테스트 필요 |
| 2026-06-16 | Poll template policy PR validation | 성공 | `./gradlew test` 9초 성공, 5개 task up-to-date | #37 구현 시 기본 커피 템플릿 테스트 필요 |
| 2026-06-16 | Poll auto-generation planning validation | 성공 | #37 설정 저장, #24 스케줄러 실행으로 책임 분리 | 자동 생성 요일/시간/마감 필드 테스트 필요 |
| 2026-06-16 | Poll auto-generation policy PR validation | 성공 | `./gradlew test` 3초 성공, 5개 task up-to-date | #24 구현 시 중복 생성 방지 테스트 필요 |
| 2026-06-16 | Coffee poll timing planning validation | 성공 | 커피 담당자 설정 시간 2개 확정 | #37 구현 시 Notion ERD 칼럼명 확인 필요 |
| 2026-06-16 | Coffee poll timing PR validation | 성공 | `./gradlew test` 4초 성공, 5개 task up-to-date | #37/#24 구현 시 자동 생성/마감 시간 테스트 필요 |
| 2026-06-17 | `./gradlew test` | 성공 | 21.29초, 5개 task up-to-date, 테스트 통과율 100% | 기능 테스트 추가 전까지 smoke baseline 유지 |
| 2026-06-17 | `./gradlew build` | 성공 | 7.58초, 8개 task up-to-date, 빌드 성공률 기준선 100% | 앱 코드 변경 시 build baseline 비교 지속 |
| 2026-06-17 | Repo monitoring audit | 성공 | 워크트리 변경 0건, `develop` 대비 4커밋/6파일/1,179라인 문서 변경, 앱 코드 변경 0개 | 헬스/응답시간 측정 대상 환경 결정 필요 |
| 2026-06-17 | `./gradlew test` 재검증 | 성공 | 31초, 5개 task up-to-date, 테스트 통과율 100% | 현재 브랜치는 문서-only 상태라 기능 테스트 확대 전 smoke baseline 유지 |
| 2026-06-17 | `./gradlew build` 재검증 | 성공 | 8초, 8개 task up-to-date, 빌드 성공률 기준선 100% | 앱 코드 변경이 생기면 오늘 수치와 비교 |
| 2026-06-17 | Local repo structure audit 재검증 | 성공 | 실구현 Java 9개, top-level 모듈 7개, CI workflow 2개, Docker Compose 서비스 5개, 마이그레이션 0개 | 헬스 체크 기준 환경 승인 전까지 운영 지표는 보류 |
| 2026-06-17 | Flyway runtime removal validation | 성공 | `./gradlew test` 35초 성공, `./gradlew build` 26초 성공, `runtimeClasspath` Flyway 항목 0개, active migration file 0개 | 최종 도메인 모델 안정화 후 Flyway migration consolidation task로 재도입 |
| 2026-06-17 | #27 auth JWT TDD validation | 성공 | `./gradlew test` 18초 성공, 테스트 파일 1개 -> 4개, 회원가입/로그인/JWT claim/Bearer `/users/me` 검증 추가 | #28 refresh/logout/Redis rotation 구현 시 인증 테스트 확장 |
| 2026-06-17 | #27 PM review security fix validation | 성공 | `./gradlew test` 16초 성공, `./gradlew build` 5초 성공, refresh token Bearer 인증 401 테스트 추가, 비활성 사용자 `/users/me` 401 테스트 추가 | #28 Redis allowlist/blacklist 구현 시 tokenType 검증 유지 |
| 2026-06-17 | #27 Docker validation | 부분 성공 | `docker compose build` 성공, `docker compose up -d postgres redis app` 후 postgres/redis healthy, app은 기존 Postgres volume credential mismatch로 `FATAL: password authentication failed for user "faithlog"` 종료 | Docker volume credential 정리 또는 승인된 DB 초기화 후 앱 헬스체크 재검증 |
| 2026-06-17 | #27 Docker local ddl-auto update validation | 성공 | `docker compose build app` 성공, `docker compose up -d app` 성공, `GET /api/v1/health` 200, Hibernate가 local Docker DB에 `users` 테이블 자동 생성 | 최종 Flyway migration consolidation 전까지 local Docker 개발 검증은 `SPRING_JPA_HIBERNATE_DDL_AUTO=update` 기본값 사용 |
| 2026-06-17 | #27 auth REST Docs validation | 성공 | `./gradlew test --tests '*AuthApiRestDocsTest'` 성공, `./gradlew asciidoctor` 성공, `./gradlew test --rerun-tasks` 11초 성공, `./gradlew build` 5초 성공, 인증 API snippets 6개 묶음과 `build/docs/asciidoc/index.html` 생성 | 새 API/변경 API는 Spring REST Docs 테스트로 상세 계약 문서화 |
| 2026-06-17 | #27 CI test profile override fix | 성공 | PR #47 Backend CI 실패 원인 확인, CI env 재현 실패 확인, 수정 후 `./gradlew test --tests '*AuthServiceTest'` 성공, `./gradlew test --rerun-tasks` 11초 성공, `./gradlew build` 2초 성공 | GitHub Actions 재실행 후 원격 check 통과 확인 |
| 2026-06-22 | #81 Gradle/test deprecation baseline | 성공 | `./gradlew test --warning-mode all` 성공. Problems report 기준 12 warnings: Asciidoctor Gradle plugin 내부 `StartParameter.isConfigurationCacheRequested` 1건, Spring Boot `@MockBean` removal warning 11건 | 안전하게 수정 가능한 테스트 deprecation 11건부터 정리 |
| 2026-06-22 | #81 `@MockBean` deprecation cleanup | 성공 | Spring Boot deprecated `@MockBean` 11건을 `org.springframework.test.context.bean.override.mockito.MockitoBean`으로 교체. 수정 후 `./gradlew test --warning-mode all` 성공, Problems report 1 warning으로 감소 | 남은 1건은 `org.asciidoctor.jvm.convert` 4.0.5 최신 버전 내부 Gradle API 사용으로 #82에서 후속 추적 |
| 2026-06-22 | #81 final validation | 성공 | `./gradlew test` 성공(236 tests / 0 failures / 0 errors / 0 skipped), `./gradlew build` 성공, `./gradlew build --warning-mode all` 성공, `./gradlew asciidoctor` 성공, `git diff --check` 성공 | Docker QA는 앱/빌드 설정 및 런타임 동작 변경이 없어 생략 |

## Resume Bullet Candidates

- Spring Boot 기반 FaithLog 프로젝트의 테스트 기준선을 수립하고, `./gradlew test` 기준 테스트 통과율 100%를 확보.
- `./gradlew build` 기준 빌드 성공 상태를 확보해 배포 전 안정성 검증 기준선을 수립.
- FaithLog 백엔드의 일일 모니터링 기준선을 정리해 7개 도메인 모듈, 74개 Java 소스, Flyway deferred 상태, 100% 테스트/빌드 성공 상태를 지속 추적할 수 있게 함.
- GitHub Issues #17~#41의 기획/구현 기준을 최신 백엔드 정책과 정합화하고, 수동 칸반 상태 잔여 0개로 Project Board 중심 운영 기준을 정리.
- GitHub Project Board의 누락/불일치 필드 24개를 정리해 이슈 본문과 칸반 운영 데이터의 정합성을 개선.
- Codex Hook 개발 규칙을 문서화하고 GitHub Issue #43 및 Project 카드와 연결해 TDD/보안/아키텍처/Obsidian 기록 기준을 표준화.
- Codex Agent 규칙 파일을 2개에서 1개로 단일화하고, 사용자 결정 우선순위와 금지 필드 검사 기준을 문서화해 개발 규칙 위반 가능성을 낮춤.
- 투표 템플릿 정책을 기본 제공 1개와 관리자 생성 3개 범주로 분리해 초기 데이터와 운영 권한 기준을 명확화.
- 투표 자동 생성 책임을 템플릿 설정과 스케줄러 실행으로 분리해 반복 운영 자동화 설계 기준을 명확화.
- 커피 담당자가 자동 생성 시간과 마감 시간을 설정하도록 투표 운영 권한과 반복 생성 정책을 구체화.
- #37/#38 구현 전에 커피 카탈로그 seed 기준, poll result 공개 범위, 3일/7일 visibility window를 정책 문서 3종에 동기화해 계약 드리프트를 줄임.
- 문서 브랜치 기준으로도 `./gradlew test`, `./gradlew build`, `./gradlew asciidoctor`를 재검증해 138개 테스트 100% 통과와 REST Docs 57개 스니펫 기준선을 유지.
- `origin/develop` 최근 4개 커밋 기준으로 FCM 토큰 등록/알림 로그, Redis 중복 방지/락, 배치 스케줄러, 조별 기도제목 보드를 149개 파일·8,775 insertions 규모로 확장해 알림 운영 자동화와 기도 모듈 범위를 넓힘.
- 조별 기도제목 기능에서 멤버별 제출 저장 구조와 동시성 테스트를 추가해 다인 수정 시나리오를 서버 검증 기준으로 관리할 수 있게 함.
- 회원가입/로그인/JWT 인증 흐름을 TDD로 구현하고, Bearer 인증 `/api/v1/users/me`와 JWT 필수 claim 검증을 포함한 테스트 파일을 1개에서 4개로 확대.
- Swagger/springdoc은 API 탐색용으로 유지하면서, 회원가입/로그인/내 정보 조회의 상세 계약을 Spring REST Docs 문서 생성 테스트로 검증하도록 확장.
- Redis allowlist/blacklist 기반 refresh/logout 흐름을 추가하고, 인증 테스트 스위트를 7개·21개 케이스까지 확장해 토큰 회전과 로그아웃 계약을 검증.
- 인증 문서화를 Spring REST Docs 중심으로 유지하면서 스니펫 묶음 10개와 AsciiDoc 계약 문서를 계속 생성 가능한 상태로 검증.
- 캠퍼스 생성/초대코드 가입 API 4개를 TDD로 구현하고, 테스트 스위트를 31개 케이스와 Spring REST Docs 스니펫 16개 묶음까지 확장해 권한/멤버십/초대코드 노출 계약을 검증.

<!-- daily-resume-monitor:start:resume-metrics:2026-06-16 -->
### 2026-06-16 Automated Resume Monitor

- Evidence source: `docs/prompts/daily-resume-monitor.md` read at runtime.
- Commits reviewed: 4
- Changed files reviewed: 6
- Dependency/config changes reviewed: 0
- DB migration changes reviewed: 0
- Local test result: 1 tests, 0 failures/errors. Measurement method: Gradle XML under `build/test-results/test`. Confidence: verified.
- Build artifacts present locally. Measurement method: `build/libs/*.jar`. Confidence: partially verified.

Metric candidates:
- Health check success rate: measure against a user-approved local or deployed URL with repeated requests.
- API response time: measure with a user-approved endpoint and command so daily values are comparable.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-16 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-17 -->
### 2026-06-17 Automated Resume Monitor

- Evidence source: `docs/prompts/daily-resume-monitor.md` read at runtime.
- Commits reviewed: 5
- Changed files reviewed: 32
- Dependency/config changes reviewed: 0
- DB migration changes reviewed: 0
- Local test result: 21 tests, 0 failures/errors/skips. Measurement method: Gradle XML under `build/test-results/test`. Confidence: verified.
- Local build result: `./gradlew build` success in 25s with 8 up-to-date tasks. Confidence: verified.
- API contract docs: `./gradlew asciidoctor` success in 3s, 10 snippet directories, `build/docs/asciidoc/index.html` present. Confidence: verified.

Metric candidates:
- Health check success rate: run `docker compose up -d postgres redis app` and repeat `curl /api/v1/health` against one approved runtime.
- API response time: measure `GET /api/v1/health` or another user-approved endpoint with a fixed local or deployed target.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-17 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-22 -->
### 2026-06-22 Automated Resume Monitor

- Evidence source: `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`.
- Current branch new commits since last run (`2026-06-20T21:00:22Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- `origin/develop` ahead of current branch: 7 commits, 226 files changed in tip-to-tip comparison
- Recent `origin/develop` feature activity reviewed explicitly: 4 commits (#67, #68, #69, #70), 149 files changed, 8,775 insertions, 22 deletions
- Local test result: 138 tests, 0 failures, 0 errors, 0 skipped. Measurement method: Gradle XML under `build/test-results/test`. Confidence: verified.
- Local build result: `./gradlew build` success in 1s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: `./gradlew build --warning-mode all` success with configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- API contract docs artifact: `build/docs/asciidoc/index.html` present at 434,854 bytes. Confidence: verified from local artifact.
- Problems report artifact: `build/reports/problems/problems-report.html` present at 129,871 bytes. Confidence: verified from local artifact.

Metric candidates:
- Latest integration test pass rate: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test`.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-22 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-23 -->
### 2026-06-23 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last run (`2026-06-21T21:01:06Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 236 insertions, 8 deletions
- `origin/develop` new commits since last run: 9
- `origin/develop` ahead of current branch: 16 commits
- Latest integration delta vs current branch: 261 files total, including 201 app files, 29 test files, 14 config/dependency files, 1 DB migration file
- Recent `origin/develop` activity reviewed explicitly: #87 Flyway/Supabase deploy setup, #85 QA Docker Compose isolation, #83 test deprecation cleanup, #80 poll N+1 improvement, #78 role-change token invalidation
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Local test result: 138 tests, 0 failures, 0 errors, 0 skipped. Measurement method: Gradle XML under `build/test-results/test`. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 8s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present at 129,871 bytes. Confidence: verified from local artifact.

Metric candidates:
- Latest integration test pass rate: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build`.
- Flyway/deploy validation on latest integration branch: run focused deploy tests only after the comparison baseline is approved.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-23 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-24 -->
### 2026-06-24 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window: 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 319 insertions, 8 deletions
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 52 commits
- Recent `origin/develop` activity reviewed explicitly: #90 performance/coverage baseline, #25 deploy/CD sync, #25 Cloud Build trigger/CD cleanup, #25 poll status date-dependency cleanup
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 422 Java sources, 55 test Java sources, 1 DB migration, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 3s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 2s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present at 129,870 bytes. Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` present at 10,574 bytes. Confidence: verified from local artifact.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts from #90.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-24 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-26 -->
### 2026-06-26 Automated Resume Monitor

- Evidence source: repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-06-24T21:01:50.868Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 428 insertions, 8 deletions
- `origin/develop` new commits since last review window: 0
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 53 commits
- Recent `origin/develop` activity reviewed explicitly: #95 Cloud Run performance baseline, #90 performance/coverage baseline, #87 Flyway/Supabase deploy setup, #85 QA Docker Compose isolation
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 422 Java sources, 55 test Java sources, 1 DB migration, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 31s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 29s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present at 129,871 bytes. Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` present at 10,574 bytes. Confidence: verified from local artifact.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build --warning-mode all`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts from #90.
- Latest integration deploy/migration smoke: on approved `develop`, run focused deploy tests for Flyway contract and role-token invalidation paths.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-26 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-28 -->
### 2026-06-28 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-06-26T21:01:17.078Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 628 insertions, 8 deletions
- `origin/develop` new commits since last review window: 0
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 53 commits
- Recent `origin/develop` activity reviewed explicitly: #95 Cloud Run performance baseline, #90 performance/coverage baseline, #63 service-admin management implementation, #25 deploy/CD sync
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 422 Java sources, 55 test Java sources, 1 DB migration, 2 GitHub Actions workflows, 3 `performance/k6` files
- Local test result: `./gradlew test` success in 6s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 2s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-06-28 06:02:58 +0900`. Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` and XML suite outputs remain present after today's rerun. Confidence: verified.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build --warning-mode all`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts from #90.
- Latest integration security regression: on approved `develop`, run `./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest` to verify the token invalidation contract added upstream.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-28 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-06-29 -->
### 2026-06-29 Automated Resume Monitor

- Evidence source: repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-06-27T21:01:08.057Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 719 insertions, 8 deletions
- `origin/develop` new commits since last review window: 0
- `origin/develop` ahead of current branch after `git fetch`: 53 commits
- Recent `origin/develop` activity reviewed explicitly: #95 Cloud Run performance baseline, #90 performance/coverage baseline, #63 service-admin management implementation, #25 deploy/CD sync
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 422 Java sources, 55 test Java sources, 1 DB migration, 2 GitHub Actions workflows, 3 `performance/k6` files
- Local test result: `./gradlew test` success in 11s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 11s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-06-29 06:01:58 +0900`. Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` and XML suite outputs remain present after today's rerun. Confidence: verified.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build --warning-mode all`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts from #90.
- Latest integration security regression: on approved `develop`, run `./gradlew test --tests com.faithlog.global.security.RoleTokenInvalidationIntegrationTest` to verify the token invalidation contract added upstream.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-06-29 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-07-02 -->
### 2026-07-02 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-06-30T21:01:49.186Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 969 insertions, 8 deletions, plus untracked root file `0`
- `origin/develop` new commits since last review window: 7 (`bc521bb`, `4c5a21a`, `61571d4`, `863877a`, `8f36f9d`, `b6d0a61`, `76b669f`)
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 74 commits
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 430 Java sources, 55 test Java sources, 4 DB migrations, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 7s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 2s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`) and stacktrace still points to `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` -> `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`. Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-07-02 06:03:40 +0900` (129,871 bytes). Confidence: verified from local artifact.
- Test report artifact: XML suite outputs remain at 24 files / 138 tests from the latest generated local report set; the current rerun completed `UP-TO-DATE`, so today did not regenerate those files. Confidence: verified.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build --warning-mode all`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts after the new billing regression tests and migration files.
- Latest integration billing/poll regression: on approved `develop`, run `./gradlew test --tests com.faithlog.billing.presentation.BillingControllerTest --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.poll.application.PollServiceTest`.
- Latest integration Flyway regression: on approved `develop`, run `./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest` so the monitor can measure migration pass/fail against the now-observed `V1`~`V4` set.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-07-02 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-07-03 -->
### 2026-07-03 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-07-01T21:00:38.611Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes: 4 docs files, 1073 insertions, 8 deletions, plus untracked root file `0`
- `origin/develop` new commits since last review window: 5 (`afeb47e`, `a88def5`, `ade0d87`, `65dcdb8`, `f680dc6`)
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 80 commits
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test sources, 1 test resource, 0 migration files
- Latest integration tree snapshot reviewed from Git: 430 Java sources, 56 test Java sources, 4 DB migrations, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 6s with 5 up-to-date tasks; latest local Gradle XML remains 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 4s with 8 up-to-date tasks; `./gradlew build --warning-mode all --stacktrace` also succeeded in 2s. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`) and stacktrace still points to `org.asciidoctor.gradle.base.AsciidoctorBasePlugin` -> `org.ysb33r.grolifant.loadable.v8.DefaultProjectTools.defaultVersionProvider`. Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-07-03 06:04:08 +0900` (129,871 bytes). Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` remains present; XML suite outputs remain at 24 files / 138 tests from the latest generated local report set. Confidence: verified.

Metric candidates:
- Latest integration pass rate and build status: switch to `develop` only after the user approves the comparison baseline, then run `./gradlew test && ./gradlew build --warning-mode all`.
- Latest integration coverage baseline: on approved `develop`, run `./gradlew test jacocoTestReport` to confirm HTML/XML coverage artifacts after the billing regression additions.
- Latest integration billing regression: on approved `develop`, run `./gradlew test --tests com.faithlog.billing.application.BillingServiceTest --tests com.faithlog.billing.application.BillingQueryServiceTest --tests com.faithlog.billing.presentation.BillingControllerTest`.
- Latest integration Flyway regression: on approved `develop`, run `./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest` so the monitor can measure migration pass/fail against the still-observed 4-file migration set.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-07-03 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-07-06 -->
### 2026-07-06 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, Obsidian `Projects/FaithLog/resume-metrics.md`, fetched Git metadata, local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since the latest recorded report (`2026-07-03`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree uncommitted changes before today's monitor write: 4 docs files, 1332 insertions, 8 deletions, plus untracked root file `0` (empty file, 0 bytes)
- `origin/develop` new commits since the latest recorded report (`2026-07-03`): 1 (`0abafe8`)
- `origin/develop` ahead of current branch after `git fetch --all --prune`: 81 commits
- Recent `origin/develop` activity reviewed explicitly: #128 FCM 토큰 upsert 무결성 보강, #125 계좌 활성 전환/정산 API 계약 보강
- Upstream delta since `f680dc6`: 16 files changed, 339 insertions, 28 deletions; 7 main Java files, 5 test Java files, 1 DB migration, 3 docs files
- Local codebase snapshot on checked-out branch: 231 Java sources, 28 test Java sources, 0 DB migrations, 2 GitHub Actions workflows
- Latest integration tree snapshot reviewed from Git: 430 Java sources, 56 test Java sources, 5 DB migrations, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 1s with 5 up-to-date tasks; latest Gradle XML suite outputs remain 24 files / 138 tests / 0 failures / 0 errors / 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 1s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`). Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-07-06 06:01:20 +0900` (129,871 bytes). Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` remains present at 10,574 bytes; current rerun completed `UP-TO-DATE`, so the HTML report timestamp remains `2026-06-20 06:03:15 +0900` while XML suite outputs still verify 138 tests. Confidence: verified.
- Health endpoint signal: `SecurityConfig` still permits `GET /api/v1/health`, but no runtime health or latency measurement was added because the approved measurement target is still pending.

Resume-ready observations:
- Current checked-out branch still has no new product/app code beyond docs, but the local verification baseline remains stable at 138 tests passing and build success with 1 known Gradle deprecation warning.
- `origin/develop` added one new integrity fix commit after the previous recorded report: `0abafe8` introduced FCM active-token uniqueness hardening, `V5__fix_fcm_token_active_uniqueness.sql`, and notification test updates.
- The latest upstream fix set since `2026-07-03` remains resume-relevant only as upstream-documented work until the user approves treating `origin/develop` as the resume citation source or the branch is synced.

Testing candidates:
- Latest integration coverage baseline: on approved `origin/develop`, run `./gradlew test jacocoTestReport` to measure HTML/XML coverage after billing and FCM regression additions.
- Latest integration Flyway regression: on approved `origin/develop`, run `./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest` to measure pass/fail against the now-observed `V1`~`V5` migration set.
- Latest integration notification regression: on approved `origin/develop`, run `./gradlew test --tests com.faithlog.notification.application.FcmTokenServiceTest --tests com.faithlog.notification.presentation.FcmTokenControllerTest --tests com.faithlog.notification.presentation.NotificationApiRestDocsTest`.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-07-06 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-07-07 -->
### 2026-07-07 Automated Resume Monitor

- Evidence source: local Git metadata, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, and local Gradle outputs.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs local `origin/develop`, plus branch divergence counts.
- Current branch new commits since the latest recorded report (`2026-07-06`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree status before today's monitor write: 4 modified docs files (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`) plus untracked root file `0`
- Local `origin/develop` new commits since the latest recorded report (`2026-07-06`): 1 (`b498356`)
- Branch divergence from local `origin/develop`: current branch ahead 4 commits, behind 82 commits
- Recent local `origin/develop` activity reviewed explicitly: #132 회원 탈퇴와 계정 소프트 삭제 구현
- Upstream delta since `0abafe8`: 20 files changed, 632 insertions, 8 deletions; 11 main Java files, 4 test Java files, 1 DB migration, 4 docs/docsite files
- Local codebase snapshot on checked-out branch: 231 Java sources, 28 test Java sources, 0 DB migrations, 2 GitHub Actions workflows
- Local `origin/develop` tree snapshot reviewed from Git: 435 Java sources, 57 test Java sources, 6 DB migrations, 2 GitHub Actions workflows
- Local test result: `./gradlew test` success in 7.8s wall-clock; Gradle XML suite outputs verify 24 files, 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all` success in 2.7s wall-clock with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure-phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`) still appears during `build`. Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-07-07 06:02:41 +0900` (129,870 bytes). Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` remains present at 10,574 bytes; current reruns completed `UP-TO-DATE`, so HTML timestamp remains `2026-06-20 06:03:15 +0900` while XML suites still verify 138 passing tests. Confidence: verified.

Resume-ready observations:
- The checked-out branch still contributes docs-only committed work, while the local verification baseline remained stable today at 138 passing tests plus one successful Gradle build.
- Local `origin/develop` advanced by one observed commit after the previous report: `b498356` added account soft-delete code paths, one Flyway migration (`V6__add_user_deleted_at.sql`), and four user/auth regression test files.
- Because the checked-out branch is still 82 commits behind local `origin/develop`, the #132 implementation evidence remains upstream-observed only and is not promoted as current-branch verified delivery.

Testing candidates:
- Latest integration account-deletion regression: on approved `origin/develop`, run `./gradlew test --tests com.faithlog.user.presentation.UserDeletionControllerTest --tests com.faithlog.user.presentation.AuthApiRestDocsTest`.
- Latest integration Flyway regression: on approved `origin/develop`, run `./gradlew test --tests com.faithlog.deploy.PostgresFlywayMigrationTest` to measure pass/fail against the now-observed `V1`~`V6` migration set.
- Latest integration coverage baseline: on approved `origin/develop`, run `./gradlew test jacocoTestReport` to measure HTML/XML coverage after the new deletion and migration changes.
- Daily runtime health and response time: keep pending until the user approves one target runtime for repeated `curl /api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-07-07 -->

<!-- daily-resume-monitor:start:resume-metrics:2026-07-11 -->
### 2026-07-11 Automated Resume Monitor

- Evidence source: Vault `AGENTS.md`, repo `AGENTS.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`, fetched Git metadata, local Gradle outputs, local Docker CLI output.
- Branch baseline reviewed: checked-out `docs/37-poll-template-planning-sync` unique diff vs fetched `origin/develop`, plus integration-branch divergence audit.
- Current branch new commits since last review window (`2026-07-09T21:01:14.351Z`): 0
- Current branch unique committed files vs `origin/develop`: 3 docs files, 104 insertions, app/test/config/migration changes 0
- Current worktree status before today's monitor write: 4 modified docs files (`docs/backend-implementation-policy.md`, `docs/codex/FAITHLOG_CODEX_HOOK.md`, `docs/decision-log.md`, `docs/resume-metrics.md`) plus untracked root file `0`
- `origin/develop` new non-merge commits since last review window: 39
- `origin/main` new non-merge commits since last review window: 0
- Branch divergence from fetched `origin/develop`: current branch ahead 4 commits, behind 134 commits
- Recent `origin/develop` activity reviewed explicitly: #146 DDD 패키지 구조 재배치, #147 campus/admin 유스케이스 분리, #148~#149 billing command/query 분리, #150 devotion 책임 분리, #151 poll core 책임 분리, #152 poll template/coffee settlement 책임 분리, #165 H2 테스트 격리 보강
- Upstream code movement observed since last review window: 39 non-merge commits; representative large refactor `8314059` alone changed 490 files with 2374 insertions and 1929 deletions
- Local codebase snapshot on checked-out branch: 8 top-level modules, 231 Java sources, 28 test Java sources, 57 REST Docs snippet groups, 2 GitHub Actions workflows, 0 DB migration files
- Local test result: `./gradlew test --warning-mode all --console=plain` success in 19s with 5 up-to-date tasks; Gradle XML suite outputs verify 24 files, 138 tests, 0 failures, 0 errors, 0 skipped. Confidence: verified.
- Local build result: `./gradlew build --warning-mode all --console=plain` success in 16s with 8 up-to-date tasks. Confidence: verified.
- Warning signal: configure-phase deprecation 1건 (`StartParameter.isConfigurationCacheRequested`) still appears during test/build. Confidence: verified.
- Problems report artifact: `build/reports/problems/problems-report.html` present and updated at `2026-07-11 06:03:50 +0900` (129,871 bytes). Confidence: verified from local artifact.
- Test report artifact: `build/reports/tests/test/index.html` remains present at 10,574 bytes; current reruns completed `UP-TO-DATE`, so HTML timestamp remains `2026-06-20 06:03:15 +0900` while XML suites still verify 138 passing tests. Confidence: verified.
- Dependency / CI / migration change signal on checked-out branch: `build.gradle.kts`, `settings.gradle.kts`, `.github/workflows`, `src/main/resources/db/migration` had no branch-unique committed changes vs `origin/develop`; local checked-out branch still has 0 migration files. Confidence: verified.
- Docker / runtime signal: `docker ps` returned `EOF` instead of a container list, so today's monitor could not confirm 0 running containers or collect health/latency evidence. Confidence: verified from local CLI failure.

Resume-ready observations:
- Current checked-out branch still contributes docs-only committed work, while the local verification baseline remains stable at 138 passing tests, successful Gradle build, 57 REST Docs snippet groups, and one known Gradle deprecation warning.
- Fetched `origin/develop` accumulated substantial upstream-only implementation work after the last review window, culminating in #152 poll template/coffee settlement separation and the earlier #146 large-scale package refactor; however, this remains upstream-observed evidence because the checked-out branch is still 134 commits behind and no approved branch-switch verification ran on `develop`.
- No new checked-out-branch implementation metric is promoted to resume-ready delivery today.

Troubleshooting:
- Problem: Docker runtime availability signal regressed from prior `docker ps` success to an immediate `EOF` failure.
- Root cause: Unverified. The monitor did not infer whether Docker Desktop, daemon socket, or CLI session state caused the failure.
- Fix: No recovery command executed. The monitor stayed read-only and recorded the failure only.
- Before / after metric: 2026-07-09 and 2026-07-10 recorded `docker ps` success with 0 running containers; 2026-07-11 recorded `docker ps` failure before container enumeration.
- Prevention candidate: decide whether the monitor may retry or start Docker runtime automatically when daemon access fails.

Testing candidates:
- Latest integration baseline on approved `develop`: `git switch develop && ./gradlew test && ./gradlew build --warning-mode all`
- Reason: today's verified pass rate and build status still come from the checked-out docs branch, while fetched `origin/develop` is 134 commits ahead.
- Expected metric: current integration-branch test pass rate, build success, and deprecation warning persistence
- Latest integration coverage baseline on approved `develop`: `git switch develop && ./gradlew test jacocoTestReport`
- Reason: upstream refactor wave #146~#152 materially changed application/service package structure and service boundaries, but no current coverage artifact was generated today.
- Expected metric: integration-branch coverage artifact generation success and updated test-count baseline
- Latest integration poll/devotion/billing regression on approved `develop`: `git switch develop && ./gradlew test --tests com.faithlog.poll.service.PollServiceTest --tests com.faithlog.devotion.service.DevotionServiceTest --tests com.faithlog.billing.service.BillingServiceTest`
- Reason: the most recent upstream wave concentrated on poll, devotion, and billing responsibility separation.
- Expected metric: domain-focused regression pass/fail across the most heavily changed service areas
- Daily runtime health and response time: keep pending until the user approves one target runtime and Docker recovery scope for repeated `/api/v1/health` measurement.
<!-- daily-resume-monitor:end:resume-metrics:2026-07-11 -->
