import unittest

from mockclient import MockClient


class Kinto_Fetch_Heartbeat(unittest.TestCase):
    """
        Test case to verify the heartbeat
        Docs: http://kinto.readthedocs.org/en/latest/api/cliquet/utilities.html#get-heartbeat
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_check_heartbeat(self):
        """Check heartbeat to make sure It's Alive."""
        resource = '__heartbeat__'
        response = self.client.get_request(resource, status_code=503)
        self.assertIn('oauth', response)
        self.assertIn('cache', response)
        self.assertIn('storage', response)
        self.assertIn('permission', response)
        self.assertEqual(response['oauth'], True)
        self.assertEqual(response['cache'], False)
        self.assertEqual(response['storage'], True)
        self.assertEqual(response['permission'], True)
