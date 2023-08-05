# -*- coding: future_fstrings -*-
import requests
import sys
import click
import ast
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.query_tasks.query import parser
from src.base_url.base_url import base_url


headers = {'content-type': 'application/json'}


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):  # pragma: no cover
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.option('--task-id', help='task id which you want to update.', required=True, type=str)
@click.option('--name', help='experiment name')
@click.option('--description', help='description')
@click.option('--tags', help='list of tags', required=False, type=list, cls=PythonLiteralOption)
@click.option('--server', help='user-defined server')
def update_field(task_id, name, description, tags, server):
    """
    :add 'update-field' for updating the field of a task\n
    :param task_id: '--task-id 0' for example\n
    :param tags: '["tag1", "tag2"]' for example\n
    :param server: user-defined server
    """
    this_url = "/api/v1/task/%s/_update" % task_id
    # get info from input params:
    info = {

    }
    if name is not None:
        info['name'] = name
    if description is not None:
        info['description'] = description
    if tags is not None:
        info['tags'] = tags
    # use this to post requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    parser(post(url, this_url, info)[1], mode='single')


def post(url, this_url, info):
    response = requests.post(url + this_url, json=info, headers=headers)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    print(f"{b}{h}Your task has been updated:{e}")
    return response.status_code, response_dic


if __name__ == '__main__':
    update_field()  # pragma: no cover
