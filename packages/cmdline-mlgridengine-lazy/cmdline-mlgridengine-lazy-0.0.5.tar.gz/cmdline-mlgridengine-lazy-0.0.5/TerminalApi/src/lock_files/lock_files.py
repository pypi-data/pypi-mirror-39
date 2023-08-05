# -*- coding: future_fstrings -*-
import requests
import sys
import click
import ast
import datetime
import pytz
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):  # pragma: no cover
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.option('--file-id-list', help='task id which you want to update.', required=True, cls=PythonLiteralOption)
@click.option('--lock-until', help='Lock the file to a specific time.', required=True, type=str)
@click.option('--task-id', help='task id which you want to update.', required=True, type=str)
@click.option('--server', help='user-defined server')
def lock_files(file_id_list, lock_until, task_id, server):
    """
    :add 'lock-files' for locking a file in binary.\n
    :param file_id_list: Lock the files for a specific task. Usage: '["id1", "id2"]'\n
    :param lock_until: '2018-10-24--21:14:20' for example\n
    :param task_id: Lock until this task finishes or deleted.\n
    :param server: user-defined server
    """
    this_url = "/api/v1/_upload/lock"
    dt = datetime.datetime.strptime(lock_until, "%Y-%m-%d--%H:%M:%S")
    timezone = pytz.timezone("Etc/Greenwich")
    utc = timezone.localize(dt).isoformat()
    # new a info and process it afterwards
    info = {
        'files': [

        ],
        'task': task_id,
        'until': utc
    }
    for file in file_id_list:
        info['files'].append(file)
    # use this to post requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = response_post(url, this_url, info)
    print(f"{y}{h}These files are locked.{e}")
    for file in response_dic['locked']:
        print("  " + file)


def response_post(url, this_url, info):
    response = requests.post(url + this_url, json=info)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


if __name__ == '__main__':
    lock_files()    # pragma: no cover
