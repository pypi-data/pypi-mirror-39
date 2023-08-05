import unittest
import mock
from unittest.mock import Mock, patch, MagicMock
from src.lock_files.lock_files import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url

info = {
        'files': [
            '1234567',
            '3456788'
        ],
        'task': task_id,
        'until': '2018-11-21T11:59:39.323+08:00'
}

res = {
    'locked': ['1234567', '3456788']
}

query_url = '/api/v1/_upload/lock'


class UploadTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(res, 200)
        status_code, response = response_post(base_url, query_url, info)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=info),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, res)

    @patch('requests.post')
    def test_launch_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_download_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_post(base_url, query_url, info)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.lock_files.lock_files.response_post')
    def test_launch_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(lock_files,
                               ['--file-id-list', '["daoscwf2ymgqeya4rmxd2iv2"]', '--lock-until', '2019-09-09--09:09:09', '--task-id', task_id])
        output = "files are locked"
        self.assertIn(output, result.output)

