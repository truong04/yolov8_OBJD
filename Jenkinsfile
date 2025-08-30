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

            steps {
                script {
                    echo '🐳 Building backend image for deploy...'
                    dockerImage_backend = docker.build(
                        "${registry_backend}:1.0.${BUILD_NUMBER}",
                        "-f model/Dockerfile model"
                    )

                    echo '📤 Pushing backend image to DockerHub...'
                    docker.withRegistry('', registryCredential) {
                        dockerImage_backend.push()
                        dockerImage_backend.push('latest')
                    }

                    echo '🐳 Building frontend image for deploy...'
                    dockerImage_frontend = docker.build(
                        "${registry_frontend}:1.0.${BUILD_NUMBER + 4}",
                        "-f UI_UX/Dockerfile UI_UX"
                    )
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
        
                    // Run docker-compose
                    sh 'docker-compose -f OBD-docker-compose.yaml up -d --build'
        
                    // 🔹 Ensure Jenkins container is connected to truong-mlop network
                    sh '''
                    JENKINS_ID=$(docker ps -q -f name=jenkins)
                    if [ ! -z "$JENKINS_ID" ]; then
                        if ! docker network inspect truong-mlop | grep -q $JENKINS_ID; then
                            echo "🔹 Connecting Jenkins container to truong-mlop network..."
                            docker network connect truong-mlop $JENKINS_ID
                        else
                            echo "🔹 Jenkins already connected to truong-mlop"
                        fi
                    fi
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '🔎 Waiting 60 seconds for containers to start...'
                    sh 'sleep 60'
                
                    echo '🔎 Testing API endpoints...'
                    sh 'curl -f http://obj_d:30000/metadata'
                    sh 'curl -f http://ui_ux:8501'
                }
            }
        }
    }
}
