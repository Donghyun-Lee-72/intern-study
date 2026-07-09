# Concept Guide

이 문서는 섹션형 스터디에서 필요한 개념을 차례대로 설명합니다. 처음 읽을 때 모든 단어를 외울 필요는 없습니다.
먼저 “AI에게 요청을 보내고, 답변을 확인하고, 문서 근거를 붙이고, 여러 단계를 연결한다”는 큰 흐름만 잡으면 됩니다.
LangChain, RAG, Pydantic 같은 도구 이름은 각 섹션 실습에서 필요한 순간에 다시 설명합니다.

## 먼저 큰 그림 보기

이번 스터디에서 만드는 흐름은 다음과 같습니다.

```text
짧은 문서 입력
-> AI 모델에게 요청
-> 필요한 정보를 정해진 형식으로 받기
-> 답변의 근거 확인
-> 여러 단계를 작은 프로그램처럼 연결
```

어려운 용어가 보이면 “지금 바로 외워야 하는 단어”가 아니라 “실습 중 다시 만나게 될 이름표”라고 생각하면 됩니다.

## 지금 몰라도 되는 것

이번 스터디는 모델 내부 수식이나 신경망 학습 과정을 배우는 수업이 아닙니다.
AI 모델이 어떻게 학습되는지보다, 이미 제공되는 모델을 Python 코드에서 안전하게 사용하는 방법을 먼저 배웁니다.
특정 연구 도메인의 깊은 이론도 암기하지 않습니다.

아래 개념은 구현에 직접 필요하므로 다룹니다. 다만 처음부터 완벽히 이해해야 하는 것은 아닙니다.

도메인 단어가 문서에 나오는 것은 피하지 않습니다. 다만 도메인 단어는 `topic`, `objective`, `method`, `result`, `limitations`, `evidence`로 구조화할 입력일 뿐이고, 깊은 이론 암기를 요구하지 않습니다.

## 1. LLM API

핵심 정의:

- LLM API는 모델을 함수처럼 호출하는 인터페이스입니다.
- 입력은 prompt와 설정값이고, 출력은 text 또는 structured data입니다.
- 같은 입력도 설정값과 모델 버전에 따라 달라질 수 있습니다.

학생이 알아야 할 것:

- LLM은 database가 아닙니다.
- 모델 출력은 검증 전까지 신뢰하면 안 됩니다.
- temperature가 높으면 표현 다양성이 늘지만 추출 안정성은 낮아질 수 있습니다.
- 실제 개발에서는 API key, 비용, rate limit, latency를 고려해야 합니다.
- key는 코드가 아니라 `.env`와 환경변수로 다룹니다.

예제에서 확인할 곳:

- `live_openai_smoke.py`: OpenAI API 연결을 최소로 확인합니다.
- `section1_llm_api.py`: live API 호출로 추출 결과를 받습니다.

확인 질문:

- LLM API 호출과 일반 Python 함수 호출은 어떤 점이 비슷하고 어떤 점이 다른가?
- 정보 추출에서 temperature를 낮게 두는 이유는 무엇인가?
- live API key를 코드에 직접 넣으면 어떤 문제가 생기는가?

## 2. Prompt

핵심 정의:

- Prompt는 모델에게 주는 전체 지시입니다.
- 좋은 prompt는 역할, 목표, 입력, 제약, 출력 형식, 실패 처리 규칙을 포함합니다.

학생이 알아야 할 것:

- “요약해줘”보다 “무엇을 어떤 형식으로, 모르면 어떻게 답할지”가 중요합니다.
- prompt만으로 hallucination을 완전히 막을 수 없습니다.
- prompt는 schema, retrieval, validation과 함께 설계해야 합니다.

예제에서 확인할 곳:

- `section1_llm_api.py`: 기술 노트를 어떻게 요약하고 추출할지 지시합니다.
- `section2_langchain_contract.py`: `PromptTemplate`으로 고정 지시문과 입력 문서를 조립합니다.

확인 질문:

- 기술 문서 추출 prompt에 반드시 들어가야 하는 요소는 무엇인가?
- prompt에 “모르면 not specified”를 넣어도 validation이 필요한 이유는 무엇인가?

## 3. Token과 Context Window

핵심 정의:

- Token은 모델이 텍스트를 처리하는 단위입니다.
- Context window는 한 번에 넣을 수 있는 입력과 출력의 최대 범위입니다.

학생이 알아야 할 것:

- 문서가 길면 전체를 넣기 어렵고 비용도 커집니다.
- context가 길다고 항상 좋은 것은 아닙니다.
- 관련 없는 정보가 많으면 모델이 중요한 근거를 놓칠 수 있습니다.
- RAG는 필요한 문서 조각만 찾아 context에 넣기 위한 설계입니다.

확인 질문:

- 긴 매뉴얼 전체를 prompt에 넣는 방식의 문제는 무엇인가?
- chunking과 retrieval이 필요한 이유는 무엇인가?

## 4. Structured Output

핵심 정의:

- Structured output은 모델 출력을 정해진 구조로 받는 방식입니다.
- JSON처럼 보이는 문자열과 검증된 데이터는 다릅니다.

학생이 알아야 할 것:

- 필드 누락, 타입 오류, JSON 깨짐이 발생할 수 있습니다.
- structured output은 다음 모듈이 사용할 수 있는 데이터 계약입니다.
- 기술 문서 추출에서는 topic, objective, method, result, limitations, evidence 같은 필드를 명확히 해야 합니다.
- 구현 방식은 크게 두 가지가 있습니다.
- 방법 A: prompt로 JSON을 요구하고, 받은 결과를 Pydantic으로 검증합니다.
- 방법 B: API의 JSON Schema/Structured Outputs 기능으로 출력 구조를 더 강하게 제한합니다.
- 이번 기초 실습은 구조와 검증 원리를 먼저 이해하기 위해 방법 A를 사용합니다. 실제 모듈 개발에서는 방법 B로 확장할 수 있습니다.

예제에서 확인할 곳:

- `schema.py`: `DocumentExtraction` schema.
- `section2_structured_output.py`: live LLM 추출 결과를 Pydantic으로 검증합니다.

확인 질문:

- 자연어 요약과 structured extraction은 언제 각각 필요한가?
- JSON 문자열이 있다고 해서 바로 믿으면 안 되는 이유는 무엇인가?

## 5. Pydantic

핵심 정의:

- Pydantic은 Python type hint 기반으로 데이터 구조와 validation을 정의하는 도구입니다.
- 이 스터디에서는 LLM 출력과 모듈 간 입출력 계약을 고정하는 데 씁니다.

학생이 알아야 할 것:

- `BaseModel`은 필드와 타입을 정의합니다.
- `Field`는 제약과 설명을 붙일 수 있습니다.
- validation error는 실패가 아니라 디버깅 신호입니다.
- Pydantic은 사실성을 검증하지 않습니다. 형식과 제약을 검증합니다.

예제에서 확인할 곳:

- `schema.py`: confidence 범위, evidence list, final answer schema.
- `test_examples.py`: schema와 workflow가 깨지지 않는지 확인합니다.

확인 질문:

- `confidence: float = Field(ge=0.0, le=1.0)`가 막아주는 오류는 무엇인가?
- Pydantic validation을 통과해도 여전히 사람이 확인해야 하는 것은 무엇인가?

## 6. Function Calling과 Tool

핵심 정의:

- Tool은 모델 또는 workflow가 호출할 수 있는 외부 기능입니다.
- Function calling은 모델이 어떤 tool을 어떤 인자로 호출할지 정하는 방식입니다.

학생이 알아야 할 것:

- 이번 필수 실습에서는 복잡한 function calling보다 명시적 Python 함수로 시작합니다.
- 좋은 tool은 입력과 출력이 좁고 명확합니다.
- `extract_percentage(text)`처럼 작은 함수가 좋은 출발점입니다.
- `analyze_everything(text)`처럼 너무 넓은 함수는 디버깅이 어렵습니다.

예제에서 확인할 곳:

- `tools.py`: tokenization, scoring, percentage extraction.
- `section4_workflow.py`: retrieval, extraction, validation, answer가 단계별로 호출됩니다.

확인 질문:

- workflow에서 tool로 분리해야 하는 작업은 무엇인가?
- 모델이 직접 답하면 안 되고 tool을 써야 하는 경우는 언제인가?

## 7. LangChain

핵심 정의:

- LangChain은 LLM application의 부품을 연결하는 프레임워크입니다.
- 이번 스터디에서는 prompt, parser, document, splitter, retriever의 역할을 이해하는 것이 중요합니다.

학생이 알아야 할 것:

- `PromptTemplate`은 모델 입력을 조립합니다.
- model call은 실제 LLM response를 만듭니다.
- output parser는 모델 출력이 schema에 맞는지 확인하고 Python 객체로 바꿉니다.
- `Document`는 문서 본문과 metadata를 함께 들고 있는 객체입니다.
- `TextSplitter`는 긴 문서를 chunk로 나눕니다.
- LangChain을 쓴다고 자동으로 좋은 답이 나오지는 않습니다.

예제에서 확인할 곳:

- `section2_langchain_contract.py`: PromptTemplate과 PydanticOutputParser.
- `section3_langchain_rag.py`: Document와 RecursiveCharacterTextSplitter.

확인 질문:

- `PromptTemplate`, model, output parser는 각각 어디에 해당하는가?
- LangChain `Document.metadata`에 source id를 넣는 이유는 무엇인가?

## 8. RAG

핵심 정의:

- RAG는 Retrieval-Augmented Generation의 줄임말입니다.
- 외부 문서에서 관련 근거를 검색한 뒤, 그 근거를 바탕으로 답변을 생성하는 패턴입니다.

학생이 알아야 할 것:

- RAG는 hallucination을 줄일 수 있지만 없애지는 못합니다.
- retrieval이 틀리면 답변도 틀릴 수 있습니다.
- 답변에는 source id와 evidence가 있어야 합니다.
- retrieved context에 답이 없으면 `not_answered: true`가 맞습니다.

예제에서 확인할 곳:

- `section3_rag.py`: keyword 기반 retriever와 grounded answer.
- `section3_langchain_rag.py`: LangChain 문서 객체로 같은 구조를 확인합니다.

확인 질문:

- RAG에서 가장 먼저 확인해야 할 것은 모델 답변인가, retrieved evidence인가?
- 답변은 그럴듯한데 evidence가 틀리면 어떻게 판단해야 하는가?

## 9. Chunking

핵심 정의:

- Chunking은 긴 문서를 작은 조각으로 나누는 과정입니다.

학생이 알아야 할 것:

- chunk가 너무 짧으면 의미가 사라집니다.
- chunk가 너무 길면 관련 없는 정보가 섞입니다.
- overlap은 경계에서 정보가 잘리는 문제를 줄입니다.
- 실제 문서에서는 제목, 섹션, 단락, 목록 같은 구조를 고려해야 합니다.

확인 질문:

- API 가이드의 인증 섹션과 오류 처리 섹션을 같은 chunk로 묶어도 되는가?
- chunk overlap이 필요한 이유는 무엇인가?

## 10. Embedding과 Vector Store

핵심 정의:

- Embedding은 텍스트를 의미 벡터로 바꾸는 과정입니다.
- Vector store는 embedding과 원문 chunk를 저장하고 유사도 검색을 제공합니다.

학생이 알아야 할 것:

- 이번 필수 예제는 lexical retrieval을 사용합니다.
- 실제 RAG에서는 lexical scoring을 embedding similarity와 vector store retriever로 바꿀 수 있습니다.
- embedding model이 바뀌면 검색 결과도 바뀔 수 있습니다.
- vector DB 선택은 데이터 규모, 업데이트 빈도, 배포 환경에 따라 달라집니다.

확인 질문:

- keyword search와 embedding search의 차이는 무엇인가?
- lexical retriever를 vector store retriever로 바꾸려면 코드의 어느 부분을 교체해야 하는가?

## 11. Grounded Answer

핵심 정의:

- Grounded answer는 답변이 특정 evidence에 근거해 생성되었다는 뜻입니다.

학생이 알아야 할 것:

- source id만 붙었다고 grounded answer가 아닙니다.
- `answer_ko`가 evidence 내용을 실제로 반영해야 합니다.
- evidence가 없으면 답하지 않는 것이 좋은 동작입니다.
- 답변과 facts는 같은 대표 evidence에서 나와야 합니다.

확인 질문:

- `answer_ko`와 `facts`가 서로 다른 문서를 근거로 하면 어떤 문제가 생기는가?
- source id는 있는데 quote가 답변을 뒷받침하지 못하면 어떻게 해야 하는가?

## 12. Workflow와 Agent

핵심 정의:

- Workflow는 사람이 단계 순서를 정한 실행 흐름입니다.
- Agent는 목표 달성을 위해 일부 행동 선택을 모델에게 맡기는 구조입니다.

학생이 알아야 할 것:

- 초심자는 먼저 명시적 workflow를 구현하는 것이 안전합니다.
- 최소 workflow는 retrieval -> extraction -> validation -> answer -> logging 순서로 볼 수 있습니다.
- Agentic AI의 핵심은 “알아서 해”가 아니라 상태, 도구, 검증, 종료 조건 설계입니다.

예제에서 확인할 곳:

- `section4_workflow.py`: 명시적 workflow.

확인 질문:

- 이번 프로젝트에서 사람이 고정해야 하는 단계와 모델에게 맡길 수 있는 단계는 무엇인가?
- log가 필요한 이유는 무엇인가?

## 13. Agent loop

핵심 정의:

- Agent loop는 모델이 다음 행동을 선택하고, tool 실행 결과를 관찰한 뒤, 다음 행동을 다시 정하는 반복 구조입니다.

학생이 알아야 할 것:

- 초심자는 먼저 사람이 단계 순서를 정한 workflow를 구현하는 것이 안전합니다.
- 개념적으로 Thought, Action, Observation, Answer 흐름을 이해하면 agent 설계를 읽는 데 도움이 됩니다.
- tool 선택 오류, 비용 증가, 오류 전파가 생길 수 있습니다.

확인 질문:

- 우리 workflow에서 Action과 Observation에 해당하는 것은 무엇인가?
- agent loop를 길게 만들수록 어떤 문제가 생길 수 있는가?
