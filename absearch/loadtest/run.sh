#!/bin/sh
# execute sanity load test
# $1: github project name
rm -rf $1
git clone http://github.com/mozilla-services/$1
cd $1/loadtests
make test
