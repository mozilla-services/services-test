# Configuration file for running our tests
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store",
        help="choose a test environment: staging or production")

@pytest.fixture
def env(request):
    return request.config.getoption("--env")
