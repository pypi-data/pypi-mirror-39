# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


@click.command()
@click.option('--task-id', help='task id which you want to retrieve.', required=True)
@click.option('--range', help='specify this to retrieve partial output', required=False)
@click.option('--server', help='user-defined server')
def retrieve_final_output(task_id, range, server, launch=False):
    """
    :add 'retrieve-final-output' param to get final output.\n
    :param task_id: the task-id you want to see.\n
    :param range: '0-100' for example (in bytes).\n
    :param server: user-defined server
    """
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    content = response_get(url, task_id, range)
    print(f"{y}{h}The output of this task is:{e}")
    if launch:      # pragma: no cover
        return content
    print(content.decode('utf-8'))


def response_get(url, task_id, range):
    # use this to get requests
    this_url = "/api/v1/task/%s/output" % task_id
    headers = {

    }
    if range is not None:
        headers["Range"] = "bytes=" + range
        response = requests.get(url + this_url, headers=headers)
    else:
        response = requests.get(url + this_url)

    if response.status_code != 200 and response.status_code != 206:
        handle_error(response.status_code, retrieve=True)
        exit(0)
    return response.content


if __name__ == "__main__":
    retrieve_final_output()     # pragma: no cover
