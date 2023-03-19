pipeline {
    agent { dockerfile true }
    tools{
        nodejs "Node"
    }
    stages {
        stage("Pull from Github Repo") {
            steps {
                sh "git pull https://github.com/BahCi-CdProject1/BAHttleship.git"
            }
        }
        stage("Build"){
            steps {
                nodejs(nodeJSInstallationName: 'Node') {
                    sh 'npm install'
                }
            }
        }    
        stage('Build docker image'){
            steps{
                script{
                    sh 'docker build --platform linux/amd64 -t bahttleship .'
                }
            }
        }

    }
}