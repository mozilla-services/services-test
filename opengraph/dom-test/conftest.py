import requests
import pytest
from bs4 import BeautifulSoup


# ommand line parser
def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="mozilla.org",
        help="Url for testing")


# Load url and parse it
@pytest.fixture
def meta(response_obj):
    soup = BeautifulSoup(response_obj.content, "html.parser")
    return soup.find_all("meta")


# Recieved url and input into requests
@pytest.fixture
def response_obj(url):
    return requests.get('http://' + url)


# Recieve url from command line
@pytest.fixture
def url(request):
    return request.config.getoption("--url")


# Required tags list
@pytest.fixture
def required_tags():
    og_required = [
        'og:title',
        'og:type',
        'og:url',
        'og:image',
    ]
    return og_required


# Empty list for tags found
@pytest.fixture
def found_tags():
    return []
