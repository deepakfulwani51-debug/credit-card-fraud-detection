pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'classicalsloth' // Your Docker Hub username
        IMAGE_NAME      = 'credit-card-fraud-detection'
        IMAGE_TAG       = "${BUILD_NUMBER}" 
    }

    stages {
        stage('1. Source Checkout') {
            steps {
                echo 'Pulling latest source code from GitHub...'
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo "Baking application code into Docker image version: ${IMAGE_TAG}..."
                script {
                    localImage = docker.build("${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('3. Publish to Docker Hub') {
            steps {
                echo 'Authenticating and pushing immutable image to the cloud...'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        localImage.push()
                        localImage.push('latest')
                    }
                }
            }
        }
    }
}
