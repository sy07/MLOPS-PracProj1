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

        stage('Building and pusing  Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pusing  Docker Image to GCR............'
                        sh '''
                        set -eux
                        export PATH="$PATH:$(GCLOUD_PATH)"

                        gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"

                        gcloud config set project "${GCP_PROJECT}"

                        gcloud auth configure-docker --quiet

                        docker build -t "gcr.io/${GCP_PROJECT}/mlops:latest" .

                        docker push "gcr.io/${GCP_PROJECT}/mlops:latest"
                        '''
                    }
                }
            }
        }
    }
}