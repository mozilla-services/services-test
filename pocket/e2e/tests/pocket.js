/*eslint-env mocha */
/*global marionette */

var chai = require('chai')
var helper = require('marionette-helper')
var restmail = require('restmail-client')
var P = require('promise')

var expect = chai.expect

const POCKET_QUEUE_URL = 'https://getpocket.com/a/queue/'
const PAGE_URL = 'https://www.nytimes.com/'

marionette.plugin('helper', helper)
marionette('getpocket.com', function () {
  const SIGNUP_URL = 'https://getpocket.com/ff_signup'

  var client = marionette.client({
    prefs: {
      'browser.shell.checkDefaultBrowser': false,
      'browser.uitour.enabled': false
    }
  })
  var email

  setup(function () {
    email = randomEmail()
    client.goUrl(SIGNUP_URL)
  })

  test('sign up', function (done) {
    fxaSignup(client, email).then(function () {
      return restmail(email).then(function (messages) {
        messages.forEach(function (message) {
          var xlink = message.headers['x-link']
          if (xlink) {
            client.goUrl(xlink)
          }
        })
      }).then(function () {
        return new P(function (resolve, reject) {
          setTimeout(function () {
            waitForElement(client, '.gsf_sendtips')

            client
              .findElement('.gsf_sendtips')
              .click()

            client
              .findElement('.button_container .button')
              .click()

            waitForElement(client, '.button_container')

            client
              .findElement('.button_container .button')
              .click()

            resolve()
          }, 8000)
        })
      }).then(function () {
        savePageToPocket(client, PAGE_URL)
      }).then(function () {
        checkPocketForPage(client, PAGE_URL)
      }).then(done)
    }).catch(function (err) {
      console.error(err)
      done(err)
    })
  })
})

/**
 * Signs the specified email address up to Firefox Accounts.
 * @param  {Object} client Marionette client.
 * @param  {String} email  [description]
 * @return {Promise}
 */
function fxaSignup (client, email) {
  return new P(function (resolve, reject) {
    const HEADER_TEXT = 'Create a Firefox Account\nto continue to Pocket'
    const SUBMIT_TEXT = 'Sign up'
    const PERMISSION_TEXT = 'Request for permission'

    // Wait for page load...
    waitForElement(client, '#fxa-signup-header')

    var headerText = client.findElement('#fxa-signup-header').text()
    var submitText = client.findElement('#submit-btn').text()
    expect(headerText).to.equal(HEADER_TEXT)
    expect(submitText).to.equal(SUBMIT_TEXT)

    client
      .findElement('.email')
      .sendKeys([email])

    client
      .findElement('#password')
      .sendKeys(['password'])

    client
      .findElement('.show-password-label')
      .click()

    client
      .findElement('#fxa-age-year')
      .sendKeys(['1990'])

    client
      .findElement('#submit-btn')
      .click()

    // Wait for page refresh...
    waitForElement(client, '#fxa-permissions-header')

    var permissionText = client.findElement('#fxa-permissions-header').text()
    expect(permissionText).to.equal(PERMISSION_TEXT)

    client
      .findElement('#accept')
      .click()

    // Wait for page refresh...
    waitForElement(client, '.verification-email-message')

    resolve()
  })
}

/**
 * Saves the specified URL to your Pocket list.
 * @param  {Object} client Marionette client.
 * @param  {String} url    The URL to navigate to and save.
 * @return {undefined}
 */
function savePageToPocket (client, url) {
  // Navigate to the specified URL.
  client
    .goUrl(url)

  client
    .setContext('chrome');

  // Click the Pocket button.
  client
    .findElement(':root')
    .findElement('#pocket-button')
    .click()

  client
    .setContext('content')
}

/**
 * Checks your Pocket items for a specific saved URL.
 * @param  {Object} client Marionette client.
 * @param  {String} url    A URL to check for.
 * @return {Boolean}       Returns `true` if the specified URL was found, otherwise `false`.
 */
function checkPocketForPage (client, url) {
  client.goUrl(POCKET_QUEUE_URL)

  waitForElement(client, '.item')

  var itemLinks = client.findElements('.item_link')
  console.log('found %d saved item(s)', itemLinks.length)
  var hasLink = itemLinks.some(function (el, idx) {
    console.log('item %d => %s', idx, el.getAttribute('href'))
    return el.getAttribute('href') === url
  })

  expect(hasLink).to.be.true
  return hasLink
}

/**
 * Generates a random email address.
 * @param  {String} domain The domain for the email address. Default: "restmail.net".
 * @return {String}        A random email address with the format `test0.0000@restmail.net`, where "0.0000" is a random number.
 */
function randomEmail (domain) {
  domain = domain || 'restmail.net'
  return ('test' + Math.random() + '@' + domain).trim()
}

/**
 * Wrapper for `client.waitFor()`.
 * @param  {Object} client Marionette client.
 * @param  {String} el     Selector for element to wait for.
 * @return {Object}        The element.
 */
function waitForElement (client, el) {
  client.waitFor(function () {
    try {
      return client.findElement(el)
    } catch (err) {
      return false
    }
  })
}
