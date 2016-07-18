import requests
import pytest
from bs4 import BeautifulSoup


# Load url and parse it
@pytest.fixture
def meta(response_obj):
    soup = BeautifulSoup(response_obj.content, "html.parser")
    return soup.find_all("meta")

@pytest.fixture
def response_obj():
    return requests.get('http://nightly.mozilla.org')

@pytest.fixture
def required_tags():
    og_required = [
        'og:title',
        'og:type',
        'og:url',
        'og:image',
    ]
    return og_required

@pytest.fixture
def found_tags():
    return []
