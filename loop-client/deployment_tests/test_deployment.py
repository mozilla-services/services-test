import requests
import demjson

MAIN_URL = 'https://call.stage.mozaws.net'
LOOP_SERVER = u'https://loop.stage.mozaws.net'
LOOP_SERVER_VERSION = u'0.20.1'
LOOP_SERVER_PUSH_SERVER_CONFIG = u'https://loop.stage.mozaws.net/' \
                                 u'push-server-config'
LOOP_SERVER_PUSH_SERVER_URI = u'wss://autopush.stage.mozaws.net'
LOOP_FXOS_APP_NAME = u'Hello Stage'


class TestDeployment:

    def test_header(self):
        r = requests.head(MAIN_URL)

        assert r.headers['Location'] == u'https://www.mozilla.org/' \
                                        u'firefox/hello/'
        assert r.headers['X-Frame-Options'] == u'SAMEORIGIN'
        assert u'Content-Security-Policy' in r.headers

    def test_server_config(self):
        r = requests.get(MAIN_URL + '/config.js')
        data = r.content
        json_object = data.split("loop.config = ")
        json_string = json_object[1].strip()[:-1]
        json_dict = demjson.decode(json_string)

        loop_config = {
            'serverUrl': LOOP_SERVER + "/v0",
            'feedbackProductName': u'Loop',
            'privacyWebsiteUrl': u'https://www.mozilla.org/privacy/'
                                 u'firefox-hello/',
            'legalWebsiteUrl': u'https://www.mozilla.org/about/legal/'
                               u'terms/firefox-hello/',
            'roomsSupportUrl': u'https://support.mozilla.org/kb/'
                               u'group-conversations-firefox-hello-webrtc',
            'guestSupportUrl': u'https://support.mozilla.org/kb/'
                               u'respond-firefox-hello-invitation-guest-mode',
            'unsupportedPlatformUrl': u'https://support.mozilla.org/kb/which-'
                                      u'browsers-will-work-firefox-'
                                      u'hello-video-chat',
            'learnMoreUrl': u'https://www.mozilla.org/hello/'
        }

        for key, value in loop_config.items():
            assert json_dict[key] == value

        assert json_dict['fxosApp']['name'] == LOOP_FXOS_APP_NAME

    def test_server_response(self):
        r = requests.get(LOOP_SERVER)
        data = r.json()

        assert 'description' in data
        assert data['endpoint'] == LOOP_SERVER
        assert data['fakeTokBox'] is False
        assert data['fxaOAuth'] is True
        assert data['homepage'] == u'https://github.com/mozilla-services/' \
                                   u'loop-server/'
        assert 'i18n' in data
        assert data['name'] == u'mozilla-loop-server'
        assert data['version'] == LOOP_SERVER_VERSION

    def test_push_server_config(self):
        r = requests.get(LOOP_SERVER_PUSH_SERVER_CONFIG)
        data = r.json()

        assert data['pushServerURI'] == LOOP_SERVER_PUSH_SERVER_URI
