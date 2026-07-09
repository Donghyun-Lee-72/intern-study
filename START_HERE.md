# START HERE

AMSL Agentic AI 스터디의 실행용 파일 패키지입니다.

교재는 웹사이트에서 읽고, 실습은 ZIP 안의 Jupyter Notebook으로 진행합니다.
이 ZIP에는 별도 `examples` 폴더가 없습니다. 학생이 봐야 할 실행 파일을 줄이기 위해
Section별 노트북과 루트 `requirements.txt`만 사용합니다.

웹사이트:

```text
https://intern-study.donghyunlee.me
```

권장 흐름은 다음과 같습니다.

1. 웹사이트의 `학습 섹션`에서 Section 0을 읽습니다.
2. 이 ZIP을 압축 해제합니다.
3. PowerShell에서 압축을 푼 루트 폴더로 이동합니다.
4. uv로 Python 3.11과 Jupyter를 실행합니다.
5. `00_start_here.ipynb`에서 `requirements.txt` 확인, 패키지 import 확인, API 연결 확인을 합니다.
6. 웹사이트 설명을 읽으며 `01`부터 `05`까지 노트북을 순서대로 실행합니다.
7. 각 Section 하단의 `결과 확인`과 실행 결과를 비교합니다.

## 1. 압축 풀기

다운로드한 ZIP 파일을 원하는 위치에 압축 해제합니다. 예시는 다음 경로를 기준으로 합니다.

```text
Documents\amsl-internship-study
```

압축을 푼 루트 폴더에는 아래 파일과 폴더가 보여야 합니다.

```text
START_HERE.md
requirements.txt
notebooks/
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
이 노트북은 루트 `requirements.txt`를 찾아 읽고, 필요한 Python 패키지가 import되는지 확인합니다.

## 4. API key 입력

이번 자료에서는 `.env` 파일을 만들지 않습니다.
각 노트북의 `API key 입력` 셀에 수업용 OpenAI API key를 직접 붙여넣습니다.

```python
OPENAI_API_KEY = "여기에_수업용_API_KEY를_붙여넣으세요"
OPENAI_MODEL = "gpt-5.4-mini"
```

주의:

- API key는 웹사이트, 채팅, GitHub, 제출물에 붙여넣지 않습니다.
- API key가 들어간 노트북은 그대로 공유하지 않습니다.
- 제출하거나 화면 공유하기 전에는 API key 문자열을 지웁니다.
- 노트북에 API key를 붙여넣은 뒤 저장하면 API key 문자열이 파일 안에 남을 수 있습니다.
- 제출, GitHub 업로드, 채팅 공유, 화면 공유 전에는 API key 셀의 문자열을 지우고 Jupyter 출력도 정리합니다.
- 수업 중 다른 모델명을 안내받으면 `OPENAI_MODEL` 값만 바꿉니다.

## 5. 실행 순서

노트북은 Section별로 나뉘어 있습니다.

- `notebooks/00_start_here.ipynb`: 처음 보기, 환경 준비, API 연결 확인
- `notebooks/01_llm_api.ipynb`: LLM API 호출과 prompt 기본
- `notebooks/02_structured_output.ipynb`: Pydantic과 구조화 출력
- `notebooks/03_rag.ipynb`: 작은 문서 corpus로 RAG 흐름 이해
- `notebooks/04_workflow.ipynb`: 검색, 판단, 답변을 연결하는 workflow
- `notebooks/05_linux_wsl.ipynb`: Linux/WSL2 특강과 uv 원칙

웹사이트에서 해당 Section을 읽고, 같은 번호의 노트북을 실행합니다.
실행 결과는 웹사이트 각 Section 하단의 `결과 확인`과 비교합니다.
문장이 완전히 같을 필요는 없습니다. 정해진 형식, 근거, 답이 없을 때의 처리 방식이 맞는지 확인합니다.

## 6. 막혔을 때 공유할 정보

API key 자체는 절대 공유하지 않습니다. 대신 아래 정보만 공유합니다.

- 현재 폴더 위치
- 실행한 명령
- 실행한 노트북 파일명과 셀 위치
- 오류 메시지
- 사용한 모델명
