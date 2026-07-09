# Lecture Notes

이 문서는 섹션형 압축 세미나에서 사용할 학생용 강의노트입니다.
처음에는 기술 용어보다 “내 코드가 AI 모델에게 요청을 보내고, 받은 답을 확인하고, 근거 있는 결과로 정리한다”는 흐름을 먼저 봅니다.
LangChain, RAG, Pydantic 같은 이름은 뒤에서 필요한 시점에 하나씩 붙입니다.

최종 목표는 거창한 자동화 agent를 한 번에 만드는 것이 아니라, 입력, 검색, 추출, 검증, 답변 생성을 안정적으로 연결하는 작은 AI 프로그램을 이해하는 것입니다.

## Section 1: LLM API와 프롬프트

### 학습 목표

이 섹션은 짧게 진행합니다. 목표는 AI 모델을 채팅창에서만 쓰는 것이 아니라, Python 코드에서 불러와 답을 받는 대상으로 이해하는 것입니다.
같은 모델이라도 입력, 맥락, 출력 형식, 설정값에 따라 결과가 달라진다는 사실을 직접 확인합니다.

### 핵심 메시지

LLM 개발의 출발점은 좋은 질문 하나가 아닙니다. 어떤 데이터를 넣을지, 무엇을 시킬지, 어떤 형식으로 받을지, 답이 없으면 어떻게 처리할지를 함께 정하는 것입니다.

### 개념 1: Prompt

Prompt는 모델에게 주는 전체 지시다. 단순한 질문 하나만 prompt가 아닙니다. 좋은 prompt는 보통 다음 요소를 포함합니다.

- 역할: 모델이 어떤 관점에서 답해야 하는가.
- 목표: 무엇을 해야 하는가.
- 맥락: 어떤 입력 데이터나 배경 정보를 참고해야 하는가.
- 제약: 무엇을 포함하거나 제외해야 하는가.
- 출력 형식: 문장, bullet, JSON, schema 등 어떤 형태로 답해야 하는가.
- 검증 기준: 좋은 답변과 나쁜 답변을 가르는 기준은 무엇인가.

나쁜 prompt 예시:

```text
이 문서 요약해줘.
```

더 나은 prompt 예시:

```text
당신은 기술 문서를 읽고 구조화하는 개발 보조자입니다.
아래 문서를 한국어로 5문장 이내로 요약하세요.

반드시 포함할 내용:
- topic
- objective
- method
- result
- limitation

문서에 없는 내용은 추측하지 말고 "not specified"라고 쓰세요.
답변에는 근거 문장을 포함하세요.

문서:
{document}
```

### 개념 2: Token

Token은 모델이 텍스트를 처리하는 단위입니다. 영어는 단어 조각 단위, 한국어는 글자나 형태소 조각에 가깝게 나뉠 수 있습니다. token 수는 세 가지에 영향을 줍니다.

- 비용: 입력과 출력 token이 많을수록 비용이 증가합니다.
- 길이 제한: context window보다 긴 문서는 한 번에 넣을 수 없습니다.
- 품질: 너무 긴 입력은 핵심 정보가 묻힐 수 있습니다.

이 과정에서 필요한 수준은 “tokenizer 내부 구현”이 아니라 “문서가 길면 비용과 성능 문제가 생기므로 chunking과 retrieval이 필요하다”입니다.

### 개념 3: Context Window

Context window는 모델이 한 번에 참고할 수 있는 입력과 출력의 최대 범위입니다. 큰 context window가 있다고 해서 항상 전체 문서를 넣는 것이 좋은 것은 아닙니다. 관련 없는 내용이 많으면 모델이 중요한 정보를 놓칠 수 있고 비용도 커집니다.

이 개념은 Section 3의 RAG로 이어집니다. RAG는 모든 문서를 context에 넣는 대신, 질문과 관련된 부분만 찾아 넣는 전략입니다.

### 개념 4: Temperature

Temperature는 답변의 무작위성을 조절합니다.

- 낮은 값: 더 안정적이고 반복 가능한 답변. 정보 추출, 분류, schema 출력에 적합.
- 중간 값: 일반 요약, 설명, 아이디어 정리에 적합.
- 높은 값: 다양한 표현이 나오지만 엉뚱한 답변 가능성이 커짐.

개발용 정보 추출에서는 보통 낮은 temperature를 기본으로 둡니다.

### 개념 5: Hallucination

Hallucination은 모델이 근거 없는 내용을 그럴듯하게 생성하는 현상입니다. 이 스터디에서는 hallucination을 “모델의 도덕적 실패”가 아니라 “검증되지 않은 생성 결과”로 봅니다. 개발자는 hallucination을 줄이기 위해 다음 방법을 사용합니다.

- 근거 문서를 함께 제공합니다.
- 모르면 모른다고 답하게 합니다.
- 출력 schema를 강제합니다.
- evidence field를 요구합니다.
- 결과를 코드로 검증합니다.
- 중요한 판단은 사람이 확인합니다.

### 중립 기술 문서 예시

입력 문서가 다음과 같다고 하자.

```text
A support ticket-routing assistant classifies incoming customer requests into billing, bug, and account categories. It reduced manual triage by 32 percent on a small evaluation set. The workflow sends low-confidence cases to a human review queue.
```

좋은 추출은 다음 정보를 포함해야 합니다.

- topic: support ticket routing.
- objective: classify incoming customer requests.
- method: classify tickets into billing, bug, and account categories.
- result: manual triage reduced by 32 percent on a small evaluation set.
- limitation: low-confidence cases require human review.
- evidence: 원문 중 어떤 문장이 근거인지.

### Live API key를 다루는 법

OpenAI API key가 제공되면 실제 API 호출을 확인할 수 있습니다. 다만 key는 비밀번호처럼 다뤄야 합니다.

- 코드에 직접 쓰지 않습니다.
- `.env`에 넣고 `python-dotenv`로 읽습니다.
- 제출물이나 채팅에 붙여 넣지 않습니다.
- 반복 가능한 로컬 검사는 `test_examples.py`로, live API 전체 검증은 `test_live_examples.py`로 분리합니다.
- 비용, rate limit, billing 상태 때문에 실패할 수 있음을 알고 있어야 합니다.

`live_openai_smoke.py`의 목적은 “모델이 좋은 답을 내는지 평가”가 아니라 “SDK, key, 모델 이름, 네트워크가 연결되는지 확인”하는 것입니다. 이후 모든 섹션 예제는 실제 LLM API를 사용합니다.

### 오해하기 쉬운 점

- “프롬프트를 잘 쓰면 항상 정답이 나온다”는 틀렸습니다. Prompt는 필요조건이지 충분조건이 아닙니다.
- “모델이 길게 답하면 더 잘한 것”도 틀렸습니다. 개발에서는 짧고 검증 가능한 출력이 더 좋습니다.
- “LLM이 모르겠다고 하면 실패”도 틀렸습니다. 근거가 부족할 때 모른다고 하는 것은 좋은 동작입니다.
- “live API를 쓰면 validation은 필요 없다”도 틀렸습니다. 실제 모델 출력일수록 schema와 evidence 검증이 필요합니다.

### 세미나 중 질문

- 같은 문서를 요약할 때, 사람이 읽는 요약과 코드 모듈에 넘길 추출 결과는 어떻게 달라지는가?
- 문서에 없는 정보를 모델이 보충하면 왜 위험한가?
- API key를 `.env`에 넣는 이유는 무엇인가?

## Section 2: Structured Output, Pydantic, LangChain 기본

### 학습 목표

이 섹션의 목표는 LLM 출력이 프로그램의 입력으로 들어갈 수 있게 만드는 것입니다. 학생들은 자연어 답변과 구조화 출력의 차이를 이해하고, Pydantic schema로 결과를 검증해야 합니다. 동시에 LangChain의 prompt/model/output parser 사고방식을 가볍게 접합니다.

### 핵심 메시지

LLM의 답변은 신뢰하기 전에 검증해야 합니다. 개발에서 중요한 것은 “모델이 그럴듯하게 말했다”가 아니라 “다음 모듈이 사용할 수 있는 구조로, 검증을 통과했다”입니다.

### 개념 1: Structured Output

Structured output은 모델에게 정해진 구조로 답하게 하는 방식입니다. 예를 들어 기술 문서에서 다음 구조를 뽑을 수 있습니다.

```json
{
  "topic": "support ticket routing",
  "objective": "classify incoming customer requests",
  "method": "route requests into billing, bug, and account categories",
  "result": "manual triage was reduced by 32 percent",
  "limitations": ["low-confidence cases require human review"],
  "evidence": [
    {
      "source_id": "note_a",
      "quote": "It reduced manual triage by 32 percent on a small evaluation set."
    }
  ]
}
```

중요한 점은 JSON처럼 보이는 텍스트와 실제 schema 검증을 통과한 데이터는 다르다는 것입니다. 모델이 따옴표를 빠뜨리거나, 필드를 누락하거나, 숫자 타입을 문자열로 낼 수 있습니다.

실제로 structured output을 구현하는 방법은 두 가지로 나눌 수 있습니다.

- 기초 실습 방식: 모델에게 JSON 형식을 요구하고, 받은 결과를 Pydantic으로 검증합니다.
- 실제 개발 확장 방식: OpenAI API의 JSON Schema/Structured Outputs 기능으로 출력 구조를 더 강하게 제한합니다.

이번 스터디는 학생이 schema와 validation의 의미를 먼저 이해하도록 기초 실습 방식을 사용합니다. 이후 실제 모듈 개발에서는 API-native structured output으로 바꿀 수 있습니다.

### 개념 2: Pydantic

Pydantic은 Python type hint를 이용해 데이터 구조를 정의하고 검증합니다. LLM 출력 검증에 특히 유용하다.

예시:

```python
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    source_id: str
    quote: str

class DocumentExtraction(BaseModel):
    topic: str = Field(description="문서의 주제")
    objective: str = Field(description="문서가 설명하는 목표")
    method: str = Field(description="목표를 달성하는 방법")
    result: str = Field(description="문서에 제시된 결과")
    limitations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
```

이 schema는 학생들에게 두 가지를 가르칩니다.

- 출력 필드를 명시적으로 설계해야 합니다.
- confidence처럼 범위가 있는 값은 코드로 검증할 수 있습니다.

### 개념 3: Unknown 처리

LLM 추출에서 중요한 것은 모르는 정보를 빈칸으로 두는 방식입니다. 프로젝트에서는 다음 정책을 권장합니다.

- 필드가 문서에 명시되어 있지 않으면 `"not specified"`를 사용합니다.
- 근거 문장이 없으면 evidence를 빈 배열로 두고, confidence를 낮게 둡니다.
- evidence가 있을 때는 문자열만 쓰지 말고 `{source_id, quote}` 형태로 출처와 원문 근거를 함께 남깁니다.
- confidence는 근거가 명확하면 0.8 이상, 추론이 섞이면 0.5 이하로 둡니다.
- 모델이 추측한 값은 결과에 넣지 않습니다.

### 개념 4: Tool-like Step

Tool-like step은 모델이 직접 답하거나 추측하지 말고, 코드 함수나 외부 시스템에 맡겨야 하는 단계를 말합니다. 초심자에게는 복잡한 function calling보다 명확한 Python 함수부터 시작하는 것이 안전하다.

예를 들어 사용자가 “문서에 성공률이 몇 퍼센트로 제시되어 있나?”라고 물었다면, workflow는 다음을 할 수 있습니다.

- 문서에서 관련 문장을 검색합니다.
- 숫자와 percent 표현을 추출합니다.
- schema에 맞는 값인지 검증합니다.
- 근거와 함께 답변을 만듭니다.

모델이 모든 것을 기억으로 답하면 안 됩니다. 외부 정보, 계산, 단위 변환, 저장 같은 작업은 명시적인 코드 단계로 분리해야 합니다.

### 개념 5: Validation Failure는 학습 신호다

Validation이 실패하면 “망했다”가 아니라 “어디가 불안정한지 발견했다”로 봐야 합니다.

예시 실패:

- `confidence`가 `"high"`라는 문자열로 나옴.
- `evidence`가 원문에 없는 문장임.
- `objective` 필드가 빠짐.
- JSON이 닫히지 않음.

대응:

- schema 설명을 더 명확하게 합니다.
- 낮은 temperature를 사용합니다.
- 재시도 로직을 만듭니다.
- 실패 로그를 남깁니다.
- 사람이 확인할 항목으로 표시합니다.

### 오해하기 쉬운 점

- “JSON으로 답해”라고 쓰면 충분하다는 생각은 위험합니다.
- Pydantic은 LLM을 똑똑하게 만드는 도구가 아니라, LLM 결과를 믿어도 되는지 확인하는 도구입니다.
- Tool calling은 agent의 전부가 아닙니다. Tool은 agent workflow의 한 부품입니다.

### 세미나 중 질문

- 기술 문서 분석에서 반드시 필요한 field는 무엇인가?
- `confidence`는 모델이 마음대로 정해도 되는가, 아니면 규칙이 필요한가?
- 근거 문장이 없는데 결과가 그럴듯하면 받아들여야 하는가?

## Section 3: RAG와 LangChain

### 학습 목표

이 섹션의 목표는 LLM이 외부 문서를 근거로 답하게 만드는 것입니다. 학생들은 RAG의 전체 흐름을 이해하고, LangChain을 이용해 작은 문서 QA 시스템을 만듭니다. 이 섹션이 전체 스터디의 중심입니다.

### 핵심 메시지

RAG는 “문서를 많이 넣는 기술”이 아닙니다. 필요한 문서 조각을 찾아서, 모델이 그 근거를 바탕으로 답하게 하는 설계 패턴입니다.

### 개념 1: Retrieval

Retrieval은 질문과 관련된 문서를 찾는 과정입니다. 단순 keyword search일 수도 있고, embedding 기반 semantic search일 수도 있습니다.

기술 문서에서는 다음 질문이 가능합니다.

- “API 온보딩 문서에 어떤 내용이 들어가야 하는가?”
- “지원 티켓 라우팅에서 실패 처리는 무엇인가?”
- “RAG 답변을 신뢰하기 전에 무엇을 확인해야 하는가?”
- “릴리스 노트 자동화에서 사람이 승인해야 하는 단계는 무엇인가?”

질문마다 필요한 문서 조각이 다릅니다.

### 개념 2: Chunking

문서 전체를 한 번에 넣기 어렵기 때문에 작은 조각으로 나눕니다. 이를 chunking이라고 합니다.

좋은 chunk는 다음 조건을 만족합니다.

- 너무 짧지 않습니다. 의미가 사라지면 검색 품질이 떨어진다.
- 너무 길지 않습니다. 관련 없는 정보가 섞이면 답변 품질이 떨어진다.
- 문장이나 단락 경계를 가능하면 유지합니다.
- overlap을 조금 둬서 경계 정보 손실을 줄입니다.

초심자에게는 처음부터 복잡한 chunking 전략보다, `RecursiveCharacterTextSplitter` 같은 기본 도구를 쓰게 하는 것이 좋습니다.

### 개념 3: Embedding

Embedding은 텍스트를 벡터로 바꾼 것입니다. 의미가 비슷한 문장은 벡터 공간에서 가깝게 위치하도록 학습되어 있습니다. RAG에서는 질문과 문서 chunk를 embedding으로 바꾼 뒤, 가까운 chunk를 찾습니다.

이 과정에서 필요한 수준:

- embedding은 텍스트 의미를 숫자 벡터로 표현합니다.
- 질문과 비슷한 문서 조각을 찾는 데 씁니다.
- embedding model이 바뀌면 검색 결과도 바뀔 수 있습니다.

### 개념 4: Vector Store

Vector store는 embedding과 원문 chunk를 저장하고, 유사도 검색을 제공합니다. 이번 필수 실습에서는 환경 부담을 줄이기 위해 lexical retrieval을 먼저 쓰고, Chroma 또는 FAISS 같은 로컬 vector store는 확장 실습으로 둡니다.

실제 프로젝트에서는 데이터 규모, 업데이트 빈도, 배포 환경에 따라 vector DB 선택이 달라질 수 있습니다. 하지만 이번 스터디에서는 vector DB 선택보다 RAG 흐름 이해가 우선입니다.

### 개념 5: Grounded Answer

RAG 답변은 근거가 있어야 합니다. “정답처럼 보이는 문장”보다 “어떤 chunk를 근거로 답했는지”가 더 중요합니다.

권장 출력:

```json
{
  "answer_ko": "API 온보딩 가이드는 인증, environment variables, rate limit, minimal smoke test, API key를 source code 밖에 보관한다는 내용을 포함해야 합니다.",
  "evidence": [
    {
      "source_id": "doc_002_api_onboarding",
      "quote": "API onboarding guides should explain authentication, environment variables, rate limits, and a minimal smoke test. API keys must be stored outside source code, and the first live request should use a low-risk prompt that checks connectivity."
    }
  ],
  "source_ids": ["doc_002_api_onboarding"],
  "not_answered": false
}
```

### LangChain의 역할

LangChain은 RAG의 각 부품을 연결하는 데 사용합니다.

- document loader.
- text splitter.
- embedding model.
- vector store.
- retriever.
- prompt template.
- LLM call.

학생들에게 LangChain의 모든 추상화 이름을 외우게 하지 않습니다. “RAG pipeline을 코드로 연결할 때 어떤 부품이 필요한가”를 이해하게 합니다.

필수 예제에서는 LangChain `Document`와 `RecursiveCharacterTextSplitter`를 실제로 사용합니다. embedding model과 vector store는 아직 붙이지 않지만, 코드에서 lexical scoring 부분이 확장 단계의 retriever로 교체될 자리임을 확인합니다.

### 오해하기 쉬운 점

- RAG를 쓰면 hallucination이 완전히 사라진다는 생각은 틀렸습니다.
- vector search 결과가 항상 맞는 문서라는 보장은 없습니다.
- retrieved context에 답이 없으면 모델은 모른다고 해야 합니다.
- 문서를 많이 넣을수록 좋은 것이 아닙니다.

### 세미나 중 질문

- 질문이 너무 넓으면 retrieval이 왜 어려워지는가?
- 근거 chunk가 틀렸는데 모델 답변이 자연스러우면 어떻게 해야 하는가?
- lexical retrieval을 embedding retriever로 바꾸려면 어느 함수를 교체해야 하는가?

## Section 4: 통합 Workflow

### 학습 목표

이 섹션의 목표는 앞 섹션의 부품을 작은 기술 문서 분석 workflow로 묶는 것입니다. 학생들은 agent를 “자율적으로 뭐든 하는 AI”가 아니라 “목표를 달성하기 위해 LLM, retrieval, validation, evidence, tool-like step을 조합한 실행 흐름”으로 이해해야 합니다.

### 핵심 메시지

Agentic AI의 핵심은 framework 이름이 아닙니다. 상태, 목표, 도구, 관찰, 검증, 종료 조건을 어떻게 설계하는지가 핵심입니다.

### 개념 1: Workflow와 Agent

Workflow는 사람이 순서를 정합니다.

```text
문서 입력 -> 검색 -> 정보 추출 -> schema 검증 -> 답변 생성
```

Agent는 일부 선택을 모델에게 맡깁니다.

```text
목표 입력 -> 다음 행동 선택 -> tool 호출 -> 결과 관찰 -> 다음 행동 선택 -> 종료
```

초심자에게는 완전한 agent보다 명시적 workflow가 더 안전하다. 따라서 이 스터디의 최종 프로젝트는 “agent-like workflow”로 시작하고, 일부 tool 선택만 agent적으로 만듭니다.

### 개념 2: Tool

Tool은 모델 또는 workflow가 사용할 수 있는 외부 기능입니다.

예시:

- 문서 chunk 검색.
- percentage 추출.
- source id 확인.
- JSON 저장.
- live API 호출.

좋은 tool은 입력과 출력이 명확하다. 예를 들어 `extract_percentage(text)`는 좋은 tool입니다. 반대로 `analyze_everything(text)`는 너무 넓고 불명확하다.

### 개념 3: State

Agent workflow에는 현재 상태가 있습니다.

예시 상태:

- user question.
- retrieved documents.
- extracted facts.
- validation result.
- called tools.
- final answer.

상태를 명시하지 않으면 디버깅이 어려워진다. 학생들은 최소한 실행 로그를 남겨야 합니다.

### 확장 개념: Agent loop

Agent loop는 모델이 다음 행동을 고르고, 실행 결과를 관찰한 뒤, 다음 행동을 다시 정하는 구조입니다. 학생용 기본 실습에서는 완전 자율 loop를 만들기보다 각 단계를 명시적으로 고정한 workflow를 먼저 구현합니다.

기본 구조 예시:

```text
Thought: 무엇이 필요한지 생각합니다.
Action: 검색, 계산, API 호출 같은 행동을 합니다.
Observation: 행동 결과를 관찰합니다.
Thought: 관찰을 바탕으로 다음 행동을 정합니다.
...
Answer: 최종 답변을 냅니다.
```

이 구조에서 중요한 질문은 “모델이 얼마나 자유롭게 행동하게 할 것인가”가 아니라 “상태, 도구, 검증, 종료 조건이 명확한가”입니다.

### 확장 개념: LangChain Agent와 Typed Agent Framework

LangChain은 다양한 구성 요소를 연결해 agent를 만들기 좋습니다. 다만 이번 섹션형 스터디의 최소 목표는 완전한 agent가 아니라 RAG 기반 workflow다.

Typed agent framework는 typed output, dependency, tool을 더 엄격하게 관리하기 위한 선택지입니다.

학생들은 둘 중 하나를 “정답 프레임워크”로 외우면 안 됩니다. 중요한 것은 다음 질문입니다.

- 입력은 무엇인가?
- 중간 상태는 무엇인가?
- 어떤 tool을 언제 호출하는가?
- 출력 schema는 무엇인가?
- 실패하면 어떻게 회복하는가?

### 오해하기 쉬운 점

- Agent는 그냥 LLM에게 “알아서 해”라고 시키는 것이 아닙니다.
- Tool이 많을수록 좋은 agent가 되는 것이 아닙니다.
- Memory는 무조건 긴 대화 기록을 넣는 것이 아닙니다.
- agent loop는 모든 문제에 쓰는 만능 구조가 아닙니다.

### 세미나 중 질문

- 현재 프로젝트에서 agent가 직접 선택해야 하는 것은 무엇이고, 사람이 workflow로 고정해야 하는 것은 무엇인가?
- 기술 문서 분석에서 필요한 tool은 몇 개면 충분한가?
- agent loop가 길어질수록 어떤 문제가 생기는가?
- 최종 답변보다 중간 로그가 더 중요한 경우는 언제인가?
