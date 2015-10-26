import os.path
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
        raise NotImplementedError("test not implemented")
    def test_replace_bucket(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_bucket(self):
        resource = 'buckets/default'
        response = self.client.request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        print(response['data'])
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
    def test_retrieve_all_buckets(self):
        """Fetch list of available buckets"""
        #
        # auth has to work to dive in API stuff...
        #
        # resource = 'buckets'
        # response = self.client.request(resource)
        # print(response)
        # self.assertIn('bucket', response)
        # self.assertEqual(response['bucket'], 'some thing!')
        raise NotImplementedError("test not implemented")
    def test_update_bucket(self):
        raise NotImplementedError("test not implemented")
    def test_delete_bucket(self):
        raise NotImplementedError("test not implemented")
