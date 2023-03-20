def app
pipeline {
    agent any
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
                    app = docker.build("0xniel/bahttleship")
                }
            }
        }
        stage('Push image to Docker Hub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'dockerpwd', variable: 'dockerpwd')]) {
                        sh 'docker login -u 0xniel -p ${dockerpwd}'
                    }
                    sh 'docker push 0xniel/bahttleship'
                }
            }
        }
        stage("Deploy to k8") {
            steps {
                script {
                    withKubeConfig([credentialsId: 'kubeconfig', serverUrl: 'https://8622FE57C97489289EB482BB6016F1A7.gr7.us-east-1.eks.amazonaws.com']) {
                        sh 'kubectl apply -f bahttleship-deployment.yaml'
                    }
                }
            }
        }

    }
}