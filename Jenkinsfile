def app
pipeline {
    agent any
    stages {
        stage("Pull from Github Repo") {
            steps {
                script{
                    checkout scm
                }
            }
        }
        stage("Run Bah Job to deploy app") {
            steps {
                script {
                    sh "kubectl create -f k8s/job-bah.yaml"
                    def podBah = sh(
                        script: "kubectl get pods -l job-name=selenium-job -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                        ).trim()
                    sh "kubectl wait ${podBah} --for=condition=Ready --timeout=60s"
                    sh "kubectl create -f k8s/svc-dns.yaml"
                }
            }
        }
        stage('Cleanup Dev Pods') {
            steps {
                script {
                    sh('kubectl delete service bahttleship')
                    sh('kubectl delete job bahttleship-job')
                    //sh('kubectl delete job selenium-job')          
                }
            }
        }
    }
  }