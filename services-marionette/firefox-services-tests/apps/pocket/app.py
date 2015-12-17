# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from firefox_services_tests.apps.base import Base

from marionette_driver import By


class Pocket(Base):
    _login_url = 'https://getpocket.com/login'
    _pocket_chrome_button = (By.ID, "#pocket-button")
    _login_with_firefox_button_locator = (
        By.CSS_SELECTOR, 'a.btn.login-btn-firefox')

    def launch_signin(self):
        Base.launch(self, self._login_url)
        self.marionette.find_element(
            *self._login_with_firefox_button_locator).click()
        from firefox_services_tests.apps.fxa.login import LoginPage
        return LoginPage(self.marionette)

    def click_pocket_chrome_button(self):
        with self.marionette.using_context(self.CHROME):
            self.wait_for_element_displayed(
                *self._pocket_chrome_button).click()
