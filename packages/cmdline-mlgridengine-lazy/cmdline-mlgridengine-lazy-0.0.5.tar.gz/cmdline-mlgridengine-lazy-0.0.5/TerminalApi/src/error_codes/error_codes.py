# -*- coding: future_fstrings -*-
from src.utils.utils import *


def handle_error(
        code,
        list_files=False,
        download_file=False,
        launch_task=False,
        retrieve=False,
        realtime=False):
    # error handler.
    if code == 200:
        return
    elif code == 400:
        call_400(list_files, download_file, retrieve)
    elif code == 401:
        call_401()
    elif code == 403:
        call_403()
    elif code == 404:
        call_404(realtime)
    elif code == 405:
        call_405()
    elif code == 409:
        call_409(launch_task, retrieve, realtime, download_file)
    elif code == 413:
        call_413()
    elif code == 500:
        call_500()
    elif code == 501:
        call_501()
    elif code == 503:
        call_503()
    elif code == 507:
        call_507()


def call_400(list_files, download_file, retrieve):
    if list_files or download_file:
        print(f"{r}{h}The task or path does not exist.{e}")
    elif retrieve:
        print(f"{r}{h}The task doesn't exist or the output doesn't exist.{e}")
    else:
        print(f"{r}{h}The request parameters or body is invalid "
              f"(e.g., syntax error).{e}")
    return


def call_401():
    print(f"{r}{h}The client does not provide authentication token "
          f"(i.e., user has not logged in).{e}")
    return


def call_403():
    print(f"{r}{h}The client does not provide authentication token "
          f"(i.e., user has not logged in).{e}")
    return


def call_404(realtime):
    if realtime:
        print(f"{r}{h}The task does not exist.{e}")
    else:
        print(f"{r}{h}Some requested object does not exist, "
              f"or some API endpoint is not supported, "
              f"or some file to be linked doesn't exist.{e}")
    return


def call_405():
    print(f"{r}{h}The API endpoint does not support the request method "
          f"(e.g., `POST` to a `GET`-only API).{e}")
    return


def call_409(launch_task, retrieve, realtime, download_file):
    if launch_task:
        print(f"{r}{h}The task status is not CREATING.{e}")
    elif retrieve:
        print(f"{r}{h}The Task is not finished.{e}")
    elif realtime:
        print(f"{r}{h}The task is not running or just finished running.{e}")
    elif download_file:
        print(f"{r}{h}The path exists but is a directory, not a file.{e}")
    else:
        print(f"{r}{h}The path exists but it is not a directory.{e}")
    return


def call_413():
    print(f"{r}{h}The uploaded assets archive is too large.{e}")
    return


def call_500():
    print(
        f"{r}{h}the server encountered an unexpected condition that prevented "
        f"it from fulfilling the request.{e}")
    return


def call_501():
    print(f"{r}{h}The requested feature is understood, "
          f"but not supported by the server.{e}")
    return


def call_503():
    print(f"{r}{h}Service Unavailable. The server is in maintenance mode.{e}")
    return


def call_507():
    print(
        f"{r}{h}Insufficient Storage. Tthe disk is full (or cached files "
        f"reaches the configured limit), and no cached file can be deleted to obtain enough space."
        f"{e}")
    return
