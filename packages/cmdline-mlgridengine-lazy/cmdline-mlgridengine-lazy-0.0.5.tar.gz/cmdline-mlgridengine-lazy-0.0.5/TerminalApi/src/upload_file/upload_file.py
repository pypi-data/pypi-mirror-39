# -*- coding: future_fstrings -*-
import requests
import sys
import click
import pytz
import datetime
import re
import os
from requests import Request, Session
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


@click.command()
@click.option('--task-id', help='task id which you want to upload file.', required=True, type=str)
@click.option('--lock-until', help='Lock the file to a specific time.', required=True, type=str)
@click.option('--path', help='The system path of the file you want to upload', required=True)
@click.option('--server', help='user-defined server')
def upload_file(task_id, lock_until, path, server, launch=False):
    """
    :add 'upload-file' for uploading a file in binary.\n
    :param task_id: Lock the file for a specific task.\n
    :param lock_until: Usage: '2018-10-24--21:14:20'\n
    :param path: path to the file\n
    :param server: user-defined server
    """
    pattern = re.compile(r'\d{4}\-\d{2}\-\d{2}\-{2}\d{2}\:\d{2}\:\d{2}')
    if re.search(pattern, lock_until) is None:
        print(f"{r}{h}Time format wrong! Check Usage for more information.{e}")
        exit(0)
    this_url = "/api/v1/_upload/simple"
    dt = datetime.datetime.strptime(lock_until, "%Y-%m-%d--%H:%M:%S")
    timezone = pytz.timezone("Etc/Greenwich")
    utc = timezone.localize(dt)
    # get info from input params:
    params = {
        'lock_for': task_id,
        'lock_until': utc
    }
    headers = {
        'Content-Type': 'multipart/form-data',
        'Content-Length': str(os.path.getsize(path))
    }
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = request_post(url, this_url, headers, params, path)
    if launch:
        return response_dic
    print(f"{y}{h}Your file id is {e}" + response_dic['id'])


def request_post(url, this_url, headers, params, path):
    req = requests.Request('POST', url + this_url, headers=headers, params=params)
    code, response_dic = read_upload(req, path)
    if code != 200:
        handle_error(code)
        exit(0)
    return code, response_dic


def read_upload(req, path):
    prepped = req.prepare()
    with open(path, 'rb') as f:
        prepped.body = f.read(os.path.getsize(path))
    s = Session()
    response = s.send(prepped, stream=True)
    return response.status_code, response.json()


if __name__ == '__main__':
    upload_file()   # pragma: no cover
