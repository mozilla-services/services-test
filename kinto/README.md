###General Configuration###

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From /kinto/

1. virtualenv .
2. ./bin/pip install -r dev-requirements.txt

NOTE -- as of 01/14/2016 we are relying on a specific branch of the [Kinto Python client](https://github.com/Kinto/kinto.py)
that implements the replication features. When the pull request containing that
code gets merged into the master branch the dev-requirements.txt file will be
updated.

###Run API tests###

1. Decide if you want to run your own local instance of [Kinto server](https://github.com/Kinto/kinto) or if you wish to use the version on the staging server that it is currently pointing at
2. If you decide to run your own instance make sure modify *api-test/mockclient.py* and change *server_url* to point at the correct Kinto server
4. Run the tests using _./bin/py.test api-test/_

###Run Integration Tests###

The integration tests were developed using Docker version 1.9.1, build a34a1d5 and
Docker Compose version 1.5.1.

1. Make sure that you have [Docker](https://www.docker.com/) installed on the system you are running the tests on
2. Start your master and read-only containers using _docker-compose up_
3. Run the tests using _./bin/py.test integration-test/_

###Run Configuration Check Tests###

The configuration check tests are designed to ensure parts of Kinto that are
used by other applications are working correctly. These tests will report results
to TestRail.

####Creating TestRail-aware Tests####

Tests that you want to report results to TestRail need to make sure that they
are importing the TestRail py.test plugin:

_from pytest_testrail.plugin import testrail_

Then you need to add a decorator to a test in order for the plugin to report
the results of the test. Here'a sample:

_@testrail('C5475')_

The value 'C5475' is the ID that TestRail assigned to the case you are testing,
which can be obtained via the TestRail admin. Without the decorator the test
will still run but no results will be reported to TestRail.


####Running The Tests####

To run the tests, do the following

1. Copy _config-check-test/testrail.cfg-dist_ to _config-check-test/testrail.cfg_ and add your TestRail user name and password to the configuration file
2. Make sure you are connected to the Mozilla VPN
3. Run the tests using _py.test --env=<ENVIRONMENT> --testrail=config-check-test/testrail.cfg config-check-test/_ where <ENVIRONMENT> is _stage_ or _prod_

These configuration check tests are currently only being run against staging
instances of Kinto.
