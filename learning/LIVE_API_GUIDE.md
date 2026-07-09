# Live OpenAI API Guide

이 문서는 제공받은 OpenAI API key를 안전하게 설정하고, 실제 API 연결을 확인하는 방법을 설명합니다.

## 1. API key가 무엇인가요?

API key는 내 코드가 OpenAI API를 사용할 수 있게 해주는 비밀번호 같은 값입니다. 이 key가 있으면 Python 코드가 모델에게 요청을 보내고 답변을 받을 수 있습니다.

따라서 API key는 다음처럼 다룹니다.

- 코드에 직접 적지 않습니다.
- 채팅이나 제출물에 붙여 넣지 않습니다.
- GitHub에 올리지 않습니다.
- 웹사이트에 입력하지 않습니다.
- 내 컴퓨터의 `.env` 파일에만 저장합니다.

## 2. `.env` 파일 만들기

예제 폴더로 이동합니다.

```powershell
cd amsl-internship-study/examples
```

환경 파일을 만듭니다.

```powershell
Copy-Item .env.example .env
notepad .env
```

`.env`에는 아래 두 줄만 둡니다.

```text
OPENAI_API_KEY=제공받은_key
OPENAI_MODEL=gpt-5.4-mini
```

`gpt-5.4-mini`는 현재 검증된 수업용 기본 모델명입니다. 수업에서 다른 저비용 모델명을 안내받으면 `OPENAI_MODEL`만 그 값으로 바꿉니다.

## 3. 첫 연결 테스트(smoke test)는 무엇인가요?

첫 연결 테스트(smoke test)는 가장 작은 연결 확인입니다. 이 테스트의 목적은 다음 네 가지를 확인하는 것입니다.

- API key가 맞는지
- 모델명이 맞는지
- 인터넷과 OpenAI API 연결이 되는지
- 필요한 Python 패키지가 설치되어 있는지

노트북에서는 `첫 연결 테스트(smoke test)` 섹션을 실행합니다. PowerShell에서는 다음 명령을 실행합니다.

```powershell
uv run --python 3.11 --with-requirements requirements.txt python live_openai_smoke.py
```

정상 예시는 다음과 같습니다.

```text
OpenAI live API 연결이 정상적으로 작동합니다.
```

이 단계가 실패하면 Section 1-4 실습을 진행하지 말고 먼저 오류를 해결합니다.

## 4. 전체 live 검증은 언제 쓰나요?

`test_live_examples.py`는 전체 예제 흐름이 실제 API로 끝까지 실행되는지 확인하는 파일입니다. 이 명령은 여러 번의 API 호출을 사용하므로, 첫 연결 테스트와 Section 1-4 실습이 끝난 뒤 마지막 확인용으로만 실행합니다.
`RUN_LIVE_OPENAI_TESTS`를 켜지 않으면 유료 호출을 하지 않고 skip 메시지만 출력됩니다.

```powershell
$env:RUN_LIVE_OPENAI_TESTS="1"
uv run --python 3.11 --with-requirements requirements.txt python test_live_examples.py
Remove-Item Env:\RUN_LIVE_OPENAI_TESTS
```

정상 예시는 다음과 같습니다.

```text
all_live_tests_passed
usage_totals {'calls': 3, 'input_tokens': ..., 'output_tokens': ..., 'total_tokens': ...}
```

일반 실습에서는 노트북의 Section 1-4 셀을 순서대로 실행하면 됩니다.

## 5. API 비용은 왜 생기나요?

API 호출은 모델에게 입력을 보내고 답변을 받는 요청입니다. 입력과 출력은 token이라는 단위로 계산됩니다. 글을 많이 보내거나 긴 답변을 많이 받으면 token 수가 늘고, token 수에 따라 비용이 생깁니다.

이번 수업은 제공받은 수업용 API key를 사용하는 흐름을 기준으로 합니다. 학생 개인 결제카드를 등록하지 않습니다. 별도로 안내받지 않았다면 개인 OpenAI 계정에 결제수단을 추가할 필요가 없습니다.

기본 계산식은 다음과 같습니다.

```text
예상 비용 = input token 수 × input token 단가 + output token 수 × output token 단가
```

이번 실습의 전체 노트북 1회 실행은 정상 경로 기준 약 12회 API 호출, 약 4,500 token 정도로 측정되었습니다. JSON 형식 수정 재시도, 모델 응답 길이, 재실행 횟수에 따라 더 늘 수 있으므로 여유 있게 1만 token 안팎으로 생각하면 됩니다.

정확한 금액은 실제 모델의 최신 가격표에 따라 달라집니다. mini 계열 모델을 쓰면 한 명이 전체 예제를 한 번 도는 비용은 보통 작게 유지됩니다.
문서의 계산 예시는 계산 방법을 보여주기 위한 가상의 예시이며, 실제 단가는 수업에서 제공받은 모델의 최신 가격표를 기준으로 확인합니다.

## 6. 비용을 줄이는 방법

- 실패한 셀만 다시 실행합니다.
- 전체 노트북을 불필요하게 반복 실행하지 않습니다.
- 긴 PDF나 큰 문서를 넣지 않습니다.
- 출력 형식을 짧고 구조적으로 요청합니다.
- 제공받은 mini/저비용 모델명을 사용합니다.

## 7. 실습 후 기록할 것

실습을 마치면 다음을 기록합니다.

- 사용한 모델명
- 실행한 노트북 섹션
- 성공한 셀과 실패한 셀
- 대략적인 token 사용량
- validation 통과 여부

API key 자체는 기록하거나 제출하지 않습니다.

## 8. 흔한 오류

### authentication 오류

가능한 원인:

- API key 오타
- key 앞뒤 공백
- 만료되거나 비활성화된 key
- `.env` 파일 위치 오류

확인 명령:

```powershell
pwd
ls -Force
```

`.env` 파일은 `examples` 폴더 안에 있어야 합니다.

### model not found 오류

가능한 원인:

- `OPENAI_MODEL` 이름이 틀렸습니다.
- 계정에서 해당 모델을 사용할 수 없습니다.

해결:

- 안내받은 모델명을 정확히 복사합니다.
- 모델명이 바뀌면 `.env`의 `OPENAI_MODEL`만 수정합니다.

### rate limit 또는 billing 오류

가능한 원인:

- 짧은 시간에 너무 많이 호출했습니다.
- 계정 한도나 결제 설정에 문제가 있습니다.

해결:

- 반복 실행을 멈춥니다.
- 실행한 명령과 오류 메시지를 확인합니다.
- 질문할 때 key는 지우고 오류 메시지만 공유합니다.

## 9. Structured output 방식

이번 실습은 모델에게 JSON 형식으로 답하게 하고, 그 결과를 Pydantic으로 검증하는 방식으로 시작합니다. 이 방식은 “모델 출력이 코드에서 믿고 쓸 수 있는 데이터인지 확인한다”는 감각을 배우기 좋습니다.

실제 개발에서는 OpenAI API의 JSON Schema 또는 Structured Outputs 기능으로 출력 구조를 더 강하게 제한할 수 있습니다. 이 기능은 확장 단계에서 다룹니다.
