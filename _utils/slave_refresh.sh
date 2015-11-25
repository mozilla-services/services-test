#!/bin/bash

if [ $# -eq 0 ]; then
    echo
    echo "WARNING!"
    echo "This script will destroy your Firefox profiles!"
    echo "if you really want to do this, run: $0 DESTROY"
    exit
    echo
else
    echo "BEGIN SLAVE REFRESH...."
    echo
fi

releases=( NN DE BETA GR )

echo
echo "--------------------"
echo "SET ENVS"
echo "--------------------"
echo
echo "set env vars"
python config_parser.py
cat "$PWD/.env"
. "$PWD/.env"

echo
echo "--------------------"
echo "UNINSTALL FIREFOXES"
echo "--------------------"
echo

for release in "${releases[@]}"
do
   PREFIX=$release
   eval "ABS_PATH_FIREFOX_BIN=\$PATH_FIREFOX_$release/$PATH_FIREFOX_BIN"
   echo "ABS_PATH_FIREFOX_BIN: $ABS_PATH_FIREFOX_BIN"
   echo "uninstalling: $release"
   if [ $OSTYPE == "cygwin"* ]; then
      #$ABS_PATH_FIREFOX_BIN/uninstall/helper -ms
      echo "$ABS_PATH_FIREFOX_BIN/uninstall/helper -ms"
   else
      #rm -rf $ABS_PATH_FIREFOX_BIN
      echo "rm -rf $ABS_PATH_FIREFOX_BIN"
   fi
done

echo
echo "--------------------"
echo "UNINSTALL PROFILES"
echo "--------------------"
echo
#rm -rf $PATH_FIREFOX_PROFILES
echo "rm -rf $PATH_FIREFOX_PROFILES"
ls "$PATH_FIREFOX_PROFILES"

echo
echo "--------------------"
echo "INSTALL FIREFOXES"
echo "--------------------"
echo
echo "mozdownloaden...."
echo
#Download the latest Firefox Aurora build for Windows (32bit):
#mozdownload --type=daily --branch=mozilla-aurora --platform=win32

for release in "${releases[@]}"
do
   PREFIX=$release
   eval "PATH_FIREFOX=\$PATH_FIREFOX_$release"
   echo "PATH_FIREFOX: $PATH_FIREFOX"
   echo "uninstalling: $release"
   if [ $OSTYPE == "cygwin"* ]; then
      echo "mozdownload (OS: cygwin): $release"
   else
      echo "mozdownload (OS:other): $release"
   fi
done

echo
echo "install"
echo "...some OS specific copypasta here...."


echo "DONE!"
