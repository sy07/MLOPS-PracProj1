pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
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
    }
}