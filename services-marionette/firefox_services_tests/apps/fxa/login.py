# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from helpers import utils
from marionette_driver import By

from apps.base import Base


class LoginPage(Base):
    _fxa_email_input_locator = (By.CSS_SELECTOR, 'input.email')
    _fxa_password_input_locator = (By.ID, 'password')
    _fxa_sign_up_button_locator = (By.ID, 'submit-btn')
    _fxa_sign_in_header_locator = (By.ID, 'fxa-signin-header')
    _fxa_sign_up_header_locator = (By.ID, 'fxa-signup-header')
    _fxa_age_input_locator = (By.ID, 'age')
    _fxa_create_account_link_locator = (By.CSS_SELECTOR, 'a.sign-up')
    _fxa_accept_request_permission_button_locator = (By.ID, 'accept')
    _fxa_signup_complete_header_locator = (By.ID, 'fxa-signup-complete-header')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

    # def login_to_fxa(self):
    #     self.wait_for_element_displayed(*self._fxa_sign_in_header_locator)
    #     # TODO: We need to add or implement functionality that pulls credentials a manifests  file
    #     self.marionette.find_element(*self._fxa_email_input_locator)\
    #         .send_keys()
    #     self.marionette.find_element(*self._fxa_password_input_locator)\
    #         .send_keys()
    #     self.click_element(*self._fxa_sign_in_button_locator).click()
    #     self.wait_for_element_displayed()

    def sign_up_for_fxa(self, start_at_signin, request_permission):
        if start_at_signin:
            self.wait_for_element_displayed(*self._fxa_sign_in_header_locator)
            self.click_element(*self._fxa_create_account_link_locator)

        self.wait_for_element_displayed(*self._fxa_sign_up_header_locator)
        # self.wait(5000)
        email_address = utils.generate_random_email_address()
        self.send_keys_to_element(
            *self._fxa_email_input_locator, **{'string': email_address})
        self.send_keys_to_element(
            *self._fxa_password_input_locator, **{'string': 'password'})
        self.send_keys_to_element(
            *self._fxa_age_input_locator, **{'string': '21'})

        self.click_element(*self._fxa_sign_up_button_locator)
        self.wait_for_element_displayed(*self._fxa_email_input_locator)
        assert self.marionette.find_element(
            *self._fxa_email_input_locator).get_attribute('value') == email_address

        if request_permission:
            self.wait_for_element_displayed(
                *self._fxa_accept_request_permission_button_locator)
            self.click_element(*self._fxa_accept_request_permission_button_locator)
        verification_url = utils.check_generated_email(email_address)

        while verification_url is None:
            verification_url = utils.check_generated_email(
                email_address)
        self.launch(verification_url)
