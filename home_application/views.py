# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from blueking.component.shortcuts import get_client_by_user
from django.views.decorators.csrf import csrf_exempt

import json

def home(request):
    """
    首页
    """
    ctr = {
        "name" : "haha",
        "list" : ['1', '2', '3']
     }


    return render_mako_context(request, '/home_application/home.html', ctr)


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')

def test(request):
    app_id = request.GET.get('app_id', '0')
    client = get_client_by_request(request)
    result = client.cc.get_app_host_list({'app_id': app_id})
    # result = client.cc.get_hosts_by_property({'app_id': app_id, 'type': 1})
    return render_json(result)

def test1():
    user = 'public'
    client = get_client_by_user(user)
    # 组件参数
    kwargs = {'app_id': '3'}
    result = client.cc.get_app_host_list(kwargs)
    # result = client.zhengxin_test.zhengxin_test()
    return render_json(result)

def getserverlist(request):
    app_id = request.GET.get('app_id', '0')
    client = get_client_by_request(request)

    result = client.cc.get_app_host_list({'app_id': app_id})
    serverlist = result['data']
    return render_json(serverlist[1])
# def getserverlist(request):
#
#     client = get_client_by_user('admin')
#
#     result = client.cc.get_app_host_list({'app_id': app_id})
#     return result

def getserverlist1(request):
    app_id = request.GET.get('app_id', '3')
    client = get_client_by_request(request)

    result = client.cc.get_app_host_list({'app_id': app_id})
    serverlist = result['data']
    return result

def showserverlist(request):
    """
    show server list
    """
    serverlist = getserverlist1(request).get('data')
    return render_mako_context(request, '/home_application/serverlist.html', {"serverlist": serverlist})
    # return render_mako_context(request, '/home_application/serverlist.html', getserverlist(request))

def getalltasks():
    # app_id = request.GET.get('app_id', '3')
    # client = get_client_by_request(request)
    app_id = 3
    client = get_client_by_user('admin')
    # result = client.job.get_tasks({'app_id': app_id})
    result = client.job.get_task({'app_id': app_id})

    return result

def gettaskstepid(request):
    task_id = request.GET.get('task_id', '2')
    app_id = request.GET.get('app_id', '3')
    client = get_client_by_request(request)
    result = client.job.get_task_detail({"app_id": app_id, "task_id": task_id})
    data = result.get('data')

    steps = []
    for step in data['nmStepBeanList']:
        steps.append(step['stepId'])
        steps
    return render_json(steps)

@csrf_exempt
def executetask(request):
    task_id = request.GET.get('task_id', '2')
    app_id = request.GET.get('app_id', '3')
    target_ip = request.GET.get('targetIP', '1:10.0.1.109')
    steps = [{
        "ipList": target_ip,
        "stepId": 2
    }]
    client = get_client_by_request(request)
    result = client.job.execute_task({"app_id": app_id, "task_id": task_id, "steps": steps})
    return render_json(result)

