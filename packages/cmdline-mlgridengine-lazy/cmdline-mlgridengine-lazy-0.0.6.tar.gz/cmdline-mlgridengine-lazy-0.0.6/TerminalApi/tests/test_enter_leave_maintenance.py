import unittest
import mock
from src.enter_leave_maintenance_mode.enter_leave_maintenance_mode import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from unittest.mock import Mock, patch
from src.base_url.base_url import base_url


res = {

}
query_req = {
    'maintenance': True
}
query_url = "/api/v1/_manage/maintenance"


class EnterLeaveMaintenanceTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        status_code, response = response_post(base_url, query_url, query_req)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @mock.patch('src.enter_leave_maintenance_mode.enter_leave_maintenance_mode.response_post')
    def test_kill_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(maintenance_mode, ['--if-maintain', True])
        output = "IN MAINTENANCE"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(maintenance_mode, ['--if-maintain', False])
        output = "Not in maintenance"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    @patch('requests.post')
    def test_response_get_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.get.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(res, 404)
        with self.assertRaises(SystemExit) as cm:
            response_post(base_url, query_url, query_req)
        self.assertEqual(cm.exception.code, 0)
