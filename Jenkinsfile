pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Run QA Tests') {
            steps {
                bat '''
                    python --version
                    pip --version
                    pip install -r requirements_win.txt
                    pytest -v
                '''
            }
        }
    }
}
