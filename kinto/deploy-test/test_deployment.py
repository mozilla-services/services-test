import datetime
import hashlib
import json
import mimetypes
import os
import requests
# import sha256
import time
import unittest
import uuid

from kinto_client import Client
# from kinto_client import cli_utils

DEFAULT_SERVER = "https://kinto.dev.mozaws.net/v1/"
FILEPATH = "dev-requirements.txt"


class DeploymentTest(unittest.TestCase):
    """
    Tests to verify deployments have been successful
    """

    def setUp(self):
        self.credentials = ('testuser', 'abc123')
        self.client = Client(server_url=DEFAULT_SERVER, auth=self.credentials)
        self.collection = uuid.uuid1()
        self.bucket = 'deploytest'
        self.client.create_bucket(self.bucket, if_not_exists=True)
        self.client.create_collection(self.collection, bucket=self.bucket)

    def test_file_operations(self):
        # Create a record so we have an ID
        n = time.time()
        d = datetime.datetime.fromtimestamp(n)
        timestamp = int(time.mktime(d.timetuple()))
        data = {'timestamp': timestamp, 'title': 'Deploy Record'}
        self.client.create_record(
            data=data,
            bucket=self.bucket,
            collection=self.collection
        )

        # Work some magic to get our records and grab the first one
        records = self.client.get_records(collection=self.collection, bucket=self.bucket)
        record = records.pop(0)
        filename = os.path.basename(FILEPATH)
        mimetype, _ = mimetypes.guess_type(FILEPATH)
        filecontent = open(FILEPATH, "r").read()
        m = hashlib.sha256()
        m.update(filecontent)
        sha256 = m.hexdigest()
        attributes = {
            'original': {
                'filename': filename,
                'hash': sha256,
                'mimetype': mimetype,
                'size': len(filecontent)
            }
        }
        record_uri = self.client._get_endpoint(
            'record',
            id=record['id'],
            collection=self.collection,
            bucket=self.bucket
        )
        attachment_uri = '%s/attachment' % record_uri
        multipart = [("attachment", (filename, filecontent, mimetype))]
        body, _ = self.client.session.request(
            method='post',
            endpoint=attachment_uri,
            data=json.dumps(attributes),
            files=multipart
        )
        self.assertEquals(body['filename'], FILEPATH)

        # retrieve the file and verify the contents match
        new_record = self.client.get_record(
            id=record['id'],
            collection=self.collection,
            bucket=self.bucket
        )
        stored_file = new_record['data']['attachment']['location']
        response = requests.get(stored_file, stream=True)
        self.assertEquals(response.text, filecontent)

    def testChangeOfHash(self):
        # Make sure old version is still accessible
        # Make sure new version is not the same URL as the old one
        # Make sure new version hash matches
        self.assertTrue(False)

    def testCleanUp(self):
        # HTTP DELETE
        # Make sure record no longer appears in collection
        # Make sure S3 bucket no longer contains latest version
        self.assertTrue(False)

    def testSanityChecks(self):
        # HTTP POST to public endpoint should fail (HTTP 405)
        # S3 bucket is protected (HTTP 403)
        # __heartbeat__ endpoint returns something reasonable
        self.assertTrue(False)
