# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from marionette_driver import By

from apps.base import Base


class Pocket(Base):
    _login_url = 'http://localhost:3000/test/'
    _pocket_logo_header_locator = (By.CSS_SELECTOR, 'h1.pocket_logo')

    def launch_signin(self):
        Base.launch(self, self._login_url)


        #self.wait_for_element_displayed(
        #    *self._pocket_start_saving_button_locator)
