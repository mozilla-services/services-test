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

    def assert_not_allowed(self, response):
        self.assertIn('errno', response)
        self.assertIn('message', response)
        self.assertIn('code', response)
        self.assertIn('error', response)
        self.assertEqual(response['errno'], 115)
        self.assertEqual(response['message'], "Method not allowed on this endpoint.")
        self.assertEqual(response['code'], 405)
        self.assertEqual(response['error'], 'Method Not Allowed')

    def create_group(self, group_id="", data=""):
        resource = 'buckets/test_bucket/groups/%s' % group_id
        data = '{"data": {"members": ["%s"]}}' % data
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
            self.group_id = "invalid_group"
        else:
            self.group_id = response['data']['id']
        return response

    def test_create_group(self):
        resource = 'buckets/test_bucket'
        # Create test_bucket
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

        # Create group
        response = self.create_group("test_group", "member_auth")
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('members', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['id'], 'test_group')
            self.assertEqual(response['data']['members'], ['member_auth'])

    def test_replace_group(self):
        resource = 'buckets/test_bucket/groups/test_group'
        data = '{"data": {"members": ["member_auth2"]}}'
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.put_request(resource, data, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.group_id = response['data']['id']
            self.assertIn('data', response)
            self.assertIn('permissions', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('members', response['data'])
            self.assertIn('write', response['permissions'])
            self.assertEqual(response['data']['id'], 'test_group')
            self.assertEqual(response['data']['members'], ['member_auth2'])

    def test_retrieve_group(self):
        if not self.group_id or self.group_id == '':
            self.create_group("test_group", "member_auth")
        resource = 'buckets/test_bucket/groups/' + self.group_id
        expected_status_code = 404 if self.client.is_read_only() else 200
        response = self.client.get_request(resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assertIn('errno', response)
            self.assertIn('message', response)
            self.assertIn('code', response)
            self.assertIn('error', response)
            self.assertEqual(response['errno'], 111)
            self.assertEqual(response['message'], "The resource you are looking for could not be found.")
            self.assertEqual(response['code'], 404)
            self.assertEqual(response['error'], 'Not Found')
        else:
            self.assertIn('data', response)
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
        expected_status_code = 405 if self.client.is_read_only() else 200
        response = self.client.delete_request(resource, status_code=expected_status_code)
        if self.client.is_read_only():
            self.assert_not_allowed(response)
        else:
            self.assertIn('data', response)
            self.assertIn('last_modified', response['data'])
            self.assertIn('id', response['data'])
            self.assertIn('deleted', response['data'])
            self.assertEqual(response['data']['id'], self.group_id)
            self.assertEqual(response['data']['deleted'], True)
