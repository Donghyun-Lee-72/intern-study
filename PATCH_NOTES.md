# 2026-07-15 학습자료 확장 패치노트

이번 업데이트는 기존 Section 0~5의 입문 흐름을 유지하면서, 문서 준비부터 Vector RAG, 평가, Tool/Agent, 미니 프로젝트까지 이어지는 Section 6~12를 추가합니다.

## 기존 Section 0~5 변경사항

- API key 입력 셀은 직접 입력뿐 아니라 `OPENAI_API_KEY` 환경변수도 사용할 수 있도록 변경했습니다.
- 모델명은 `OPENAI_MODEL` 환경변수로 바꿀 수 있으며, 별도 설정이 없으면 수업 기본 모델을 사용합니다.
- Section 3과 4의 자유 형식 JSON 생성을 OpenAI structured output으로 변경했습니다. 필드 누락이나 이름 변경 때문에 실습이 불규칙하게 실패하는 문제를 줄였습니다.
- Section 4에서는 미리 결정된 workflow route가 모델 응답에서 바뀌지 않는지 검사합니다.
- 모든 notebook의 cell ID와 저장된 output을 정리해 새 환경에서 처음부터 실행할 수 있게 했습니다.
- `START_HERE.md`, `requirements.txt`, 다운로드 ZIP을 전체 과정 기준으로 갱신했습니다.

## 새로 추가된 Section

- **Section 6 — 문서와 chunk:** 긴 문서를 나누고 `source_id`, `chunk_id`, 원문 위치를 보존합니다.
- **Section 7 — Embedding과 VectorStore:** lexical 검색과 의미 검색을 비교하고 실제 embedding을 선택적으로 검증합니다.
- **Section 8 — Retriever 평가:** 작은 gold set으로 Recall@k, threshold, filter와 실패 원인을 점검합니다.
- **Section 9 — 추적 가능한 Vector RAG:** 검색·생성·검증을 분리하고 `answered`, `not_answered`, `needs_review` 정책과 exact citation을 검사합니다.
- **Section 10 — RAG 평가:** retrieval과 generation을 따로 측정하고 한 설정만 바꾼 baseline/candidate 실험을 수행합니다.
- **Section 11 — Tool과 Agent:** tool schema, routing, 종료 조건, 정책 차단과 오류 처리를 통해 제어 가능한 agent 흐름을 학습합니다.
- **Section 12 — 미니 프로젝트:** 공통 corpus와 평가 계약으로 baseline을 만든 뒤 각자 한 가지 개선을 측정합니다.

## 사이트와 배포 파일 변경사항

- 메인 학습 지도에 Section 6~12를 추가하고 각 Section의 독립 학습 페이지를 연결했습니다.
- Section 페이지에 이전/다음 이동, 참고자료 `ⓘ` 카드, 모바일 레이아웃을 추가했습니다.
- ZIP에 notebook 00~12, 확장 실습용 데이터 4개, 갱신된 requirements와 시작 안내를 포함했습니다.
- 내부 제작 계획·리뷰·비밀 파일은 공개 저장소 대상에서 제외했습니다.

## 검증 결과

- 배포 ZIP을 새 폴더에 압축 해제한 뒤 notebook 00~12를 순서대로 실행했습니다.
- API가 필요한 기존 Section과 Section 7·9의 live gate를 수업용 프로젝트 key로 실제 검증했습니다.
- notebook schema, 구조화 출력, citation validation, 내부 링크, 외부 참고 링크, 모바일 Chromium 렌더링을 확인했습니다.
- 공개 산출물에서 API key literal, 개인 이메일, 개인 절대경로와 비공개 저장소 경로가 없는지 검사했습니다.

학습자는 기존과 같이 웹사이트에서 설명을 읽고 같은 번호의 notebook을 위에서 아래로 실행하면 됩니다. Section 6부터는 앞 Section의 산출물을 다음 Section의 입력과 평가 기준으로 연결합니다.
