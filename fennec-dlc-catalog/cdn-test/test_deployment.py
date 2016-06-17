import hashlib
import requests


def test_contents(conf, env):
    print("\nTesting for uploaded Fennec fonts in %s\n" % env)
    uploaded_fonts = [
        'CharisSILCompact-B.ttf',
        'CharisSILCompact-BI.ttf',
        'CharisSILCompact-I.ttf',
        'CharisSILCompact-R.ttf',
        'ClearSans-Bold.ttf',
        'ClearSans-BoldItalic.ttf',
        'ClearSans-Italic.ttf',
        'ClearSans-Light.ttf',
        'ClearSans-Medium.ttf',
        'ClearSans-MediumItalic.ttf',
        'ClearSans-Regular.ttf',
        'ClearSans-Thin.ttf',
    ]
    r = requests.get(conf.get(env, 'font_collection'))
    response = r.json()

    for font in response['data']:
        # Make sure we have a font
        assert font['kind'] == 'font'

        # Is it a font we are expecting to see?
        assert font['original']['filename'] in uploaded_fonts

        # Make sure the file exists and does not have a 0 size
        response = requests.get(conf.get(env, 's3_location') + font['attachment']['location'])
        assert response.status_code != 404
        assert len(response.content) > 0

        # Check the file hash matches
        m = hashlib.sha256()
        m.update(response.content)
        assert font['attachment']['hash'] == m.hexdigest()
