# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from firefox_puppeteer.testcases.base import FirefoxTestCase
from marionette_driver import By
# TODO: Add 'base' from here, or import from "../../services-marionette/firefox_services_tests/apps/base.py"?
from base import Base


class Push(Base):
    _test_url = 'http://localhost:3000/test/'
    _mocha_complete_id = (By.CSS_SELECTOR, 'p#complete')

    def launch_express(self):
        Base.launch(self, self._test_url)
        # TODO: Add code to wait for the #complete id and ensure there were 0 errors.


class TestPush(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.push_page = Push(self.marionette)

    def test_push_mocha(self):
        self.push_page.launch_express()
