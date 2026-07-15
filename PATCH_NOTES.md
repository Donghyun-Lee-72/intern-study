# 2026-07-15 학습자료 확장 패치노트

이번 업데이트는 기존 Section 0~5의 입문 흐름을 유지하면서, 문서 준비부터 Vector RAG, 평가, Tool/Agent, 미니 프로젝트까지 이어지는 Section 6~12를 추가합니다.

## 기존 Section 0~5 변경사항

기존 Section의 학습 주제와 순서는 바꾸지 않았습니다. 새 Section과 연결해도 처음 학습하는 사람이 기존 흐름을 그대로 따라갈 수 있도록 실행 안정성과 검증 방식을 보완했습니다.

### Section 0 — 환경 준비와 API 연결 확인

- API key를 셀에 직접 입력하는 기존 방식은 유지하면서, 담당자 검증이나 별도 실행 환경에서는 `OPENAI_API_KEY` 환경변수를 사용할 수 있게 했습니다.
- 모델명도 `OPENAI_MODEL` 환경변수로 바꿀 수 있으며, 별도 설정이 없으면 수업 기본 모델을 사용합니다.
- key가 설정되지 않았을 때 무엇을 확인해야 하는지 오류 메시지를 명확하게 수정했습니다.
- `requirements.txt` 확인, package import, 실제 API 연결 확인이라는 기존 통과 기준은 유지했습니다.

### Section 1 — LLM API와 prompt

- 학습 내용과 prompt 예시는 변경하지 않았습니다.
- Section 0과 동일한 API key·모델 설정 방식을 적용해 notebook마다 설정 방법이 달라지는 문제를 없앴습니다.
- 실제 API 호출과 출력 길이 제한이 현재 OpenAI SDK 및 수업 기본 모델에서 동작하는지 다시 확인했습니다.

### Section 2 — Structured output과 Pydantic

- Pydantic schema, validation 성공·실패, “형식 검증은 사실 검증이 아니다”라는 학습 목표는 유지했습니다.
- API key·모델 설정을 다른 Section과 통일했습니다.
- 기존 JSON 출력과 Pydantic validation 예제가 현재 의존성 버전에서 실행되는지 다시 검증했습니다.

### Section 3 — 문서 근거를 사용하는 RAG

- 모델이 자유 형식 JSON을 생성하고 `json.loads`로 해석하던 부분을 OpenAI structured output으로 변경했습니다.
- `answered`, `answer_ko`, `evidence` 중 일부 필드가 빠져 notebook이 불규칙하게 실패하던 가능성을 줄였습니다.
- `answered=true`일 때는 `source_id`와 원문 quote를 반환하고, 답할 근거가 없을 때는 빈 evidence를 반환하도록 계약을 명시했습니다.
- lexical retrieval과 “검색된 근거를 먼저 확인한다”는 기존 학습 흐름은 그대로 유지했습니다.

### Section 4 — Workflow와 상태 분기

- 자유 형식 JSON 출력을 `WorkflowResult` structured output으로 변경했습니다.
- 모델이 `source`처럼 비슷하지만 잘못된 필드명을 반환하던 문제를 schema 수준에서 방지했습니다.
- 검색 결과로 미리 결정된 `answer`, `not_answered`, `needs_review` route를 모델이 임의로 바꾸지 않는지 assertion을 추가했습니다.
- 검색 → route 결정 → 답변 → 다음 행동이라는 기존 workflow 학습 순서는 유지했습니다.

### Section 5 — Linux/WSL2 특강

- Linux/WSL2의 위치와 학습 범위는 변경하지 않았습니다. Section 1~4의 필수 AI 실습을 마친 뒤 진행하는 선택적 환경 확장 단계로 유지했습니다.
- 새 Section 6~12를 Windows PowerShell 환경에서도 시작할 수 있으므로 WSL2가 후속 학습의 필수 조건으로 오해되지 않도록 전체 안내를 맞췄습니다.

### 기존 notebook 공통 정리

- notebook 00~05의 cell ID를 정규화하고 이전 실행 output을 제거했습니다.
- 새 환경에서 위에서 아래로 실행할 때 이전 실행 흔적과 현재 결과가 섞이지 않도록 했습니다.
- `START_HERE.md`, `requirements.txt`, 다운로드 ZIP을 전체 Section 0~12 기준으로 갱신했습니다.

## 새로 추가된 Section

- **Section 6 — 문서와 chunk:** 긴 문서를 나누고 `source_id`, `chunk_id`, 원문 위치를 보존합니다.
- **Section 7 — Embedding과 VectorStore:** lexical 검색과 의미 검색을 비교하고 실제 embedding을 선택적으로 검증합니다.
- **Section 8 — Retriever 평가:** 작은 gold set으로 Recall@k, threshold, filter와 실패 원인을 점검합니다.
- **Section 9 — 추적 가능한 Vector RAG:** 검색·생성·검증을 분리하고 `answered`, `not_answered`, `needs_review` 정책과 exact citation을 검사합니다.
- **Section 10 — RAG 평가:** retrieval과 generation을 따로 측정하고 한 설정만 바꾼 baseline/candidate 실험을 수행합니다.
- **Section 11 — Tool과 Agent:** tool schema, routing, 검색 후 근거 검증, 종료 조건, 정책 차단과 오류 처리를 통해 제어 가능한 agent 흐름을 학습합니다.
- **Section 12 — 미니 프로젝트:** 공통 corpus와 평가 계약으로 baseline을 만든 뒤 각자 한 가지 개선을 측정합니다. 답변 가능 여부와 정책에 따라 적용되는 평가 지표를 구분합니다.

## 사이트와 배포 파일 변경사항

- 메인 학습 지도에 Section 6~12를 추가하고 각 Section의 독립 학습 페이지를 연결했습니다.
- Section 페이지에 이전/다음 이동, 참고자료 `ⓘ` 카드, 모바일 레이아웃을 추가했습니다.
- ZIP에 notebook 00~12, 확장 실습용 데이터 4개, 갱신된 requirements와 시작 안내를 포함했습니다.
- API를 사용하는 notebook 00~04와 선택 실습이 있는 Section 7·9에는 파일 상단에서 수업용 key를 설정할 수 있는 셀을 두었습니다. API가 필요 없는 Section에는 기본 실습에 key가 필요하지 않다고 표시했습니다.
- Section 10·12에서는 인용과 검색 지표가 적용되지 않는 사례를 성공으로 계산하지 않도록 정리했고, Section 11에는 검색 결과를 검증 Tool로 확인하는 2단계 실행을 추가했습니다.
- 내부 제작 계획·리뷰·비밀 파일은 공개 저장소 대상에서 제외했습니다.

## 검증 결과

- 배포 ZIP을 새 폴더에 압축 해제한 뒤 notebook 00~12를 순서대로 실행했습니다.
- API가 필요한 기존 Section과 Section 7·9의 live gate를 수업용 프로젝트 key로 실제 검증했습니다.
- notebook schema, 구조화 출력, citation validation, 내부 링크, 외부 참고 링크, 모바일 Chromium 렌더링을 확인했습니다.
- 공개 산출물에서 API key literal, 개인 이메일, 개인 절대경로와 비공개 저장소 경로가 없는지 검사했습니다.

학습자는 기존과 같이 웹사이트에서 설명을 읽고 같은 번호의 notebook을 위에서 아래로 실행하면 됩니다. Section 6부터는 앞 Section의 산출물을 다음 Section의 입력과 평가 기준으로 연결합니다.
