# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from firefox_services_tests.apps.base import Base
from firefox_services_tests.helpers import utils

from marionette_driver import By


class LoginPage(Base):
    _fxa_email_input_locator = (By.CSS_SELECTOR, 'input.email')
    _fxa_password_input_locator = (By.ID, 'password')
    _fxa_sign_in_button_locator = (By.ID, 'submit-btn')
    _fxa_sign_in_header_locator = (By.ID, 'fxa-signin-header')
    _fxa_sign_up_header_locator = (By.ID, 'fxa-signup-header')
    _fxa_age_input_locator = (By.ID, 'age')
    _fxa_create_account_link_locator = (By.CSS_SELECTOR, 'a.sign-up')
    _fxa_accept_request_permission_button_locator = (By.ID, 'accept')
    _fxa_signup_complete_header_locator = (By.ID, 'fxa-signup-complete-header')
    _pocket_start_saving_button_locator = (
        By.XPATH, '//a[text()="Start Saving"]')
    _pocket_logo_header_locator = (By.CSS_SELECTOR, 'h1.pocket_logo')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

    def login_to_fxa(self, app_header):
        self.wait_for_element_displayed(*self._fxa_sign_in_header_locator)
        self.marionette.find_element(*self._fxa_email_input_locator)\
            .send_keys('tryloopprod@mailinator.com')
        self.marionette.find_element(*self._fxa_password_input_locator)\
            .send_keys('tryloopprod')
        self.click_element(*self._fxa_sign_in_button_locator).click()
        self.wait_for_element_displayed(*app_header)

    def sign_up_for_fxa(self):
        self.wait_for_element_displayed(*self._fxa_sign_in_header_locator)
        self.click_element(*self._fxa_create_account_link_locator)
        self.wait_for_element_displayed(*self._fxa_sign_up_header_locator)
        email_address = utils.generate_random_email_address()
        self.send_keys_to_element(
            *self._fxa_email_input_locator, **{'string': email_address})
        self.send_keys_to_element(
            *self._fxa_password_input_locator, **{'string': 'password'})
        self.send_keys_to_element(
            *self._fxa_age_input_locator, **{'string': '21'})
        self.click_element(*self._fxa_sign_in_button_locator)
        self.wait_for_element_displayed(*self._fxa_email_input_locator)
        assert self.marionette.find_element(
            *self._fxa_email_input_locator).get_attribute('value') == email_address
        self.wait_for_element_displayed(
            *self._fxa_accept_request_permission_button_locator)
        self.click_element(*self._fxa_accept_request_permission_button_locator)
        verification_url = utils.check_generated_email(email_address)
        while verification_url is None:
            verification_url = utils.check_generated_email(
                email_address)
        self.launch(verification_url)
        self.wait_for_element_displayed(
            *self._pocket_start_saving_button_locator)
        self.click_element(*self._pocket_start_saving_button_locator)
        self.wait_for_element_not_displayed(
            *self._pocket_start_saving_button_locator)
        self.wait_for_element_displayed(*self._pocket_logo_header_locator)
