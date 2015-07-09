clear 
echo
echo "-------------------"
echo "SETUP"
echo "-------------------"
echo

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

npm install

../../_shared/install_ff_nightly.sh

if [ -z "$RUNTIME" ]; then
  #RUNTIME=/Applications/Firefox.app/Contents/MacOS/firefox-bin
  RUNTIME=/Volumes/FirefoxNightly.app/Contents/MacOS/firefox-bin
fi

echo
echo "-------------------"
echo "RUN TEST"
echo "-------------------"
echo
node_modules/.bin/marionette-mocha \
  --host marionette-firefox-host \
  --runtime $RUNTIME \
  --timeout 6000s \
  tests/loop_signup.js
