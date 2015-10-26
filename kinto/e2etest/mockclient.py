import json
import base64
import urllib2

stage_url = "https://kinto.stage.mozaws.net/v1/"

class MockClient(object):
  def request(self, resource):
    base64string = base64.encodestring('%s:%s' % ("testuser", "abc123")).replace('\n', '')
    url = stage_url + resource
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
    # response = urlopen(url)
    raw_data = response.read().decode('utf-8')
    return json.loads(raw_data)
