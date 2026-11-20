pipeline {
    agent any

    environment {
        APP_IMAGE   = 'dance-studio-app'
        NGINX_IMAGE = 'dance-studio-nginx'
        // уникальный тег образа для каждой сборки: например main-12, dev-5
        TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }

    stages {
        // скачивание исходного кода той ветки, в которой лежит этот Jenkinsfile
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // проверка, что Jenkins видит Docker
        stage('Docker Info') {
            steps {
                bat 'docker version'
                bat 'docker compose version'
            }
        }

        // сборка двух образов: приложения и веб-сервера nginx
        stage('Build Images') {
            steps {
                bat 'docker build -t %APP_IMAGE%:%TAG% .'
                bat 'docker build -t %NGINX_IMAGE%:%TAG% nginx'
            }
        }

        // автотесты запускаются ВНУТРИ собранного образа приложения
        stage('Tests') {
            steps {
                bat 'docker run --rm %APP_IMAGE%:%TAG% python -m pytest -v'
            }
        }

        // проверка синтаксиса конфигурации nginx
        stage('Nginx Config Test') {
            steps {
                bat 'docker run --rm --add-host app:127.0.0.1 %NGINX_IMAGE%:%TAG% nginx -t'
            }
        }

        // остановка версии из ЛР1 (задача планировщика), чтобы она не мешала; только для main
        stage('Stop Old Version') {
            when { branch 'main' }
            steps {
                powershell '''
                    Stop-ScheduledTask -TaskName 'LibraryApp' -ErrorAction SilentlyContinue
                    Unregister-ScheduledTask -TaskName 'LibraryApp' -Confirm:$false -ErrorAction SilentlyContinue
                    exit 0
                '''
            }
        }

        // развёртывание: проверенные образы помечаются как latest и запускаются через docker compose; только для main
        stage('Deploy') {
            when { branch 'main' }
            steps {
                bat 'docker tag %APP_IMAGE%:%TAG% %APP_IMAGE%:latest'
                bat 'docker tag %NGINX_IMAGE%:%TAG% %NGINX_IMAGE%:latest'
                bat 'docker compose up -d --no-build --remove-orphans'
            }
        }

        // проверка, что приложение отвечает через nginx на порту 80
        stage('Health Check') {
            when { branch 'main' }
            steps {
                retry(10) {
                    sleep time: 3, unit: 'SECONDS'
                    bat 'curl.exe -fsS http://localhost/health'
                }
                bat 'docker compose ps'
                echo 'Application deployed in Docker: http://localhost'
            }
        }
    }

    post {
        always {
            // удаляем временные теги сборки, чтобы не копить образы (latest остаётся)
            bat(script: 'docker rmi %APP_IMAGE%:%TAG% %NGINX_IMAGE%:%TAG%', returnStatus: true)
        }
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'CI/CD pipeline failed!'
        }
    }
}
