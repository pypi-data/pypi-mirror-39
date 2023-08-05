# -*- coding: future_fstrings -*-
import requests
import sys
import click
import ast
sys.path.append('./')
from src.error_codes.error_codes import handle_error
from src.utils.utils import *
from src.base_url.base_url import base_url


this_url = "/api/v1/task/_create"


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.option('--name', help='task name')
@click.option('--description', help='description')
@click.option('--tags', help='list of tags', type=list, cls=PythonLiteralOption, required=False)
@click.option('--user-env', help='the environmental variables specified by the user')
# @click.option('--args', help='the task program arguments', required=True, type=list, cls=PythonLiteralOption)
# TODO comment down and uncomment up
@click.option('--args', help='the task program arguments', required=True, type=str)
@click.option('--image', help='docker image name', required=True)  # TODO optional (api)
@click.option('--memory', help='the memory in MBs', type=int, required=True)
@click.option('--cpu', help='the number of CPUs', type=int, required=True)
@click.option('--gpu', help='the number of GPUs', type=int)
@click.option('--disk', help='the disk space in MBs', type=int)
@click.option('--port', help='the number of ports', type=int)
@click.option('--archive-type', help='archive type')
@click.option('--data', help='upload archive data')
@click.option('--work-dir', help='/path/to/the/work_dir')
@click.option('--launch', help='bool to decide whether launch it immediately', type=bool, default=False)
@click.option('--server', help='user-defined server')
def create_task(name, description, tags, user_env, args, image, memory,
                cpu, gpu, disk, port, archive_type, data, work_dir, launch, server):
    """
    :add 'create-task' for creating tasks.\n
    :param tags: usage: --tags '["tag1", "tag2", "tag3"]'\n
    :param args: usage: --args '["python", "main.py"]'\n
    :param server: user-defined server
    """

    # get info from input params:
    info = {
        'args': args,
        'resources': {
            'memory': memory,
            'cpu': cpu
        }
    }
    if name is not None:
        info['name'] = name
    if description is not None:
        info['description'] = description
    if tags is not None:
        info['tags'] = tags
    if work_dir is not None:
        info['options'] = {
            'work_dir': work_dir
        }
    if image is not None:
        info['container'] = {
            'type': "MESOS",
            'image': image
        }
    if gpu is not None:
        info['resources']['gpu'] = gpu
    if disk is not None:
        info['resources']['disk'] = disk
    if port is not None:
        info['resources']['port'] = port
    if archive_type is not None and data is not None:
        info['archive'] = {
            'type': archive_type,
            'data': data
        }
    if user_env is not None:
        info['user_env'] = user_env

    url = base_url
    if server is not None:  # pragma: no cover
        url = server

    response_dic = response_post(url, info)[1]
    if launch:
        return response_dic
    format_printer(response_dic)


def response_post(url, info):
    response = requests.post(url + this_url, json=info)
    if response.status_code != 200:
        handle_error(response.status_code)
        exit(0)
    response_dic = response.json()
    return response.status_code, response_dic


def format_printer(response_dic):
    print(f"{b}{h}Information about the task you created:")
    print(f"  {y}{h}task_id: {e}" + response_dic['id'])
    if 'container' in response_dic:
        print(f"  {y}{h}container: {e}")
        print(
            f"    {g}{h}type: {e}" +
            response_dic['container']['type'])
        if 'image' in response_dic['container']:
            print(
                f"    {g}{h}image: {e}" +
                response_dic['container']['image'])

    print(f"  {y}{h}resources: {e}")
    print(f"    {g}{h}memory: {e}" +
          str(response_dic['resources']['request']['memory']))
    print(f"    {g}{h}cpu: {e}" +
          str(response_dic['resources']['request']['cpu']))

    if 'gpu' in response_dic['resources']['request']:
        print(f"    {g}{h}gpu: {e}" + str(response_dic['resources']['request']['gpu']))

    if 'disk' in response_dic['resources']['request']:
        print(f"    {g}{h}disk: {e}" + str(response_dic['resources']['request']['disk']))

    if 'port' in response_dic['resources']['request']:
        print(f"    {g}{h}port: {e}" + str(response_dic['resources']['request']['port']))

    print(f"  {y}{h}resources: {e}")
    if 'create_time' in response_dic['create_time']:
        print(f"    {g}{h}create_time: {e}" + str(response_dic['create_time']))
    print(f"{b}{h}Task created successfully!{e}")


if __name__ == "__main__":
    create_task()   # pragma: no cover
