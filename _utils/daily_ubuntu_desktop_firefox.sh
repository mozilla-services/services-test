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

echo
echo  "--------------------------"
echo "CLEANUP FIREFOXE SYMLINKS"
echo  "--------------------------"
echo
cd ${HOME_JENKINS_SLAVE}
rm -rf firefox*
ls -la

echo
echo  "--------------------------"
echo "SYMLINK FIREFOXES"
echo  "--------------------------"
echo


ln -sf "${HOME_JENKINS_SLAVE}/workspace/${JOB_NAME}/_utils/_temp/browsers" firefoxes

ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-nightly/firefox" firefox-nightly
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-developer-edition/firefox" firefox-developer-edition
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-beta/firefox" firefox-beta
ln -sf "${HOME_JENKINS_SLAVE}/firefoxes/firefox-release/firefox" firefox-release
ln -sf "${HOME_JENKINS_SLAVE}/firefox-nightly" firefox
ls -la

echo
echo  "--------------------------"
echo "ADD FIREFOXES TO PATH"
echo  "--------------------------"
echo

echo "export PATH=${HOME_JENKINS_SLAVE}:${PATH}" > /home/ubuntu/.bash_aliases
echo
