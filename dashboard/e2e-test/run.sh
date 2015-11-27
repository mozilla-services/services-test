#!/bin/bash +x
# $1: the environment to run the test in such as dev or stage

#-------------------
# Install deps
#-------------------

npm install

#-------------------
# Env vars
#-------------------
export DISPLAY=:11.0
export NODE_ENV=$1

#-------------------
# Run server if required
#-------------------

if [ "$1" == "dev" ]; then
  docker run -t -i -d -P -p 80:80 mozservicesqa/dashboard
fi

#-------------------
# Run test
#-------------------
npm run dashboard-ubuntu
