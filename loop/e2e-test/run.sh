if [ -z "$RUNTIME" ]; then
  RUNTIME=/Applications/Firefox.app/Contents/MacOS/firefox-bin
fi

node_modules/.bin/marionette-mocha \
  --host marionette-firefox-host \
  --runtime $RUNTIME \
  --timeout 6000s \
  tests/loop_signup.js
