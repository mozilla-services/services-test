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

    def test_create_bucket(self):
        resource = 'buckets'
        data = '{"data": {"id": "test_bucket"}}'
        response = self.client.post_request(resource, data)
        self.assertIn('data', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_bucket')

    def test_replace_bucket(self):
        resource = 'buckets/test_bucket'
        response = self.client.put_request(resource)
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

    # patch request for update currently broken, see:
    # https://github.com/mozilla-services/cliquet/issues/516
    def test_update_bucket_no_data(self):
        # resource = 'buckets/test_bucket'
        # data = ''
        # response = self.client.patch_request(resource, data)
        # self.assertIn('data', response)
        # self.assertIn('permissions', response)
        # self.assertIn('last_modified', response['data'])
        # self.assertIn('id', response['data'])
        raise NotImplementedError("bucket update currently broken for patch with no data")

    def test_update_bucket_with_data(self):
        resource = 'buckets/test_bucket'
        data = '{"data": {"id": "test_update_bucket"}}'
        response = self.client.patch_request(resource, data)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_update_bucket')

    def test_delete_bucket(self):
        resource = 'buckets'
        data = '{"data": {"id": "delete_bucket"}}'
        response = self.client.post_request(resource, data)
        self.assertIn('data', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'delete_bucket')

        resource = 'buckets/delete_bucket'
        response = self.client.delete_request(resource)
        self.assertIn('data', response)
        self.assertIn('deleted', response['data'])
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'delete_bucket')
        self.assertEqual(response['data']['deleted'], True)
