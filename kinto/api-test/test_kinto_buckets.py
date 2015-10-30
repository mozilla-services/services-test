import unittest

from mockclient import MockClient


class Kinto_Buckets(unittest.TestCase):
    """
        Tests to verify the Kinto buckets function
        Docs: http://kinto.readthedocs.org/en/latest/api/buckets.html
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def assert_not_allowed(self, response):
        self.assertIn('errno', response)
        self.assertIn('message', response)
        self.assertIn('code', response)
        self.assertIn('error', response)
        self.assertEqual(response['errno'], 115)
        self.assertEqual(response['message'], "Method not allowed on this endpoint.")
        self.assertEqual(response['code'], 405)
        self.assertEqual(response['error'], 'Method Not Allowed')

    def test_create_bucket(self):
        resource = 'buckets'
        data = '{"data": {"id": "test_bucket", "foo": "bar"}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.post_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], 'test_bucket')

    def test_replace_bucket(self):
        resource = 'buckets/test_bucket'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], 'test_bucket')

    def test_retrieve_bucket(self):
        resource = 'buckets/test_bucket'
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_bucket')

    def test_retrieve_all_buckets(self):
        resource = 'buckets'
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        for item in response['data']:
            self.assertIn('last_modified', item)
            self.assertIn('id', item)

    def test_update_bucket_no_data(self):
        resource = 'buckets/test_bucket'
        data = ''
        expected_status_code = 405 if self.client.is_read_only() else 400
        response = self.client.patch_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('errno', response)
            self.assertIn('message', response)
            self.assertIn('code', response)
            self.assertIn('error', response)
            self.assertEqual(response['errno'], 107)
            self.assertEqual(response['message'], "Provide at least one of data or permissions")
            self.assertEqual(response['code'], 400)
            self.assertEqual(response['error'], 'Invalid parameters')

    def test_update_bucket_with_data(self):
        # For now bucket patch only allow permission updates
        # See kinto#239
        resource = 'buckets/test_bucket'
        data = '{"permissions": {"read": ["basicauth:foobar"]}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.patch_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['permissions']['read'], ['basicauth:foobar'])

    def test_delete_bucket(self):
        # Create the bucket
        resource = 'buckets'
        data = '{"data": {"id": "delete_bucket"}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.post_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], 'delete_bucket')

        # Delete the bucket
        resource = 'buckets/delete_bucket'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.delete_request(resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('deleted', response['data'])
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], 'delete_bucket')
            self.assertEqual(response['data']['deleted'], True)
