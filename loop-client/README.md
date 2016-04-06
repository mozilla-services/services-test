# Tests for Loop-Client

##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /loop-client/

1. virtualenv .
2. ./bin/pip install -r requirements.txt

Verify that the `manifest.ini` file contains expected values since the tests
rely on using it for assertions.

## Deployment Tests

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test -v --env=stage deployment_tests/`
