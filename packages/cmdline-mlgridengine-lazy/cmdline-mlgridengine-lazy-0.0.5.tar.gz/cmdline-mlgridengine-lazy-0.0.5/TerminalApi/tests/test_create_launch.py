import unittest
import mock
import click
from unittest.mock import Mock, patch, MagicMock
from src.create_launch import create_launch
from src.create_task import create_task
from click.testing import CliRunner
from tests.test_info import *
from tests.test_launch_task import success_res as res_
from src.base_url.base_url import base_url
from tests.test_create_task import success_res as launch_res
import io
import sys
file_id_lis = ['1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890',
               '1234567890']
tmp_dic_ = {
    'create_time_int': 917474903,
    'start_time': '2018-11-21T22:32:16.182+08:00',
    'file_size': 0,
    'container': {
        'type': 'MESOS',
        'image': 'docker.peidan.me/haowenxu/ml-runtime:gpu'},
    'exit_code': '0',
    'id': 'mlge2.zu5tbjbzz3oxeqb9bvbc3xu1',
    'status': 'COMPLETED',
    'resources': {
        'request': {
            'memory': 128,
            'cpu': 1.0,
            'gpu': 1},
        'assigned': {
            'gpu': 0,
            'disk': 0,
            'port': [],
            'cpu': 0.0,
            'memory': 0}},
    'args': [
        'python',
        'count.py',
        '-n',
        '3'],
    'stop_time': '2018-11-21T22:32:19.927+08:00',
    'create_time': '2018-11-21T22:32:14.167+08:00'}

get_doc_ = {
    'create_time_int': 917993789,
    'start_time': '2018-11-21T22:40:56.131+08:00',
    'file_size': 0,
    'container': {
        'type': 'MESOS',
        'image': 'docker.peidan.me/haowenxu/ml-runtime:gpu'},
    'exit_code': '',
    'id': 'mlge2.d7aqmmx1yhdq8mkrd338peiy',
    'status': 'COMPLETED',
    'resources': {
        'request': {
            'memory': 128,
            'cpu': 1.0,
            'gpu': 1},
        'assigned': {
            'gpu': 0,
            'disk': 0,
            'port': [],
            'cpu': 0.0,
            'memory': 0}},
    'args': [
        'python',
        '-u',
        'app.py'],
    'stop_time': '',
    'create_time': '2018-11-21T22:40:53.053+08:00'}

get_doc_killed = {
    'create_time_int': 917474903,
    'start_time': '2018-11-21T22:32:16.182+08:00',
    'file_size': 0,
    'container': {
        'type': 'MESOS',
        'image': 'docker.peidan.me/haowenxu/ml-runtime:gpu'},
    'exit_code': '0',
    'id': 'mlge2.zu5tbjbzz3oxeqb9bvbc3xu1',
    'status': 'KILLED',
    'resources': {
        'request': {
            'memory': 128,
            'cpu': 1.0,
            'gpu': 1},
        'assigned': {
            'gpu': 0,
            'disk': 0,
            'port': [],
            'cpu': 0.0,
            'memory': 0}},
    'args': [
        'python',
        'count.py',
        '-n',
        '3'],
    'stop_time': '2018-11-21T22:32:19.927+08:00',
    'create_time': '2018-11-21T22:32:14.167+08:00'}

create_launch_dic_final = ['--name',
                                name,
                                '--description',
                                description,
                                '--tags',
                                tags,
                                '--user-env',
                                '',
                                '--args',
                                '["python", "app.py"]',
                                '--image',
                                docker,
                                '--memory',
                                memory,
                                '--cpu',
                                cpu,
                                '--gpu',
                                gpu,
                                '--disk',
                                disk,
                                '--port',
                                port,
                                '--archive-type',
                                'zip',
                                '--data',
                                '',
                                '--lock-until',
                                '2019-09-09--11:11:11',
                                '--file-path-list',
                                '["src/base_url/__init__.py"]',
                                '--tar-path-list',
                                '[]',
                                '--dest-file-list',
                                '["__init__.py"]',
                                '--dest-tar-list',
                                '[]',
                                '--range',
                                '1-100',
                                '--retrieve-final',
                                True,
                                '--retrieve-real-time',
                                False,
                                '--offset',
                                0]

create_launch_dic_realtime = ['--name',
                                name,
                                '--description',
                                description,
                                '--tags',
                                tags,
                                '--user-env',
                                '',
                                '--args',
                                '["python", "app.py"]',
                                '--image',
                                docker,
                                '--memory',
                                memory,
                                '--cpu',
                                cpu,
                                '--gpu',
                                gpu,
                                '--disk',
                                disk,
                                '--port',
                                port,
                                '--archive-type',
                                'zip',
                                '--data',
                                '',
                                '--lock-until',
                                '2019-09-09--11:11:11',
                                '--file-path-list',
                                '["src/base_url/__init__.py"]',
                                '--tar-path-list',
                                '[]',
                                '--dest-file-list',
                                '["__init__.py"]',
                                '--dest-tar-list',
                                '[]',
                                '--range',
                                '1-100',
                                '--retrieve-final',
                                False,
                                '--retrieve-real-time',
                                True,
                                '--offset',
                                0]


class CreateLaunchTest(unittest.TestCase):
    def test_call_create_task(self):
        create_launch.invoke_create = MagicMock(return_value=success_res)
        ID = create_launch.call_create_task(
            base_url,
            True,
            10,
            None,
            name,
            description,
            tags,
            '',
            '["ls", "-a"]',
            docker,
            memory,
            cpu,
            gpu,
            disk,
            port,
            'zip',
            'data',
            None)
        self.assertEqual(ID, task_id)

    def test_call_create_task_None(self):
        create_launch.invoke_create = MagicMock(return_value=success_res)
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        with self.assertRaises(SystemExit) as cm:
            create_launch.call_create_task(
                base_url,
                True,
                None,
                None,
                name,
                description,
                tags,
                '',
                '["ls", "-a"]',
                docker,
                memory,
                cpu,
                gpu,
                disk,
                port,
                'zip',
                'data',
                None)
        self.assertEqual(cm.exception.code, 0)
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn('You must set 「offset」', capturedoutput.getvalue())

    def test_call_upload_file(self):
        create_launch.invoke_upload = MagicMock(return_value='1234567890')
        file_id_list, tar_id_list = create_launch.call_upload_file(
            base_url, '["/Users/ligen/Desktop/app.py"]', '2018-09-09--12:12:12', '["app.py"]', None, task_id, '[]', '[]')
        self.assertEqual(file_id_list, file_id_lis)

    def test_call_launch_task(self):
        create_launch.call_launch_task = MagicMock(return_value=res_)
        launch_dic = create_launch.call_launch_task(
            base_url, None, '["1234567890"]', '[]', task_id, '["app.py"]', '[]')
        self.assertEqual(launch_dic, res_)

    def test_call_final(self):
        create_launch.get_tmp_dic = MagicMock(return_value=tmp_dic_)
        create_launch.call_retrieve_final = MagicMock(
            return_value=b'3\n2\n1\n0')
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        create_launch.call_final(base_url, None, task_id, '0-100')
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn('3', capturedoutput.getvalue())

    def test_call_realtime(self):
        create_launch.get_real_time_output = MagicMock(
            return_value=(10, 1, b'1\n2\n3\n4\n5\n'))
        create_launch.get_real_time_tmp_dic = MagicMock(return_value=get_doc_)
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        create_launch.call_real_time(base_url, None, task_id, 1, None)
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn('3', capturedoutput.getvalue())
        create_launch.get_real_time_tmp_dic = MagicMock(return_value=get_doc_killed)

    def test_create_launch(self):
        create_launch.call_create_task = MagicMock(return_value=task_id)
        create_launch.call_upload_file = MagicMock(
            return_value=(['file1', 'file2'], ['tar1', 'tar2']))
        create_launch.call_launch_task = MagicMock(return_value=launch_res)
        create_launch.call_final = MagicMock(return_value=None)
        create_launch.call_real_time = MagicMock(return_value=None)
        runner = CliRunner()
        result = runner.invoke(create_launch.create_launch, create_launch_dic_final)
        output = 'You have launched a task successfully'
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(create_launch.create_launch, create_launch_dic_realtime)
        output = 'You have launched a task successfully'
        self.assertIn(output, result.output)
        self.assertEqual(result.exit_code, 0)

    def test_print_running(self):
        capturedoutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedoutput  # and redirect stdout.
        create_launch.print_running((100, 10, b'1\n2\n3\n4\n5\n6\n7\n8\n9'), b'1')
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual('\n2\n3\n4\n5\n6\n7\n8\n9\n', capturedoutput.getvalue())

        sys.stdout = capturedoutput  # and redirect stdout.
        create_launch.print_running((100, 10, b'19'), b'1')
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual('\n2\n3\n4\n5\n6\n7\n8\n9\n9\n', capturedoutput.getvalue())
