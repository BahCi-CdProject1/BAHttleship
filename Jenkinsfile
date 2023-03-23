def app
pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                script{
                    checkout scm
                }
            }
        }
        stage('Prep - Dependencies') {
            steps {
                nodejs(nodeJSInstallationName: 'Node') {
                    sh 'npm install'
                }
            }
        }  
        stage('Build - Docker Build') {
            steps{
                script {
                    app = docker.build("0xniel/bahttleship")
                }
            }
        }
        stage('Build - Docker Push') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'dockerpwd', variable: 'dockerpwd')]) {
                        sh 'docker login -u 0xniel -p ${dockerpwd}'
                    }
                    sh 'docker push 0xniel/bahttleship'
                }
            }
        }
        stage('Test - Deploy Dev Pod') {
            steps {
                withAWS(credentials: 'my_credential', endpointUrl: 'https://FC86AB859A592865CC5267C69ABD33CE.gr7.us-east-1.eks.amazonaws.com') {
                    script {
                        sh ('aws eks update-kubeconfig --name terraform-eks-demo --region us-east-1')
                        sh "kubectl create -f k8s/job-bah.yaml"
                        def podBah = sh(script: "kubectl get pods -l job-name=bahttleship-job -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                        println "podBah = ${podBah}"
                        sh "kubectl wait pod ${podBah} --for=condition=Ready --timeout=60s"
                        sh "kubectl create -f k8s/svc-dns.yaml"
                    }
                }
            }
        }
        stage('Test - Deploy Selenium') {
            steps {
                withAWS(credentials: 'my_credential', endpointUrl: 'https://FC86AB859A592865CC5267C69ABD33CE.gr7.us-east-1.eks.amazonaws.com') {
                    script {
                        sh ('aws eks update-kubeconfig --name terraform-eks-demo --region us-east-1')
                        sh "kubectl create -f k8s/job-sel.yaml"
                        def podSel = sh(script: "kubectl get pods -l job-name=selenium-job -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                        println "podSel = ${podSel}"
                        sh "kubectl wait pod ${podSel} --for=jsonpath='{.status.phase}'=Succeeded --timeout=60s"
                        def podRun = sh(script: "kubectl logs ${podSel}", returnStdout: true)
                        println "Selenium Test Results \n${podRun}"
                    }
                }
            }
        }
    }
    post('Post Actions') {
        always {
            withAWS(credentials: 'my_credential', endpointUrl: 'https://FC86AB859A592865CC5267C69ABD33CE.gr7.us-east-1.eks.amazonaws.com') {
                script {
                    try {
                        sh('kubectl delete service bahttleship')
                    } catch (Exception e) {
                        println "An error occured during the post-stage: ${e.message}"
                    }
                    try {
                        sh('kubectl delete job bahttleship-job')
                    } catch (Exception e) {
                        println "An error occured during the post-stage: ${e.message}"
                    }
                    try {
                        sh('kubectl delete job selenium-job')
                    } catch (Exception e) {
                        println "An error occured during the post-stage: ${e.message}"
                    }
                }
            }
        }
        success {
            withAWS(credentials: 'my_credential', endpointUrl: 'https://FC86AB859A592865CC5267C69ABD33CE.gr7.us-east-1.eks.amazonaws.com') {
                script {
                    sh ('aws eks update-kubeconfig --name terraform-eks-demo --region us-east-1')
                    sh "kubectl apply -f bahttleship-deployment.yaml"
                }
            }
        }
        failure {
            script {
                def build = currentBuild.rawBuild
                def result = currentBuild.result

                // Summarize the errors that caused the failure
                def failureCauses = build.getFailureCauses()
                def errorSummary = failureCauses.collect {
                    "- ${it.getShortDescription()}"
                }.join("\n")

                // Print the error summary to the console
                println "Pipeline failed with errors:\n${errorSummary}"
            }
        }
    }
}    
