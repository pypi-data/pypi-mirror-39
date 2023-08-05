# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


@click.command()
@click.option('--server', help='user-defined server')
def exec_cleanup(server):
    # use this to get requests
    """
    :add 'exec-cleanup' for executing background cleanup jobs\n
    :param server: user-defined server
    """
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = response_post(url)
    print(f"{y}{h} %s{e}" % response_dic['statistics']["deleted_tasks"] + "have been deleted in this operation.")


def response_post(url):
    this_url = "/api/v1/_manage/cleanup"
    info = {

    }
    response = requests.post(url + this_url, json=info)

    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


if __name__ == "__main__":
    exec_cleanup()      # pragma: no cover
