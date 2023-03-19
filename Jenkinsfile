def app
pipeline {
    agent {
        any
        // docker {
        //     image 'ubuntu'
        //     args '-u root:sudo -v $HOME/workspace/Docker_Pipeline:/bahttleship'
        // }
    }
    tools{
        nodejs "Node"
    }

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