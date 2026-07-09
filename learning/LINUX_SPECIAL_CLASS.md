# Section 5: Linux/WSL2 개발 환경 입문

이 문서는 Section 1-4의 Agentic AI 기본 실습을 마친 뒤 마지막에 다룰 Linux 개발 환경 입문 자료입니다. 초반 실습은 Windows PowerShell + uv로 시작하고, Linux/WSL2는 Section 5에서 분리해 다룹니다. 이유는 환경 구축이 LLM/RAG 학습을 방해하지 않게 하기 위해서입니다.

수강생 중 일부는 Ubuntu 기반 환경이나 기본 명령어를 접해본 적이 있을 수 있습니다. 그래도 Section 5는 처음 쓰는 학생도 따라올 수 있게 `pwd`, `ls`, `cd`부터 시작합니다. 이미 경험이 있는 학생은 Windows와 WSL2의 경로 차이, VS Code Remote - WSL, uv 환경 재구성에 더 집중합니다.

## 1. Section 5의 목표

Section 5가 끝났을 때 학생은 다음을 설명하고 직접 해볼 수 있어야 합니다.

- Linux가 무엇이고 왜 개발에서 자주 쓰이는지 설명합니다.
- Ubuntu, Debian, Red Hat 계열 같은 Linux 종류를 아주 얕게 구분합니다.
- Windows에서 WSL과 WSL2가 어떤 역할을 하는지 이해합니다.
- WSL2에 Ubuntu를 설치하고 기본 터미널을 열 수 있습니다.
- Windows 파일과 Linux 파일 위치가 다르다는 것을 이해합니다.
- 파일 탐색기에서 WSL 파일 시스템을 열 수 있습니다.
- VS Code로 WSL 내부 폴더에 원격 접속할 수 있습니다.
- `bash`, `shell`, `terminal`, `command`의 차이를 대략 설명합니다.
- 기본 Linux 명령어로 폴더 이동, 파일 확인, 패키지 설치, Python 실행을 할 수 있습니다.

## 2. 왜 Linux를 배우는가

많은 AI/ML 개발 환경은 Linux 기준으로 설명됩니다.

- 서버와 클라우드 VM은 Linux가 많습니다.
- 연구 코드와 오픈소스 예제가 Linux 명령어를 기준으로 쓰이는 경우가 많습니다.
- GPU 서버, Docker, 배포, cron, shell script는 Linux 경험이 있으면 훨씬 이해하기 쉽습니다.
- Windows에서 개발하더라도 WSL2를 쓰면 Linux 환경을 로컬에서 연습할 수 있습니다.

하지만 Linux는 처음부터 필수로 넣으면 환경 설정 부담이 큽니다. 그래서 Section 1-4에서는 PowerShell + uv로 실습을 끝내고, Section 5에서 Linux를 따로 배웁니다.

## 3. Linux 종류를 아주 얕게 보기

학생이 처음 알아야 할 수준은 다음 정도면 충분합니다.

- Ubuntu: 입문자와 개발자가 많이 쓰는 배포판. WSL2에서 기본 선택지로 적합합니다.
- Debian: 안정성을 중시하는 계열. Ubuntu의 기반이 되는 배포판입니다.
- Red Hat/Fedora/CentOS 계열: 기업 서버에서 자주 보이는 계열입니다.
- Arch 계열: 직접 구성하는 성격이 강해 초심자 수업용으로는 우선순위가 낮습니다.

Section 5에서는 **Ubuntu on WSL2**만 다룹니다.

## 4. WSL과 WSL2

WSL은 Windows 안에서 Linux 환경을 사용할 수 있게 해주는 기능입니다. WSL2는 더 실제 Linux에 가까운 방식으로 동작합니다.

학생이 알아야 할 핵심:

- WSL2는 Windows 안에 Linux 개발 공간을 하나 더 만드는 것입니다.
- Windows 파일 경로와 Linux 파일 경로가 다릅니다.
- WSL2 안에서 설치한 Python/package는 Windows PowerShell의 Python/package와 다릅니다.
- VS Code는 Remote - WSL 확장을 통해 WSL 내부 폴더를 직접 열 수 있습니다.

## 5. WSL2 설치 흐름

실제 수업 전에 Windows 버전과 권한을 확인한 뒤 명령을 확정합니다.

예상 흐름:

```powershell
wsl --install
wsl --set-default-version 2
wsl --list --verbose
```

설치 중 확인할 것:

- 재부팅이 필요한지.
- Ubuntu 사용자 이름과 비밀번호를 만들었는지.
- 설치 후 `Ubuntu` 앱이 열리는지.
- `wsl --list --verbose`에서 VERSION이 2로 보이는지.

## 6. 문서함 GUI로 접근하기

처음 WSL2를 사용할 때 가장 헷갈리는 지점은 “내 파일이 어디 있는가”입니다.

WSL 파일은 Windows 파일 탐색기에서 다음처럼 접근할 수 있습니다.

```text
\\wsl$
```

예상 설명:

- `\\wsl$`는 Windows 파일 탐색기에서 Linux 파일 시스템을 보여주는 특수 경로입니다.
- Ubuntu 안의 홈 폴더는 보통 `\\wsl$\\Ubuntu\\home\\사용자이름` 근처에 있습니다.
- Windows의 `C:\Users\...`와 WSL의 `/home/...`는 다른 위치입니다.
- 개발 프로젝트는 가능하면 WSL의 `/home/사용자이름/projects` 아래에 둡니다.

## 7. VS Code 원격 접근

VS Code에서 WSL을 편하게 쓰려면 Remote - WSL 확장을 사용합니다.

예상 흐름:

1. VS Code 설치.
2. Extensions에서 `WSL` 또는 `Remote Development` 설치.
3. Ubuntu 터미널에서 프로젝트 폴더로 이동.
4. 다음 명령 실행:

```bash
code .
```

이 명령은 현재 Linux 폴더를 VS Code로 여는 명령입니다. 처음 실행하면 VS Code가 WSL 서버 구성 요소를 설치할 수 있습니다.

## 8. bash/shell/terminal 구분

초심자용 설명:

- Terminal: 명령어를 입력하는 창.
- Shell: 명령어를 해석해서 실행하는 프로그램.
- Bash: Linux에서 많이 쓰는 shell 중 하나.
- PowerShell: Windows에서 많이 쓰는 shell.

같은 `python --version` 명령이라도 PowerShell에서 실행하는지, WSL Ubuntu bash에서 실행하는지에 따라 다른 Python이 잡힐 수 있습니다.

## 9. 기본 Linux 명령어

처음에는 아래만 익히면 충분합니다.

이미 Linux 명령어를 써 본 학생은 명령어 이름을 외우는 데서 멈추지 말고, “현재 어느 폴더에서 실행 중인지”, “이 Python은 Windows Python인지 WSL Python인지”, “파일이 Windows 쪽에 있는지 Linux 쪽에 있는지”를 확인하는 습관을 만듭니다.

```bash
pwd                  # 지금 위치
ls                   # 파일 목록
ls -la               # 숨김 파일까지 자세히 보기
cd folder_name       # 폴더 이동
cd ..                # 상위 폴더로 이동
mkdir projects       # 폴더 만들기
touch memo.txt       # 빈 파일 만들기
cat memo.txt         # 파일 내용 보기
cp a.txt b.txt       # 파일 복사
mv a.txt folder/     # 파일 이동 또는 이름 변경
rm memo.txt          # 파일 삭제
python3 --version    # Python 버전 확인
which python3        # 어떤 Python이 실행되는지 확인
```

주의:

- `rm`은 휴지통으로 보내지 않고 바로 삭제할 수 있습니다.
- 처음에는 `rm -rf`를 쓰지 않습니다.
- 명령어를 복사해 실행하기 전에 지금 위치를 `pwd`로 확인합니다.

## 10. Linux에서 uv와 Python 실행

Section 5에서는 Windows에서 배운 uv 개념을 Linux에서도 다시 확인합니다.

예상 흐름:

```bash
python3 --version
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
uv run --python 3.11 python --version
uv run --python 3.11 --with-requirements requirements.txt python live_openai_smoke.py
```

이번 과정에서는 Linux에서도 Python library를 uv로 준비하고, 별도 안내가 없으면 `uv run --python 3.11 --with-requirements ...` 형식을 우선 사용합니다.
Linux package 설치나 `sudo`, `apt`가 필요한 경우에는 먼저 이유를 설명하고 별도 명령을 안내받은 뒤 진행합니다.

Windows PowerShell과 Linux shell 비교:

- Windows 경로 구분자: `\`
- Linux 경로 구분자: `/`
- Windows PowerShell 명령과 Linux bash 명령은 서로 다를 수 있습니다.

## 11. Section 5 진행 흐름

90~120분 기준:

1. 10분: Linux가 왜 중요한지.
2. 10분: Linux 종류와 Ubuntu 선택 이유.
3. 20분: WSL2 설치와 Ubuntu 실행.
4. 15분: Windows 파일과 WSL 파일 위치 차이.
5. 15분: VS Code Remote - WSL 연결.
6. 20분: 기본 명령어 실습.
7. 20분: uv/Python smoke test를 Linux에서 다시 실행.

## 12. 성공 기준

학생이 아래를 할 수 있으면 충분합니다.

- Ubuntu 터미널을 열 수 있습니다.
- `pwd`, `ls`, `cd`, `mkdir`를 사용할 수 있습니다.
- `\\wsl$`로 Linux 파일에 접근할 수 있습니다.
- VS Code로 WSL 폴더를 열 수 있습니다.
- Windows PowerShell 환경과 WSL Linux 환경이 서로 다르다는 점을 설명할 수 있습니다.
- Linux에서도 Python/uv 환경을 만들 수 있습니다.
