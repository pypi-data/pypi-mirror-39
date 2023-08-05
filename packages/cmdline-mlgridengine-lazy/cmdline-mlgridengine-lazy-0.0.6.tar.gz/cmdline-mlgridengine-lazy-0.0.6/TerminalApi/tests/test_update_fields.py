import unittest
import mock
from unittest.mock import Mock, patch
from src.update_fields.update_fields import update_field, post
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


name = 'no_name'
description = 'no_description'
tags = [
    'tag1',
    'tag2'
]

success_res = {
    u'status': u'COMPLETED',
    u'container': {
        u'image': u'docker.peidan.me/haowenxu/ml-runtime:gpu',
        u'type': u'MESOS'},
    u'description': u'no_description',
    u'tags': [
        u'tag1',
        u'tag2'],
    u'start_time': u'2018-11-17T17:03:57.691+08:00',
    u'args': u'python printstr.py --count 10000',
    u'exit_code': u'0',
    u'name': u'no_name',
    u'create_time': u'2018-11-17T17:03:54.190+08:00',
    u'stop_time': u'2018-11-17T17:03:58.420+08:00',
    u'file_size': 0,
    u'id': u'mlge2.zrtjuwu1ohracluioxdmofhn',
    u'resources': {
        u'assigned': {
                    u'memory': 0,
                    u'gpu': 0,
                    u'disk': 0,
                    u'port': [],
                    u'cpu': 0},
        u'request': {
            u'cpu': 1,
            u'memory': 100}},
    u'create_time_int': 552174925}

query_req = {
    'name': name,
    'description': description,
    'tags': tags
}


class UploadFieldTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_update_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        updt_url = '/api/v1/task/%s/_update' % task_id
        status_code, response = post(base_url, updt_url, query_req)
        self.assertEqual(
            mock.call(
                url + updt_url,
                json=query_req,
                headers={
                    'content-type': 'application/json'}),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @patch('requests.post')
    def test_post_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_update_post())

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        updt_url = '/api/v1/task/%s/_update' % task_id
        with self.assertRaises(SystemExit) as cm:
            post(base_url, updt_url, query_req)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.update_fields.update_fields.post')
    def test_update_fields(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(
            update_field, [
                '--task-id', task_id, '--name', name, '--tags', '["tag1", "tag2"]'])
        output = "Task mlge2.zrtjuwu1ohracluioxdmofhn:"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)
