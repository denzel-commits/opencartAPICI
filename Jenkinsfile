pipeline{
    agent {
        node{
            label 'docker-agent-python311'
        }
    }
    environment{
        PYTHONPATH = "${WORKSPACE}"
    }
    parameters{
        string(name: 'BASE_URL', defaultValue: 'http://192.168.1.127:8081', description: 'Enter system Base URL')
        choice(name: 'WORKERS_NUMBER', choices: ['1', '2', '3', '4'], description: 'Select the number of selenium workers')
        choice(name: 'LOG_LEVEL', choices: ['WARNING', 'INFO'], description: 'Log level')
    }
    stages{
        stage("Build"){
            steps{
                echo "Building..."
                sh 'pip install -r requirements.txt'
            }
        }
        stage("Test"){
            steps{
                echo "Testing..."
                sh 'python -m pytest -n=${params.WORKERS_NUMBER}'
            }
        }
    }
    post{
        always{
                allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'target/allure-results']]
                ])
        }
    }
}