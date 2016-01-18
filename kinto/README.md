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

1. Make sure that you have [Docker](https://www.docker.com/) installed on the system you are running the tests on
2. Start your master and read-only containers using _docker-compose up_
3. Run the tests using _./bin/py.test integration-test/_
