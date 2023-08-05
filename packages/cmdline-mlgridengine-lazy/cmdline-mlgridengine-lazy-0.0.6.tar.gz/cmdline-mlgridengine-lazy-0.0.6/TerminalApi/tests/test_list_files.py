import unittest
import mock
from src.list_files.list_files import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url

path = None
path_ = ''
success_doc_res = {u'path': u'',
                   u'entities': [{u'isdir': False,
                                  u'thumbnail': u'',
                                  u'mtime': u'2018-11-15T17:08:33.000+08:00',
                                  u'name': u'test.py',
                                  u'size': 64}]}


class GetDocTest(unittest.TestCase):
    @mock.patch('requests.get')
    def test_response_get_path_None(self, mock_class):
        mock_class.return_value = MockResponse(success_doc_res, 200)
        list_url = "/api/v1/task/%s/_listdir/" % task_id
        status_code, response = list_files_call(base_url, task_id, path)
        self.assertEqual(mock.call(url + list_url), mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_doc_res)

    @mock.patch('requests.get')
    def test_response_get_path(self, mock_class):
        mock_class.return_value = MockResponse(success_doc_res, 200)
        list_url = "/api/v1/task/%s/_listdir/%s" % (task_id, path_)
        status_code, response = list_files_call(base_url, task_id, path)
        self.assertEqual(mock.call(url + list_url), mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_doc_res)

    @mock.patch('src.list_files.list_files.list_files_call')
    def test_list_files(self, mock_class):
        mock_class.return_value = (200, success_doc_res)
        runner = CliRunner()
        result = runner.invoke(list_files, ['--task-id', task_id, '--path', path])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            'Files of the specified directory ',
            result.output)
