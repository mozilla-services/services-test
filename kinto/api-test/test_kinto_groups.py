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
        self.group_id = ""

    def tearDown(self):
        self.client = None

    def create_group(self, group_id="", data=""):
        resource = 'buckets/test_bucket/groups/#{group_id}'
        data = '{"data": {"members": #{data}}}'
        response = self.client.put_request(resource, data)
        print("+++create_group+++")
        print(response)
        print("+++create_group+++")
        self.group_id = response['data']['id']

    def test_create_group(self):
        resource = 'buckets/test_bucket'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_bucket')

        self.create_group("test_group", "member_auth")

        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('members', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')
        self.assertEqual(response['data']['members'], 'member_auth')

    def test_replace_group(self):
        resource = 'buckets/test_bucket/groups/test_group'
        data = '{"data": {"members": "member_auth"}}'
        response = self.client.put_request(resource, data)
        self.group_id = response['data']['id']
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('members', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')
        self.assertEqual(response['data']['members'], 'member_auth')

    def test_retrieve_group(self):
        if not self.group_id or self.group_id == '':
            self.create_group("test_group", "member_auth")
        resource = 'buckets/test_bucket/groups/' + self.group_id
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        for record in response['data']:
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertEqual(response['data']['id'], self.group_id)

    def test_retrieve_all_groups(self):
        resource = 'buckets/test_bucket/groups'
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        for record in response['data']:
            self.assertIn('last_modified', record)
            self.assertIn('id', record)

    def test_delete_group(self):
        if not self.group_id or self.group_id == '':
            self.create_group("test_group", "member_auth")
        resource = 'buckets/test_bucket/groups/' + self.group_id
        response = self.client.delete_request(resource)
        self.assertIn('data', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('deleted', response['data'])
        self.assertEqual(response['data']['id'], self.group_id)
        self.assertEqual(response['data']['deleted'], True)
