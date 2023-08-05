import unittest
import mock
from src.delete_task.delete_task import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


success_res = {

}

query_req = {

}


class CreateTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        status_code, response = response_post(base_url, query_req)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @mock.patch('src.delete_task.delete_task.response_post')
    def test_kill_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(delete_task, ['--task-id', task_id])
        output = "Task %s has been deleted!" % task_id
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)
