import unittest
import mock
from unittest.mock import Mock, patch
from src.create_task.create_task import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url
import io
import sys


success_res = {
    'create_time_int': 639389381,
    'start_time': '',
    'file_size': 0,
    'container': {
        'type': 'MESOS',
        'image': 'docker.peidan.me/haowenxu/ml-runtime:gpu'},
    'exit_code': '',
    'id': 'mlge2.mhntqf28v8yl1fe3lpdvn2y9',
    'status': 'CREATING',
    'resources': {
        'request': {
            'memory': 128,
            'cpu': 1,
            'gpu': 1},
        'assigned': {
            'gpu': 0,
            'disk': 0,
            'port': [],
            'cpu': 0,
            'memory': 0}},
    'args': [
        'python',
        '-u',
        'app.py'],
    'stop_time': '',
    'create_time': '2018-11-18T17:17:28.645+08:00'}


query_req = {
    'name': name,
    'description': description,
    'tags': tags,
    'options': {
        'work_dir': '~/'
    },
    'container': {
        'type': 'MESOS',
        'image': 'docker.peidan.me/haowenxu/ml-runtime:gpu'
    },
    'resources': {
        'gpu': gpu,
        'cpu': cpu,
        'disk': disk,
        'memory': memory,
        'port': port
    },
    'args': '["ls", "-a"]',
    'user_env': 'no_env'
}


class CreateTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        query_url = '/api/v1/task/_create'
        status_code, response = response_post(base_url, query_req)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=query_req),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @patch('requests.post')
    def test_download_post_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_download_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_post(base_url, query_req)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.create_task.create_task.response_post')
    def test_create_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(create_task, ['--args', '["python", "app.py"]', '--memory', memory, '--cpu', cpu, '--image', 'docker.peidan.me/haowenxu/ml-runtime:gpu'])
        output = "Information about the task"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    def test_format(self):
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        format_printer(success_res)  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn('created successfully', capturedoutput.getvalue())
