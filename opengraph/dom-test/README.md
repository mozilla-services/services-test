# OpenGraph Standards test

This test will check and see if a website has the 4 required Opengraph tags, as found on http://ogp.me/

This test is written for pytest.
## Files
* manifest.ini - Manifest file containing the URLs for testing.
* jenkins.ini - Jenkins config file.
* conftest.py - All configuration and fixtures for pytest.
* run - Script file for jenkins.
* test_opengraph_standards.py - The main test file.
* parse_manifest.py - Python script to parse manifest.ini file. Used in run file.
## Requirements

All requirements will be installed by the run file (see Test Execution section below) and assume a Linux or OSX test environment.

This test runs against remote URLs and doesn't require a browser.
## Test Execution

```sh
$ cd services-test/opengraph/dom-test
$ run
```
