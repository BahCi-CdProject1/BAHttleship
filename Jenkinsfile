pipeline {
    agent any
    tools{
        nodejs "Node"
    }
    stages {
        stage("Pull from Github Repo") {
            steps {
                sh "git clone https://github.com/BahCi-CdProject1/BAHttleship.git"
            }
        }
        stage("Build"){
            steps {
                nodejs(nodeJSInstallationName: 'Node') {
                    sh 'npm install'
                }
            }
        }    

        // stage("Push file to web instance") {
        //     steps {
        //         sh "scp -r -v -o StrictHostKeyChecking=no -i /var/lib/jenkins/.ssh/test-app1.pem /var/lib/jenkins/workspace/pipeline-test1/web*/* ubuntu@10.64.10.1:/var/www/html"
        //     }
        // }
    }
}