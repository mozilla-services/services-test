#!/bin/bash +x

# TODO: replace this with env var
#HOME_JENKINS_SLAVE="/home/jenkins-slave"

echo  "--------------------------"
echo "INSTALL FIREFOXES"
echo  "--------------------------"
echo

virtualenv venv
chmod -R 777 venv
. ./venv/bin/activate
pip install ff-tool

ff -c nightly --install-only
ff -c aurora --install-only
ff -c beta --install-only
ff -c release --install-only

ls ${HOME_JENKINS_SLAVE}

echo
echo  "--------------------------"
echo "SYMLINK FIREFOXES"
echo  "--------------------------"
echo

ln -sf "${HOME_JENKINS_SLAVE}/workspace/${JOB_NAME}/_temp/browsers" "${HOME_JENKINS_SLAVE}/firefoxes" 

ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-nightly/firefox" "${HOME_JENKINS_SLAVE/firefox-nightly"
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-developer-edition/firefox" "${HOME_JENKINS_SLAVE}/firefox-developer-edition"
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-beta/firefox" "${HOME_JENKINS_SLAVE/firefox-beta"
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-release/firefox" "${HOME_JENKINS_SLAVE/firefox-release"
ln -sf "${HOME_JENKINS_SLAVE}/firefox-nightly" "${HOME_JENKINS_SLAVE/firefox"

echo  "--------------------------"
echo "ADD FIREFOXES TO PATH"
echo  "--------------------------"

echo "export PATH=${HOME_JENKINS_SLAVE}:${PATH}" > /home/ubuntu/.bash_aliases
