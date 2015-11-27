#push the docker image that was built prior to testing
docker push mozservicesqa/dashboard
# run vagrant provision on the controller to get the new docker image deployed
ssh -i ~/.ssh/services-qa-jenkins.pem ubuntu@52.91.46.204 "cd services-qa-utils; vagrant provision services-qa-dashboard;"
