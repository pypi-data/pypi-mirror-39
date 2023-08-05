import unittest
import mock
from src.batch_operation.batch_operation import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from unittest.mock import MagicMock
from src.batch_operation import batch_operation


success_res_ = {
    'tasks': [
        'mlge2.4qhs8bnldpvpsgok2jjk5ko1',
        'mlge2.xcqmxpwq9lcyjlzty4gohjdy',
        'mlge2.x5yfe0qvnf2twwbdgt257heh'
    ]
}

query_req = {
    'tasks': [
        'mlge2.4qhs8bnldpvpsgok2jjk5ko1',
        'mlge2.xcqmxpwq9lcyjlzty4gohjdy',
        'mlge2.x5yfe0qvnf2twwbdgt257heh'
    ]
}

query_res = {
    'tasks': [
        success_res, success_res, success_res
    ]
}


class CreateTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_del(self, mock_class):
        mock_class.return_value = MockResponse(success_res_, 200)
        query_url = '/api/v1/task/_delete'
        status_code, response = process_post(url, query_url, query_req)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=query_req),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res_)

    @mock.patch('requests.post')
    def test_kill(self, mock_class):
        mock_class.return_value = MockResponse(success_res_, 200)
        query_url = '/api/v1/task/_kill'
        status_code, response = process_post(url, query_url, query_req)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=query_req),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res_)

    @mock.patch('requests.post')
    def test_query(self, mock_class):
        mock_class.return_value = MockResponse(success_res_, 200)
        query_url = '/api/v1/task/_get'
        status_code, response = process_post(url, query_url, query_req)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=query_req),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res_)

    @mock.patch('src.batch_operation.batch_operation.process_post')
    def test_batch_del(self, mock_class):
        mock_class.return_value = (200, success_res_)
        runner = CliRunner()
        result = runner.invoke(batch_del, ['--task-id-list', '["mlge2.4qhs8bnldpvpsgok2jjk5ko1","mlge2.xcqmxpwq9lcyjlzty4gohjdy", "mlge2.x5yfe0qvnf2twwbdgt257heh"]'])
        output = "These tasks are deleted"
        self.assertIn(output, result.output)

    @mock.patch('src.batch_operation.batch_operation.process_post')
    def test_batch_kill(self, mock_class):
        mock_class.return_value = (200, success_res_)
        runner = CliRunner()
        result = runner.invoke(batch_kill, ['--task-id-list',
                                           '["mlge2.4qhs8bnldpvpsgok2jjk5ko1","mlge2.xcqmxpwq9lcyjlzty4gohjdy", "mlge2.x5yfe0qvnf2twwbdgt257heh"]'])
        output = "These tasks are killed"
        self.assertIn(output, result.output)

    @mock.patch('src.batch_operation.batch_operation.process_post')
    def test_batch_query(self, mock_class):
        mock_class.return_value = (200, query_res)
        runner = CliRunner()
        result = runner.invoke(batch_query, ['--task-id-list',
                                           '["mlge2.4qhs8bnldpvpsgok2jjk5ko1","mlge2.xcqmxpwq9lcyjlzty4gohjdy", "mlge2.x5yfe0qvnf2twwbdgt257heh"]'])
        output = "Document of tasks"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    @mock.patch('requests.post')
    def test_response_not_200(self, mock_class):
        batch_operation.read_upload = MagicMock(return_value=(404, success_res_))
        mock_class.return_value = MockResponse(success_res_, 404)
        with self.assertRaises(SystemExit) as cm:
            process_post(url, '/api/v1/task/_get', query_req)
        self.assertEqual(cm.exception.code, 0)
