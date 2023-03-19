pipeline {
    agent any
    tools{
        nodejs "Node"
    }
    def app
    stages {
        stage("Pull from Github Repo") {
            steps {
                // sh "git pull https://github.com/BahCi-CdProject1/BAHttleship.git"
                script{
                    checkout scm
                }
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
                script {
                    app = docker.build("bahttleship")
                }
            }
        }

    }
}