import unittest

from mockclient import MockClient


class Kinto_Fetch_Heartbeat(unittest.TestCase):
    """
        Test case to verify the heartbeat
        Docs: http://kinto.readthedocs.org/en/latest/api/
        cliquet/utilities.html#get-heartbeat
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_check_heartbeat(self):
        """Check heartbeat to make sure It's Alive."""
        resource = '__heartbeat__'
        expected_response = {
            'cache': True,
            'oauth': True,
            'permission': True,
            'storage': True
        }
        self.assertEquals(
            sorted(expected_response),
            sorted(self.client.get_request(resource, status_code=503))
        )
