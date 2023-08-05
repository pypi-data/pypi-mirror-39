# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


@click.command()
@click.option('--task-id', help='task id which you want to launch.', required=True)
@click.option('--server', help='user-defined server')
def delete_task(task_id, server):
    """
    :add 'delete-task' for killing a task.\n
    :param server: user-defined server
    """
    url = base_url
    if server is not None:  # pragma: no cover
        url = base_url
    code, response_dic = response_post(url, task_id)
    if code == 200 and response_dic == {}:
        print(f"{g}{h}Task %s has been deleted!{e}" % task_id)


def response_post(url, task_id):
    this_url = "/api/v1/task/%s/_delete" % task_id
    # new a info and process it afterwards
    info = {

    }
    # use this to post requests
    response = requests.post(url + this_url, json=info)
    if response.status_code != 200:
        handle_error(response.status_code, launch_task=True)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


if __name__ == '__main__':
    delete_task()   # pragma: no cover
