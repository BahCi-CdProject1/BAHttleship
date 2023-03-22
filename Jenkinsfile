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
                    sh ('aws eks update-kubeconfig --name terraform-eks-demo --region us-east-1')
                    def jobBah = readFile('k8s/job-bah.yaml')
                    def deployResult = kubernetesDeploy(
                        kubeYaml: jobBah,
                        deployType: 'create',
                        wait: true
                        )
                        if (deployResult.status != 'Success') {
                        error("Failed to deploy job: ${deployResult.message}")
                        }
            }
            }
        }
        stage('Run Selenium Test') {
            steps {
                script {
                    def jobSel = readFile('k8s/job-sel.yaml')
                    
                    //deploy the selenium pod
                    def deployResult = kubernetesDeploy(
                        kubeYaml: jobSel,
                        deployType: 'create',
                        wait: true
                        )
                        if (deployResult.status != 'Success') {
                        error("Failed to deploy job: ${deployResult.message}")
                        }
                    //find the pod name
                    def podName = sh(
                        script: "kubectl get pods -l job-name=selenium-job -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    // wait for the pod to complete the job
                    sh "kubectl wait --for=condition=complete pod/${podName}"
                    
                    // get the logs for the pod
                    def logs = sh(
                        script: "kubectl logs ${podName}",
                        returnStdout: true
                    )
                    
                    // print the logs to the console
                    echo "Job logs:\n${logs}"

            }
        }

        stage('Cleanup Dev Pods') {
        steps {
            script {
                sh('kubectl delete service bahttleship')
                sh('kubectl delete job bahttleship-job')
                sh('kubectl delete job selenium-job')          
            }
        }
      }
    }
  }
}