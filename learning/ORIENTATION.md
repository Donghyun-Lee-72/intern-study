# Section 0: 시작 전 준비

이 문서는 스터디를 시작하기 전에 내 컴퓨터에서 실습이 돌아가도록 준비하는 안내입니다. 이번 과정은 Windows 사용자를 기준으로 하며, PowerShell과 uv를 사용합니다.

## 1. 오리엔테이션의 목표

오리엔테이션이 끝나면 다음을 할 수 있어야 합니다.

- PowerShell에서 현재 폴더를 확인하고 명령을 실행할 수 있습니다.
- uv를 설치하고 실행할 수 있습니다.
- uv가 준비한 Python 3.12 실행 환경을 확인할 수 있습니다.
- 실습 파일 ZIP을 다운로드하고 압축을 풀 수 있습니다.
- Jupyter Notebook 또는 VS Code Notebook으로 `.ipynb` 파일을 열 수 있습니다.
- `.env` 파일에 API key와 모델명을 넣을 수 있습니다.
- 첫 연결 테스트(smoke test)로 실제 OpenAI API 응답을 받을 수 있습니다.
- 오류가 나면 key, model, package, network, path 중 어디를 먼저 확인할지 알 수 있습니다.

오리엔테이션은 어려운 개념을 배우는 시간이 아니라, **실습이 돌아가는 컴퓨터를 만드는 시간**입니다.

## 2. 이번 과정의 기본 환경

이번 과정에서는 다음 조합을 표준으로 사용합니다.

- OS: Windows
- 터미널: PowerShell
- Python 환경/패키지 관리: uv
- 실행 도구: VS Code Notebook 또는 Jupyter Notebook
- API 호출: OpenAI API

WSL2, Linux, bash, VS Code Remote - WSL은 기본 섹션을 마친 뒤 Section 5에서 따로 다룹니다. 처음부터 WSL2를 설치하지 않는 이유는 재부팅, Ubuntu 계정, Windows/Linux 경로 차이, VS Code 원격 연결 같은 변수가 많기 때문입니다.

Anaconda는 이번 과정의 표준 환경으로 쓰지 않습니다. 이미 설치되어 있다면 Jupyter 실행용으로만 사용할 수 있지만, 패키지 설치와 예제 실행의 기준은 uv입니다.

## 3. 준비물

수업 전에는 다음을 준비합니다.

- 개인 노트북
- 인터넷 연결
- 최신 브라우저
- VS Code 또는 Jupyter Notebook
- uv가 준비하는 Python 3.12 실행 환경
- 제공받은 OpenAI API key
- 안내받은 수업용 모델명

PowerShell에서 uv가 보이는지 확인합니다.

```powershell
uv --version
```

오류가 나면 아래 설치 명령을 먼저 실행합니다. 이번 과정에서는 Python을 브라우저에서 따로 다운로드하는 것을 기본 경로로 두지 않고, uv가 Python 3.12 실행 환경을 준비하게 합니다.

## 4. uv가 무엇인가요?

uv는 Python 프로젝트의 가상환경과 패키지를 빠르게 관리해주는 도구입니다. 처음에는 네 가지만 기억하면 됩니다.

- 가상환경은 프로젝트마다 독립된 Python 작업 공간입니다.
- 패키지는 프로젝트에 필요한 외부 라이브러리입니다.
- `uv venv`는 가상환경을 만듭니다.
- `uv run ...`은 가상환경 활성화가 헷갈릴 때도 필요한 패키지와 함께 명령을 실행하게 해줍니다.
- 이번 실습에서는 대부분 `uv run --python 3.12 --with-requirements requirements.txt ...` 형식을 사용합니다.

uv 설치:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
uv run --python 3.12 python --version
```

설치 직후 `uv` 명령을 찾지 못하면 PowerShell을 새로 열고 다시 확인합니다.

## 5. 실습 파일 ZIP 다운로드

처음 시작할 때는 노트북만 받지 말고 실습 파일 ZIP을 다운로드합니다. ZIP은 교재가 아니라 실행용 파일 묶음입니다. 개념 설명과 섹션별 학습 순서는 웹사이트에서 읽습니다. ZIP 안에는 다음이 들어 있습니다.

- 실행 노트북
- Python 예제 코드
- 작은 예제 데이터
- 실행용 설정 예시
- `.env.example`

압축을 풀면 다음 구조가 보입니다.

```text
amsl-internship-study/
  START_HERE.md
  notebooks/
  examples/
  examples/.env.example
```

웹사이트는 정식 교재를 읽고 파일을 받는 곳입니다. API key를 웹사이트에 입력하지 않습니다.

## 6. `.env` 파일 만들기

API key는 코드에 직접 쓰지 않고 `.env` 파일에 넣습니다.

```powershell
cd amsl-internship-study/examples
Copy-Item .env.example .env
notepad .env
```

`.env`에는 두 줄만 둡니다.

```text
OPENAI_API_KEY=여기에_제공받은_API_KEY
OPENAI_MODEL=gpt-5.4-mini
```

`gpt-5.4-mini`는 현재 검증된 수업용 기본 모델명입니다. 수업에서 안내받은 모델명이 다르면 `OPENAI_MODEL`만 수정합니다.

## 7. 첫 연결 테스트

첫 연결 테스트(smoke test)는 “모델이 좋은 답을 하는지”가 아니라 “내 환경에서 API 호출이 가능한지”를 확인합니다.

```powershell
uv run --python 3.12 --with-requirements requirements.txt python live_openai_smoke.py
```

성공하면 다음과 비슷한 메시지가 나옵니다.

```text
OpenAI live API 연결이 정상적으로 작동합니다.
```

실패하면 아직 Section 1 실습으로 넘어가지 않습니다. 먼저 웹사이트의 `오류 해결` 문서에서 key, model, network, package, path 문제를 확인합니다.

## 8. 노트북 열기

가장 단순한 실습 방식은 uv로 Jupyter를 실행해 노트북을 여는 것입니다. `amsl-internship-study` 폴더로 돌아가서 실행합니다.

```powershell
cd ..
uv run --python 3.12 --with-requirements examples/requirements.txt --with notebook jupyter notebook notebooks/amsl_agentic_ai_live_api_study.ipynb
```

VS Code를 사용한다면 `notebooks/amsl_agentic_ai_live_api_study.ipynb` 파일을 직접 열어도 됩니다. 이 경우 노트북 커널이 수업용 uv/Python 3.12 환경인지 확인합니다. Anaconda나 예전 전역 Python 커널이 선택되어 있으면 패키지 설치와 API 실행 결과가 달라질 수 있습니다.

## 9. Section 0 완료 목표

Section 0의 목표는 모든 개념을 완벽히 이해하는 것이 아닙니다. 목표는 각자 로컬 컴퓨터에서 실제 API 호출이 되는 상태를 만드는 것입니다.

여기까지 되면 Section 0은 충분합니다.

1. 웹사이트에서 Section 0 읽기
2. 실습 파일 ZIP 다운로드
3. `.env` 작성
4. 첫 연결 테스트 성공
5. 노트북 열기
6. Section 1을 시작할 준비 완료

## 10. 오류를 질문할 때

API key는 공유하지 않습니다. 대신 다음 정보를 공유합니다.

- OS
- Python 버전
- 실행한 명령
- 오류 메시지 전체
- 사용한 모델명
- 현재 PowerShell 위치
- notebook 실행인지 script 실행인지

좋은 질문 예시는 다음과 같습니다.

```text
OS: Windows 11
Python: 3.12.4
위치: amsl-internship-study/examples
명령: uv run --python 3.12 --with-requirements requirements.txt python live_openai_smoke.py
모델: gpt-5.4-mini
오류: model_not_found ...
```

Section 1-4의 실제 실행 순서는 [실습 과제](PRACTICALS.md)와 [예제 코드 사용법](EXAMPLES.md)을 봅니다.
