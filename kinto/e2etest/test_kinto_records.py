import os.path
import unittest

from mockclient import MockClient

class Kinto_Records(unittest.TestCase):
    """
        Tests to verify the Kinto records function
        Docs: http://kinto.readthedocs.org/en/latest/api/records.html
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_upload_record(self):
        raise NotImplementedError("test not implemented")
    def test_replace_record(self):
        raise NotImplementedError("test not implemented")
    def test_update_record(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_record(self):
        raise NotImplementedError("test not implemented")
    def test_retrieve_all_records(self):
        raise NotImplementedError("test not implemented")
    def test_delete_record(self):
        raise NotImplementedError("test not implemented")
