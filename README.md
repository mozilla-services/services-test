services-test
===================================

Description
----------------------

This repo is intended for: testing tools, test manifests and scripts used by the Mozilla Cloud Services team as part of the Mozilla Cloud Services automated test pipeline.

See: [services-qa-jenkins](https://github.com/mozilla-services/services-qa-jenkins) for how these tests are used in jenkins jobs.

Repo Structure
----------------------
To contribute a new automated test to the services-test repo, please adhere to the following guidelines.  This following file structure is required by Jenkins to execute automated tests.

* __project__ (directory)
 * One directory per project.  For example:
   * services-test/absearch
   * services-test/autopush, etc.
* __README.md__ (file) 
 * Add README file in project folder with links to: project repo (github), readthedocs, testplan, etc. 
* __test-type__ (directory)
 * One project child directory per test-type.  For example:
  * services-test/absearch/e2e-test
  * services-test/absearch/schema-check, etc.
* __run__ (file)
 * Add a "run" file in each test-type directory which should install all dependencies and kick off a test of the type indicated by the parent directory
 * example: [example run file](/demo/e2e-test/run)
* __manifest.ini__ (file)
 * Add a manifest file in each test-type directory which should specify any environment-specific parameters
  * example: [example manifest.ini](/demo/e2e-test/manifest.ini)
* __misc__ (files)
 * Any additional files needed by that test type should be self-contained in that directory.

Docker Instructions
----------------------

If you don't have docker, follow [these instructions](https://docs.docker.com/installation/mac/)

To build your own image from the latest code, from the root of services-test (where the Dockerfile is)
* docker build -t mozilla-services/services-test .
* docker run -i -t mozilla-services/services-test /bin/bash

Run tests from the image’s bash shell, e.g.:
* $ absearch/schema-check/run.sh

TODO: Docker hub

Test Execution via Docker
----------------------

Execute the schema_check test on absearch:

docker run -it -v /Users/your-username/path/to/services-qa-secrets/secrets:/secrets -v /Users/your-username/.ssh/id_rsa:/root/.ssh/id_rsa -p 5900 -e HOME=/ -w /services-test/absearch/schema-check/ mozilla-services/services-test ./run.sh


Test Manifests
----------------------

A "test manifest" (manifest.json) ican be found in each project directory.
This file specifies all the test types:
tag-check, stack-check, e2e-test, etc. that will be run in any given
test environment: stage, pre-prod, prod, etc.
(see below)


Test Environments
----------------------
Environments where tests should be run for a given project

 TEST ENV       |    DESCRIPTION
 ---------------|---------------------------------------------------
 stage          | where most testing happens before prod deployment
 stage-loadtest | this is a special env for msisnd where we need a different setup for loadtesting.  In general loadtesting can take place in stage.
 pre-prod       | final verification in an actual prod env (before DNS switch)
 prod           | final verification to make sure prod deploy was successful. Also, continuous prod testing can be executed as a kind of prod "health check"


Test Types
----------------------
Specify what kinds of tests should be run for any given environment

 TEST TYPE     | DESCRIPTION
 ------------- | -------------------------------------------
 stack-check   | verify stack procs, urls, etc. are running
 config-check  | verify application configuration
 e2e-test      | client-side test
 loadtest      | verify application scalability
 schema-check  | API test
 security      | ZAP test (TBD)
 cdn-test      | check existence/delivery of remote files


Services-Ops
----------------------
Tests can be invoked from the Cloud-Services CI pipeline with the following
command:

```
$ services-test/_utils/ci_run_tests -p <project-name> -e <test-env>
```

where project-name = absearch, pocket, autopush, loop-server, etc.
and test-env = dev, stage, pre-prod, prod, etc.




Reference
----------------------

https://github.com/mozilla-services/services-qa-jenkins
* Vagrant/Puppet scripts for setting up Services QA Jenkins infrastructure

https://github.com/rpappalax/deploy-verify
* swiss-army knife tool for handling deployment ticket creation, updates, stack-checks, etc.
