#!/bin/bash +x

#-------------------
# Install deps
#-------------------

npm install

#-------------------
# Run test
#-------------------
export DISPLAY=:11.0

npm run dashboard-ubuntu
