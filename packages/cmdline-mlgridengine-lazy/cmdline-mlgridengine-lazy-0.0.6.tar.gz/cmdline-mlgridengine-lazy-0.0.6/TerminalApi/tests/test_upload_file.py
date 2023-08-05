import unittest
import mock
from unittest.mock import Mock, patch, MagicMock
from src.upload_file.upload_file import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.upload_file import upload_file
from src.base_url.base_url import base_url

info = {

}

res = {'id': 'ctddo5keoss4mwpeiwfborc5'}
query_url = '/api/v1/_upload/simple'
headers = {
        'Content-Type': 'multipart/form-data',
        'Content-Length': '100'
}
params = {
        'lock_for': task_id,
        'lock_until': '2018-11-21T11:59:39.323+08:00'
}


class UploadTest(unittest.TestCase):
    @mock.patch('requests.Request')
    def test_post(self, mock_class):
        upload_file.read_upload = MagicMock(return_value=(200, res))
        mock_class.return_value = MockResponse(res, 200)
        status_code, response = request_post(base_url, query_url, headers, params, '/User/ligen/Desktop/app.py')
        self.assertEqual(status_code, 200)
        self.assertEqual(response, res)

    @patch('requests.post')
    def test_response_post_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        upload_file.read_upload = MagicMock(return_value=(404, res))
        mock_class.return_value = MockResponse(res, 404)
        with self.assertRaises(SystemExit) as cm:
            request_post(base_url, query_url, headers, params, '/User/ligen/Desktop/app.py')
        self.assertEqual(cm.exception.code, 0)

    def test_upload_file(self):
        upload_file.read_upload = MagicMock(return_value=(200, res))
        upload_file.request_post = MagicMock(return_value=(200, res))
        runner = CliRunner()
        result = runner.invoke(upload_file.upload_file, ['--task-id', task_id, '--lock-until', '2018-01-01--01:01:01', '--path', 'src/base_url/__init__.py'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Your file id is', result.output)
