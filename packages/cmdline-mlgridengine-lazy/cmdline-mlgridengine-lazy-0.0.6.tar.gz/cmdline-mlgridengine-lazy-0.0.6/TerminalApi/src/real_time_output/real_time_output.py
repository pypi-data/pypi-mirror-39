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
@click.option('--offset', help='The offset of the output (in bytes) to read begin. -1 refers to eof', required=True, type=int)
@click.option('--count', help='The maximum number of output (in bytes) to read', type=int, required=False)
@click.option('--server', help='user-defined server')
def real_time_output(task_id, offset, count, server, launch=False):
    """
    :add 'real-time-output' to retrieve output real-time.\n
    :param offset: 100 for example\n
    :param count: 100 for example\n
    :param server: user-defined server
    """
    # use this to get requests
    url = base_url
    if server is not None:
        url = server

    code, header, content = response_get(url, task_id, offset, count)
    if code != 200 and code != 204:
        if code == 500 and launch:
            return 'TRY_AGAIN'
        else:
            handle_error(code, realtime=True)
            exit(0)
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    if not launch:
        print(f"{y}{h}The output of this task is:{e}")
        tmp_str = b''
        while True:
            while True:
                if code != 200 and code != 204:
                    continue
                code, header, content = response_get(url, task_id, offset, count)
                val = (code, header, content)
                tmp_str = print_(val, tmp_str)
                break

    content_length = header['Content-Length']
    output = content
    _offset = output.split(b'\r\n')[0]
    output = output.split(b'\r\n')[1:][0]
    return content_length, _offset, output


def response_get(url, task_id, offset, count):
    this_url = "/api/v1/task/%s/output/_poll" % task_id
    params = {
        'offset': offset
    }
    if count is not None:
        params['count'] = count
    response = requests.get(url + this_url, params=params)
    return response.status_code, response.headers, response.content


def print_(tp, tp_st):
    l, o, out = tp
    if tp_st != out:
        if b'\n' in out.replace(tp_st, b'', 1):
            for i in out.replace(tp_st, b'').rstrip().split(b'\n'):
                print(i.decode('utf-8'))
        else:
            print(out.replace(tp_st, b'').rstrip().decode('utf-8'))
        tp_st = out
    return tp_st


if __name__ == "__main__":
    real_time_output()      # pragma: no cover
