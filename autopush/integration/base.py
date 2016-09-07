# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from marionette_driver import expected, Wait, Actions
from marionette_driver.errors import NoSuchElementException

import re


class Base(object):

    def __init__(self, marionette):
        self.marionette = marionette
        self.CHROME = 'chrome'
        self.CONTENT = 'content'
        self.set_context(self.CONTENT)
        self.action = Actions(marionette)

    def launch(self, url):
        if url is not None:
            regex = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
                r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if regex.match(url):
                self.marionette.navigate(url)
            else:
                raise ValueError('Url is malformed.')
        else:
            raise ValueError("Url must contain a value.")

    def is_element_present(self, by, locator):
        try:
            self.marionette.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_displayed(self, by, locator):
        try:
            return self.marionette.find_element(by, locator).is_displayed()
        except NoSuchElementException:
            return False

    def wait_for_element_displayed(self, by, locator):
        return Wait(self.marionette).until(expected.element_displayed(
            Wait(self.marionette).until(
                expected.element_present(by, locator))))

    def wait_for_element_present(self, by, locator):
        Wait(self.marionette).until(expected.element_present(by, locator))

    def wait_for_element_enabled(self, by, locator):
        Wait(self.marionette).until(
            expected.element_enabled(lambda m: m.find_element(by, locator)))

    def wait_for_element_not_displayed(self, by, locator):
        Wait(self.marionette).until(expected.element_not_displayed(
            Wait(self.marionette).until(
                expected.element_present(by, locator))))

    def wait_for_element_not_present(self, by, locator):
        Wait(self.marionette).until(expected.element_not_present(by, locator))

    def wait_for_element_not_enabled(self, by, locator):
        Wait(self.marionette).until(
            expected.element_not_enabled(
                lambda m: m.find_element(by, locator)))

    def set_context(self, context):
        if context != self.CHROME and context != self.CONTENT:
            raise AttributeError(
                '{} is not a context that you can switch to'.format(context))
        else:
            self.marionette.set_context(context)

    def click_element(self, by, locator):
        self.marionette.find_element(by, locator).click()

    def send_keys_to_element(self, by, locator, string):
        self.marionette.find_element(by, locator).send_keys(string)

    def wait(self, time):
        self.action.wait(time).perform()


class PageRegion(Base):

    def __init__(self, marionette, element):
        self.root_element = element
        Base.__init__(self, marionette)
