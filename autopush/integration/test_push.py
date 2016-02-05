# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from firefox_puppeteer.testcases.base import FirefoxTestCase
from marionette_driver import By
# TODO: If Marionette base files will reside locally, we'll want to
#       reference a relative path to those, rather than duplicate
#       base file for every single test.
from base import Base


MARIONETTE_TIMEOUT = 60000  # 60 seconds


class Push(Base):
    _test_url = 'http://localhost:3000/test/'
    _mocha_complete_id = (By.CSS_SELECTOR, 'p#complete')
    _mocha_passes_id = (By.CSS_SELECTOR, 'li.passes em')
    _mocha_failures_id = (By.CSS_SELECTOR, 'li.failures em')
    _mocha_errors_id = (By.CSS_SELECTOR, 'pre.error')

    def print_summary(self, num_mocha_passes, num_mocha_failures):
        print("\nMOCHA SUMMARY\n-------------")
        print("passed: {0}".format(num_mocha_passes))
        print("failed: {0}".format(num_mocha_failures))
        print("")

    def launch_express(self):
        self.marionette.timeout = MARIONETTE_TIMEOUT

        Base.launch(self, self._test_url)

        # Wait for "#complete" element
        self.wait_for_element_displayed(*self._mocha_complete_id)

        num_mocha_passes = int(self.marionette.find_element(*self._mocha_passes_id).text)
        num_mocha_failures = int(self.marionette.find_element(*self._mocha_failures_id).text)

        self.print_summary(num_mocha_passes, num_mocha_failures)

        if num_mocha_failures == 0:
            # All our mocha tests have passed. Exit now. \o/
            return

        mocha_errors_list = self.marionette.find_elements(*self._mocha_errors_id)

        for item in mocha_errors_list:
            print("----------")
            print(item.text)
            print("\n")

        assert False


class TestPush(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.push_page = Push(self.marionette)

    def test_push_mocha(self):
        self.push_page.launch_express()
