import os.path
import unittest

from mockclient import MockClient

class Kinto_Fetch_Buckets(unittest.TestCase):
    """
        Test case to return list of available buckets
        Docs: http://kinto.readthedocs.org/en/latest/api/buckets.html#buckets-get
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def run_test(self):
        """Fetch list of available buckets"""
        #
        # auth has to work to dive in API stuff...
        #
        # resource = 'buckets'
        # response = self.client.request(resource)
        # print(response)
        # self.assertIn('bucket', response)
        # self.assertEqual(response['bucket'], 'some thing!')
        return True
