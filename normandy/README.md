##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /normandy/

1. virtualenv venv
2. ./venv/bin/pip install -r dev-requirements.txt

##Running Tests

To run the tests you will need a copy of Firefox with [Marionette support enabled](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/Builds).

It is recommended that you start Firefox with a brand new profile to eliminate
unforeseen conflicts with other extensions and preferences.

Make sure to check each test for any values that need to be modified from their
defaults. Several tests rely on a specific extension being installed.

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test /path/to/test.py`
