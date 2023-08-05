import unittest
import mock
from src.real_time_output.real_time_output import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


content_length = 30
_offset = 10
output = {
    b'hello world\nhello world\nhello world\n'
}
code = 200
headers = {
    'Range': 'bytes=0-100'
}
return_headers = {
    'Content-Length': content_length
}


class MockResponse:
    def __init__(self, status_code, headers, output):
        self.content = output
        self.status_code = status_code
        self.headers = headers


class RetrieveFinalTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_response_get(self, mock_class):
        mock_class.return_value = MockResponse(code, return_headers, output)
        inspect_url = "/api/v1/task/%s/output/_poll" % task_id
        _code, _headers, _content = response_get(base_url, task_id, _offset, None)
        self.assertEqual(mock.call(url + inspect_url, params={'offset': _offset}), mock_class.call_args)
        self.assertEqual(_code, 200)
        self.assertEqual(_headers, return_headers)
        self.assertEqual(_content, output)

    @mock.patch('src.real_time_output.real_time_output.response_get')
    def test_retrieve_real_time(self, mock_class):
        mock_class.return_value = (code, return_headers, output)
        runner = CliRunner()
        result = runner.invoke(real_time_output, ['--task-id', task_id, '--offset', 10])
        self.assertIn('The output of this task', result.output)
