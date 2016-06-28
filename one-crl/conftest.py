# Configuration file for running our tests
import configparser
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        help="choose a test environment: staging or production"
    )


@pytest.fixture
def env(request):
    return request.config.getoption("--env")


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config
