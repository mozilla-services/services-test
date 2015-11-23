#!/bin/bash +x
# $1: the environment to run the test in such as dev or stage

#-------------------
# Install deps
#-------------------

npm install

#-------------------
# Run test
#-------------------
export DISPLAY=:11.0
export NODE_ENV=$1

#TODO: allow test to run in other OSes eventually
npm run dashboard-ubuntu
