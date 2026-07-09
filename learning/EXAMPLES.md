# Examples

예제는 “작고 실행 가능하게” 만드는 것을 우선합니다.
기본 경로에서는 노트북만 위에서 아래로 실행하면 됩니다. 아래 Python 파일들은 노트북에서 하는 일을 섹션별 파일로 나눈 것입니다.
처음에는 파일 이름을 모두 이해하려고 하지 말고, 노트북 실행이 끝난 뒤 같은 흐름을 스크립트로 다시 확인할 때 참고하면 됩니다.

섹션별 메인 예제는 실제 OpenAI API를 호출합니다. 문서를 찾는 일부 단계와 `test_examples.py`는 로컬에서 수행하지만, 요약, 추출, 근거 기반 답변 생성, 최종 사실 정리는 실제 AI 응답을 사용합니다.

## 파일 목록

이 목록은 처음부터 외우는 목차가 아닙니다. 노트북을 먼저 실행한 뒤, “이 셀이 어느 파일에 해당하나?”를 확인할 때 사용합니다.

- `requirements.txt`: 실행에 필요한 패키지 목록입니다.
- `.env.example`: API key를 넣는 `.env` 파일의 예시입니다.
- `../notebooks/amsl_agentic_ai_live_api_study.ipynb`: 학생이 주로 실행할 통합 노트북입니다.
- `data/notes.json`: 실습에 쓰는 짧은 기술 노트입니다.
- `data/corpus/*.txt`: 문서 근거 찾기 실습용 짧은 문서입니다.
- `schema.py`: AI 답변이 정해진 형식인지 확인하는 코드입니다.
- `tools.py`: 문서에서 필요한 부분을 찾고 숫자를 뽑는 보조 코드입니다.
- `section1_llm_api.py`: 실제 AI 호출과 prompt 구조를 보는 예제입니다.
- `section2_structured_output.py`: AI 답변을 정해진 형식으로 바꾸고 확인하는 예제입니다.
- `section2_langchain_contract.py`: prompt와 출력 확인 도구를 연결하는 예제입니다.
- `section3_rag.py`: 문서에서 근거를 찾고 그 근거로 답하는 예제입니다.
- `section3_langchain_rag.py`: 같은 흐름을 연결 도구의 문서 객체로 보는 예제입니다.
- `section4_workflow.py`: 여러 단계를 하나로 연결한 예제입니다.
- `live_openai_smoke.py`: 실제 API 첫 연결 테스트입니다.
- `test_examples.py`: 비용 없는 로컬 검사입니다. schema, retrieval, not_answered policy, workflow 실패 케이스처럼 API 없이 확인할 수 있는 규칙을 점검합니다.
- `test_live_examples.py`: 명시 플래그를 켠 뒤 실행하는 실제 API 전체 검증입니다.

## 학습 의도

예제는 production code가 아닙니다. 다음 질문에 답할 수 있게 하는 교육용 코드입니다.

- 입력은 무엇인가?
- 출력은 어떤 형식을 따라야 하는가?
- evidence는 어디서 오는가?
- 모르는 경우 어떻게 표현하는가?
- 실패를 어디서 발견하는가?
- `answer_ko`가 evidence를 바탕으로 질문에 직접 답하는가?
- 실제 API 호출 결과는 왜 매번 조금 달라질 수 있는가?

## 연결 도구와의 관계

`section3_rag.py`는 표준 라이브러리로 단어 기반 문서 검색을 구현합니다. `section3_langchain_rag.py`는 같은 흐름을 LangChain의 문서 객체와 문서 나누기 도구로 보여줍니다.

두 예제 모두 embedding/vector DB를 쓰지 않습니다. 이유는 첫 RAG 실습에서 DB 설정 문제를 피하고 구조를 먼저 이해하기 위해서입니다. 실제 RAG에서는 lexical scoring을 embedding similarity와 vector store retriever로 바꿉니다. 답변 생성은 live LLM을 사용합니다.

LangChain splitter 예제는 짧은 수업용 문서가 한 chunk 안에 들어가도록 크게 잡아두었습니다. 실제 프로젝트에서는 문서가 길어지므로 chunk size, overlap, 문장/단락 경계를 조정해야 합니다.

대응 관계:

- `load_corpus()` -> document loader.
- `section3_langchain_rag.py`의 `split_documents()` -> text splitter.
- `score()` -> embedding similarity 또는 retriever scoring.
- `retrieve()` -> retriever.
- `answer_question()` -> retrieved context를 바탕으로 답변을 합성하고 `GroundedAnswer` schema로 검증하는 단계.

## 기대 실행 순서

학생 기본 경로:

1. `notebooks/amsl_agentic_ai_live_api_study.ipynb`를 엽니다.
2. 위에서부터 순서대로 실행합니다.
3. 마지막 토큰 사용량 셀에서 사용량을 확인합니다.

스크립트 경로:

1. `live_openai_smoke.py`로 OpenAI API 연결 확인.
2. `section1_llm_api.py`로 prompt와 live LLM 출력 확인.
3. `section2_structured_output.py`로 Pydantic validation 확인.
4. `section2_langchain_contract.py`로 LangChain prompt/parser 계약 확인.
5. `section3_rag.py`로 retrieval/evidence + live answer 확인.
6. `section3_langchain_rag.py`로 LangChain 객체 확인.
7. `section4_workflow.py`로 전체 흐름 확인.
8. `test_examples.py`로 비용 없는 로컬 검사 확인. 이 파일은 LLM 품질 검사가 아니라 API 없이 잡을 수 있는 기본 규칙 검사입니다.
9. 마지막 확인이 필요할 때 `RUN_LIVE_OPENAI_TESTS=1`을 켠 뒤 `test_live_examples.py`로 live API 전체 검증.

## Lexical, LangChain, Live API의 차이

- Lexical retrieval: 단어 겹침으로 문서를 찾습니다. embedding보다 약하지만 구조 학습에 좋습니다.
- LangChain example: LangChain 문서 객체와 splitter를 사용하고, lexical retriever 자리에 확장 단계에서 vector store retriever를 넣을 수 있게 합니다. 아직 vector DB는 없습니다.
- Live API: 실제 OpenAI API를 호출합니다. 결과 문장은 변할 수 있고 key, network, rate limit, billing 상태에 영향을 받습니다.
- Real RAG: 실제 LLM, embedding model, vector store를 연결합니다. 수업 후반 또는 확장 과제입니다.
