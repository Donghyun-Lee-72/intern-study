# START HERE

이 저장소는 이동현이 개인적으로 제작한 Agentic AI 학습자료입니다.
설명은 로컬 학습 페이지에서 읽고, 실습은 Jupyter Notebook으로 진행합니다.
특정 기관의 공식 자료가 아니며, 학습 페이지 자체에는 방문자 분석이나 외부 추적 기능이 없습니다.

저장소 루트에서 로컬 학습 페이지를 실행합니다.

```powershell
uv run --no-project python serve.py
```

브라우저에서 `http://127.0.0.1:8767`을 엽니다.

권장 흐름은 다음과 같습니다.

1. 로컬 학습 페이지의 `학습 섹션`에서 Section 0을 읽습니다.
2. PowerShell에서 clone하거나 압축을 푼 저장소 루트로 이동합니다.
3. uv로 Python 3.11과 Jupyter를 실행합니다.
4. `00_start_here.ipynb`에서 `requirements.txt` 확인, package import 확인, API 연결 확인을 합니다.
5. 로컬 학습 페이지의 설명을 읽으며 `01`부터 `12`까지 노트북을 순서대로 실행합니다.
6. 각 Section 하단의 `결과 확인`과 실행 결과를 비교합니다.

## 1. 저장소 받기

GitHub 저장소를 clone하거나 **Code → Download ZIP**으로 받은 뒤 원하는 위치에 압축을 풉니다.
예시는 다음 경로를 기준으로 합니다.

```text
Documents\agentic-ai-study
```

저장소 루트에는 아래 파일과 폴더가 보여야 합니다.

```text
START_HERE.md
requirements.txt
notebooks/
data/
```

## 2. PowerShell 열기

압축을 푼 루트 폴더에서 PowerShell을 엽니다.

확인:

```powershell
uv --version
uv run --python 3.11 python --version
```

`uv`가 없으면 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

이번 실습에서는 Python을 브라우저에서 따로 다운로드하는 것을 기본 경로로 두지 않습니다.
`uv run --python 3.11 ...` 명령이 필요한 Python을 준비해 실행합니다.
처음 실행할 때 Python 다운로드가 한 번 진행될 수 있습니다.

## 3. Jupyter 열기

루트 폴더에서 아래 명령을 실행합니다.

```powershell
uv run --python 3.11 --with-requirements requirements.txt --with notebook jupyter notebook notebooks
```

브라우저가 열리면 먼저 `00_start_here.ipynb`를 실행합니다.
이 노트북은 루트 `requirements.txt`를 찾아 읽고, 필요한 Python library가 import되는지 확인합니다.

## 4. API key 입력

이번 자료에서는 `.env` 파일을 만들지 않습니다.
실제 API 실습을 선택했다면 환경변수 `OPENAI_API_KEY`를 설정하거나 Notebook의 숨김 입력 프롬프트에
본인 계정에서 발급한 OpenAI API key를 입력합니다. 입력값은 셀 source나 출력에 저장되지 않습니다.
현재 모델 접근 권한과 최신 가격을 확인하고 비용을 감당할 수 있을 때만 실행하세요.

주의:

- API key는 로컬 학습 페이지, 채팅, GitHub, 제출물에 붙여넣지 않습니다.
- Notebook source에 key 문자열을 직접 써 넣지 않습니다.
- 공유하거나 화면을 보여주기 전에는 출력과 환경변수를 다시 확인합니다.
- 예시 모델을 사용할 수 없으면 최신 공식 문서를 확인한 뒤 `OPENAI_MODEL` 값만 바꿉니다.

## 5. 실행 순서

노트북은 Section별로 나뉘어 있습니다.

- `notebooks/00_start_here.ipynb`: 처음 보기, 환경 준비, API 연결 확인
- `notebooks/01_llm_api.ipynb`: LLM API 호출과 prompt 기본
- `notebooks/02_structured_output.ipynb`: Pydantic과 구조화 출력
- `notebooks/03_rag.ipynb`: 작은 문서 corpus로 RAG 흐름 이해
- `notebooks/04_workflow.ipynb`: 검색, 판단, 답변을 연결하는 workflow
- `notebooks/05_linux_wsl.ipynb`: Linux/WSL2 특강과 uv 원칙
- `notebooks/06_documents_chunks.ipynb`: 문서 분할과 metadata 보존
- `notebooks/07_embeddings_vector_search.ipynb`: embedding과 vector 검색
- `notebooks/08_retrieval_evaluation.ipynb`: retriever 평가
- `notebooks/09_traceable_vector_rag.ipynb`: 추적 가능한 Vector RAG
- `notebooks/10_rag_evaluation.ipynb`: RAG 평가와 개선
- `notebooks/11_tools_agent_graph.ipynb`: tool, agent, graph 제어
- `notebooks/12_capstone_starter.ipynb`: 미니 프로젝트 starter와 평가 harness

로컬 학습 페이지에서 해당 Section을 읽고, 같은 번호의 노트북을 실행합니다.
실행 결과는 각 Section 하단의 `결과 확인`과 비교합니다.
문장이 완전히 같을 필요는 없습니다. 정해진 형식, 근거, 답이 없을 때의 처리 방식이 맞는지 확인합니다.

## 6. 막혔을 때 공유할 정보

API key 자체는 절대 공유하지 않습니다. 대신 아래 정보만 공유합니다.

- 현재 폴더 위치
- 실행한 명령
- 실행한 노트북 파일명과 셀 위치
- 오류 메시지
- 사용한 모델명
