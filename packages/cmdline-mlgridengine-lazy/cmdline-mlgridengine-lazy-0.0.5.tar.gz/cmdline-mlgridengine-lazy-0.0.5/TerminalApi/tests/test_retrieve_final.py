import unittest
import mock
from unittest.mock import Mock, patch
from src.retrieve_final_output.retrieve_final_output import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


retrieve_res = {
    'hello world',
    'hello world',
    'hello world',
    'hello world',
    'hello world',
    'hello world',
    'hello world'
}

headers = {
    'Range': 'bytes=0-100'
}


class RetrieveFinalTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(retrieve_res, 200)
        inspect_url = "/api/v1/task/%s/output" % task_id
        response = response_get(base_url, task_id, '0-100')
        self.assertEqual(mock.call(url + inspect_url, headers=headers), mock_class.call_args)
        self.assertEqual(response, retrieve_res)

    @patch('requests.get')
    def test_response_get_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.get.return_value = mock_response
        self.assertFalse(self.test_response_get())

    @mock.patch('requests.get')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(retrieve_res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_get(base_url, task_id, '0-100')
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.retrieve_final_output.retrieve_final_output.response_get')
    def test_retrieve_final(self, mock_class):
        mock_class.return_value = retrieve_res
        runner = CliRunner()
        result = runner.invoke(retrieve_final_output, ['--task-id', task_id, '--range', '0-100'])
        self.assertIn('The output of this task', result.output)

