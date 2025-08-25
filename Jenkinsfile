pipeline{
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry_backend = 'truong1301/obj_d'
        registry_frontend = 'truong1301/ui_ux'
        //:v1.0.0
        registryCredential = 'dockerhub'
    }

    stages{
        stage('Deploy with Docker Compose') {
            steps {
                script {
                    sh 'docker compose -f OBD-docker-compose.yaml up -d --build'
                }
            }
        }
        stage('Test'){
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps{
                echo '🔎 Testing model...'
                sh 'sleep 10' // đợi container chạy ổn định
                sh 'curl -f http://localhost:8080/metadata'
                sh 'pip install -r requirements.txt && pytest'
            }
        }

        stage('Build'){
            steps{
                script {
                    echo '🐳 Building backend image for deploy...'
                    dockerImage_backend = docker.build("${registry_backend}:1.0.${BUILD_NUMBER}")

                    echo '📤 Pushing backend image to DockerHub...'
                    docker.withRegistry('', registryCredential) {
                        dockerImage_backend.push()
                        dockerImage_backend.push('latest')
                    }

                    echo '🐳 Building frontend image for deploy...'
                    dockerImage_frontend = docker.build("${registry_frontend}:1.0.${BUILD_NUMBER + 4}")

                    echo '📤 Pushing frontend image to DockerHub...'
                    docker.withRegistry('', registryCredential) {
                        dockerImage_frontend.push()
                        dockerImage_frontend.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo '🚀 Deploying with docker-compose...'
                    sh 'docker compose -f OBD-docker-compose.yaml up -d --build'
                }
            }
        }
    }
}
