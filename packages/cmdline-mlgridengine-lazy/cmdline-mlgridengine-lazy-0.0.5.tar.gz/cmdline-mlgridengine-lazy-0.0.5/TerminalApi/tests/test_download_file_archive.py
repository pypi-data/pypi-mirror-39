import unittest
import mock
from src.download_task_file.download_task_file import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url

success_res = b'import time\nfor i in range(0, 6000):\n\tprint("Hello world!")\n\ttime.sleep(1)\n'
path = 'app.py'
format = 'tar'


class DownloadTaskFileTest(unittest.TestCase):
    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        download_url = "/api/v1/task/_download/%s.%s" % (task_id, format)
        response = response_get(base_url, task_id, format)
        self.assertEqual(mock.call(url + download_url, stream=True), mock_class.call_args)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, success_res)
        res = response_get(base_url, task_id, format)
        self.assertEqual(mock.call(url + download_url, stream=True), mock_class.call_args)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, success_res)
        return response

    @mock.patch('requests.get')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_get(base_url, task_id, format)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.download_task_file.download_task_file.response_get')
    @mock.patch('src.download_file.download_file.save_file')
    def test_download_task_file(self, mock_save, mock_class):
        mock_class.return_value = (200, success_res)
        mock_save.return_value = path
        runner = CliRunner()
        result = runner.invoke(download_task_file, ['--task-id', task_id, '--format', format])
        self.assertEqual(result.exit_code, 1)
