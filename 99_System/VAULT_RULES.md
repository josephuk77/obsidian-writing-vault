# VAULT_RULES

---
tags:
  - type/project
  - status/active
---

## 기본 원칙

- 이 vault는 개인 지식, 프로젝트 기획, 블로그 초안, 참고자료를 관리한다.
- 기존 파일과 폴더는 명시 요청 없이 삭제하지 않는다.
- `.obsidian/`은 Obsidian 설정 폴더이므로 직접 수정하지 않는다.
- `scripts/`는 기존 자동화 자산이므로 요청 없이 삭제하거나 변경하지 않는다.
- Raw Source는 원본 보존용이므로 수정하지 않는다.

## 정보 흐름

1. 빠른 메모는 `00_Inbox/`에 둔다.
2. 학습 정리는 `02_Study/`에 둔다.
3. 프로젝트 기획은 `04_Projects/`에 둔다.
4. 공통 참고자료는 `05_Resources/`에 둔다.
5. 프로젝트를 넘나드는 AI 업무 기록은 `06_AI_Sessions/`에 둔다.
6. 반복 작성 양식은 `90_Templates/`에 둔다.
7. 운영 규칙은 `99_System/`에 둔다.

## AI 업무 위키 원칙

- 전역 AI 업무 공간은 `06_AI_Sessions/`이다.
- 전역 Raw Source는 `06_AI_Sessions/raw/`에 둔다.
- 전역 Wiki는 `06_AI_Sessions/wiki/`에 둔다.
- 전역 대화 기록은 `06_AI_Sessions/conversations/`에 둔다.
- 전역 산출물은 `06_AI_Sessions/output/`에 둔다.
- 프로젝트가 명확한 자료는 `04_Projects/{project}/`에 둔다.
- 세션 복구는 `index.md`와 `log.md`를 기준으로 한다.

## 프로젝트 원칙

- 프로젝트 폴더는 실제 코드 레포가 아니라 기획 허브로 시작한다.
- Notion 원문은 `10_RAW_SOURCE/notion/`에 보존한다.
- 사용자가 직접 작성한 프로젝트 문서는 `15_MY_DOCUMENTS/`에 둔다.
- AI가 작업하며 필요한 맥락과 가정은 `16_AI_CONTEXT/`에 둔다.
- 실제 프로젝트 진행에 필요한 핵심 기준 정보는 `20_CORE/`에 둔다.
- 정리본과 설명형 위키 문서는 `20_WIKI/`에 둔다.
- 결정 기록은 `30_DECISIONS/`에 둔다.
- 에러 기록은 `40_ERRORS/`에 둔다.
- 산출물은 `90_OUTPUTS/`에 둔다.
