# -*- coding: future_fstrings -*-
import requests
import sys
import os
import click
import shutil
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url
import errno


@click.command()
@click.option('--task-id', type=str, help='which task', required=True)
@click.option('--path', help='the directory of the files')
@click.option('--range-to-download', help='Specify this header to download partial content of the file.')
@click.option('--server', help='user-defined server')
def download_file(task_id, path, range_to_download, server):
    """
    :add 'download-file' for downloading the file given directory\n
    :param path: 'optional, string containing slashes ("/")' Path (relative to the root working directory) of the file to be downloaded.\n
    :param range_to_download: 'bytes=500-999' or 'bytes=500-' for example\n
    :param server: user-defined server
    """
    # use this to get requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    response = response_get(url, path, task_id, range_to_download)
    file_name = save_file(path, response)
    print(f"{g}{h}Download successfully! Your file location: {e}%s" % ('./download/%s' % file_name))


def response_get(url, path, task_id, range_to_download):
    if path is not None:
        this_url = "/api/v1/task/%s/_getfile/%s" % (task_id, path)
    else:
        this_url = "/api/v1/task/%s/_getfile/" % task_id
    if range_to_download is not None:
        headers = {
            'Range': range_to_download
        }
        response = requests.get(url + this_url, headers=headers, stream=True)
    else:
        response = requests.get(url + this_url, stream=True)

    if response.status_code != 200 and response.status_code != 206:
        handle_error(response.status_code, download_file=True)
        exit(0)
    return response


def save_file(path, response):
    # TODO now path must be file name, probably because of backend.
    if path is None:
        print(f"{r}{h}You should specify file name!{e}")
        exit(0)
    file_name = path
    for idx, i in enumerate(path):
        if i == '/':
            file_name = path[(idx + 1):]
    if file_name is None:
        file_name = 'download'
    filename = './download/%s' % file_name
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    write_file(filename, response)
    return file_name


def write_file(filename, response):
    with open(filename, 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)


if __name__ == "__main__":
    download_file()     # pragma: no cover
