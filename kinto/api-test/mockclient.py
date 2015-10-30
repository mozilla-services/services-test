import json
import base64
import requests

stage_url = "https://kinto.stage.mozaws.net/v1/"


class MockClient(object):

    def __init__(self):
        self.auth_string = base64.b64encode('%s:%s' % ("testuser", "abc123"))
        self.auth_header = {"Authorization": "Basic %s" % self.auth_string}

    def get_request(self, resource):
        url = stage_url + resource
        r = requests.get(url, headers=self.auth_header)
        return json.loads(r.content.decode('utf-8'))

    def post_request(self, resource, data=""):
        url = stage_url + resource
        r = requests.post(url, data, headers=self.auth_header)
        return json.loads(r.content.decode('utf-8'))

    def put_request(self, resource, data=""):
        url = stage_url + resource
        r = requests.put(url, headers=self.auth_header)
        return json.loads(r.content.decode('utf-8'))

    def patch_request(self, resource, data=""):
        url = stage_url + resource
        r = requests.patch(url, data, headers=self.auth_header)
        return json.loads(r.content.decode('utf-8'))

    def delete_request(self, resource):
        url = stage_url + resource
        r = requests.delete(url, headers=self.auth_header)
        return json.loads(r.content.decode('utf-8'))
