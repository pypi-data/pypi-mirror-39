import unittest
import mock
from unittest.mock import Mock, patch
from src.event_bus.event_bus import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


res = {
    "event_type": 'task_created',
    "event_time": '2018-11-21T11:59:39.323+08:00	'
}
inspect_url = '/api/v1/events'


class ServerInspectTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_get(self, mock_class):
        mock_class.return_value = MockResponse(res, 200)
        status_code, response = get(base_url, inspect_url, {'event_type':'["task_created"]', 'task_id':'["%s"]' % task_id})
        self.assertEqual(mock.call(url + inspect_url, params={'event_type':'["task_created"]', 'task_id':'["%s"]'%task_id}), mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, res)

    @patch('requests.get')
    def test_response_get_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.get.return_value = mock_response
        self.assertFalse(self.test_get())

    @mock.patch('requests.get')
    def test_response_not_200(self, mock_class):
        mock_class.return_value = MockResponse(res, 404)
        with self.assertRaises(SystemExit) as cm:
            get(base_url, inspect_url, {'event_type':'["task_created"]', 'task_id':'["%s"]' % task_id})
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.event_bus.event_bus.get')
    def test_server_inspect(self, mock_class):
        mock_class.return_value = (200, res)
        runner = CliRunner()
        result = runner.invoke(event_bus, ['--event-type', '["type1", "type2"]', '--task-id', '["id1", "id2"]'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('event_type', result.output)

        result = runner.invoke(event_bus, ['--event-type', '["type1"]', '--task-id', '["id1"]'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('event_type', result.output)

        result = runner.invoke(event_bus, ['--event-type', None, '--task-id', None])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('event_type', result.output)
