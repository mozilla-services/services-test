#!/bin/bash

echo "--------------------------"
echo "REMOVE mozilla-central"
echo "--------------------------"

rm -rf mozilla-central

echo "--------------------------"
echo "CLONE mozilla-central"
echo "--------------------------"

hg clone http://hg.mozilla.org/mozilla-central

echo "--------------------------"
echo "SYMLINK mozilla-central"
echo "--------------------------"

cd "${HOME_JENKINS_SLAVE}"
ln -sf "${HOME_JENKINS_SLAVE}/workspace/${JOB_NAME}/_utils/mozilla-central" mozilla-central > /home/ubuntu/.bash_aliases
