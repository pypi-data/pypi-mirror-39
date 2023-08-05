# -*- coding: future_fstrings -*-
import sys
import click
import time
import ast
sys.path.append('./')
from src.utils.utils import *
from src.create_task.create_task import create_task
from src.lauch_task.lauch_task import launch_task
from src.upload_file.upload_file import upload_file
from src.query_tasks.query import parser
from src.query_tasks.query import query_task
from src.retrieve_final_output.retrieve_final_output import retrieve_final_output
from src.real_time_output.real_time_output import real_time_output
from src.get_doc.get_doc import get_doc
from src.base_url.base_url import base_url


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):  # pragma: no cover
        try:
            if value is None:
                return
            return ast.literal_eval(value)
        except BaseException:
            raise click.BadParameter(value)


@click.command()
@click.pass_context
@click.option('--name', help='task name')
@click.option('--description', help='description')
@click.option('--tags', help='list of tags', type=list, cls=PythonLiteralOption)
@click.option('--user-env', help='environmental variables')
@click.option('--args', help='commands', required=True, type=list, cls=PythonLiteralOption)
@click.option('--image', help='name of docker image', required=True)
@click.option('--memory', help='memory in MBs', type=int, required=True)
@click.option('--cpu', help='number of CPUs', type=int, required=True)
@click.option('--gpu', help='number of GPUs', type=int)
@click.option('--disk', help='disk space in MBs', type=int)
@click.option('--port', help='number of ports', type=int)
@click.option('--archive-type', help='archive type, including .zip')
@click.option('--data', help='archive data to be uploaded')
@click.option('--work-dir', help='eg. /path/to/the/work_dir')
@click.option('--lock-until', help='Lock the file to a specific time.', type=str)
@click.option('--file-path-list', help='The system path of the files you want to upload', type=list, cls=PythonLiteralOption)
@click.option('--tar-path-list', help='The system path of the tars you want to upload', type=list, cls=PythonLiteralOption)
@click.option('--dest-file-list', help='destination of this file in working directory', required=False, type=list, cls=PythonLiteralOption)
@click.option('--dest-tar-list', help='destination directory to extract this archive', required=False, type=list, cls=PythonLiteralOption)
@click.option('--range', help='specify this to retrieve partial output', required=False)
@click.option('--retrieve-final', help='set this to be true if you want to retrieve final output immediately', default=False)
@click.option('--retrieve-real-time', help='set this to be true if you want to retrieve real time output immediately', default=False)
@click.option('--offset', help='The offset of the output (in bytes) to read begin. -1 refers to eof', required=False, type=int)
@click.option('--count', help='The maximum number of output (in bytes) to read', type=int, required=False)
@click.option('--server', help='user-defined server')
def create_launch(ctx, name, description, tags, user_env, args, image, memory, cpu, gpu, disk, port, archive_type, data, work_dir, lock_until, file_path_list, tar_path_list, dest_file_list, dest_tar_list, range, retrieve_final, retrieve_real_time, offset, count, server):
    """
    :add 'create-launch' for create a task and launch it at the same time.\n
    :param tags: usage: --tags '["tag1", "tag2", "tag3"]'\n
    :param args: usage: --args '["python", "main.py"]'\n
    :param lock_until: usage: '2018-10-24--21:14:20'\n
    :param file_path_list: the path list of the files you want to upload. (not archive) usage: '["path/of/file1", "path/of/file2"]'\n
    :param dest_file_list: the name of the file. Usage: '["file1.py", "file2.cpp"]'\n
    :param server: user-defined server\n

    A template is shown in launch-final.sh and launch-real-time.sh
    """
    url = base_url
    if server is not None:
        url = server

    _id = call_create_task(url, retrieve_real_time, offset, ctx, name, description, tags, user_env, args, image, memory, cpu, gpu, disk, port, archive_type, data, work_dir)

    file_id_list, tar_id_list = call_upload_file(url, file_path_list, lock_until, dest_file_list, ctx, _id, tar_path_list, dest_tar_list)

    launch_dic = call_launch_task(url, ctx, file_id_list, tar_id_list, _id, dest_file_list, dest_tar_list)

    call_print(url, launch_dic, retrieve_final, ctx, _id, range, retrieve_real_time, offset, count)


def call_create_task(url, retrieve_real_time, offset, ctx, name, description, tags, user_env, args, image, memory, cpu, gpu, disk, port, archive_type, data, work_dir):
    if retrieve_real_time is True and offset is None:
        print(f"{r}{h} You must set 「offset」 to check real time output.{e}")
        exit(0)
    response_dic = invoke_create(name, description, tags, user_env, args, image, memory, cpu, gpu, disk, port, archive_type, data, work_dir, ctx, url)
    _id = response_dic['id']
    return _id


def invoke_create(name, description, tags, user_env, args, image, memory, cpu, gpu, disk, port, archive_type, data, work_dir, ctx, url):
    response_dic = ctx.invoke(create_task, name=name, description=description, tags=tags, user_env=user_env, args=args, image=image, memory=memory, cpu=cpu, gpu=gpu, disk=disk, port=port, archive_type=archive_type, data=data, work_dir=work_dir, server=url, launch=True)
    return response_dic


def call_upload_file(url, file_path_list, lock_until, dest_file_list, ctx, _id, tar_path_list, dest_tar_list):
    file_id_list = []
    if file_path_list is not None:
        if lock_until is None:
            print(f"{r}{h}ERROR! You must specify lock-until!{e}")
            exit(0)
        if dest_file_list is None:
            print(f"{r}{h}ERROR! You must specify dest-file-list!{e}")
            exit(0)
        for i in file_path_list:
            file_id = invoke_upload(url, ctx, _id, lock_until, i)
            file_id_list.append(file_id)

    tar_id_list = []
    if tar_path_list is not None:
        if lock_until is None:
            print(f"{r}{h}ERROR! You must specify lock-until!{e}")
            exit(0)
        if dest_tar_list is None:
            print(f"{r}{h}ERROR! You must specify dest-tar-list!{e}")
            exit(0)
        for i in tar_path_list:
            tar_id = invoke_upload(url, ctx, _id, lock_until, i)
            tar_id_list.append(tar_id)
    return file_id_list, tar_id_list


def invoke_upload(url, ctx, _id, lock_until, i):
    ID = ctx.invoke(upload_file, task_id=_id, lock_until=lock_until, path=i, server=url, launch=True)['id']
    return ID


def call_launch_task(url, ctx, file_id_list, tar_id_list, _id, dest_file_list, dest_tar_list):
    launch_dic = ctx.invoke(launch_task, server=url, file_id_list=file_id_list, tar_id_list=tar_id_list, task_id=_id, dest_file_list=dest_file_list, dest_tar_list=dest_tar_list, launch=True)
    return launch_dic


def call_print(url, launch_dic, retrieve_final, ctx, _id, range, retrieve_real_time, offset, count):
    print(f"{b}{h}You have launched a task successfully!{e}")
    parser(launch_dic, mode='single')
    if retrieve_final:
        call_final(url, ctx, _id, range)
    elif retrieve_real_time:
        call_real_time(url, ctx, _id, offset, count)


def call_final(url, ctx, _id, range):
    print(f"{g}{h}The task is running...\nYou can get your output after it is finished...\nRUNNING...{e}")
    while True:
        tmp_dic = get_tmp_dic(url, ctx, _id)
        if tmp_dic['status'] != 'COMPLETED':  # pragma: no cover
            time.sleep(0.2)
            continue
        if tmp_dic['status'] == 'COMPLETED':
            output_ = call_retrieve_final(url, ctx, _id, range)
            print(output_.decode('utf-8'))
            break


def get_tmp_dic(url, ctx, _id):
    tmp_dic = {}
    flag = False
    while True:     # pragma: no cover
        tmp_doc = ctx.invoke(query_task, server=url, launch=True)['tasks']
        for task in tmp_doc:
            if task['id'] == _id:
                tmp_dic = task
                flag = True
                break
        if flag:
            break
    return tmp_dic


def call_retrieve_final(url, ctx, _id, range):
    output_ = ctx.invoke(retrieve_final_output, task_id=_id, range=range, server=url, launch=True)
    return output_


def get_real_time_tmp_dic(url, ctx, _id):
    tmp_dic = ctx.invoke(get_doc, task_id=_id, server=url, launch=True)
    return tmp_dic


def get_real_time_output(url, ctx, _id, offset, count):
    val = ctx.invoke(real_time_output, task_id=_id, offset=offset, count=count, server=url, launch=True)
    return val


def call_real_time(url, ctx, _id, offset, count):
    print(f"{g}{h}The task is running...\n{e}")
    print(f"{y}{h}The output of this task is:{e}")
    tmp_str = b''
    while True:
        tmp_dic = get_real_time_tmp_dic(url, ctx, _id)
        if tmp_dic['status'] == 'COMPLETED' or tmp_dic['status'] == 'KILLED' or tmp_dic['status'] == 'DELETED':
            print_com_kill(tmp_dic)
            break
        if tmp_dic['status'] == 'RUNNING':  # pragma: no cover
            while True:
                val = get_real_time_output(url, ctx, _id, offset, count)
                if len(val) == 1:
                    continue
                elif len(val) == 3:
                    tmp_str = print_running(val, tmp_str)
                    break


def print_com_kill(tmp_dic):
    if tmp_dic['status'] == 'COMPLETED':
        print(f"{y}{h}      TASK FINISHED!{e}")
    elif tmp_dic['status'] == 'KILLED':
        print(f"{y}{h}      TASK KILLED!{e}")


def print_running(val, tmp_str):
    len_, offset_, output_ = val
    if tmp_str != output_:
        # TODO maybe buggy (fix it perhaps :)
        if b'\n' in output_.replace(tmp_str, b'', 1):
            for i in output_.replace(tmp_str, b'').rstrip().split(b'\n'):
                print(i.decode('utf-8'))
        else:
            print(output_.replace(tmp_str, b'').rstrip().decode('utf-8'))
        tmp_str = output_
    return tmp_str


if __name__ == "__main__":
    create_launch()     # pragma: no cover
