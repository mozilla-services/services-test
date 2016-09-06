#!/bin/bash +x

virtualenv venv
. venv/bin/activate
python ./setup.py develop

fab setup || exit 1
echo "-----------------------------------Setup Complete----------------------------------"
echo "---------------------------Virtual Environment Activated---------------------------"
python ./test/control-script.py -a ${ACCOUNT_AUTH} -n ${NUMBERS} -H ${GATEWAY_HOST_NUMBER} || exit 1
echo "------------------------------------Completed Test---------------------------------"
echo "------------------------------------Begin Teardown---------------------------------"
fab teardown || exit 1
echo "-----------------------------------Finished Teardown-------------------------------"
echo "---------------------------Virtual Environment Deactivated-------------------------"
deactivate
rm -fr venv
