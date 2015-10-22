import os.path
import unittest

from mockclient import MockClient

class Kinto_Groups(unittest.TestCase):
    """
        Tests to verify the Kinto groups function
        Docs: http://kinto.readthedocs.org/en/latest/api/groups.html
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_create_group(self):
        raise NotImplementedError("test not implemented")
    def test_replace_group(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_group(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_all_groups(self):
        raise NotImplementedError("test not implemented")
    def test_delete_group(self):
        raise NotImplementedError("test not implemented")
