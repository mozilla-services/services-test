# One CRL

Tests for QA Cloud Services to use for the One CRL project.

## Installation

It is highly recommended to use [VirtualEnv](https://virtualenv.pypa.io/en/stable/)
and Python 3 is required (development work was done with Python 3.5.1).

```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

### Config Check

These tests are looking at consistency at the API level. They make calls to
specific end points and makes sure that responses make sense. To run them
do the following:

`py.test --env=<environment> check_config/test_api_fields.py`

Where `<environment>` is one of `stage` or `prod`
