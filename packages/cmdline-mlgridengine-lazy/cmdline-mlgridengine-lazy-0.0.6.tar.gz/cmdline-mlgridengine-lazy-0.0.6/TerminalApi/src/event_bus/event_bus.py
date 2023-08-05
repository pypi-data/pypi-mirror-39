# -*- coding: future_fstrings -*-
import requests
import sys
import click
import ast
import json
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.option('--event-type', help='The type of events to be subscribed', cls=PythonLiteralOption, type=list)
@click.option('--task-id', help='The ID of the task whose events should be subscribed.', cls=PythonLiteralOption, type=list)
@click.option('--server', help='user-defined server')
def event_bus(event_type, task_id, server):
    """
    :add 'event-bus' for allowing clients and third-party systems to subscribe events from the server.\n
    :param event_type: '["type1", "type2"]' for example\n
    :param task_id: '["id1", "id2"]' for example\n
    :param server: user-defined server
    """
    # use this to get requests
    this_url = "/api/v1/events"
    params = {

    }
    if event_type is not None:
        if len(event_type) == 1:
            params['event_type'] = event_type[0]
        else:
            params['event_type'] = event_type
    if task_id is not None:
        if len(task_id) == 1:
            params['task_id'] = task_id[0]
        else:
            params['task_id'] = task_id
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    response_dic = get(url, this_url, params)[1]
    print(response_dic)


def get(url, this_url, params):
    response = requests.get(url + this_url, params=params)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


if __name__ == "__main__":
    event_bus()     # pragma: no cover
