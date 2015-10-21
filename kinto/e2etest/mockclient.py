import json
from urllib2 import urlopen

stage_url = "https://kinto.stage.mozaws.net/v1/"

class MockClient(object):
  def request(self, resource):
    url = stage_url + resource
    response = urlopen(url)
    raw_data = response.read().decode('utf-8')
    return json.loads(raw_data)
