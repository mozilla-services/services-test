services-test
===================================

Description
----------------------

This repo is intended for: testing tools, test manifests and scripts used by the Mozilla Cloud Services team as part of the Jenkins automated test pipeline.

See: [services-qa-jenkins](https://github.com/mozilla-services/services-qa-jenkins) for how these tests are used in jenkins jobs.

Includes
----------------------
* One directory per project (i.e. absearch, loop, autopush, etc.)
* Each project directory contains sub-directories (1 per test type)
* Within each test type sub-directory you will find a "run.sh" file which should install all dependencies and kick off a test of the type indicated by the parent directory
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
 tag-check     | download tag, make project run unit tests
 stack-check   | verify stack procs, urls, etc. are running
 e2e-test      | client-side test
 loadtest      | verify application scalability
 schema-check  | API test
 security      | ZAP test (TBD)


Reference
----------------------

https://github.com/mozilla-services/services-qa-jenkins
* Vagrant/Puppet scripts for setting up Services QA Jenkins infrastructure

https://github.com/rpappalax/deploy-verify
* swiss-army knife tool for handling deployment ticket creation, updates, stack-checks, etc.
