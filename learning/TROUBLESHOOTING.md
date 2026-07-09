# Troubleshooting: 오류 해결

오류가 나면 먼저 실행한 명령, 현재 폴더, 오류 메시지를 확인합니다. 이번 과정의 기본 터미널은 Windows PowerShell입니다.

## 1. Python 명령이 안 됩니다

먼저 Python이 보이는지 확인합니다.

```powershell
python --version
```

`python` 명령을 찾을 수 없으면 Python 설치 시 **Add python.exe to PATH**가 빠졌을 수 있습니다.

권장 순서:

1. <https://www.python.org/downloads/>에서 Python 3.11 이상을 설치합니다.
2. 설치 첫 화면에서 **Add python.exe to PATH**를 체크합니다.
3. 설치가 끝나면 PowerShell을 완전히 닫고 새로 엽니다.
4. 다시 `python --version`을 실행합니다.

그래도 안 되면 Windows 설정에서 `앱 실행 별칭`을 검색하고, Python 관련 별칭이 python.org 설치와 충돌하지 않는지 확인합니다.

## 2. uv 명령이 안 됩니다

먼저 uv가 설치되어 있는지 확인합니다.

```powershell
uv --version
```

uv가 없다면 설치합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

설치 직후 `uv` 명령을 찾지 못하면 PowerShell을 완전히 닫고 새로 연 뒤 다시 `uv --version`을 실행합니다.

## 3. 현재 폴더가 틀렸습니다

파일을 찾을 수 없다는 오류가 나면 PowerShell이 다른 폴더에 있을 가능성이 큽니다.

```powershell
pwd
ls
```

예제 스크립트를 실행할 때는 보통 아래 위치에 있어야 합니다.

```text
amsl-internship-study/examples
```

## 4. `.env` 파일을 못 읽습니다

API key 오류가 나면 `.env` 파일이 `examples` 폴더 안에 있는지 확인합니다.

```powershell
ls -Force
```

정상이라면 `.env`와 `.env.example`이 함께 보입니다.

`.env` 내용은 두 줄만 둡니다.

```text
OPENAI_API_KEY=제공받은_key
OPENAI_MODEL=gpt-5.4-mini
```

주의할 점:

- 파일 이름이 `.env.txt`가 아니어야 합니다.
- `OPENAI_API_KEY` 앞뒤에 공백이 없어야 합니다.
- API key를 채팅이나 제출물에 붙여 넣지 않습니다.

## 5. API key 오류가 납니다

가능한 원인은 다음과 같습니다.

- API key 오타
- key 앞뒤 공백
- 만료되거나 비활성화된 key
- `.env` 파일 위치 오류
- 네트워크 문제

먼저 첫 연결 테스트(smoke test)만 다시 실행합니다.

```powershell
uv run --with-requirements requirements.txt python live_openai_smoke.py
```

## 6. model not found 오류가 납니다

`OPENAI_MODEL` 값이 계정에서 사용할 수 없는 모델명일 수 있습니다.

해결 방법:

- 안내받은 모델명을 정확히 복사합니다.
- `.env`의 `OPENAI_MODEL`만 수정합니다.
- 모델명을 바꾼 뒤 PowerShell을 다시 열거나 명령을 다시 실행합니다.

## 7. 패키지 import 오류가 납니다

예: `ModuleNotFoundError`, `ImportError`

먼저 requirements 기준으로 실행합니다. 이 방식은 패키지 설치와 실행을 한 번에 처리하므로, 가상환경 활성화가 익숙하지 않아도 따라 하기 쉽습니다.

```powershell
uv run --with-requirements requirements.txt python live_openai_smoke.py
```

계속 실패하면 터미널이 `examples` 폴더 안에 있는지 확인하고, ZIP을 새 폴더에 다시 풀어서 같은 명령을 실행합니다. PowerShell에서 activation이 막히는 경우도 있으므로, 처음 실습에서는 activate를 고집하지 말고 `uv run --with-requirements requirements.txt ...` 방식을 사용합니다.

## 8. 한글이 깨져 보입니다

파일은 UTF-8로 저장해야 합니다. PowerShell 출력이 깨지면 다음을 한 번 실행해 봅니다.

```powershell
chcp 65001
```

## 9. LLM 답변이 매번 조금 다릅니다

정상입니다. LLM은 같은 질문에도 문장이 조금 달라질 수 있습니다.

이번 실습에서 더 중요한 것은 다음입니다.

- JSON 구조가 유지되는지
- Pydantic validation을 통과하는지
- evidence/source id가 유지되는지
- 답이 없을 때 모른다고 처리하는지

## 10. Pydantic validation이 실패합니다

모델이 JSON 형식을 정확히 지키지 않았거나 필드를 빠뜨렸을 수 있습니다.

확인할 것:

- prompt에서 출력 형식을 더 명확히 했는지
- schema의 필드 설명이 충분한지
- 모르는 값 처리 규칙이 있는지
- 모델 출력이 JSON처럼 보이지만 실제 JSON은 아닌지

validation 실패는 나쁜 것만은 아닙니다. 모델 출력이 불안정한 부분을 찾아낸 것이므로, prompt나 schema를 고치면 됩니다.

## 11. RAG 답변이 이상합니다

먼저 검색된 source를 확인합니다. 잘못된 문서 조각이 검색되면 답변도 틀릴 수 있습니다.

확인할 것:

- 질문에 중요한 단어가 들어 있는지
- 검색된 evidence가 질문과 관련 있는지
- answer가 evidence 내용을 실제로 반영하는지
- evidence가 없는데 모델이 추측하지 않는지

## 12. 비용이 걱정됩니다

비용을 줄이려면 다음을 지킵니다.

- 실패한 셀만 다시 실행합니다.
- 전체 노트북을 반복해서 실행하지 않습니다.
- 긴 PDF나 큰 문서를 넣지 않습니다.
- 출력이 너무 길어지지 않게 요청합니다.
- token 사용량 확인 셀을 실행해 기록합니다.

## 13. 질문할 때 무엇을 보내야 하나요?

API key는 보내지 않습니다. 아래 정보만 공유합니다.

- 실행한 명령
- 오류 메시지 전체
- Python 버전
- 현재 폴더
- 사용한 모델명
- notebook 실행인지 script 실행인지

예시:

```text
Python: 3.12.4
위치: amsl-internship-study/examples
명령: uv run --with-requirements requirements.txt python live_openai_smoke.py
모델: gpt-5.4-mini
오류: authentication failed ...
```

## 14. Linux 명령어는 어디서 배우나요?

섹션형 기본 수업은 Windows PowerShell 기준으로 진행합니다. Linux, WSL2, bash, VS Code Remote - WSL은 마지막 `LINUX_SPECIAL_CLASS.md`에서 따로 다룹니다.
