import os
import unittest
import datetime
from test.mocks.s3 import S3
from test.mocks.cloudformation import Cloudformation
import cfnctl.lib.bucket as bucket

class TestLibBucket(unittest.TestCase):
    
    def test_template_url(self):
        local_url = bucket.get_file_url('foo', 'baz', 'bar.template')
        file_url = bucket.get_file_url('foo', 'baz', 'file:///test/bar.template')
        http_url = bucket.get_file_url('foo', 'baz', 'https://www.templates.com/bar.template')
        self.assertEqual(local_url, 'https://s3.amazonaws.com/foo/baz/bar.template')
        self.assertEqual(file_url, 'https://s3.amazonaws.com/foo/baz/bar.template')
        self.assertEqual(http_url, 'https://www.templates.com/bar.template')
    

    def test_upload_template(self):
        '''upload a template with just a name
        '''
        def upload(file_path, bucket, template_name):
            self.assertEqual(template_name, 'baz/bar.template')
            self.assertEqual(bucket, 'foo')
            self.assertEqual(file_path, os.path.abspath('bar.template'))
            return
        client = S3()
        client.mock('upload_file', upload)
        bucket.upload_file(client, 'baz', 'foo', 'bar.template')
        self.assertEqual(client.called['upload_file'], 1)
        self.assertEqual(True, True)

    def test_upload_template_url(self):
        '''should not attempt to upload a template that is already a url
        '''
        def upload(file_path, bucket, template_name):
            return
        client = S3()
        client.mock('upload_file', upload)
        bucket.upload_file(client, 'baz', 'foo', 'http://templates.com/bar.template')
        self.assertEqual(client.called['upload_file'], 0)
    
    def test_upload_template_file_path(self):
        '''upload a template with just a name
        '''
        def upload(file_path, bucket, template_name):
            self.assertEqual(template_name, 'baz/bar.template')
            self.assertEqual(bucket, 'foo')
            self.assertEqual(file_path, os.path.abspath('file:///foo/bar.template'))
            return
        client = S3()
        client.mock('upload_file', upload)
        bucket.upload_file(client, 'baz', 'foo', 'file:///foo/bar.template')
        self.assertEqual(client.called['upload_file'], 1)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
