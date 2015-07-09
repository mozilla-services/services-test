var Promise = require('promise');
var expect = require('chai').expect;

var profile = require('../profile');

marionette.plugin('helper', require('marionette-helper'));
marionette('loop', function() {
  var client = marionette.client(profile);

  suiteSetup(function() {
  });

  setup(function() {
    client.setSearchTimeout(10000)
  });

  suiteTeardown(function() {
  });

  test('clicking on hello icon', function() {
    client.setContext('chrome');

    client
      .findElement(':root')
      .findElement('#loop-button')
      .click()

    //client
    //  .findElement('#loop-notification-panel')

    // client.waitFor(function () {
    //   return client.findElement('#loop-button')
    //   // client.findElement('#fte-button');
    // });

    // client.waitFor(function () {
    //   return client.findElement('#loop-notification-panel');
    // });

    var loopDoc = client.findElement('#loop-panel-iframe');

    client.switchToFrame(loopDoc);
    client.findElement('#fte-button').click();

      //.findElement('#fte-button')
      //.click()
      //.switchToFrame('chat-frame')

    // console.log('clicked loop button');

    // client.findElement('#downloads-button')
      //.click()


/*
    client
      .switchToFrame('chatbox')

    client.findElement('.signin-link a')
      .click()*/

    // Wait around for a bit to see what happens when we click hello.
    return sleep(50000000);
  });
});

function sleep(millis) {
  return new Promise(function(resolve) {
    setTimeout(resolve, millis);
  });
}
