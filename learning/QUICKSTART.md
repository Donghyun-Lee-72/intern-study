# Quickstart: 첫 실행 순서

이 문서는 웹사이트에서 Section 0을 읽은 뒤, 실습 파일 ZIP으로 첫 연결 테스트까지 실행하는 안내입니다. 자세한 배경 설명은 `ORIENTATION.md`에 있고, 여기서는 바로 따라 칠 명령을 정리합니다.

## 1. 필요한 것

- Windows PowerShell
- Python 3.11 이상
- uv
- VS Code 또는 Jupyter Notebook
- 제공받은 OpenAI API key

먼저 PowerShell에서 Python이 보이는지 확인합니다.

```powershell
python --version
```

여기서 오류가 나면 Python이 설치되어 있지 않거나 PATH가 잡히지 않은 상태입니다. Python 3.11 이상을 설치하고, 설치 화면에서 **Add python.exe to PATH**를 체크한 뒤 PowerShell을 완전히 닫고 새로 열어 다시 실행합니다.

## 2. uv 설치 확인

uv는 이번 실습에서 패키지 설치와 실행을 도와주는 도구입니다.

```powershell
uv --version
```

uv가 없으면 다음 명령으로 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

## 3. 실습 파일 ZIP 다운로드

처음 시작할 때는 노트북만 받지 말고 **실습 파일 ZIP**을 받습니다. ZIP 안에는 노트북, 예제 코드, 데이터, 실행용 설정 예시가 들어 있습니다. 개념 설명과 섹션별 학습 순서는 웹사이트에서 읽습니다.

압축을 풀면 `amsl-internship-study` 폴더가 생깁니다. PowerShell에서 그 폴더로 이동합니다.

```powershell
cd amsl-internship-study
```

## 4. API key 설정

예제는 실제 OpenAI API를 호출합니다. API key는 코드에 직접 쓰지 않고 `.env` 파일에 넣습니다.

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

`gpt-5.4-mini`는 현재 검증된 수업용 기본 모델명입니다. 제공받은 모델명이 다르면 `OPENAI_MODEL` 값만 바꿉니다.

## 5. 첫 연결 테스트

먼저 첫 연결 테스트(smoke test)만 실행합니다. 이 단계는 “실습 내용이 맞는지”가 아니라 “내 API key, 모델명, 네트워크, 패키지 설치가 맞는지”를 확인하는 단계입니다.

```powershell
uv run --with-requirements requirements.txt python live_openai_smoke.py
```

성공하면 다음과 비슷한 메시지가 나옵니다.

```text
OpenAI live API 연결이 정상적으로 작동합니다.
```

여기서 실패하면 Section 1 실습으로 넘어가지 말고 웹사이트의 `오류 해결` 문서를 먼저 확인합니다.

## 6. 노트북 열기

가장 권장하는 실습 방식은 VS Code Notebook입니다. VS Code에서 `notebooks/amsl_agentic_ai_live_api_study.ipynb` 파일을 직접 열면 됩니다.

Jupyter 화면으로 열고 싶다면 `amsl-internship-study` 폴더로 돌아간 뒤 uv로 실행합니다.

```powershell
cd ..
uv run --with notebook jupyter notebook notebooks/amsl_agentic_ai_live_api_study.ipynb
```

PowerShell에서는 `uv`로 패키지를 관리하고, 노트북 안의 `%pip install ...` 셀은 현재 노트북 실행 환경에 필요한 패키지를 설치합니다. 둘 다 같은 목적이지만 실행 위치가 다릅니다.

## 7. 노트북 실행 순서

노트북은 위에서 아래로 순서대로 실행합니다.

1. 패키지 설치 셀
2. API key/model 설정 셀
3. 첫 연결 테스트(smoke test) 셀
4. Section 1-4 노트북 실습 셀
5. token 사용량 확인 셀

중간에 오류가 나면 전체 노트북을 처음부터 다시 실행하지 말고, 실패한 셀과 바로 앞 셀부터 확인합니다. 오류 설명은 웹사이트의 `오류 해결` 탭을 봅니다.

Section 5 Linux/WSL2는 노트북 셀이 아니라 마지막 개발 환경 섹션입니다. 웹사이트의 `학습 섹션`과 `Section 5 상세 자료`를 보면서 진행합니다.

## 8. 스크립트로 실행하고 싶을 때

노트북 대신 Python 파일을 직접 실행하고 싶으면 `examples` 폴더에서 아래 명령을 순서대로 실행합니다.

```powershell
uv run --with-requirements requirements.txt python section1_llm_api.py
uv run --with-requirements requirements.txt python section2_structured_output.py
uv run --with-requirements requirements.txt python section2_langchain_contract.py
uv run --with-requirements requirements.txt python section3_rag.py
uv run --with-requirements requirements.txt python section3_langchain_rag.py
uv run --with-requirements requirements.txt python section4_workflow.py
```

`test_examples.py`는 비용이 들지 않는 로컬 확인용입니다. 실제 LLM 품질을 보는 파일은 아닙니다.

```powershell
uv run --with-requirements requirements.txt python test_examples.py
```

## 9. API key 주의사항

- API key를 코드, 채팅, 제출물에 붙여 넣지 않습니다.
- `.env` 파일을 GitHub에 올리지 않습니다.
- 화면 공유 중에는 API key가 보이지 않게 합니다.
- 오류를 질문할 때는 key를 지우고 오류 메시지만 공유합니다.

## 10. 실패하면 무엇을 공유하나요?

질문할 때는 다음 정보를 함께 공유하면 원인을 빨리 찾을 수 있습니다.

- 실행한 명령
- 전체 오류 메시지
- Python 버전
- 사용한 모델명
- PowerShell에서 현재 위치한 폴더

예시:

```text
Python: 3.12.4
위치: amsl-internship-study/examples
명령: uv run --with-requirements requirements.txt python live_openai_smoke.py
모델: gpt-5.4-mini
오류: model_not_found ...
```
