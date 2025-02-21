# Jenkins worker image

The files in this folder are used to create the image of a Jenkins worker for the Jenkins [amazon-ecs plugin].

[amazon-ecs plugin]: https://wiki.jenkins.io/display/JENKINS/Amazon+EC2+Container+Service+Plugin

Usage:
1. Make sure you're logged into AWS with the appropriate credentials on your computer.
2. Find out what the latest version of the jenkins-worker is by searching inside the `jenkins-worker` ECR registry.
3. You can either replace the current build, if your change is low-risk, or create a new version allowing you
   the ability to rollback.
4. Run these commands, specifying the version you wish to publish as.
   ```shell
   VERSION=0.8
   REGISTRY="$(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.eu-west-2.amazonaws.com"
   aws ecr get-login-password --region eu-west-2 | docker login -u AWS --password-stdin $REGISTRY
   docker buildx build --platform linux/amd64 --tag $REGISTRY/jenkins-worker:$VERSION --push .
   ```
5. If you have specified a new version, you'll need to generate a new ECS Task Definition revision pointing to 
   that image label.
   You can then specify that revision within Jenkins -> Configure System -> ECS agent template -> Task Definition Override,
   All subsequent Jenkins builds will use that new worker image, and if you want to rollback the previous revision
   can be placed within the Task Definition Overview box.