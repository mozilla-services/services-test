#push the docker image that was built prior to testing
docker push mozservicesqa/dashboard
# run vagrant provision on the controller to get the new docker image deployed
ssh -oStrictHostKeyChecking=no -i ~/.ssh/services-qa-jenkins.pem ubuntu@services-qa-jenkins-controller.stage.mozaws.net "cd services-qa-utils; vagrant provision services-qa-dashboard;"
