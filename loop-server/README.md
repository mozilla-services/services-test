# Tests for Loop Server

##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /loop-server/

1. `virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

Verify that the `manifest.ini` file contains expected values since the tests
rely on using it for assertions.

## Configuration Check Tests

The tests are using [pytest](http://pytest.org/latest/) so to run them do the
following:

`py.test -v --env=stage config-check/`
