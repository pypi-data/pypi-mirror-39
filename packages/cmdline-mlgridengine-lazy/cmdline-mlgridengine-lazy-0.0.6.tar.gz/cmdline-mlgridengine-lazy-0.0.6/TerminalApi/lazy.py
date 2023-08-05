#!/usr/bin/env python3
import click
import sys
sys.path.append('./')
from src.server_inspection.server_inspect import server_inspect
from src.query_tasks.query import query_task
from src.create_task.create_task import create_task
from src.delete_task.delete_task import delete_task
from src.download_file.download_file import download_file
from src.get_doc.get_doc import get_doc
from src.kill_task.kill_task import kill_task
from src.lauch_task.lauch_task import launch_task
from src.list_files.list_files import list_files
from src.lock_files.lock_files import lock_files
from src.update_fields.update_fields import update_field
from src.create_launch.create_launch import create_launch
from src.batch_operation.batch_operation import batch_del, batch_kill, batch_query
from src.download_task_file.download_task_file import download_task_file
from src.enter_leave_maintenance_mode.enter_leave_maintenance_mode import maintenance_mode
from src.event_bus.event_bus import event_bus
from src.execute_cleanup.execute_cleanup import exec_cleanup
from src.login.login import login
from src.logout.logout import logout
from src.upload_file.upload_file import upload_file
from src.real_time_output.real_time_output import real_time_output
from src.retrieve_final_output.retrieve_final_output import retrieve_final_output


@click.group()
def cli():
    pass    # pragma: no cover


cli.add_command(server_inspect)
cli.add_command(query_task)
cli.add_command(create_task)
cli.add_command(delete_task)
cli.add_command(download_file)
cli.add_command(get_doc)
cli.add_command(kill_task)
cli.add_command(launch_task)
cli.add_command(list_files)
cli.add_command(lock_files)
cli.add_command(update_field)
cli.add_command(create_launch)
cli.add_command(batch_kill)
cli.add_command(batch_del)
cli.add_command(batch_query)
cli.add_command(download_task_file)
cli.add_command(maintenance_mode)
cli.add_command(event_bus)
cli.add_command(exec_cleanup)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(upload_file)
cli.add_command(real_time_output)
cli.add_command(retrieve_final_output)


if __name__ == '__main__':
    cli()  # pragma: no cover
