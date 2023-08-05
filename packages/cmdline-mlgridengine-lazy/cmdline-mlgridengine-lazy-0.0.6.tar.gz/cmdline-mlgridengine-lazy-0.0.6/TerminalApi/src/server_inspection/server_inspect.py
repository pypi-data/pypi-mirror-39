from __future__ import print_function
from __future__ import division

import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.base_url.base_url import base_url
from src.utils.utils import *


def response_get(url):
    # use this to get requests
    this_url = "/api/_inspect"
    response = requests.get(url + this_url, timeout=5)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


def info_process(response_dic):
    # start to proceed the return dictionary and print them pretty.
    print(y + h + "Feature sets of the server are listed as follows:" + e)
    print(g + "Server version:" + e)
    print("    " + response_dic['version'])
    print(g + "The highest API version:" + e)
    print("    " + response_dic['api_version'])
    print(g + "Whether or not the server is in maintenance:" + e)
    print("    " + str(response_dic['maintenance']))
    print(g + "Features supported by the server:" + e)

    for key in response_dic['features']:
        print("    " + key)
    print(g + "limits:" + e)

    for key in response_dic['limits']:
        dic = response_dic['limits']

        if key == 'task.assets_archive.max_size':
            print(
                b + "Maximum size in MB of the file uploaded by /api/v1/task/_create: " + e + str(dic[key]))

        elif key == 'archive.compression.supported_file_types':
            total = ""

            for name in dic[key]:
                total += name
                total += ' '
            print(
                b + "These compression archive types are supported: " + e +
                total)
        elif key == 'archive.decompression.supported_file_types':
            total = ""
            for name in dic[key]:
                total += name
                total += ' '
            print(
                b + "These decompression archive types are supported: " + e +
                total)
    print(g + "Backend specific options for creating the task:" + e)
    if 'task_options' in response_dic:
        if 'work_dir' in response_dic['task_options']:
            print(g + "Working directory of the task:" + e)
            print(g + "type:" + response_dic['task_options']['work_dir']['type'] + e)
            print(g + 'description:' + response_dic['task_options']['work_dir']['description'] + e)


@click.command()
@click.option('--server', help='user-defined server')
def server_inspect(server):
    """
    :add 'server-inspect' param to inspect server features.\n
    :param server: user-defined server
    """
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = response_get(url)
    info_process(response_dic)


if __name__ == "__main__":
    server_inspect()    # pragma: no cover
