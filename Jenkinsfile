pipeline {
    agent any

    stages {
        stage('Python 가상환경 준비 및 버전 확인') {
            steps {
                bat '''
                REM ===== Python 절대경로 (최초 진입점) =====
                set PYTHON_EXE=C:\\Users\\qlalf\\AppData\\Local\\Programs\\Python\\Python311\\python.exe

                REM ===== 1. 가상환경 생성 =====
                if not exist venv (
                    "%PYTHON_EXE%" -m venv venv
                )

                REM ===== 2. 가상환경 활성화 =====
                call venv\\Scripts\\activate

                REM ===== 3. Python 버전 확인 =====
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

        stage('pytest 실행') {
            steps {
                bat '''
                call venv\\Scripts\\activate

                pip install -r requirements_win.txt
                pytest
                '''
            }
        }
    }
}
