# Configuration file for running our tests
import configparser
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        help="choose an environment: staging or production"
    )


# A fixture to make sure values from our config file are available
@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture
def env(request):
    return request.config.getoption("--env")
