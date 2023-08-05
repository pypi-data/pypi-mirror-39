# -*- coding: future_fstrings -*-
import requests
import sys
import click
import ast
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url
from src.query_tasks.query import parser


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.option('--file-id-list', help='file id which you want to link.', required=False, cls=PythonLiteralOption, type=list)
@click.option('--tar-id-list', help='compressed file id which you want to extract.', required=False, cls=PythonLiteralOption, type=list)
@click.option('--task-id', help='task id which you want to launch.', required=True, type=str)
@click.option('--dest-file-list', help='destination of this file in working directory', required=False, cls=PythonLiteralOption, type=list)
@click.option('--dest-tar-list', help='destination directory to extract this archive', required=False, cls=PythonLiteralOption, type=list)
@click.option('--server', help='user-defined server')
def launch_task(file_id_list, tar_id_list, task_id, dest_file_list, dest_tar_list, server, launch=False):
    """
    :add 'launch-task' for launching a given task.\n
    :param file_id_list: Usage: '["id1", "id2", "id3"]'\n
    :param dest_file_list: This is the name of files. Usage: '["file1.py", "file2.cpp"]'\n
    :param server: user-defined server
    """
    this_url = "/api/v1/task/%s/_start" % task_id
    # new a info and process it afterwards
    info = {
        'assets': [

        ]
    }

    meet_test(file_id_list, tar_id_list, dest_file_list, dest_tar_list)

    if file_id_list:
        for idx, i in enumerate(file_id_list):
            info['assets'].append({
                'type': 'file',
                'id': i,
                'dest': dest_file_list[idx]
            })

    if tar_id_list:
        for idx, j in enumerate(tar_id_list):
            info['assets'].append({
                'type': '.zip',
                'id': j,
                'dest': dest_tar_list[idx]
            })

    # use this to post requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = request_post(url, this_url, info)
    if launch:
        return response_dic
    print(f"{b}{h}You've launched a task, and here is its information:{e}")
    parser(response_dic, mode='single')


def request_post(url, this_url, info):
    response = requests.post(url + this_url, json=info)
    if response.status_code != 200:
        handle_error(response.status_code, launch_task=True)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


def meet_test(file_id_list, tar_id_list, dest_file_list, dest_tar_list):
    if file_id_list is None and tar_id_list is None:
        print(f"{r}{h}You must specify file-id-list or tar-id-list!{e}")
        exit(0)
    if file_id_list != [] and file_id_list is not None and dest_file_list is None:
        print(f"{r}{h}You must specify dest_file_list!{e}")
        exit(0)
    if tar_id_list != [] and tar_id_list is not None and dest_tar_list is None:
        print(f"{r}{h}You must specify dest_tar_list!{e}")
        exit(0)
    if file_id_list != [] and file_id_list is not None and len(file_id_list) != len(dest_file_list):
        print(f"{r}{h}The length of dest_file must match file_id_list's.{e}")
        exit(0)
    if tar_id_list != [] and tar_id_list is not None and len(tar_id_list) != len(dest_tar_list):
        print(f"{r}{h}The length of dest_tar must match tar_id_list's.'{e}")
        exit(0)


if __name__ == '__main__':
    launch_task()       # pragma: no cover
