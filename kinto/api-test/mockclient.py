import json
import base64
import requests

stage_url = "https://kinto.dev.mozaws.net/v1/"


class MockClient(object):

    def __init__(self):
        self.readonly = ""
        self.auth_string = base64.b64encode('%s:%s' % ("testuser", "abc123"))
        self.headers = {
            "Authorization": "Basic %s" % self.auth_string,
            "Content-Type": "application/json"
        }

    def is_read_only(self):
        if not self.readonly or self.readonly == "":
            self.readonly = self.get_read_only_state()
        return self.readonly

    def get_read_only_state(self):
        url = stage_url
        r = requests.get(url, headers=self.headers)
        response = json.loads(r.content.decode('utf-8'))
        return response['settings']['readonly']

    def get_request(self, resource, status_code=None):
        url = stage_url + resource
        r = requests.get(url, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))

    def post_request(self, resource, data=None, status_code=None):
        url = stage_url + resource
        r = requests.post(url, data, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))

    def post_json_request(self, resource, data=None, status_code=None):
        url = stage_url + resource
        r = requests.post(url, json=data, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content)

    def put_request(self, resource, data=None, status_code=None):
        url = stage_url + resource
        r = requests.put(url, data, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))

    def patch_request(self, resource, data=None, status_code=None):
        url = stage_url + resource
        r = requests.patch(url, data, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))

    def delete_request(self, resource, status_code=None):
        url = stage_url + resource
        r = requests.delete(url, headers=self.headers)
        if r.status_code != status_code:
            r.raise_for_status()
        return json.loads(r.content.decode('utf-8'))
