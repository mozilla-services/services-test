# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import time
import urllib2

_rest__email_client = 'http://restmail.net/mail/'


def generate_random_email_address(domain=None):
    domain = 'restmail.net' if domain is None else str(domain)
    return 'test' + str(time.time()) + '@' + domain


def check_generated_email(email_address):
    try:
        data = pull_email_messages(email_address)
        activation_link = data['headers']['x-link']
        return activation_link
    except IndexError:
        check_generated_email(email_address)


def pull_email_messages(email_address):
    response = urllib2.urlopen(
        _rest__email_client + email_address.split('@')[0])
    data = json.load(response)[0]
    time.sleep(.5)
    return data
