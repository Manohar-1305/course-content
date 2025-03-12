pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'  // Replace with the actual Flask app file
        VIRTUAL_ENV = '.venv'  // Virtual environment folder
        IMAGE_NAME = 'course-web-app'
        IMAGE_TAG = 'v3' // Default tag for staging
        ENVIRONMENT = 'dev'  // Set your environment here (e.g., 'poc', 'prod')
        SCANNER_HOME = '/opt/sonar-scanner'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Manohar-1305/course-content.git'
            }
        }

        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage('Install python3-venv') {
            steps {
                script {
                    sh 'sudo apt-get update'
                    sh 'sudo apt-get install -y python3-venv'
                }
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    sh 'python3 -m venv $VIRTUAL_ENV'
                    sh '$VIRTUAL_ENV/bin/pip install --upgrade pip'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '$VIRTUAL_ENV/bin/pip install -r requirements.txt || ls -l'
                    sh '$VIRTUAL_ENV/bin/pip install pytest'
                }
            }
        }

        stage('OWASP FS Scan') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh '$VIRTUAL_ENV/bin/pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    script {
                        sh '''
                        /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectName=Flaskapp \
                        -Dsonar.projectKey=Flaskapp
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    sh 'trivy image --format table -o trivy-image-report.html $IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Snyk Security Scan') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'Snyk-Token', variable: 'SNYK_TOKEN')]) {
                        sh '''
                        snyk auth $SNYK_TOKEN
                        snyk container test $IMAGE_NAME:$IMAGE_TAG --severity-threshold=high --json > snyk-report.json
                        snyk-to-html -i snyk-report.json -o snyk-report.html
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'snyk-report.json, snyk-report.html', fingerprint: true
                }
                failure {
                    echo "Snyk scan failed! Check snyk-report.json for details."
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin'
                    }
                    sh 'docker tag $IMAGE_NAME:$IMAGE_TAG manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'
                    sh 'docker push manoharshetty507/$IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh '''
                    docker run -d --name course-web-container -p 5000:5000 $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Prune Docker Images') {
            steps {
                script {
                    sh 'docker system prune -af --volumes'
                }
            }
        }
    }
}
