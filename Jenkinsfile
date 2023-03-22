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
                        def podBah = sh(
                            script: "kubectl get pods -l job-name=bahttleship-job -o jsonpath='{.items[0].metadata.name}'",
                            returnStdout: true
                            ).trim()
                        sh "kubectl wait ${podBah} --for=condition=Ready --timeout=60s"
                        sh "kubectl create -f k8s/svc-dns.yaml"
                    }
                }
            }
        }
        stage('Cleanup Dev Pods') {
            steps {
                withAWS(credentials: 'my_credential', endpointUrl: 'https://FC86AB859A592865CC5267C69ABD33CE.gr7.us-east-1.eks.amazonaws.com') {
                    script {
                        sh('kubectl delete service bahttleship')
                        sh('kubectl delete job bahttleship-job')
                        //sh('kubectl delete job selenium-job')          
                    }
                }
            }
        }
    }
}