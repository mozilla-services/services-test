/*eslint-env mocha */
/*global marionette */

var chai = require('chai')
var helper = require('marionette-helper')
var restmail = require('restmail-client')
var P = require('promise')

var expect = chai.expect

marionette.plugin('helper', helper)
marionette('dashboard', function () {
  const DASHBOARD_URL = 'https://getpocket.com/ff_signup'

  var client = marionette.client({
    prefs: {
      'browser.shell.checkDefaultBrowser': false,
      'browser.uitour.enabled': false
    }
  })
  var email

  setup(function () {
    client.goUrl(DASHBOARD_URL)
  })

  test('check links', function (done) {
    waitForElement(client, 'a')
    var overall_dashboard_link = client.findElement("//a[@href='/quality']")
    expect('a[href=/quality]').dom.to.have.count(1)
    expect(overall_dashboard_link).to.exist
    overall_dashboard_link.click()
    waitForElement(client, 'div.ready')
    var overall_header = client.findElement("//div[text()='Overall Services QA Metrics and KPIs']")
    expect(overall_header).to.exist
  })
})

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
