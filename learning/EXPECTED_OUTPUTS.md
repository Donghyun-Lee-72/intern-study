# Expected Outputs

이 문서는 예제 실행 후 학생이 스스로 결과를 점검하기 위한 기준입니다. 출력 문장이 완전히 같을 필요는 없지만, 아래 의미와 형식 조건을 만족해야 합니다.

## 공통 통과 기준

- 스크립트가 오류 없이 실행됩니다.
- JSON 출력이 깨지지 않습니다.
- `evidence`에는 `source_id`와 원문 근거가 들어갑니다.
- corpus에 없는 정보는 추측하지 않습니다.
- 답이 없으면 `not_answered: true`를 사용합니다.
- 실행 결과를 `CONCEPT_GUIDE.md`의 개념과 연결해 설명할 수 있습니다.

## Section 0: 환경 확인

확인 파일: `live_openai_smoke.py`

기대 결과:

- `uv --version`이 동작합니다.
- `uv run --python 3.12 python --version`이 Python 3.12 실행 환경을 보여줍니다.
- `OPENAI_API_KEY`가 없으면 skip 메시지가 나옵니다.
- key가 유효하면 한국어 한 문장으로 연결 성공 메시지가 나옵니다.
- 첫 연결 테스트(smoke test)는 모델 품질 평가가 아니라 SDK, key, 모델 이름, 네트워크 연결 확인입니다.

## Section 1: AI에게 요청 보내기

확인 파일: `section1_llm_api.py`

기대 결과:

- `note_a`는 support ticket routing, manual triage reduction, human review fallback을 포함합니다.
- `note_b`는 retrieval-augmented QA, internal API guide, source identifiers를 포함합니다.
- `note_c`는 release note generation, PR summaries, maintainer approval을 포함합니다.
- `note_d`는 구체 metric이나 validation plan이 없으므로 일부 필드를 `not specified`로 둡니다.

학생이 설명해야 할 것:

- prompt에 역할, 목표, 제약, 출력 형식이 들어갑니다.
- 실제 AI 출력은 모델과 prompt에 따라 표현이 조금 달라질 수 있습니다.
- 긴 문서는 한 번에 모두 넣기 어렵기 때문에 필요한 부분을 찾아 넣는 방식이 필요합니다.

## Section 2-1: 구조화 출력 확인

확인 파일: `section2_structured_output.py`

기대 결과:

- 실행하면 `outputs` 폴더에 note별 JSON 파일이 로컬로 생성됩니다.
- 각 파일은 `DocumentExtraction` 데이터 구조 검사를 통과합니다.
- `confidence`는 0과 1 사이 숫자입니다.
- `note_d`는 모르는 정보를 지어내지 않고 낮은 confidence를 갖습니다.

좋은 답변:

- “JSON처럼 보이는 문자열”과 “형식 검사를 통과한 데이터”를 구분해서 설명합니다.

## Section 2-2: LangChain parser 계약 확인

확인 파일: `section2_langchain_contract.py`

기대 결과:

- `PromptTemplate`이 schema 안내문을 포함한 prompt를 만듭니다.
- live model text는 JSON 문자열로 출력됩니다.
- 출력 확인 도구가 JSON 문자열을 `DocumentExtraction` 객체로 parse합니다.

학생이 설명해야 할 것:

- PromptTemplate은 모델 입력을 조립합니다.
- 모델 호출은 실제 LLM response를 만듭니다.
- Output parser는 모델 출력이 정해진 형식에 맞는지 확인하고 Python 객체로 바꿉니다.
- parser는 형식을 검증하지만 답변의 사실성을 보장하지 않습니다.

## Section 3-1: 문서 근거 답변 확인

확인 파일: `section3_rag.py`

테스트 질문별 기대 의미:

- `API onboarding guide에는 무엇이 들어가야 해?`
  - source: `doc_002_api_onboarding`
  - answer: authentication, environment variables, rate limits, minimal smoke test, API key를 source code 밖에 보관한다는 내용을 포함해야 합니다.
- `support ticket routing workflow에는 어떤 fallback이 필요해?`
  - source: `doc_001_support_triage`
  - answer: uncertain case를 처리하는 fallback path가 필요하며, ticket text evidence와 confidence score를 함께 봐야 합니다.
- `문서 근거가 있는 답변을 신뢰하기 전에 무엇을 확인해야 해?`
  - source: `doc_003_rag_quality`
  - answer: retrieved chunks가 질문에 직접 답하는지, source id와 quote가 유지되는지 확인해야 합니다.
- `pricing 정책은 어디에 있어?`
  - answer: corpus에 근거가 없으므로 답하지 않음.
  - `not_answered: true`.

주의:

- 이 예제는 keyword overlap을 쓰므로 표현이 크게 바뀐 질문에는 약할 수 있습니다. 이 한계를 설명할 수 있어야 합니다.

## Section 3-2: LangChain 문서 객체 확인

확인 파일: `section3_langchain_rag.py`

기대 결과:

- `Document` 객체에 `page_content`와 `metadata.source_id`가 들어갑니다.
- `RecursiveCharacterTextSplitter`가 문서를 chunk로 나눕니다.
- 답변 의미는 `section3_rag.py`와 같아야 합니다.
- 수업용 짧은 corpus에서는 답변에 필요한 근거가 `quote` 안에 들어가야 합니다.

학생이 설명해야 할 것:

- 현재 lexical scoring 부분은 확장 단계에서 embedding retriever로 교체할 수 있는 자리입니다.
- 연결 도구를 쓴다고 자동으로 좋은 답이 나오는 것은 아닙니다. source, evidence, answer 검증이 여전히 필요합니다.
- vector store는 embedding과 chunk를 저장하고 유사도 검색을 제공하는 확장 부품입니다.

## Section 4: workflow 연결 확인

확인 파일: `section4_workflow.py`

기대 결과:

- 출력에는 `answer_ko`, `facts`, `evidence`, `not_answered`, `log`가 모두 있습니다.
- 성공 케이스에서는 `facts`가 evidence에서 나옵니다.
- 실패 케이스에서는 `facts`가 `not specified` 중심이고 confidence가 낮습니다.
- `log`에는 실행 단계가 남습니다.

## Section 5: Linux/WSL2 환경 확인

기대 결과:

- PowerShell과 WSL Ubuntu shell이 다른 실행 환경이라는 점을 설명합니다.
- `pwd`, `ls`, `cd`로 현재 위치와 파일 목록을 확인할 수 있습니다.
- Windows 파일 경로와 Linux 파일 경로가 다를 수 있음을 설명합니다.
- VS Code Remote - WSL로 Linux 폴더를 여는 흐름을 설명합니다.
- Linux에서도 uv/Python 환경을 만들 수 있음을 확인합니다.

## test_examples.py

기대 결과:

- `local_tests_passed`가 출력됩니다.
- `API는`, `fallback이`처럼 한국어 조사가 붙은 질문도 검색됩니다.
- schema validation, retrieval, not_answered policy, workflow 실패 케이스를 API 없이 확인합니다.

## test_live_examples.py

기대 결과:

- key 제공 후 실행하면 `all_live_tests_passed`가 출력됩니다.
- 이어서 `usage_totals`에 호출 수와 input/output/total token 수가 출력됩니다.
- pricing처럼 corpus에 없는 질문은 `not_answered: true`가 됩니다.

좋은 최종 설명:

- “검색된 문서에서 답을 만들고, 같은 evidence로 구조화 facts를 만든 뒤, 정해진 형식으로 검증했습니다.”

나쁜 최종 설명:

- “연결 도구를 썼으니 맞습니다.”
- “모델이 답했으니 맞습니다.”
- “source id는 있지만 answer와 evidence가 실제로 연결되는지는 확인하지 않았습니다.”
