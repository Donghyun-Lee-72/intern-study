# Practicals

실습은 학생이 “읽고 이해했다”가 아니라 “작게 실행했다”를 기준으로 합니다.
일정표처럼 날짜로 나누지 않고, Section 0부터 가능한 만큼 순서대로 진행합니다.
대부분의 학생은 웹사이트의 학습 섹션을 읽은 뒤 노트북을 위에서 아래로 실행하면 됩니다.

처음 읽을 때 아래 용어를 모두 외울 필요는 없습니다. 노트북을 실행하면서 “AI에게 요청한다 -> 답을 확인한다 -> 문서 근거가 있는지 본다 -> 모르면 모른다고 처리한다”는 흐름만 잡으면 됩니다.

## 공통 규칙

- 대부분의 메인 예제는 실제 OpenAI API를 사용하지만, `test_examples.py`는 API key 없이 로컬 규칙만 확인합니다.
- API key와 모델명은 `examples/.env`에서 관리합니다.
- 모든 출력은 가능하면 정해진 형식으로 저장합니다.
- 중요한 답변에는 근거 문장과 출처 표시를 붙입니다.
- 모르는 내용은 `not specified` 또는 `not_answered: true`처럼 “모른다”고 표시합니다.
- 각 섹션 실습 전 필요한 개념을 짧게 읽고, 실습 후 자기 말로 설명합니다.

## Section 0: 시작 전 준비

예상 소요시간: 60-90분.

목표:

- 웹사이트 학습 섹션의 전체 흐름을 읽습니다.
- uv, uv가 준비한 Python 3.12, PowerShell 실행 위치를 확인합니다.
- 실습 파일 ZIP을 풀고 노트북을 열 준비를 합니다.
- `examples/.env`에 API key와 모델명을 넣습니다.
- 첫 연결 테스트(smoke test)를 통과합니다.

실행:

```powershell
cd amsl-internship-study/examples
Copy-Item .env.example .env
notepad .env
uv run --python 3.12 --with-requirements requirements.txt python live_openai_smoke.py
```

완료 기준:

- `uv --version`과 `uv run --python 3.12 python --version`이 동작합니다.
- `live_openai_smoke.py`가 한국어 연결 성공 메시지를 출력합니다.
- key를 코드, 제출물, 채팅에 직접 붙여 넣지 않습니다.

막히면 볼 문서:

- [빠른 실행 순서](QUICKSTART.md)
- [API key와 연결 테스트](LIVE_API_GUIDE.md)
- [오류 해결](TROUBLESHOOTING.md)

## Section 1: AI에게 요청 보내기

예상 소요시간: 60-90분.

목표:

- AI 모델을 채팅창이 아니라 Python 코드에서 호출하는 대상으로 이해합니다.
- prompt에 역할, 목표, 입력, 제약, 출력 형식이 들어간다는 점을 확인합니다.
- 짧은 기술 노트에서 topic, objective, method, result, limitations, evidence를 뽑아봅니다.

실행:

```powershell
uv run --python 3.12 --with-requirements requirements.txt python section1_llm_api.py
```

완료 기준:

- 실행이 오류 없이 끝납니다.
- `note_d`에서 없는 정보를 지어내지 않는 이유를 설명할 수 있습니다.
- 좋은 prompt 요소 5개를 적습니다.

제출 또는 정리:

- 실행 화면 캡처 또는 출력 복사.
- AI 요청, prompt, 사용량, 근거 없는 답변을 각각 1문장으로 설명.

## Section 2: 답변을 정해진 형식으로 받기

예상 소요시간: 60-90분.

목표:

- LLM 출력이 프로그램의 다음 입력으로 들어가려면 schema가 필요하다는 점을 이해합니다.
- Pydantic validation이 형식과 제약을 확인하지만 사실성을 보장하지는 않는다는 점을 확인합니다.
- LangChain의 prompt/model/output parser 역할을 가볍게 봅니다.

실행:

```powershell
uv run --python 3.12 --with-requirements requirements.txt python schema.py
uv run --python 3.12 --with-requirements requirements.txt python section2_structured_output.py
uv run --python 3.12 --with-requirements requirements.txt python section2_langchain_contract.py
```

완료 기준:

- `schema.py`가 예시 객체를 출력합니다.
- `note_a`-`note_d`가 validation을 통과합니다.
- prompt preview, live model text, parsed Pydantic object의 차이를 설명할 수 있습니다.
- structured output, Pydantic, parser, validation의 차이를 설명할 수 있습니다.

도전 과제:

- 답변 형식에 `task_type` 필드를 추가합니다.
- 형식 검사가 깨지면 오류를 읽고 수정합니다.

## Section 3: 문서 근거로 답하게 하기

예상 소요시간: 90-120분.

목표:

- RAG를 “관련 문서를 먼저 찾고, 찾은 근거 안에서 답하는 흐름”으로 이해합니다.
- source id와 evidence quote를 유지해야 하는 이유를 확인합니다.
- 답이 없는 질문에서 `not_answered: true`가 나오는지 확인합니다.
- lexical retrieval과 실제 embedding/vector DB RAG의 차이를 설명합니다.

실행:

```powershell
uv run --python 3.12 --with-requirements requirements.txt python section3_rag.py
uv run --python 3.12 --with-requirements requirements.txt python section3_langchain_rag.py
```

테스트 질문:

- `API onboarding guide에는 무엇이 들어가야 해?`
- `support ticket routing workflow에는 어떤 fallback이 필요해?`
- `RAG 답변을 신뢰하기 전에 무엇을 확인해야 해?`
- `pricing 정책은 어디에 있어?`

완료 기준:

- 답이 있는 질문은 관련 source를 찾습니다.
- 답이 있는 질문의 `answer_ko`에는 문서 근거를 바탕으로 한 내용 답변이 들어갑니다.
- 답이 없는 질문은 `not_answered: true`가 됩니다.
- `section3_rag.py`와 `section3_langchain_rag.py`가 source id와 evidence를 유지한다는 점을 확인합니다.

## Section 4: 여러 단계를 하나로 연결하기

예상 소요시간: 60-90분.

목표:

- 문서 찾기, 정보 뽑기, 형식 확인, 답변 생성을 하나의 workflow로 묶습니다.
- 완전 자율 agent보다 고정 workflow가 초심자 실습에서 더 안전한 이유를 이해합니다.
- 사용량 확인 셀에서 호출 수와 token 수를 기록합니다.

실행:

```powershell
uv run --python 3.12 --with-requirements requirements.txt python section4_workflow.py
```

완료 기준:

- `answer_ko`, `facts`, `evidence`, `log`가 모두 출력됩니다.
- source id가 유지됩니다.
- 답이 없는 질문에서 지어내지 않습니다.
- `facts`가 `answer_ko`와 같은 evidence에서 나옵니다.

제출 또는 정리:

- 성공 케이스 2개.
- 실패 케이스 1개.
- 각 케이스의 JSON 출력.
- 고정된 실행 흐름과 더 자율적인 AI 도우미의 차이, 현재 과제에서 고정 흐름을 우선하는 이유를 설명한 짧은 메모.

## Section 5: Linux/WSL2 개발 환경 입문

예상 소요시간: 90-120분.

목표:

- Windows PowerShell과 Linux shell이 서로 다른 실행 환경이라는 점을 이해합니다.
- WSL2에 Ubuntu를 설치하는 흐름을 봅니다.
- Windows 파일 위치와 Linux 파일 위치가 다르다는 점을 확인합니다.
- VS Code Remote - WSL로 Linux 폴더를 여는 방식을 이해합니다.
- 기본 Linux 명령어와 uv/Python 실행 흐름을 확인합니다.

실행:

```bash
pwd
ls
python3 --version
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

완료 기준:

- `pwd`, `ls`, `cd`가 무엇을 확인하는 명령인지 설명할 수 있습니다.
- `\\wsl$`로 WSL 파일에 접근할 수 있다는 점을 압니다.
- Windows PowerShell의 Python과 WSL Ubuntu의 Python이 다를 수 있음을 설명할 수 있습니다.
- Linux에서도 uv/Python 환경을 만들 수 있습니다.

상세 자료:

- [Section 5 Linux/WSL2](LINUX_SPECIAL_CLASS.md)

## 추가: 자율 실행 도구 읽기

시간이 남으면 LangChain agent 또는 typed agent framework의 짧은 소개 글만 읽습니다. 필수 구현 과제는 아니며, “AI가 다음 행동을 직접 고르는 구조도 있다” 정도만 이해하면 됩니다.

읽고 답할 질문:

- 우리 workflow에서 action에 가까운 단계는 무엇인가?
- observation에 가까운 데이터는 무엇인가?
- 왜 이번 스터디에서는 완전 자율 agent보다 고정 workflow가 더 안전한가?

## 추가: 얕은 도메인 브릿지

시간이 남으면 짧은 소재/연구 문서 snippet 하나를 corpus로 추가합니다.

완료 기준:

- 도메인 단어를 외우는 것이 아니라, source id와 quote를 유지합니다.
- `topic`, `objective`, `method`, `result`, `limitations`로 구조화합니다.
- 도메인 문서에서도 evidence가 없으면 답하지 않습니다.
