import unittest
import mock
from src.download_file.download_file import response_get, download_file, save_file
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url

success_res = b'import time\nfor i in range(0, 6000):\n\tprint("Hello world!")\n\ttime.sleep(1)\n'
path = 'app.py'
range_to_download = '0-100'


class DownloadFileTest(unittest.TestCase):
    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        download_url = '/api/v1/task/%s/_getfile/%s' % (task_id, path)
        response = response_get(base_url, path, task_id, None)
        self.assertEqual(mock.call(url + download_url, stream=True), mock_class.call_args)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, success_res)
        res = response_get(base_url, path, task_id, range_to_download)
        self.assertEqual(mock.call(url + download_url, stream=True, headers={'Range': range_to_download}), mock_class.call_args)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, success_res)
        return response

    @mock.patch('requests.get')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_get(base_url, path, task_id, None)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('requests.get')
    def test_response_get_path_none(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        download_url = '/api/v1/task/%s/_getfile/' % task_id
        response = response_get(base_url, None, task_id, None)
        self.assertEqual(mock.call(url + download_url, stream=True), mock_class.call_args)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, success_res)

    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    @mock.patch('src.download_file.download_file.write_file')
    def test_save_file(self, mock_exists, mock_make_dirs, mock_write):
        mock_exists.return_value = False
        mock_write.return_value = None
        file_name = save_file(path, self.test_response_get())
        self.assertEqual(file_name, path)
        mock_make_dirs.assert_called_with('./download')

        mock_exists.return_value = False
        mock_write.return_value = None
        file_name = save_file(path, self.test_response_get_path_none())
        self.assertEqual(file_name, path)
        mock_make_dirs.assert_called_with('./download')

    @mock.patch('src.download_file.download_file.response_get')
    @mock.patch('src.download_file.download_file.save_file')
    def test_download_file(self, mock_save, mock_class):
        mock_class.return_value = (200, success_res)
        mock_save.return_value = path
        runner = CliRunner()
        result = runner.invoke(download_file, ['--task-id', task_id, '--path', path])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Download successfully!', result.output)
