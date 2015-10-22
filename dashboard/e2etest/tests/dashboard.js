/*eslint-env mocha */
/*global marionette */

var chai = require('chai')
var helper = require('marionette-helper')
var restmail = require('restmail-client')
var P = require('promise')

var expect = chai.expect

marionette.plugin('helper', helper)
marionette('dashboard', function () {
  const DASHBOARD_URL = 'http://dashboard.stage.mozaws.net' //TODO: move to config file

  var client = marionette.client({
    prefs: {
      'browser.shell.checkDefaultBrowser': false,
      'browser.uitour.enabled': false
    }
  })

  setup(function () {
    client.setSearchTimeout(5000)
    client.goUrl(DASHBOARD_URL)
  })

  test('check links', function (done) {
    waitForElement(client, "#overall")
    var overall_dashboard_link = client.findElement("#overall")
    expect(overall_dashboard_link).to.exist
    overall_dashboard_link.click()
    waitForElement(client, "#dashboard_title")
    var title = client.findElement('#dashboard_title').text()
    expect(title).to.equal("Overall Services QA Metrics and KPIs")
    done()
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
      console.error(err)
      return false
    }
  })
}
