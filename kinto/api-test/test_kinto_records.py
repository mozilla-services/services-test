import unittest

from .mockclient import MockClient


class Kinto_Records(unittest.TestCase):
    """
        Tests to verify the Kinto records function
        Docs: http://kinto.readthedocs.org/en/latest/api/records.html
    """

    def setUp(self):
        self.client = MockClient()
        self.record_id = ""

    def tearDown(self):
        self.client = None

    def create_record(self, data=""):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        data = '{"data": {"test": #{data}}}'
        response = self.client.post_request(resource, data)
        self.record_id = response['data']['id']

    def test_upload_record(self):
        resource = 'buckets/test_bucket'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_bucket')

        resource = 'buckets/test_bucket/collections/test_collection'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')

        self.create_record("sample_record")

        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('test', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['test'], 'sample_record')
        self.assertEqual(response['data']['id'], self.record_id)

    def test_replace_record(self):
        resource = 'buckets/test_bucket/collections/test_collection/records/' + self.record_id
        data = '{"data": {"test": "new_record"}}'
        response = self.client.put_request(resource, data)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')

    def test_update_record(self):
        raise NotImplementedError("test not implemented")

    # should return one specific record in data, with id and last_modified
    def test_retrieve_record(self):
        if not self.record_id or self.record_id == '':
            self.create_record("sample_record")
        resource = 'buckets/test_bucket/collections/test_collection/records/' + self.record_id
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        for record in response['data']:
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], self.record_id)

    # should return an array in data, each item being a record with a unique id and last_modified
    def test_retrieve_all_records(self):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        for record in response['data']:
            self.assertIn('last_modified', record)
            self.assertIn('id', record)

    def test_delete_record(self):
        if not self.record_id or self.record_id == '':
            self.create_record("sample_record")
        resource = 'buckets/test_bucket/collections/test_collection/records/' + self.record_id
        response = self.client.delete_request(resource)
        self.assertIn('data', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('deleted', response['data'])
        self.assertEqual(response['data']['deleted'], True)

    def test_delete_all_records(self):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        response = self.client.delete_request(resource)
        self.assertIn('data', response)
        for record in response['data']:
            self.assertIn('last_modified', record)
            self.assertIn('id', record)
            self.assertIn('deleted', record)
            self.assertEqual(record['deleted'], True)
