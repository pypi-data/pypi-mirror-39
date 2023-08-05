import unittest
import mock
from src.get_doc.get_doc import get_doc, response_get
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


success_doc_res = {
    u'status': u'CREATING',
    u'container': {
        u'image': u'docker.peidan.me/haowenxu/ml-runtime:gpu',
        u'type': u'MESOS'},
    u'start_time': u'',
    u'args': u'python app.py',
    u'exit_code': u'',
    u'create_time': u'2018-11-14T18:45:21.661+08:00',
    u'stop_time': u'',
    u'file_size': 0,
    u'id': u'mlge2.LiI30zxtij6i4PHwVmoVuwb7',
    u'resources': {
        u'assigned': {
            u'memory': 0,
            u'gpu': 0,
            u'disk': 0,
            u'port': [],
            u'cpu': 0},
        u'request': {
            u'gpu': 1,
            u'cpu': 1,
            u'memory': 128}}}


class GetDocTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(success_doc_res, 200)
        inspect_url = '/api/v1/task/%s' % task_id
        status_code, response = response_get(base_url, task_id)
        self.assertEqual(mock.call(url + inspect_url), mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_doc_res)

    @mock.patch('src.get_doc.get_doc.response_get')
    def test_server_inspect(self, mock_class):
        mock_class.return_value = (200, success_doc_res)
        runner = CliRunner()
        result = runner.invoke(get_doc, ['--task-id', task_id])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('\x1b[34m\x1b[1mThe document of the specified', result.output)
