import base64
import datetime
import re
import requests
import time
import unittest

from kinto_client import Client
from kinto_client import replication

class Kinto_Sync(unittest.TestCase):
    """
    Tests that given two Kinto servers you can successfully sync data
    from one to the other
    """

    def setUp(self):
        self.master_url = "http://192.168.99.100:8888/v1/"
        self.read_only_url = "http://192.168.99.100:8889/v1/"
        self.credentials = ('testuser', 'abc123')
        self.master = Client(server_url=self.master_url, auth=self.credentials)
        self.read_only = Client(server_url=self.read_only_url, auth=self.credentials)

        # Try and create our buckets and collections
        try:
            self.master.get_bucket('test')
        except:
            self.master.create_bucket('test')

        try:
            self.master.get_collection('test_collection', bucket='test')
        except:
            self.master.create_collection('test_collection', bucket='test')

        try:
            self.read_only.get_bucket('test')
        except:
            self.read_only.create_bucket('test')

        try:
            self.read_only.get_collection('test_collection', bucket='test')
        except:
            self.read_only.create_collection('test_collection', bucket='test')

    def test_sync(self):
        # Generate some random records
        collection = self.get_timestamp()
        self.master.create_collection(collection, bucket='test')
        self.read_only.create_collection(collection, bucket='test')
        x = 1
        while x <= 10:
            self.read_only.create_record(
                data=self.create_record(),
                bucket='test',
                collection=collection)
            x = x + 1

        # Pause and generate some more random records on the master end-point
        time.sleep(3)

        x = 1
        while x <= 5:
            self.master.create_record(
                data=self.create_record(),
                bucket='test',
                collection=collection)
            x = x + 1

        # Get the timestamp of our last record by doing an HTTP query of the
        # read-only collection and grabbing the Etag value from the header
        response = self.read_only.get_records(bucket='test', collection=collection)
        last_record = response[-1]
        since = last_record['last_modified']

        # Query the master using that value for all the records since that one
        new_records = self.master.get_records(bucket='test', collection=collection, _since=since)

        # Add those records to our read-only end-point
        for data in new_records:
            new_data = {'internal_id': data['internal_id'], 'title': data['title']}
            self.read_only.create_record(data=new_data, bucket='test', collection=collection)

        master_records = self.master.get_records(bucket='test', collection=collection)
        read_only_records = self.read_only.get_records(bucket='test', collection=collection)

        # We should have 5 records in master and 15 in read-only
        self.assertEquals(5, len(master_records))
        self.assertEquals(15, len(read_only_records))

        # Clean up our collections
        self.master.delete_collection(collection, bucket='test')
        self.read_only.delete_collection(collection, bucket='test')

    def test_update(self):
        # Create ten records
        collection = self.get_timestamp()
        self.master.create_collection(collection, bucket='test')
        self.read_only.create_collection(collection, bucket='test')

        records = {}
        x = 1

        # Insert them into master
        while x <= 10:
            data = self.create_record()
            record = self.master.create_record(data=data, collection=collection, bucket='test')
            x = x + 1

        # Replicate them over to the read-only instance
        origin = dict(
            server_url=self.master_url,
            auth=self.credentials,
            bucket='test',
            collection=collection
        )

        destination = dict(
            server_url=self.read_only_url,
            auth=self.credentials,
            bucket='test',
            collection=collection
        )

        replication.replicate(origin, destination)
        records = self.read_only.get_records(bucket='test', collection=collection)
        self.assertEquals(10, len(records))

        # Change one record and update master
        records = self.master.get_records(bucket='test', collection=collection)
        record = records[1]
        record['title'] = 'Updated record'
        updated_id = record['id']
        self.master.update_record(record, bucket='test', collection=collection)
        replication.replicate(origin, destination)

        # Verify that the matched record was changed
        record = self.read_only.get_record(updated_id, bucket='test', collection=collection)
        self.assertEquals(updated_id, record['data']['id'])

        # Verify that we have ten records in each system
        self.assertEquals(
            len(self.master.get_records(bucket='test', collection=collection)),
            len(self.read_only.get_records(bucket='test', collection=collection))
        )

        self.master.delete_collection(collection, bucket='test')
        self.read_only.delete_collection(collection, bucket='test')

    def get_timestamp(self):
        n = time.time()
        d = datetime.datetime.fromtimestamp(n)
        return int(time.mktime(d.timetuple()))

    def create_record(self):
        data = {'internal_id': self.get_timestamp(), 'title': 'Test Record'}
        return data
