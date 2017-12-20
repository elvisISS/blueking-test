# -*- coding: utf-8 -*-
"""
Task
"""

from common.mymako import render_mako_context, render_json
#from blueking.component.shortcuts import get_client_by_request
from blueking.component.shortcuts import get_client_by_user

def test1():
    user = 'public'
    client = get_client_by_user(user)
    # 组件参数
    kwargs = {'app_id': '3'}
    result = client.cc.get_app_host_list(kwargs)
    # result = client.job.get_cron(kwargs)
    return result

def query(task_id):
    username = 'public'
    task_id = '8'
    steps = {
        "ipList": "1:10.0.1.109,1:10.0.1.188,1:10.0.1.120",
        "stepId": 1,
    }
    client = get_client_by_user(username)

    result = client.job.get_task_ip_log({"task_id": task_id})

    return result

def execute(task_id):
    username = 'public'
    task_id = '8'
    app_id = '3'
    steps = [{
        "ipList": "1:10.0.1.109,1:10.0.1.188,1:10.0.1.120",
        "stepId": 1
    }]
    client = get_client_by_user(username)
    result = client.job.execute_task({"app_id": app_id, "task_id": task_id, "steps": steps})

    return result