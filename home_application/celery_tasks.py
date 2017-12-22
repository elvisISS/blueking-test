# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from blueking.component.shortcuts import get_client_by_user
from common.mymako import render_json
from views import get_instance_detail

from common.log import logger


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))

@task
def hello_world():
    print 'hello world'


def get_tasks_detail(instance_id):
    # app_id = request.GET.get('app_id', '3')
    app_id = 3
    # client = get_client_by_request(request)

    client = get_client_by_user('admin')
    result = client.job.get_task_result({'app_id': app_id, 'task_instance_id': instance_id})


    return result

@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def checkcpu():
    task_id = '2'
    app_id = '3'
    target_ip = '1:10.0.1.109'


    steps = [{
        "ipList": target_ip,
        "stepId": 2
    }]
    client = get_client_by_user('admin')
    result = client.job.execute_task({"app_id": app_id, "task_id": task_id, "steps": steps})

    result_new = get_tasks_detail(result['data']['taskInstanceId'])
    # print type(result_new['data'][0]['stepAnalyseResult'][0]['ipLogContent'][0]['endTime'])
    # try:
    #     content = result_new['data'][0]['stepAnalyseResult'][0]['ipLogContent'][0]
    #     end_time = datetime.now()
    #     start_time = datetime.now()
    #     ip = content['ip']
    #     # log_content = result_new['data'][0]['resultTypeText']
    #     name = result_new['data'][0]['stepInstanceName']
    #     # instance_id = result_new['data'][0]['stepInstanceId']
    #     # types = result_new['data'][0]['stepAnalyseResult'][0]['resultType'][0]
    #
    #     try:
    #         Taskhistory.objects.create(end_time=end_time, start_time=start_time, ip=ip,
    #                                    name=name, username=get_current_username(request))
    #     except Exception as ex:
    #         print str(ex)
    #         print get_client_by_user(request)
    #     data = {'result': True}
    #     return JsonResponse(data)
    # except Exception as ex:
    #     print str(ex)
    #     print '1'
    #     print result_new['data'][0]['stepAnalyseResult']
    #     print type(content['endTime'])
    #     print content['endTime']
    return render_json(result_new)