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
def logout(server):
    """
    :add 'logout' for user logout.\n
    :param server: user-defined server
    """
    # use this to get requests
    this_url = "/api/v1/auth/_logout"
    info = {

    }
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    post(url, this_url, info)
    print(f"{y}{h}Logout succeed.{e}")


def post(url, this_url, info):
    response = requests.post(url + this_url, json=info)

    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    return response.status_code, response.json()


if __name__ == "__main__":
    logout()    # pragma: no cover
