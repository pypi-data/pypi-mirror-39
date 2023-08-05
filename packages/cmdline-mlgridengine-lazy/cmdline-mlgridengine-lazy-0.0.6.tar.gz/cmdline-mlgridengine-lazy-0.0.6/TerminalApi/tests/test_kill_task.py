import unittest
import mock
from src.kill_task.kill_task import *
from click.testing import CliRunner
from tests.test_info import *
from tests.test_mock import MockResponse
from src.base_url.base_url import base_url


success_res = {
    u'status': u'KILLED',
    u'container': {
        u'image': u'docker.peidan.me/haowenxu/ml-runtime:gpu',
        u'type': u'MESOS'},
    u'create_time_int': 641471862,
    u'start_time': u'2018-11-18T17:52:16.500+08:00',
    u'args': [
        u'python',
        u'-u',
        u'app.py'],
    u'exit_code': u'',
    u'create_time': u'2018-11-18T17:52:11.127+08:00',
    u'stop_time': u'',
    u'file_size': 0,
    u'id': u'mlge2.yqvcloapraq6rlrsvpvlha7n',
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


query_req = {

}


class CreateTaskTest(unittest.TestCase):
    @mock.patch('requests.post')
    def test_post(self, mock_class):
        mock_class.return_value = MockResponse(success_res, 200)
        status_code, response = response_post(base_url, query_req)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, success_res)

    @mock.patch('src.kill_task.kill_task.response_post')
    def test_kill_task(self, mock_class):
        mock_class.return_value = (200, success_res)
        runner = CliRunner()
        result = runner.invoke(kill_task, ['--task-id', task_id])
        output = "You have been successfully killed"
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)
