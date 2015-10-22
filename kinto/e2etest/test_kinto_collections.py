import os.path
import unittest

from mockclient import MockClient

class Kinto_Collections(unittest.TestCase):
    """
        Tests to verify the Kinto collections function
        Docs: http://kinto.readthedocs.org/en/latest/api/collections.html
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_create_collection(self):
        raise NotImplementedError("test not implemented")
    def test_update_collection(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_collection(self):
        raise NotImplementedError("test not implemented")
    def test_delete_collection(self):
        raise NotImplementedError("test not implemented")
