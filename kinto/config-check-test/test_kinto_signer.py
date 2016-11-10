import ConfigParser
import pytest
from kinto_signer.serializer import canonical_json
from kinto_signer.signer.local_ecdsa import ECDSASigner
from kinto_http import Client, KintoException
from pytest_testrail.plugin import testrail


@pytest.fixture
def conf():
    config = ConfigParser.ConfigParser()
    config.read('manifest.ini')
    return config


def get_collection_data(client):
    collection = client.get_collection()
    records = client.get_records(_sort='-last_modified')
    timestamp = client.get_records_timestamp()
    return collection, records, timestamp


def verify_signer_id(collection, key_name):
    return collection['data']['signature']['signer_id'] == key_name


def verify_signatures(collection, records, timestamp):
    try:
        serialized = canonical_json(records, timestamp)
        signature = collection['data']['signature']
        with open('pub', 'w') as f:
            f.write(signature['public_key'])
        signer = ECDSASigner(public_key='pub')
        return signer.verify(serialized, signature) is None
    except KintoException as e:
        if e.response.status_code == 401:
            return -1
        return 0


@testrail('C5478')
def test_addons_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='addons'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.statuys_code == 401:
            pytest.fail('blocklists/addons does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@testrail('C5475')
def test_plugins_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='plugins'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.statuys_code == 401:
            pytest.fail('blocklists/plugins does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@testrail('C5476')
def test_gfx_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='gfx'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.statuys_code == 401:
            pytest.fail('blocklists/gfx does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@testrail('C5477')
def test_certificates_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='blocklists',
        collection='certificates'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.statuys_code == 401:
            pytest.fail('blocklists/certificates does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


def test_certificate_pinning_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'server'),
        bucket='pinning',
        collection='pins'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'pinningpreload_key')
    except KintoException as e:
        if e.response.statuys_code == 401:
            pytest.fail('pinning/pins does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))
