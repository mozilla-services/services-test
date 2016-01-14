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

1. Modify api-test/mockclient.py and change _stage_url_ to point to the Kinto server that you're testing
2. Run the tests using _./bin/py.test api-test/_

###Run Integration Tests###

1. Make sure that you have [Docker](https://www.docker.com/) installed on the system you are running the tests on
2. Start your master and read-only containers using _docker-compose up_
3. Change the URL's for _self.master_url_ and _self.read_only_ to point at the IP of your containers. These tests were written on OS-X El Capitan with Docker installed using [Docker Toolbox](https://www.docker.com/toolbox)
4. Run the tests using _./bin/py.test integration_test/
