import json
cmd = '["python", "app.py"]'
name = "test"
description = "test description"
tags = '["tag1","tag2","tag3"]'
docker = "test_docker_name"
memory = 128.0
cpu = 1.0
gpu = 1
disk = 128.0
ports = 1
task_id = "mlge2.gkerk95g3hqwnnrwsz4bl8f9"
create_time = "2018-10-10T12:22:31Z"
stop_time = "2018-10-11T12:22:31Z"
start_time = "2018-10-11T12:22:31Z"
status = "CREATING"
success_res = {
    "id": task_id,
    "name": name,
    "description": description,
    "tags": tags.split(','),
    "create_time": create_time,
    "start_time": start_time,
    "stop_time": stop_time,
    "status": status,
    "exit_code": 0,
    "user_env": '',
    "args": cmd,
    "container": {
        "type": "docker",
        "image": docker,
    },
    "resources": {
        "request": {
            "memory": memory,
            "cpu": cpu,
            "gpu": gpu,
            "disk": disk,
            "port": ports,
        },
        "assigned": {
            "memory": 128,
            "cpu": 1.0,
            "gpu": 1,
            "disk": 128,
            "port": [8000, 2333],
        }
    },
    "exc_info": {
        "hostname": "hostname",
        "pid": 2333,
        "work_dir": "/home/test/",
        "env": {},
    },
    "file_size": 1024,
}
failed_res = {
    "error": 1,
    "reason": "some short description",
    "description": "some long description",
}
success_res_format = json.dumps(success_res, indent=4) + '\n'
failed_res_format = json.dumps(failed_res, indent=4) + '\n'
ip = 'http://mlgridengine2.cluster.peidan.me'
port = 7002
url = ip + ':' + str(port)
