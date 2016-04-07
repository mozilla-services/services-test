import ConfigParser
import json
import pytest
import requests


# A fixture to make sure values from our config file are available
@pytest.fixture
def conf():
    config = ConfigParser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_v1_fetch_bundle(conf, env):
    # Make call to fetch_bundle URL
    data = {
        'locale': 'en-US',
        'version': '44.0.1',
    }
    r = requests.post(
        conf.get(env, 'recipe.server') + '/api/v1/fetch_bundle/',
        data = data
    )
    response = r.json()

    assert u'recipes' in response
    assert len(response['recipes']) > 0
    assert u'name' in response['recipes'][0]['action']
    assert u'implementation_url' in response['recipes'][0]['action']
    assert conf.get(env, 'recipe.server') in response['recipes'][0]['action']['implementation_url']
