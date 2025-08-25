pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment {
        registry_backend   = 'truong1301/obj_d'
        registry_frontend  = 'truong1301/ui_ux'
        registryCredential = 'dockerhub'
    }

    stages {

        stage('Build & Push') {
            when {
                anyOf {
                    changeset "**/backend/**"
                    changeset "**/frontend/**"
                    changeset "Dockerfile.backend"
                    changeset "Dockerfile.frontend"
                }
            }
            steps {
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
                    sh 'docker compose --file OBD-docker-compose.yaml up -d --build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '🔎 Waiting for containers to be healthy...'
                    sh 'docker compose --file OBD-docker-compose.yaml wait obj_module'
                    sh 'docker compose --file OBD-docker-compose.yaml wait ui_ux_module'

                    echo '🔎 Testing API endpoints...'
                    sh 'curl -f http://localhost:30000/metadata'
                    sh 'curl -f http://localhost:8501'
                }
            }
        }
    }
}
