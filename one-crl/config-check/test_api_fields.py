import requests


def test_api_fields(conf, env):
    api_url = conf.get(env, 'api_url')
    r = requests.get(api_url + "/v1/buckets/blocklists/collections/")
    response = r.json()
    data = response['data']
    signature_fields = {
        'x5u', 'content-signature', 'signature_encoding', 'signature',
        'public_key', 'hash_algorithm', 'ref'
    }

    for entry in data:
        assert 'certificates' in entry['id']

        for field in signature_fields:
            assert field in entry['signature']

        r = requests.get(entry['signature']['x5u'])
        assert r.status_code == 200
