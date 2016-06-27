##General Configuration

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /normandy/

1. `virtualenv venv`
2. `source venv/bin/activate` to turn on the virtualenv
2. `./venv/bin/pip install -r dev-requirements.txt`

##Running Tests

Check the `manifest.ini` file for values that are required for the tests to run
in specific environments.

### Schema Check Tests

These tests are designed to look for changes to the API that Firefox will
communicate with. To run them:

`py.test --env=<environment> schema-check/`

where `<environment>` is one of `dev`, `stage`, or `prod`
