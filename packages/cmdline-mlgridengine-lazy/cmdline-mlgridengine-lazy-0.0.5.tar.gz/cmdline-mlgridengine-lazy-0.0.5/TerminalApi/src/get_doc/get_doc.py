# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.query_tasks.query import parser
from src.base_url.base_url import base_url


@click.command()
@click.option('--task-id', type=str, help='which task', required=True)
@click.option('--server', help='user-defined server')
def get_doc(task_id, server, launch=False):
    """
    :add 'get-doc' for getting the document of a task\n
    :param server: user-defined server
    """
    # use this to get requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = response_get(url, task_id)
    if launch:
        return response_dic
    print(f"{b}{h}The document of the specified task is listed as follows:{e}")
    parser(response_dic, mode='single')


def response_get(url, task_id):
    this_url = "/api/v1/task/%s" % task_id
    response = requests.get(url + this_url)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


if __name__ == "__main__":
    get_doc()   # pragma: no cover
