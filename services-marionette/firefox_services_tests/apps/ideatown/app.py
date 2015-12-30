# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from apps.base import Base
from marionette_driver import By


class IdeaTown(Base):
    _login_url = 'https://ideatown.stage.mozaws.net'
    _login_with_firefox_button_locator = (
        By.CSS_SELECTOR, 'div.cta-layout a.fxa-alternate')
    _ideatown_sign_me_up_button_locator = (
        By.XPATH, '//a[text()="Sign Me Up!"]')
    _pocket_logo_header_locator = (By.CSS_SELECTOR, 'h1.pocket_logo')

    def launch_signin(self):
        Base.launch(self, self._login_url)

        self.click_element(*self._login_with_firefox_button_locator)
        self.wait_for_element_displayed(*self._ideatown_sign_me_up_button_locator)

        self.click_element(*self._ideatown_sign_me_up_button_locator)
        from firefox_services_tests.apps.fxa.login import LoginPage
        login_page = LoginPage(self.marionette)
        login_page.login_to_fxa()
