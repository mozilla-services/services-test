import ConfigParser
import demjson
import pytest
import requests


# A fixture to make sure values from our config file are available
@pytest.fixture
def conf():
    config = ConfigParser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_header(conf, env):
    r = requests.head(conf.get(env, 'root'))
    assert r.headers['Location'] == conf.get(env, 'location')
    assert r.headers['X-Frame-Options'] == u'SAMEORIGIN'
    assert u'Content-Security-Policy' in r.headers


def test_server_config(conf, env):
    r = requests.get(conf.get(env, 'root') + '/config.js')
    data = r.content
    json_object = data.split("loop.config = ")
    json_string = json_object[1].strip()[:-1]
    json_dict = demjson.decode(json_string)

    loop_config = {
        'serverUrl': conf.get(env, 'loop_server') + "/v0",
        'feedbackProductName': conf.get(env, 'feedbackProductName'),
        'privacyWebsiteUrl': conf.get(env, 'privacyWebsiteUrl'),
        'legalWebsiteUrl': conf.get(env, 'legalWebsiteUrl'),
        'roomsSupportUrl': conf.get(env, 'roomsSupportUrl'),
        'guestSupportUrl': conf.get(env, 'guestSupportUrl'),
        'unsupportedPlatformUrl': conf.get(env, 'unsupportedPlatformUrl'),
        'learnMoreUrl': conf.get(env, 'learnMoreUrl'),
    }

    for key, value in loop_config.items():
        assert json_dict[key] == value

    assert json_dict['fxosApp']['name'] == conf.get(env, 'loop_fxos_app_name')


def test_server_response(conf, env):
    r = requests.get(conf.get(env, 'loop_server'))
    data = r.json()

    assert 'description' in data
    assert data['endpoint'] == conf.get(env, 'loop_server')
    assert conf.get(env, 'fakeTokBox') == str(data['fakeTokBox'])
    assert conf.get(env, 'fxaOAuth') == str(data['fxaOAuth'])
    assert data['homepage'] == conf.get(env, 'homePage')
    assert 'i18n' in data
    assert data['name'] == conf.get(env, 'name')
    assert data['version'] == conf.get(env, 'loop_server_version')


def test_push_server_config(conf, env):
    r = requests.get(conf.get(env, 'loop_server_push_server_config'))
    data = r.json()

    assert data['pushServerURI'] == conf.get(env, 'loop_server_push_server_uri')
