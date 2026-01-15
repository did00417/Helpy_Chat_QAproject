pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Python 가상환경 준비 및 버전 확인') {
            steps {
                bat '''
                REM =========================
                REM 1. 가상환경 생성 (없으면)
                REM =========================
                if not exist venv (
                    python -m venv venv
                )

                REM =========================
                REM 2. 가상환경 활성화
                REM =========================
                call venv\\Scripts\\activate

                REM =========================
                REM 3. Python 버전 확인
                REM =========================
                for /f "tokens=2 delims= " %%v in ('python --version') do set PY_VER=%%v

                echo 현재 Python 버전: %PY_VER%

                if NOT "%PY_VER%"=="3.11.9" (
                    echo ❌ Python 3.11.9가 아닙니다. 빌드를 중단합니다.
                    exit /b 1
                )

                echo ✅ Python 버전 조건 통과
                '''
            }
        }

        stage('의존성 설치 및 pytest 실행') {
            steps {
                bat '''
                REM 가상환경 다시 활성화
                call venv\\Scripts\\activate

                REM pip 최신화
                pip install --upgrade pip

                REM 의존성 설치
                if exist requirements_win.txt (
                    pip install -r requirements_win.txt
                )

                REM pytest 실행 (-v: 상세 로그, -s: print 출력 허용)
                pytest -vs
                '''
            }
        }
    }
}
