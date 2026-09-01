# Practical Agentic AI

이 저장소는 이동현(Donghyun Lee)이 개인적으로 제작한 Agentic AI 학습자료입니다.
어떤 기관의 공식 자료도 아니며, 특정 기관의 승인이나 보증을 의미하지 않습니다.

- 공개 학습 사이트: <https://agentic-ai.donghyunlee.me>

## 구성

- `index.html`, `sections/`: 개념 설명과 단계별 학습 페이지
- `notebooks/`: Section 0–12 실행용 Jupyter Notebook
- `data/`: 문서 처리·검색·평가 실습용 가상 데이터
- `START_HERE.md`: 실습 실행 안내

## 시작하기

저장소를 clone하거나 GitHub의 **Code → Download ZIP**으로 받은 뒤, 저장소 루트에서 다음 명령을 실행합니다.

```bash
uv run --no-project python serve.py
```

공개 사이트 <https://agentic-ai.donghyunlee.me>에서 Section 0부터 진행할 수 있습니다. 로컬 사본은 브라우저에서 `http://127.0.0.1:8767`을 열면 됩니다. Notebook 실행 방법은 `START_HERE.md`를 참고하세요.

## 개인정보와 API 키

- 공개 페이지의 기본 방문 통계에는 Google Analytics 4를 사용하며, Google Signals와 광고 개인화 신호는 비활성화합니다.
- 별도의 자체 방문자 수집기나 D1 데이터베이스로 방문 정보를 전송하지 않습니다.
- 실제 API 키, 개인 식별정보, Notebook 실행 출력은 저장하지 않습니다.
- API 실습은 사용자가 본인 계정에서 발급한 키와 최신 가격·모델 정보를 확인한 뒤 진행해야 합니다.
- 키가 입력된 Notebook은 커밋하거나 공유하지 마세요.

## 저작권

본문과 실습 예제는 별도 표시가 없는 한 이동현이 직접 작성했습니다. 참고자료의 저작권과 이용 조건은 각 원저작자에게 있습니다.
이 저장소에는 별도 오픈소스 라이선스가 부여되어 있지 않습니다.
