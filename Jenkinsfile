pipeline {
    agent any

    stages {
        stage('Prepare Python venv & Version Check') {
            steps {
                bat '''
                REM ===== Python absolute path (entry point) =====
                set PYTHON_EXE=C:\\Users\\qlalf\\AppData\\Local\\Programs\\Python\\Python311\\python.exe

                REM ===== 1. Create virtual environment if not exists =====
                if not exist venv (
                    "%PYTHON_EXE%" -m venv venv
                )

                REM ===== 2. Activate virtual environment =====
                call venv\\Scripts\\activate

                REM ===== 3. Check Python version =====
                for /f "tokens=2 delims= " %%v in ('python --version') do set PY_VER=%%v
                echo Current Python version: %PY_VER%

                if NOT "%PY_VER%"=="3.11.9" (
                    echo ERROR: Python version must be 3.11.9. Aborting build.
                    exit /b 1
                )

                echo OK: Python version check passed
                '''
            }
        }

        stage('Run pytest') {
            steps {
                bat '''
                call venv\\Scripts\\activate

                pip install -r requirements_win.txt

                REM -v : verbose output
                REM -s : show print() output
                REM --junitxml : generate test report for Jenkins
                pytest -vs --junitxml=pytest-report.xml
                '''
            }
        }
    }

    post {
        always {
            echo 'Collecting test reports and artifacts'

            // Pytest result summary in Jenkins UI
            junit allowEmptyResults: true, testResults: 'pytest-report.xml'

            // Selenium screenshots (if exist)
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        }
    }
}
