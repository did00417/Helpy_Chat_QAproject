pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Run QA Tests') {
            steps {
                bat '''
                    "C:\\Users\\qlalf\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" --version
                    "C:\\Users\\qlalf\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install -r requirements_win.txt
                    "C:\\Users\\qlalf\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pytest -v
                '''
            }
        }
    }
}
