#!/bin/bash +x
# $1: test branch

rm -rf services-quality-dashboard
git clone http://github.com/mozilla-services/services-quality-dashboard
cd services-quality-dashboard
git checkout $1
docker build -t mozservicesqa/dashboard .
