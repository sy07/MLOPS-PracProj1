pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "primal-ivy-475212-d0"
        GCLOUD_PATH ="/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins..................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-token', url: 'https://github.com/sy07/MLOPS-PracProj1.git']])
                }
            }
        }

        stage('Setting up Virtual Environment and installing dependencies'){
            steps{
                script{
                    echo 'Setting up Virtual Environment and installing dependencies'
                    sh ''' 
                    set -eux
                    python3 -m venv "$VENV_DIR"
                    . "${VENV_DIR}/bin/activate"
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing Docker Image to GCR'){
            agent {
                docker {
                image 'google/cloud-sdk:slim'
                args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            environment {
                GCP_PROJECT = 'primal-ivy-475212-d0'
            }
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                sh '''
                    set -eux

                    # Install Docker CLI inside this container (Debian-based)
                    apt-get update
                    apt-get install -y --no-install-recommends docker.io
                    docker --version

                    gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
                    gcloud config set project "${GCP_PROJECT}"
                    # Configure only the registry you need (faster, fewer warnings)
                    gcloud auth configure-docker gcr.io --quiet

                    docker build -t "gcr.io/${GCP_PROJECT}/mlops:latest" .
                    docker push "gcr.io/${GCP_PROJECT}/mlops:latest"
                '''
                }
            }
            }

        stage('Deploying to Google Cloud Run'){
            agent {
                docker {
                image 'google/cloud-sdk:slim'
                args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            environment {
                GCP_PROJECT = 'primal-ivy-475212-d0'
            }
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                echo 'Deploying to Google Cloud Run.............'                    
                sh '''
                    set -eux

                    # Install Docker CLI inside this container (Debian-based)
                    apt-get update
                    apt-get install -y --no-install-recommends docker.io
                    docker --version

                    gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
                    gcloud config set project "${GCP_PROJECT}"
                    
                    gcloud run deploy mlops \
                        --image=gcr.io/${GCP_PROJECT}/mlops:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow=unauthenticated
                '''
                }
            }
        }    
    }
}