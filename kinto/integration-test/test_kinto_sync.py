import datetime
import os
import string
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
        # Figure out what the IP address where the containers are running
        f = os.popen('which docker-machine')
        docker_machine = str(f.read()).strip()

        if string.find(docker_machine, "/docker-machine") == -1:
            print("Could not find docker-machine in our path")
            exit()

        f = os.popen('%s ip default' % docker_machine)
        ip = str(f.read()).strip()

        # Set our master and read-only end points and create our test bucket
        self.master_url = "http://%s:8888/v1/" % ip
        self.read_only_url = "http://%s:8889/v1/" % ip
        self.credentials = ('testuser', 'abc123')
        self.master = Client(server_url=self.master_url, auth=self.credentials)
        self.read_only = Client(
            server_url=self.read_only_url, auth=self.credentials)
        self.bucket = self.get_timestamp()
        self.master.create_bucket(self.bucket)
        self.read_only.create_bucket(self.bucket)

    def test_sync(self):
        # Generate some random records
        collection = self.get_timestamp()
        self.master.create_collection(collection, bucket=self.bucket)
        self.read_only.create_collection(collection, bucket=self.bucket)
        for x in range(10):
            self.read_only.create_record(
                data=self.generate_record(),
                bucket=self.bucket,
                collection=collection)

        # Pause and generate some more random records on the master end-point
        time.sleep(3)
        for x in range(5):
            self.master.create_record(
                data=self.generate_record(),
                bucket=self.bucket,
                collection=collection)

        # Get the timestamp of our last record by doing an HTTP query of the
        # read-only collection and grabbing the Etag value from the header
        response = self.read_only.get_records(
            bucket=self.bucket, collection=collection)
        last_record = response[-1]
        since = last_record['last_modified']

        # Query the master using that value for all the records since that one
        new_records = self.master.get_records(
            bucket=self.bucket, collection=collection, _since=since)

        # Add those records to our read-only end-point
        for data in new_records:
            new_data = {
                'internal_id': data['internal_id'],
                'title': data['title']
            }
            self.read_only.create_record(
                data=new_data, bucket=self.bucket, collection=collection)

        master_records = self.master.get_records(
            bucket=self.bucket, collection=collection)
        read_only_records = self.read_only.get_records(
            bucket=self.bucket, collection=collection)

        # We should have 5 records in master and 15 in read-only
        self.assertEquals(5, len(master_records))
        self.assertEquals(15, len(read_only_records))

        # Clean up our collections
        self.master.delete_collection(collection, bucket=self.bucket)
        self.read_only.delete_collection(collection, bucket=self.bucket)

    def test_update(self):
        # Create ten records
        collection = self.get_timestamp()
        self.master.create_collection(collection, bucket=self.bucket)
        self.read_only.create_collection(collection, bucket=self.bucket)

        # Insert them into master
        for x in range(10):
            record = self.master.create_record(
                data=self.generate_record(),
                collection=collection,
                bucket=self.bucket)

        # Replicate them over to the read-only instance
        origin = dict(
            server_url=self.master_url,
            auth=self.credentials,
            bucket=self.bucket,
            collection=collection)

        destination = dict(
            server_url=self.read_only_url,
            auth=self.credentials,
            bucket=self.bucket,
            collection=collection)

        replication.replicate(origin, destination)
        records = self.read_only.get_records(
            bucket=self.bucket, collection=collection)
        self.assertEquals(10, len(records))

        # Change one record and update master
        records = self.master.get_records(
            bucket=self.bucket, collection=collection)
        record = records[1]
        record['title'] = 'Updated record'
        updated_id = record['id']
        self.master.update_record(
            record, bucket=self.bucket, collection=collection)
        replication.replicate(origin, destination)

        # Verify that the matched record was changed
        record = self.read_only.get_record(
            updated_id, bucket=self.bucket, collection=collection)
        self.assertEquals(updated_id, record['data']['id'])

        # Verify that we have ten records in each system
        self.assertEquals(
            len(self.master.get_records(
                bucket=self.bucket, collection=collection)),
            len(self.read_only.get_records(
                bucket=self.bucket, collection=collection)))

        self.master.delete_collection(collection, bucket=self.bucket)
        self.read_only.delete_collection(collection, bucket=self.bucket)

    def get_timestamp(self):
        n = time.time()
        d = datetime.datetime.fromtimestamp(n)
        return int(time.mktime(d.timetuple()))

    def generate_record(self):
        data = {'internal_id': self.get_timestamp(), 'title': 'Test Record'}
        return data
