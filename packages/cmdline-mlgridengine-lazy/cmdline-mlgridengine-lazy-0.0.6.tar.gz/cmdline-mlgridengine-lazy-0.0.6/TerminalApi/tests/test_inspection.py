import unittest
import mock
from unittest.mock import Mock, patch
from requests import Timeout
from src.server_inspection.server_inspect import server_inspect, response_get
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


server_inspect_res = {
    u'features': [
        u'authentication',
        u'resumable_upload',
        u'upload_cache',
        u'persistent_files',
        u'socket_output'],
    u'limits': {
        u'archive.compression.supported_file_types': [
            u'.zip',
            u'.tar',
            u'.tar.gz',
            u'.tar.xz',
            u'.tar.bz2',
            u'.rar',
            u'.7z'],
        u'task.assets_archive.max_size': 50,
        u'archive.decompression.supported_file_types': [
            u'.zip',
            u'.tar',
            u'.tar.gz',
            u'.tar.xz',
            u'.tar.bz2',
            u'.rar',
            u'.7z']},
    u'task_options': {
        u'work_dir': {
            u'type': u'str',
            u'description': u'working directory of the task.'}},
    u'version': u'v1',
    u'maintenance': False,
    u'api_version': u'v1'}


class ServerInspectTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(server_inspect_res, 200)
        inspect_url = '/api/_inspect'
        status_code, response = response_get(base_url)
        self.assertEqual(
            mock.call(
                url + inspect_url,
                timeout=5),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, server_inspect_res)

    @patch('requests.get')
    def test_response_get_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout('Dummy Exception')
        self.assertFalse(self.test_response_get())

    @patch('requests.get')
    def test_response_get_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.get.return_value = mock_response
        self.assertFalse(self.test_response_get())

    @mock.patch('requests.get')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(server_inspect_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_get(base_url)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.server_inspection.server_inspect.response_get')
    def test_server_inspect(self, mock_class):
        mock_class.return_value = (200, server_inspect_res)
        runner = CliRunner()
        result = runner.invoke(server_inspect)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Feature sets of the server are listed', result.output)
        self.assertIn('description:', result.output)
