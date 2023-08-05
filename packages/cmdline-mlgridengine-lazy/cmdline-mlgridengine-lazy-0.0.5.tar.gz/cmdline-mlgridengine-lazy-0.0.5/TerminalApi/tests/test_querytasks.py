import unittest
import mock
from unittest.mock import Mock, patch
from src.query_tasks.query import query_task, response_post, format_print
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url
import io
import sys


skip = -1
limit = 10
query = ''

query_success_res = {
    'estimated_total': 1,
    'tasks': [success_res],
}

query_req = {
    'limit': limit,
}


class QueryTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(query_success_res, 200)
        query_url = '/api/v1/task/_query'
        status_code, response = response_post(base_url, query_req)
        self.assertEqual(mock.call(url + query_url, json=query_req, headers={'content-type': 'application/json'}),
                         mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, query_success_res)

    @patch('requests.post')
    def test_response_post_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(query_success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_post(base_url, query_req)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.query_tasks.query.response_post')
    def test_server_inspect(self, mock_class):
        mock_class.return_value = (200, query_success_res)
        runner = CliRunner()
        result = runner.invoke(query_task, ['--skip', skip, '--limit', limit, '--query', query])
        output = "\x1b[32m\x1b[34mThere are 1 tasks that"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    def test_format(self):
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        format_print(success_res, task_id)  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn('description', capturedoutput.getvalue())
        self.assertIn('user_env', capturedoutput.getvalue())
        self.assertIn('file_size', capturedoutput.getvalue())
        self.assertIn('create_time', capturedoutput.getvalue())
        self.assertIn('=========', capturedoutput.getvalue())
