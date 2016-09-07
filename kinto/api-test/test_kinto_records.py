# -*- coding: utf-8 -*-
import unittest

from mockclient import MockClient


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

    def assert_not_allowed(self, response):
        self.assertIn('errno', response)
        self.assertIn('message', response)
        self.assertIn('code', response)
        self.assertIn('error', response)
        self.assertEqual(response['errno'], 115)
        self.assertEqual(response['message'],
                         "Method not allowed on this endpoint.")
        self.assertEqual(response['code'], 405)
        self.assertEqual(response['error'], 'Method Not Allowed')

    def create_record(self, data=""):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        data = '{"data": {"test": "%s"}}' % data
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.post_request(
            resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
            self.record_id = "invalid_group"
        else:
            self.record_id = response['data']['id']
        return response

    def test_upload_record(self):
        # Create bucket
        resource = 'buckets/test_bucket'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(
            resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], 'test_bucket')

        # Create collection
        resource = 'buckets/test_bucket/collections/test_collection'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(
            resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('schema', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['id'], 'test_collection')

        # Create record
        response = self.create_record("sample_record")
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('test', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['test'], 'sample_record')
            self.assertEqual(response['data']['id'], self.record_id)

    def test_replace_record(self):
        if not self.record_id:
            self.create_record("sample_record")

        resource = 'buckets/test_bucket/collections/test_collection/records/'\
                   + self.record_id
        data = '{"data": {"test": "new_record"}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(
            resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['id'], self.record_id)
            self.assertEqual(response['data']['test'], "new_record")

    def test_update_record(self):
        if not self.record_id:
            self.create_record("sample_record")

        resource = 'buckets/test_bucket/collections/test_collection/records/'\
                   + self.record_id
        data = '{"data": {"test": "updated_record"}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.patch_request(
            resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['id'], self.record_id)
            self.assertEqual(response['data']['test'], "updated_record")

    # should return one specific record in data, with id and last_modified
    def test_retrieve_record(self):
        if not self.record_id or self.record_id == '':
            self.create_record("sample_record")
        resource = 'buckets/test_bucket/collections/test_collection/records/'\
                   + self.record_id
        expected_status_code = 400 if self.client.is_read_only() else 200
        response = self.client.get_request(
            resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assertIn('errno', response)
            self.assertIn('message', response)
            self.assertIn('code', response)
            self.assertIn('error', response)
            self.assertEqual(response['errno'], 107)
            self.assertEqual(response['message'], "path: Invalid record id")
            self.assertEqual(response['code'], 400)
            self.assertEqual(response['error'], 'Invalid parameters')
        else:
            self.assertIn('data', response)
            for record in response['data']:
                self.assertIn('last_modified', response['data'])
                self.assertIn('id', response['data'])
                self.assertEqual(response['data']['id'], self.record_id)

    # should return an array in data, each item being a record with a unique
    # id and last_modified
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
        resource = 'buckets/test_bucket/collections/test_collection/records/'\
                   + self.record_id
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.delete_request(
            resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('deleted', response['data'])
            self.assertEqual(response['data']['deleted'], True)

    def test_delete_all_records(self):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.delete_request(
            resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            for record in response['data']:
                self.assertIn('last_modified', record)
                self.assertIn('id', record)
                self.assertIn('deleted', record)
                self.assertEqual(record['deleted'], True)

    def test_badly_formed_records(self):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        expected_status_code = 405 if self.client.is_read_only() else 400
        data = '{"data": {"test": }'
        self.client.post_request(
            resource, data, status_code=expected_status_code)

    def test_utf8_stored_correctly(self):
        resource = 'buckets/test_bucket/collections/test_collection/records'
        expected_status_code = 405 if self.client.is_read_only() else 200
        greeting = u'Comment ça va ? Très bien'
        data = {'data': {'greeting': greeting}}
        response = self.client.post_json_request(
            resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertEqual(greeting, response['data']['greeting'])
