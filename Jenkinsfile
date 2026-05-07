pipeline {
    agent any

    environment {
        IMAGE_NAME = "myadavg/booking-app:v3"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/myadavg/Booking-platform.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                kubectl set image deployment/booking-app \
                booking-app=myadavg/booking-app:v3
                '''
            }
        }
    }
}