# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from firefox_puppeteer.testcases.base import FirefoxTestCase

from apps.ideatown.app import IdeaTown


class TestIdeaTownCreateNewFxaSignIn(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.ideatown_page = IdeaTown(self.marionette)
        # TODO: Probably have some Firefox Accounts login info

    def test_create_new_fxa_account_sign_into_pocket(self):
        self.ideatown_page.launch_signin()
