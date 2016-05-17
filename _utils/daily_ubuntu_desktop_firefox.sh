#!/bin/bash +x

echo  "--------------------------"
echo "INSTALL FIREFOXES"
echo  "--------------------------"


virtualenv venv
chmod -R 777 venv
. ./venv/bin/activate
pip install ff-tool
#pip install -r requirements.txt
#python setup.py develop

ff -c nightly --install-only
ff -c aurora --install-only
ff -c beta --install-only
ff -c release --install-only

HOME_JENKINS="/home/jenkins-slave"

echo  "--------------------------"
echo "SYMLINK FIREFOXES"
echo  "--------------------------"


cd "${HOME_JENKINS}"
rm firefoxes
ln -sf "${HOME_JENKINS}/workspace/${JOB_NAME}/_temp/browsers" firefoxes 

ln -sf "${HOME_JENKINS}/firefoxes/firefox-nightly/firefox" firefox-nightly
ln -sf "${HOME_JENKINS}/firefoxes/firefox-developer-edition/firefox" firefox-developer-edition
ln -sf "${HOME_JENKINS}/firefoxes/firefox-beta/firefox" firefox-beta
ln -sf "${HOME_JENKINS}/firefoxes/firefox-release/firefox" firefox-release
ln -sf "${HOME_JENKINS}/firefox-nightly" firefox

echo  "--------------------------"
echo "ADD FIREFOXES TO PATH"
echo  "--------------------------"

echo "export PATH=${HOME_JENKINS}:${PATH}" > /home/ubuntu/.bash_aliases
