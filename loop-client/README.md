# Tests for Loop-Client

##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /loop-client/

1. virtualenv .
2. ./bin/pip install -r requirements.txt

##Running Tests

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test /path/to/test.py`

## Deployment Tests

Make sure to edit the constants that point to various Loop sever end points as
they differ between staging and production.
