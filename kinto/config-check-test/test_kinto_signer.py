import ConfigParser
import pytest
from kinto_signer.serializer import canonical_json
from kinto_signer.signer.local_ecdsa import ECDSASigner
from kinto_http import Client
from pytest_testrail.plugin import testrail


@pytest.fixture
def conf(request):
    config = ConfigParser.ConfigParser()
    config.read('manifest.ini')
    return config


def verify_signatures(client):
    dest_col = client.get_collection()
    records = client.get_records(_sort='-last_modified')
    timestamp = client.get_records_timestamp()
    serialized = canonical_json(records, timestamp)
    signature = dest_col['data']['signature']
    with open('pub', 'w') as f:
        f.write(signature['public_key'])
    signer = ECDSASigner(public_key='pub')
    return signer.verify(serialized, signature) is None


@testrail('C5478')
def test_addons_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='addons'
    )
    assert verify_signatures(client)


@testrail('C5475')
def test_plugins_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='plugins'
    )
    assert verify_signatures(client)


@testrail('C5476')
def test_gfx_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='gfx'
    )
    assert verify_signatures(client)


@testrail('C5477')
def test_certificates_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='certificates'
    )
    assert verify_signatures(client)
