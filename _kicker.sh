#!/bin/bash

PROJECT="$1"
TAG="$2"
TEST_ENV=`echo $3 | tr [a-z] [A-Z]`
clear

if [ $# -ne 3 ]; then
    echo
    echo "Usage: $0 <project_name> <tag #> <test env: STAGE | PROD>";
    echo
    echo "Missing param(s). ABORTING!"
    echo
    exit 1
fi

if [ ! -d "$PROJECT" ]; then
    echo
    echo "project: \"$PROJECT\" doesn't exit.  ABORTING!"
    echo
    exit 1
fi

echo
echo "#############################################################"
echo "VERIFYING: ${PROJECT} $TAG - $TEST_ENV"
echo "#############################################################"
echo
cd $PROJECT
pwd
echo

# loop through sub dirs (1 dir / test type) # and execute run.sh for each
array=( $( ls -1p | grep / | sed 's/^\(.*\)/\1/') )

for dir in "${array[@]}"
do
   dir_name=${dir%?}
   echo $dir_name
   echo
   echo "================================================="
   echo "$dir_name" | tr a-z A-Z
   echo "================================================="
   echo
   ./${dir%?}/run.sh
done

echo
echo "MISSION ACCOMPLISHED!"
echo
