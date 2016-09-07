### Deployment Tests for Fennec DLC Catalog

This repo contains tests to be run whenever fonts for Fennec are to be
uploaded into the Kinto-powered backend.

## Requirements

* Python 3.4
* [Virtualenv](https://virtualenv.pypa.io/en/latest/)

It's also recommended you install [pyenv](https://github.com/yyuu/pyenv) and
use it to keep the Python version local to this project

## Installation

* Create our virtual environment using `virtualenv venv -p python3.4`
* Then install our dependencies using `pip install -r requirements.txt`

## Running tests

Tests can be run using `py.test --env <environment> cdn-test/`

Values for environment are `stage` or `production`
