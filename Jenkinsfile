pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'  // Replace with the actual Flask app file
        VIRTUAL_ENV = '.venv'  // Virtual environment folder
        IMAGE_NAME = 'course-webapp'
        IMAGE_TAG = 'v1' // Default tag for staging
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                git credentialsId: 'your-credentials-id', branch: 'main', url: 'https://github.com/Manohar-1305/course-content.git'
            }
        }

        stage('Install python3-venv') {
            steps {
                script {
                    // Use sudo for apt-get commands
                    sh 'sudo apt-get update'
                    sh 'sudo apt-get install -y python3-venv'
                }
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    // Create and activate the virtual environment
                    sh 'python3 -m venv $VIRTUAL_ENV'
                    sh '$VIRTUAL_ENV/bin/pip install --upgrade pip'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install the necessary dependencies
                    sh '$VIRTUAL_ENV/bin/pip install -r requirements.txt'
                    sh '.venv/bin/pip install pytest'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run unit tests using pytest
                    sh '$VIRTUAL_ENV/bin/pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image with the name 'course-webapp'
                    sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
                }
            }
        }
stage('Trivy Scan') {
    steps {
        script {
            // Run Trivy image scan on the locally built Docker image
            sh 'trivy image --format table -o trivy-image-report.html $IMAGE_NAME:$IMAGE_TAG'
        }
    }
}
stage('Push Docker Image to Docker Hub') {
    steps {
        script {
            // Login to Docker Hub using Jenkins credentials (docker-cred)
            withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                sh 'echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin'
            }

            // Tag the local image with Docker Hub repository and tag
            sh 'docker tag $IMAGE_NAME:$IMAGE_TAG manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'

            // Push the image to Docker Hub
            sh 'docker push manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'
          }
        }
      }
    }   
}
