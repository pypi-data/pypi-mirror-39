import unittest
import mock
from unittest.mock import Mock, patch
from src.lauch_task.lauch_task import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


success_res = {
    u'status': u'DEPLOYING',
    u'container': {
        u'image': u'docker.peidan.me/haowenxu/ml-runtime:gpu',
        u'type': u'MESOS'},
    u'create_time_int': 692638096,
    u'start_time': u'',
    u'args': [
        u'python',
        u'-u',
        u'app.py'],
    u'exit_code': u'',
    u'create_time': u'2018-11-19T08:04:57.360+08:00',
    u'stop_time': u'',
    u'file_size': 0,
    u'id': u'mlge2.v40otjvsbg6tlvsbrxhqi8w5',
    u'resources': {
        u'assigned': {
                    u'memory': 0,
                    u'gpu': 0,
                    u'disk': 0,
                    u'port': [],
                    u'cpu': 0},
        u'request': {
            u'gpu': 1,
            u'cpu': 1,
            u'memory': 128}}}


query_req = {'assets': [
    {'dest': 'app.py', 'type': 'file', 'id': u'daoscwf2ymgqeya4rmxd2iv2'}]}


class CreateTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        query_url = "/api/v1/task/%s/_start" % task_id
        status_code, response = request_post(base_url, query_url, query_req)
        self.assertEqual(
            mock.call(
                url + query_url,
                json=query_req),
            mock_class.call_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @patch('requests.post')
    def test_launch_err(self, mock_requests):
        mock_response = Mock(status_code=500)
        mock_requests.post.return_value = mock_response
        self.assertFalse(self.test_post())

    @mock.patch('requests.post')
    def test_download_not_200(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 404)
        with self.assertRaises(SystemExit) as cm:
            request_post(base_url, "/api/v1/task/%s/_start" % task_id, query_req)
        self.assertEqual(cm.exception.code, 0)

    @mock.patch('src.lauch_task.lauch_task.request_post')
    def test_launch_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(launch_task, ['--file-id-list', '["daoscwf2ymgqeya4rmxd2iv2"]', '--dest-file-list', '["app.py"]', '--task-id', 'mlge2.v40otjvsbg6tlvsbrxhqi8w5'])
        output = "You've launched a task"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(launch_task,
                               ['--tar-id-list', '["daoscwf2ymgqeya4rmxd2iv2"]', '--dest-tar-list', '["app.py"]',
                                '--task-id', 'mlge2.v40otjvsbg6tlvsbrxhqi8w5'])
        output = "You've launched a task"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    def test_meet_test(self):
        def raise_exception(_1, _2, _3, _4):
            with self.assertRaises(SystemExit) as cm:
                meet_test(_1, _2, _3, _4)
            self.assertEqual(cm.exception.code, 0)

        raise_exception(None, None, None, None)
        raise_exception(['1', '2'], None, None, None)
        raise_exception(None, ['1', '3'], None, None)
        raise_exception(['1', '3'], None, ['1'], None)
        raise_exception(None, ['1', '3'], None, ['1'])
