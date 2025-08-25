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
                    sh '''
                    for CONTAINER in obj_d ui_ux; do
                        if [ $(docker ps -aq -f name=$CONTAINER) ]; then
                            echo "🔹 Removing existing container $CONTAINER..."
                            docker rm -f $CONTAINER
                        fi
                    done
                    '''
        
                    // Remove old network if exists
                    sh '''
                    NETWORK_NAME=$(docker network ls --filter name=mlops-lab02_main_truong-mlop -q)
                    if [ ! -z "$NETWORK_NAME" ]; then
                        echo "🔹 Removing existing network $NETWORK_NAME..."
                        docker network rm $NETWORK_NAME
                    fi
                    '''
                    sh 'docker-compose -f OBD-docker-compose.yaml up -d --build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '🔎 Waiting for containers to be healthy...'
                
                    def wait_for_healthy = { container_name ->
                        sh """
                        STATUS=""
                        until [ "\$STATUS" == "healthy" ]; do
                            STATUS=\$(docker inspect --format='{{.State.Health.Status}}' $container_name 2>/dev/null || echo "starting")
                            echo "Waiting for $container_name... Status: \$STATUS"
                            sleep 2
                        done
                        """
                    }
                
                    wait_for_healthy("obj_module")
                    wait_for_healthy("ui_ux_module")
                
                    echo '🔎 Testing API endpoints...'
                    sh 'curl -f http://localhost:30000/metadata'
                    sh 'curl -f http://localhost:8501'
                }
            }
        }
    }
}
