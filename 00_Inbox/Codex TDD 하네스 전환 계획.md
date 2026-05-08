---
title: "Codex TDD 하네스 전환 계획"
created: "2026-05-08"
updated: "2026-05-09"
type: planning
status: draft
tags: [codex, tdd, hooks, agents, skills, workflow]
source_notes:
  - https://github.com/jha0313/harness_framework
  - https://developers.openai.com/codex/hooks
  - https://developers.openai.com/codex/skills
publish_url:
---

# Codex TDD 하네스 전환 계획

## 작성된 글

- [[2026-05-09_바이브코딩을 그냥 맡기는 게 아니라 하네스로 통제하기]]

## 목표

기존 Claude 중심 작업 흐름을 Codex 중심 작업 흐름으로 옮긴다.

핵심은 단순히 파일 이름을 바꾸는 것이 아니라, Codex가 프로젝트를 읽고, 계획을 세우고, 작은 단위로 구현하고, TDD와 검증 커맨드를 강제하도록 작업 환경을 정리하는 것이다.

## 수업 레포 참고

수업에서 사용한 레포:

```text
https://github.com/jha0313/harness_framework
```

확인일:

```text
2026-05-09
```

이 레포는 Claude 기준의 Harness 프레임워크 예시다. 따라서 그대로 복사하기보다 Codex에 맞게 변환해서 사용한다.

### 원본 레포 구조

GitHub에서 확인한 주요 구조:

```text
harness_framework/
├── .claude/
│   ├── commands/
│   │   ├── harness.md
│   │   └── review.md
│   └── settings.json
├── docs/
│   ├── ADR.md
│   ├── ARCHITECTURE.md
│   ├── PRD.md
│   └── UI_GUIDE.md
├── scripts/
│   ├── execute.py
│   └── test_execute.py
├── .gitignore
└── CLAUDE.md
```

### Codex로 옮길 때의 대응 관계

| 수업 레포 기준 | Codex 기준 |
| --- | --- |
| `.claude/commands/harness.md` | `.agents/skills/harness/SKILL.md` |
| `.claude/commands/review.md` | `.agents/skills/review/SKILL.md` 또는 `AGENTS.md`의 review 규칙 |
| `.claude/settings.json` | `.codex/config.toml`, `.codex/hooks.json` |
| `CLAUDE.md` | `AGENTS.md` |
| `scripts/execute.py` | `scripts/execute.py` 유지하되 `claude -p` 호출부를 Codex 실행 방식에 맞게 수정 |
| `docs/*.md` | `docs/*.md` 유지 |

핵심:

- 수업 레포의 `harness.md`는 Codex에서는 slash command가 아니라 skill로 옮긴다.
- 수업 레포의 `CLAUDE.md`는 Codex에서는 `AGENTS.md`로 옮긴다.
- 수업 레포의 `execute.py`는 좋은 뼈대지만 내부에서 `claude -p`를 호출하므로 Codex용으로 수정해야 한다.
- 수업 레포에는 `UI_GUIDE.md`도 있으므로, 프론트엔드 프로젝트라면 문서 3종에 더해 `docs/UI_GUIDE.md`도 작성하는 것이 좋다.

### 원본 CLAUDE.md에서 가져올 내용

수업 레포의 `CLAUDE.md`는 템플릿 형태다.

포함된 축:

- 프로젝트명
- 기술 스택
- 아키텍처 규칙
- CRITICAL 규칙
- TDD 개발 프로세스
- conventional commits 규칙
- 개발, 빌드, lint, test 명령어

Codex에서는 이 내용을 `AGENTS.md`로 옮긴다.

추가로 강화할 점:

- “테스트를 먼저 작성한다”는 문장만 두지 않고 TDD guard hook으로 강제한다.
- `npm run build`, `npm run lint`, `npm run test`는 pre-commit verification hook에도 넣는다.
- 프로젝트별 명령어가 Gradle, Maven, pnpm, bun 등으로 다르면 `AGENTS.md`와 hook을 함께 수정한다.

### docs 템플릿에서 가져올 내용

수업 레포의 `docs/`에는 4개 문서가 있다.

```text
docs/PRD.md
docs/ARCHITECTURE.md
docs/ADR.md
docs/UI_GUIDE.md
```

`PRD.md`:

- 목표
- 사용자
- 핵심 기능
- MVP 제외 사항
- 디자인 방향

`ARCHITECTURE.md`:

- 디렉토리 구조
- 패턴
- 데이터 흐름
- 상태 관리

`ADR.md`:

- 프로젝트 철학
- ADR-001, ADR-002, ADR-003 형식의 기술 결정 기록
- 결정, 이유, 트레이드오프

`UI_GUIDE.md`:

- 디자인 원칙
- AI 느낌이 강한 UI 안티패턴
- 색상
- 컴포넌트 스타일
- 레이아웃
- 타이포그래피
- 애니메이션
- 아이콘 규칙

정리:

- 백엔드나 CLI 프로젝트라면 `PRD.md`, `ARCHITECTURE.md`, `ADR.md` 3종이면 충분할 수 있다.
- 프론트엔드가 있는 프로젝트라면 `UI_GUIDE.md`까지 포함한다.
- 브라우저 테스트 섹션은 `UI_GUIDE.md`와 연결해서 검증한다.

### harness.md에서 가져올 내용

수업 레포의 `.claude/commands/harness.md`가 하네스의 핵심이다.

주요 흐름:

1. 탐색: `/docs/` 하위 문서를 읽는다.
2. 논의: 구현 전에 필요한 기술 결정을 사용자와 논의한다.
3. Step 설계: 여러 step으로 쪼개고 피드백을 받는다.
4. 파일 생성: `phases/index.json`, `phases/{task-name}/index.json`, `step{N}.md`를 만든다.
5. 실행: `python3 scripts/execute.py {task-name}`로 순차 실행한다.

이 내용은 Codex에서는 `.agents/skills/harness/SKILL.md`로 옮긴다.

Codex용으로 바꿀 문구:

- “Claude 세션” → “Codex 세션”
- “CLAUDE.md” → “AGENTS.md”
- “Claude command” → “Codex skill”
- `/claude/commands` 경로 → `.agents/skills`

### review.md에서 가져올 내용

수업 레포의 `.claude/commands/review.md`는 변경 사항 리뷰용이다.

확인 항목:

- 아키텍처 준수
- 기술 스택 준수
- 테스트 존재
- CRITICAL 규칙 위반 여부
- 빌드 가능 여부

Codex에서는 이 내용을 둘 중 하나로 옮긴다.

1. 간단히 쓸 경우: `AGENTS.md`의 review 체크리스트로 넣는다.
2. 자주 쓸 경우: `.agents/skills/review/SKILL.md`로 만든다.

프론트엔드 프로젝트라면 여기에 브라우저 테스트 결과도 추가한다.

추가 체크 항목:

- desktop/mobile viewport 브라우저 검증을 했는가?
- 콘솔 에러가 없는가?
- 네트워크 실패가 없는가?
- 핵심 사용자 흐름이 실제 브라우저에서 동작하는가?

### execute.py에서 가져올 내용

수업 레포의 `scripts/execute.py`는 phase 안의 step을 순차 실행하는 하네스다.

주요 기능:

- `feat-{phase}` 브랜치 생성 또는 checkout
- `CLAUDE.md`와 `docs/*.md` 내용을 guardrail로 step 프롬프트에 주입
- 완료된 step의 `summary`를 다음 step context로 누적 전달
- 실패 시 최대 3회 재시도
- step output을 `step{N}-output.json`으로 저장
- 코드 커밋과 메타데이터 커밋을 분리
- `started_at`, `completed_at`, `failed_at`, `blocked_at` 기록
- `--push` 옵션으로 실행 후 push

Codex로 옮길 때 수정할 부분:

- `CLAUDE.md` 로딩을 `AGENTS.md` 로딩으로 바꾼다.
- 프롬프트 문구에서 Claude를 Codex로 바꾼다.
- `claude -p --dangerously-skip-permissions --output-format json` 호출부를 Codex CLI 실행 방식에 맞게 바꾼다.
- Codex hook과 충돌하지 않도록 `execute.py`의 커밋 전 검증 흐름을 명확히 한다.
- UI step이면 브라우저 테스트 결과를 step summary 또는 output JSON에 남기도록 확장한다.

### test_execute.py에서 가져올 내용

수업 레포에는 `scripts/test_execute.py`도 있다.

의미:

- `execute.py`를 리팩터링할 때 기존 동작이 유지되는지 검증하기 위한 안전망이다.
- 하네스 자체도 TDD 대상이라는 뜻이다.

Codex용으로 옮길 때도 유지한다.

추천:

```bash
pytest scripts/test_execute.py
```

하네스 자체를 수정할 때는 먼저 `test_execute.py`를 보강하고, 그 다음 `execute.py`를 바꾼다.

## 수업 레포를 Codex용으로 적용하는 순서

1. `harness_framework` 레포 구조를 참고한다.
2. `.claude`와 `CLAUDE.md`는 그대로 쓰지 않고 Codex 구조로 변환한다.
3. `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/ADR.md`, `docs/UI_GUIDE.md` 템플릿을 프로젝트에 맞게 작성한다.
4. `CLAUDE.md` 템플릿 내용을 `AGENTS.md`에 옮긴다.
5. `.claude/commands/harness.md` 내용을 `.agents/skills/harness/SKILL.md`로 옮긴다.
6. `.claude/commands/review.md` 내용을 `AGENTS.md` 또는 `.agents/skills/review/SKILL.md`로 옮긴다.
7. `scripts/execute.py`를 가져온 뒤 Codex 호출 방식으로 수정한다.
8. `scripts/test_execute.py`를 유지하고 하네스 수정 전후에 실행한다.
9. `.codex/config.toml`과 `.codex/hooks.json`을 추가한다.
10. TDD guard hook과 pre-commit verification hook을 추가한다.
11. UI 프로젝트라면 브라우저 테스트 규칙을 `UI_GUIDE.md`, step AC, review skill에 모두 연결한다.

## 수업 레포 기반 최종 목표 구조

Codex용으로 정리한 최종 목표 구조:

```text
project/
├── .codex/
│   ├── config.toml
│   ├── hooks.json
│   └── hooks/
│       ├── tdd-guard.sh
│       └── pre-commit-verify.sh
├── .agents/
│   └── skills/
│       ├── harness/
│       │   └── SKILL.md
│       └── review/
│           └── SKILL.md
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── ADR.md
│   └── UI_GUIDE.md
├── phases/
│   └── index.json
├── scripts/
│   ├── execute.py
│   └── test_execute.py
└── AGENTS.md
```

## 전환해야 할 이름

| 기존 | 변경 |
| --- | --- |
| `.claude/` | `.codex/` |
| `CLAUDE.md` 또는 `claud.md` | `AGENTS.md` |
| `commands/` | `skills/` |
| Claude command | Codex skill |
| `hooks.json` | Codex hooks 설정 |

주의할 점:

- 단순 rename으로 끝내지 않는다.
- Codex 공식 구조에 맞게 `.codex/config.toml`, `.codex/hooks.json`, `.codex/hooks/*.sh`, `.agents/skills/*/SKILL.md`로 재배치한다.
- `CLAUDE.md`에 있던 강제 규칙은 `AGENTS.md`와 hook으로 나눈다.
- md 파일에 적힌 규칙은 명령일 뿐이다. 반드시 강제해야 하는 규칙은 hook으로 옮긴다.

## Codex hooks 설정

Codex hooks는 Codex lifecycle 중 특정 시점에 결정적인 스크립트를 실행하는 장치다.

공식 문서 기준으로 hooks 기능은 `config.toml`에 아래처럼 켠다.

```toml
[features]
codex_hooks = true
```

메모:

- `hooks=true`가 아니라 `codex_hooks = true`다.
- hook 파일은 보통 `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` 중 하나에 둔다.
- repo-local hook을 쓸 때는 Codex가 프로젝트 `.codex/` layer를 trusted로 인식해야 한다.
- hook 명령은 Codex가 어느 하위 디렉토리에서 시작돼도 동작하도록 git root 기준 경로를 쓰는 것이 좋다.

## 사용할 hook

### TDD guard hook

파일 후보:

```text
.codex/hooks/tdd-guard.sh
```

역할:

- 구현 작업 전에 테스트 작성 또는 테스트 계획을 요구한다.
- 테스트 없이 바로 production code만 수정하려는 흐름을 막는다.
- TDD 개발 방식을 Codex에게 “권장”하는 수준이 아니라 “강제”한다.

강제하고 싶은 규칙:

- 새 기능은 실패하는 테스트를 먼저 만든다.
- 버그 수정은 재현 테스트를 먼저 만든다.
- 테스트가 어려운 작업이면 그 이유와 대체 검증 방법을 먼저 기록한다.

### Pre-commit verification hook

파일 후보:

```text
.codex/hooks/pre-commit-verify.sh
```

역할:

- 커밋 전에 lint, build, test를 실행한다.
- 실패하면 커밋 또는 완료 보고를 막는다.
- 프로젝트별 커맨드는 `package.json`, `build.gradle`, `pom.xml` 등을 기준으로 자동 감지하거나 `AGENTS.md`에 명시한다.

기본 검증 후보:

```bash
npm run lint
npm run build
npm test
```

Spring/Gradle 프로젝트라면:

```bash
./gradlew test
./gradlew build
```

## hook을 쓰는 이유

hook은 “반드시 지켜야 하는 규칙”을 강제하기 위해 사용한다.

문서에 적힌 명령은 Codex가 참고할 수는 있지만, 반드시 실행된다는 보장은 없다. 반면 hook은 특정 이벤트에서 실제 스크립트를 실행하므로 TDD, lint, build, test 같은 품질 기준을 작업 흐름에 끼워 넣을 수 있다.

단, hooks는 보안 경계가 아니라 guardrail로 이해해야 한다. 공식 문서에서도 `PreToolUse`는 Bash, `apply_patch`, MCP tool 일부를 가로챌 수 있지만 모든 우회 경로를 완전히 막는 것은 아니라고 설명한다. 따라서 중요한 규칙은 hook과 `AGENTS.md`에 함께 둔다.

## 기획 중심 작업 흐름

강조점:

- 코딩보다 기획이 먼저다.
- 시작 전에 `/clear`로 컨텍스트를 비운다.
- plan mode에서 아이디어, 사용할 기술, API, 아키텍처 후보를 먼저 넣는다.
- 한 번의 플랜으로 바로 구현하지 않는다.
- 플랜을 여러 번 돌리며 더 상세하게 요구한다.
- 강사님은 보통 5번 이상 플랜을 반복한다고 정리한다.
- 플랜이 괜찮아지면 아키텍처와 기술 질문으로 들어간다.

추천 흐름:

1. `/clear`로 컨텍스트 정리
2. plan mode 진입
3. 프로젝트 아이디어와 사용하고 싶은 기술 입력
4. 1차 플랜 작성
5. 더 작고 구체적인 플랜 요구
6. 아키텍처, 스택, API, 데이터 흐름 질문
7. 문서 3종 작성
8. `AGENTS.md` 업데이트 지시
9. 세션 저장 또는 fork
10. skill을 사용해 phase와 step으로 작업 분리

## 프로젝트 문서 3종

위치:

```text
docs/
```

### PRD.md

포함할 내용:

- 프로젝트명
- 목표
- 사용자
- 핵심 기능
- MVP 범위
- 제외할 상황

목적:

- 무엇을 만들지 명확히 한다.
- Codex가 구현 중 범위를 벗어나지 않게 한다.

### ARCHITECTURE.md

포함할 내용:

- 기술 스택
- 디렉토리 구조
- 주요 모듈
- 데이터 흐름
- API 구조
- 테스트 전략
- 배포 방식

목적:

- 기술적으로 어떻게 만들지 정리한다.
- 각 step이 같은 구조를 따르도록 기준을 만든다.

### ADR.md

형식:

```md
# ADR-001: {결정 사항}

## 결정

{뭘 결정했는지}

## 이유

{왜 선택했는지}

## 트레이드오프

{뭘 포기했는지}
```

목적:

- 철학과 기술 결정 이유를 남긴다.
- 나중에 왜 이 선택을 했는지 설명할 수 있게 한다.

## AGENTS.md 업데이트

문서 3종을 만든 뒤 Codex에게 `AGENTS.md` 업데이트를 지시한다.

들어가야 할 내용:

- 프로젝트 목적
- 중요한 폴더
- 사용 기술
- TDD 원칙
- lint/build/test 커맨드
- 금지 사항
- 커밋 전 검증 규칙
- docs 문서를 먼저 읽으라는 규칙
- phase/step 기반 작업 방식

## harness skill 만들기

위치:

```text
.agents/skills/harness/SKILL.md
```

Codex 공식 문서 기준으로 skill은 `SKILL.md`를 가진 디렉토리이며, repository scope에서는 `.agents/skills` 아래에 둘 수 있다.

사용 방식:

```text
$harness
```

목적:

- 작업을 최대한 작게 나누게 한다.
- phase와 step 파일을 만들게 한다.
- 각 step이 독립된 Codex 세션에서 실행돼도 맥락을 잃지 않도록 만든다.

## harness workflow

### A. 탐색

Codex는 먼저 `/docs/` 하위 문서를 읽는다.

읽어야 할 문서:

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR.md`
- `AGENTS.md`

필요하면 Explore 에이전트를 병렬로 사용한다.

### B. 논의

구현을 위해 구체화하거나 기술적으로 결정해야 할 사항이 있으면 사용자에게 질문한다.

예시:

- API는 REST로 갈지 GraphQL로 갈지
- DB는 PostgreSQL로 갈지 MySQL로 갈지
- 인증은 세션 기반인지 JWT 기반인지
- 테스트는 단위 테스트 중심인지 통합 테스트 중심인지

### C. Step 설계

사용자가 구현 계획 작성을 지시하면 여러 step으로 쪼갠 초안을 만든다.

설계 원칙:

- Scope 최소화: 하나의 step은 하나의 레이어 또는 모듈만 다룬다.
- 자기완결성: 각 step 파일은 독립된 Codex 세션에서 실행 가능해야 한다.
- 사전 준비 강제: 읽어야 할 문서와 이전 step 산출물 경로를 명시한다.
- 시그니처 수준 지시: 함수, 클래스, API 인터페이스만 제시하고 내부 구현은 Codex에게 맡긴다.
- 핵심 규칙 명시: 멱등성, 보안, 데이터 무결성 같은 규칙은 반드시 적는다.
- AC는 실행 가능한 커맨드로 쓴다.
- 주의사항은 “X를 하지 마라. 이유: Y” 형식으로 쓴다.
- step name은 kebab-case slug를 사용한다.

### D. 파일 생성

사용자가 승인하면 아래 파일을 생성한다.

```text
phases/index.json
phases/{task-name}/index.json
phases/{task-name}/step0.md
phases/{task-name}/step1.md
phases/{task-name}/step2.md
```

### E. 실행

실행 명령:

```bash
python3 scripts/execute.py {task-name}
python3 scripts/execute.py {task-name} --push
```

`execute.py`가 맡을 일:

- `feat-{task-name}` 브랜치 생성 및 checkout
- `AGENTS.md`와 `docs/*.md`를 매 step 프롬프트에 포함
- 완료된 step의 summary를 다음 step에 전달
- 실패 시 최대 3회 재시도
- 코드 변경 커밋과 메타데이터 커밋 분리
- `started_at`, `completed_at`, `failed_at`, `blocked_at` 기록

## phases 파일 구조

### top-level index

```json
{
  "phases": [
    {
      "dir": "0-mvp",
      "status": "pending"
    }
  ]
}
```

상태:

- `pending`
- `completed`
- `error`
- `blocked`

타임스탬프는 생성 시 넣지 않고 `execute.py`가 상태 변경 시 자동 기록한다.

### task index

```json
{
  "project": "<프로젝트명>",
  "phase": "<task-name>",
  "steps": [
    { "step": 0, "name": "project-setup", "status": "pending" },
    { "step": 1, "name": "core-types", "status": "pending" },
    { "step": 2, "name": "api-layer", "status": "pending" }
  ]
}
```

상태 전이:

| 전이 | 기록 필드 | 기록 주체 |
| --- | --- | --- |
| completed | `completed_at`, `summary` | Codex 세션, `execute.py` |
| error | `failed_at`, `error_message` | Codex 세션, `execute.py` |
| blocked | `blocked_at`, `blocked_reason` | Codex 세션, `execute.py` |

`summary`는 다음 step에 전달되므로, 생성된 파일과 핵심 결정이 한 줄로 들어가야 한다.

## step 파일 템플릿

````md
# Step {N}: {이름}

## 읽어야 할 파일

먼저 아래 파일들을 읽고 프로젝트의 아키텍처와 설계 의도를 파악하라:

- `/docs/ARCHITECTURE.md`
- `/docs/ADR.md`
- {이전 step에서 생성/수정된 파일 경로}

이전 step에서 만들어진 코드를 꼼꼼히 읽고, 설계 의도를 이해한 뒤 작업하라.

## 작업

{구체적인 구현 지시. 파일 경로, 클래스/함수 시그니처, 로직 설명을 포함한다.
코드 스니펫은 인터페이스/시그니처 수준만 제시하고 구현체는 에이전트에게 맡긴다.
단, 설계 의도에서 벗어나면 안 되는 핵심 규칙은 명확히 적는다.}

## Acceptance Criteria

```bash
npm run build
npm test
```

## 검증 절차

위 AC 커맨드를 실행한다.

아키텍처 체크리스트를 확인한다:

- `ARCHITECTURE.md` 디렉토리 구조를 따르는가?
- `ADR.md` 기술 스택을 벗어나지 않았는가?
- `AGENTS.md` CRITICAL 규칙을 위반하지 않았는가?

결과에 따라 `phases/{task-name}/index.json`의 해당 step을 업데이트한다:

- 성공: `"status": "completed"`, `"summary": "산출물 한 줄 요약"`
- 수정 3회 시도 후에도 실패: `"status": "error"`, `"error_message": "구체적 에러 내용"`
- 사용자 개입 필요: `"status": "blocked"`, `"blocked_reason": "구체적 사유"` 후 즉시 중단

## 금지사항

- 기존 테스트를 깨뜨리지 마라. 이유: 이전 기능 회귀를 막아야 한다.
- 이 step 범위를 벗어난 모듈을 수정하지 마라. 이유: 실패 원인을 추적하기 어려워진다.
````

## 세션 백업 흐름

기획이 끝나면 `/fork`로 세션을 저장해 둔다.

이유:

- 개발이 틀어졌을 때 기획 단계로 돌아오기 위한 보험이다.
- 잘 된 계획 상태를 기준점으로 남길 수 있다.

이후 Codex CLI에서:

```bash
codex resume
```

저장된 세션을 확인하고, `/rename`으로 기획 단계 세션임을 알아보기 쉽게 이름을 바꾼다.

## 자주 쓰는 Codex 명령 메모

- `/clear`: 컨텍스트 비우기
- `/fork`: 현재 세션을 저장해 보험용 분기 만들기
- `codex resume`: 저장된 세션 확인 및 재개
- `/rename`: 세션 이름 변경
- `$harness`: 작업을 phase와 step으로 작게 나누는 skill 사용
- `/side`: 메인 컨텍스트가 아닌 서브 컨텍스트에서 질문
- `/goal`: 마이그레이션처럼 긴 목표를 추적할 때 사용
- `/copy`: 출력 메시지 복사
- `Ctrl + R`: 내가 작성한 프롬프트 검색

메모:

- `/goal`을 쓸 때는 먼저 Codex에게 목표 설정 명령을 어떻게 구성할지 물어보는 것이 좋다.
- `/side`는 메인 스레드 컨텍스트를 오염시키지 않고 확인 질문을 던질 때 사용한다.

## 수업 메모

- 1분마다 stress 업데이트를 해달라는 말은 진행 상황을 보고하라는 뜻으로 이해한다.
- stuck 된 것 같으면 다시 실행한다.
- 하네스 공부는 필수다.
- AI 모델은 점점 상향 평준화될 가능성이 높다.
- Codex CLI는 오픈소스이므로 직접 구조를 공부하는 것이 좋다.

## 실행 계획

### 1단계: 현재 Claude 설정 조사

확인할 것:

- `.claude/` 존재 여부
- `CLAUDE.md`, `claud.md` 존재 여부
- `commands/` 존재 여부
- 기존 `hooks.json` 존재 여부
- 기존 slash command 내용

산출물:

- 전환 대상 목록
- 보존해야 할 규칙 목록

### 2단계: Codex 구조로 rename

작업:

- `.claude/`를 `.codex/`로 변경
- `CLAUDE.md` 또는 `claud.md`를 `AGENTS.md`로 변경
- `commands/` 내용을 `.agents/skills/` 아래 skill로 전환

검증:

```bash
find . -maxdepth 3 -type f | sort
```

### 3단계: 문서 3종 작성

작업:

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR.md`
- 프론트엔드가 있으면 `docs/UI_GUIDE.md`도 작성

검증:

```bash
ls docs
```

### 4단계: AGENTS.md 업데이트

작업:

- docs를 먼저 읽으라는 규칙 추가
- TDD 원칙 추가
- 커밋 전 검증 커맨드 추가
- phase/step 작업 방식 추가

검증:

```bash
sed -n '1,220p' AGENTS.md
```

### 5단계: hooks 설정

작업:

- `.codex/config.toml`에 `[features] codex_hooks = true` 확인 또는 추가
- `.codex/hooks.json` 생성
- `.codex/hooks/tdd-guard.sh` 생성
- `.codex/hooks/pre-commit-verify.sh` 생성
- 실행 권한 부여

검증:

```bash
test -f .codex/config.toml
test -f .codex/hooks.json
test -x .codex/hooks/tdd-guard.sh
test -x .codex/hooks/pre-commit-verify.sh
```

### 6단계: harness skill 작성

작업:

- `.agents/skills/harness/SKILL.md` 생성
- 탐색, 논의, step 설계, 파일 생성, 실행 규칙 포함

검증:

```bash
test -f .agents/skills/harness/SKILL.md
```

### 7단계: execute.py 하네스 작성

작업:

- `scripts/execute.py` 생성
- 수업 레포의 `scripts/execute.py`를 참고하되 Codex용으로 수정
- `phases/index.json`과 task index 읽기
- step 순차 실행
- 실패 시 3회 재시도
- 상태와 타임스탬프 기록
- `--push` 옵션 지원
- `scripts/test_execute.py`로 execute.py 리팩터링 안전망 유지

검증:

```bash
python3 scripts/execute.py --help
pytest scripts/test_execute.py
```

### 8단계: 샘플 phase로 검증

작업:

- 작은 샘플 task 생성
- `$harness`로 phase/step 설계
- `execute.py`로 실행
- hook이 실제로 막아야 할 상황을 막는지 확인

검증:

```bash
python3 scripts/execute.py 0-mvp
```

### 9단계: 브라우저 테스트 추가

목적:

- lint, build, test로 잡히지 않는 실제 화면 문제를 확인한다.
- 버튼, 폼, 라우팅, 반응형 레이아웃, 콘솔 에러, 네트워크 에러를 직접 확인한다.
- 사용자가 실제로 쓰는 핵심 흐름이 깨지지 않았는지 증거를 남긴다.

브라우저 테스트는 자동 테스트를 대체하지 않는다. 먼저 unit/integration test를 통과시키고, 그 다음 실제 브라우저에서 사용자 흐름을 검증한다.

#### 기본 흐름

1. 개발 서버를 실행한다.
2. 브라우저로 로컬 URL에 접속한다.
3. 핵심 사용자 시나리오를 직접 수행한다.
4. 데스크톱과 모바일 viewport를 모두 확인한다.
5. 콘솔 에러와 네트워크 실패를 확인한다.
6. 스크린샷 또는 테스트 로그를 남긴다.
7. 발견한 문제를 수정하고 같은 흐름을 다시 검증한다.

예시:

```bash
npm run dev
```

접속:

```text
http://localhost:3000
```

프로젝트에 따라 포트가 다르면 실제 dev server 출력에 나온 URL을 사용한다.

#### Codex에서 브라우저 테스트를 시키는 프롬프트

```text
브라우저로 http://localhost:3000에 접속해서 핵심 사용자 흐름을 테스트해줘.

확인할 것:
- 첫 화면이 정상 렌더링되는가
- 주요 버튼이 클릭되는가
- 폼 입력과 제출이 동작하는가
- 페이지 이동 또는 라우팅이 정상인가
- 모바일 viewport에서도 레이아웃이 깨지지 않는가
- 콘솔 에러가 없는가
- 네트워크 요청 실패가 없는가

문제를 발견하면 재현 절차, 기대 결과, 실제 결과, 스크린샷 여부를 정리하고 수정해줘.
수정 후 같은 브라우저 테스트를 다시 실행해줘.
```

#### 테스트해야 할 화면

최소 확인 대상:

- 첫 진입 화면
- 로그인 또는 인증 화면이 있다면 로그인 흐름
- 핵심 CRUD 화면
- 상세 페이지
- 설정 또는 프로필 페이지
- 에러 상태
- 빈 상태
- 로딩 상태

반응형 확인 대상:

- desktop: 1440px 또는 1280px
- tablet: 768px
- mobile: 390px 또는 375px

#### 브라우저 QA 체크리스트

- 화면이 blank page로 뜨지 않는가?
- 첫 렌더링 시 hydration error가 없는가?
- 텍스트가 버튼이나 카드 밖으로 삐져나오지 않는가?
- UI 요소가 서로 겹치지 않는가?
- 클릭 가능한 요소에 hover/focus 상태가 있는가?
- 주요 버튼이 실제 동작하는가?
- 폼 validation 메시지가 이해 가능한가?
- 실패 상황에서 사용자가 다음 행동을 알 수 있는가?
- 모바일에서 스크롤, 탭, 입력이 자연스러운가?
- 콘솔에 error 또는 warning이 반복 출력되지 않는가?
- API 요청 실패가 화면에 조용히 묻히지 않는가?

#### step Acceptance Criteria에 넣는 예시

프론트엔드 작업 step에는 브라우저 검증을 AC에 포함한다.

````md
## Acceptance Criteria

```bash
npm run lint
npm run build
npm test
```

브라우저 검증:

- `npm run dev`로 개발 서버를 실행한다.
- `http://localhost:3000`에 접속한다.
- 핵심 사용자 흐름을 desktop과 mobile viewport에서 각각 테스트한다.
- 콘솔 에러와 네트워크 실패가 없는지 확인한다.
- 문제가 있으면 수정 후 같은 흐름을 다시 테스트한다.
````

#### 브라우저 테스트 결과 기록 형식

```md
## Browser QA Result

- URL: http://localhost:3000
- Viewports: desktop 1440px, mobile 390px
- Tested flows:
  - 첫 화면 렌더링
  - 로그인
  - 항목 생성
  - 상세 페이지 이동
- Console errors: 없음
- Network failures: 없음
- Issues found:
  - 없음
- Screenshots:
  - desktop-home.png
  - mobile-home.png
```

#### 발견한 버그 기록 형식

```md
## Bug

- 제목: 모바일에서 저장 버튼 텍스트가 잘림
- 재현 절차:
  1. http://localhost:3000 접속
  2. viewport를 390px로 변경
  3. 작성 화면으로 이동
  4. 저장 버튼 확인
- 기대 결과: 버튼 텍스트가 한 줄 또는 자연스러운 줄바꿈으로 보인다.
- 실제 결과: 버튼 텍스트가 오른쪽으로 잘린다.
- 원인 후보: 버튼 width가 고정되어 있고 긴 한글 텍스트를 처리하지 못한다.
- 수정 방향: 버튼에 `min-width`, `white-space`, responsive layout을 조정한다.
```

#### 하네스에 반영할 규칙

- UI가 있는 step은 반드시 브라우저 테스트를 포함한다.
- 브라우저 테스트 실패는 step 완료로 처리하지 않는다.
- 스크린샷이나 재현 절차 없이 “확인했다”고만 쓰지 않는다.
- 콘솔 에러가 남아 있으면 완료하지 않는다. 이유: 사용자 화면은 정상처럼 보여도 런타임 오류가 숨어 있을 수 있다.
- 모바일 viewport를 생략하지 않는다. 이유: 데스크톱에서 정상이어도 모바일에서 레이아웃이 깨질 수 있다.
- 브라우저 테스트에서 발견한 버그는 수정 후 같은 시나리오로 재검증한다.

## 최종 체크리스트

- `.claude`가 `.codex`로 전환됐는가?
- `CLAUDE.md` 또는 `claud.md`가 `AGENTS.md`로 전환됐는가?
- `commands`가 `skills`로 전환됐는가?
- `.codex/config.toml`에 `[features] codex_hooks = true`가 있는가?
- TDD guard hook이 있는가?
- lint/build/test hook이 있는가?
- `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/ADR.md`가 있는가?
- 프론트엔드 프로젝트라면 `docs/UI_GUIDE.md`가 있는가?
- `.agents/skills/harness/SKILL.md`가 있는가?
- `.agents/skills/review/SKILL.md` 또는 `AGENTS.md` review 체크리스트가 있는가?
- `scripts/execute.py`가 phase/step 실행을 관리하는가?
- `scripts/test_execute.py`가 하네스 자체를 검증하는가?
- 각 step의 Acceptance Criteria가 실제 실행 가능한 커맨드인가?
- UI가 있는 step에 브라우저 테스트 AC가 포함됐는가?
- desktop과 mobile viewport를 모두 검증했는가?
