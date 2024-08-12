pipeline {
    agent{
        label 'jenkins-workers'
    }

    environment {
        INBOUND_IMAGE_PREFIX = "${DOCKER_REGISTRY}/mhs/inbound:"
        OUTBOUND_IMAGE_PREFIX = "${DOCKER_REGISTRY}/mhs/outbound:"
        ROUTE_IMAGE_PREFIX = "${DOCKER_REGISTRY}/mhs/route:"
    }

    parameters {
        string (name: "Docker_Hub_Version", defaultValue: "1.0.2", description: "Tagged version in Docker Hub")
      }

    stages {
        stage('Pull from Docker Hub') {
            steps {
                sh "docker pull nhsdev/nia-mhs-inbound:${params.Docker_Hub_Version}"
                sh "docker pull nhsdev/nia-mhs-outbound:${params.Docker_Hub_Version}"
                sh "docker pull nhsdev/nia-mhs-route:${params.Docker_Hub_Version}"
            }
        }

        stage('Push to ECR') {
            steps {
                tagAndPushImage("nhsdev/nia-mhs-inbound:${params.Docker_Hub_Version}", "${INBOUND_IMAGE_PREFIX}${params.Docker_Hub_Version}")
                tagAndPushImage("nhsdev/nia-mhs-outbound:${params.Docker_Hub_Version}", "${OUTBOUND_IMAGE_PREFIX}${params.Docker_Hub_Version}")
                tagAndPushImage("nhsdev/nia-mhs-route:${params.Docker_Hub_Version}", "${ROUTE_IMAGE_PREFIX}${params.Docker_Hub_Version}")
            }
        }
    }
}

int ecrLogin(String aws_region) {
    String dockerLogin = "aws ecr get-login-password --region ${aws_region} | docker login -u AWS --password-stdin \"https://\$(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.${aws_region}.amazonaws.com\""
    return sh(label: "Logging in with Docker", script: dockerLogin, returnStatus: true)
}

void tagAndPushImage(String localImageName, String imageName, String context = '.') {
    if (ecrLogin(TF_STATE_BUCKET_REGION) != 0 )  { error("Docker login to ECR failed") }
    sh label: 'Tag ecr image', script: 'docker tag ' + localImageName + ' ' + imageName
    String dockerPushCommand = "docker push " + imageName
    if (sh (label: "Pushing image", script: dockerPushCommand, returnStatus: true) !=0) { error("Docker push image failed") }
    sh label: 'Deleting local ECR image', script: 'docker rmi ' + imageName
}
