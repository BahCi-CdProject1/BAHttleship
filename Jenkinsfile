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
        stage("Run Selenium Test") {
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
    post('Cleanup Dev Pods') {
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
    }
}
    
