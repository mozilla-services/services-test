# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from firefox_puppeteer.testcases.base import FirefoxTestCase
from marionette_driver import By
from apps.base import Base

#from apps.pocket.app import Push


class Push(Base):
    _login_url = 'http://localhost:3000/test/'
    _pocket_logo_header_locator = (By.CSS_SELECTOR, 'h1.pocket_logo')

    def launch_express(self):
        Base.launch(self, self._login_url)

class TestPush(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.push_page = Push(self.marionette)

    def test_push_mocha(self):
        self.push_page.launch_express()
