# -*- coding: future_fstrings -*-
import requests
import sys
import click
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


this_url = "/api/v1/task/_query"
headers = {'content-type': 'application/json'}


@click.command()
@click.option('--skip', default=0, help='number of tasks to skip at the front')
@click.option('--limit', default=100, help='maximum number of tasks to obtain')  # TODO default value configurable
@click.option('--query', default="", help='query string')
@click.option('--server', help='user-defined server')
def query_task(skip, limit, query, server, launch=False):
    """
    :add 'query-task' for querying tasks\n
    :param server: user-defined server
    """

    # get info from input params:
    info = {
        "skip": skip,
        "limit": limit,
        "query": query
    }
    # use this to post requests
    url = base_url
    if server is not None:  # pragma: no cover
        url = server
    code, response_dic = response_post(url, info)
    if launch:   # pragma: no cover
        return response_dic
    # start to proceed the return dictionary and print them pretty.
    total_tasks = response_dic['estimated_total']
    print(f"{g}{b}There are %d tasks that meet the requirements: "
          f"{e}" % total_tasks)
    parser(response_dic['tasks'])


def response_post(url, info):
    response = requests.post(url + this_url, json=info, headers=headers)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


def parser(info, mode="multi"):
    if mode == 'multi':
        for tasks in info:
            name = tasks['id']
            format_print(tasks, name)
    elif mode == 'single':
        name = info['id']
        format_print(info, name)


def format_print(tasks, name):
    print(f"{g}{h}Task %s: {e}" % name)
    if 'name' in tasks:
        print(f"{y}  name: {e}" + tasks['name'])
    print(f"{y}  start_time: {e}" + tasks['start_time'])
    if 'description' in tasks:
        print(f"{y}  description: {e}" + tasks['description'])
    print(f"{y}  file_size: {e}" + str(tasks['file_size']))
    if 'user_env' in tasks:
        print(f"{y}  user_env: {e}" + tasks['user_env'])
    print(f"{y}  tags: {e}")
    if 'tags' in tasks:
        for tags in tasks['tags']:
            print("    " + tags)
    print(f"{y}  container: {e}")
    for i in tasks['container']:
        print("    " + i + ": " + tasks['container'][i])
    print(f"{y}  exit_code: {e}" + str(tasks['exit_code']))
    print(f"{y}  id: {e}" + str(tasks['id']))
    print(f"{y}  status: {e}" + str(tasks['status']))
    print(f"{y}  resources: {e}")
    for i in tasks['resources']:
        print("    " + i + ": ")
        for j in tasks['resources'][i]:
            print("      " + j + ": " + str(tasks['resources'][i][j]))
    print(f"{y}  args: {e}" + str(tasks['args']))
    print(f"{y}  stop_time: {e}" + str(tasks['stop_time']))
    print(f"{y}  create_time: {e}" + str(tasks['create_time']))
    print(f"{y}=========================================={e}")


if __name__ == "__main__":
    query_task()        # pragma: no cover
