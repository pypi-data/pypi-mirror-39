# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


@click.command()
@click.option('--if-maintain', help='whether or not to turn on maintenance mode', required=True, type=bool)
@click.option('--server', help='user-defined server')
def maintenance_mode(if_maintain, server):
    """
        :add 'maintenance-mode' param to Check Maintenance Mode.\n
        :param server: user-defined server
    """
    # use this to get requests
    this_url = "/api/v1/_manage/maintenance"
    info = {
        'maintenance': if_maintain
    }
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    response_post(url, this_url, info)
    print(f"{g}{h}You've changed the server maintenance mode: {e}")
    if if_maintain:
        print(f"{y}{h}  IN MAINTENANCE.{e}")
    else:
        print(f"{y}{h}  Not in maintenance.{e}")


def response_post(url, this_url, info):
    response = requests.post(url + this_url, json=info)

    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    return response.status_code, response.json()


if __name__ == "__main__":
    maintenance_mode()  # pragma: no cover
