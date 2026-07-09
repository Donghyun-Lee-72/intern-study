# START HERE

AMSL Agentic AI 스터디의 **실습 파일 패키지**입니다.

이 ZIP은 교재가 아니라 실행용 파일 묶음입니다. 처음부터 모든 용어를 알 필요는 없습니다.
개념 설명, 섹션별 학습 순서, AI 사용 키와 비용 안내, 오류 해결은 먼저 웹사이트에서 읽습니다.
ZIP 안의 파일은 실행용입니다. `docs.html` 같은 웹 문서는 `file://`로 직접 열면 일부 내용이 보이지 않을 수 있으니, 교재는 아래 웹사이트에서 봅니다.

웹사이트:

```text
https://intern-study.donghyunlee.me
```

권장 흐름은 다음과 같습니다.

1. 웹사이트의 `학습 섹션`에서 Section 0을 읽고 준비를 시작합니다.
2. 내 컴퓨터에서 uv와 uv가 준비한 Python 실행 환경을 확인합니다.
3. 이 ZIP을 압축 해제합니다.
4. 아래 명령으로 첫 연결 테스트를 합니다.
5. 웹사이트의 `학습 섹션`을 보면서 노트북 셀을 순서대로 실행합니다.
6. 실행 후 웹사이트의 `결과 확인`과 비교합니다.
7. 마지막 Section 5에서 Linux/WSL2 개발 환경을 별도로 확인합니다.

## 1. 압축 풀기

다운로드한 zip 파일을 원하는 위치에 압축 해제합니다. 예시는 다음 경로를 기준으로 합니다.

```text
Documents\amsl-internship-study
```

## 2. PowerShell 열기

압축을 푼 폴더에서 PowerShell을 엽니다.

확인:

```powershell
uv --version
uv run --python 3.12 python --version
```

`uv`가 없으면 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

이번 실습에서는 Python을 브라우저에서 따로 다운로드하는 것을 기본 경로로 두지 않습니다.
`uv run --python 3.12 ...` 명령이 필요한 Python을 준비해 실행합니다.
처음 실행할 때 Python 다운로드가 한 번 진행될 수 있습니다.

## 3. API key 설정

```powershell
cd examples
Copy-Item .env.example .env
notepad .env
```

`.env`에는 두 줄만 둡니다.

```text
OPENAI_API_KEY=제공받은_key
OPENAI_MODEL=gpt-5.4-mini
```

`gpt-5.4-mini`는 현재 검증된 수업용 기본 모델명입니다. 수업 중 다른 모델명을 안내받으면 `OPENAI_MODEL` 값만 바꿉니다.

## 4. 첫 연결 테스트

```powershell
uv run --python 3.12 --with-requirements requirements.txt python live_openai_smoke.py
```

성공하면 웹사이트의 `학습 섹션` 탭으로 돌아가 Section 1부터 읽고, 노트북에서 해당 셀을 실행합니다.
실행 결과는 웹사이트의 `결과 확인` 탭과 비교합니다. 문장이 완전히 같을 필요는 없습니다.
정해진 형식, 근거, 답이 없을 때의 처리 방식이 맞는지 확인합니다.
Section 5 Linux/WSL2는 노트북 셀이 아니라 웹사이트의 마지막 개발 환경 섹션으로 진행합니다.

## 5. 파일 구성

- `notebooks/amsl_agentic_ai_live_api_study.ipynb`: 웹사이트 설명을 따라 실행하는 실행 노트북입니다.
- `examples/`: 노트북과 같은 흐름을 Python 파일로 실행해 볼 수 있는 예제 코드입니다.
- `examples/data/`: 문서에서 근거를 찾아 답하는 실습에 사용할 짧은 데이터입니다.
- `examples/.env.example`: API key 설정 예시입니다.

API key는 코드, 채팅, 제출물에 붙여 넣지 않습니다.
