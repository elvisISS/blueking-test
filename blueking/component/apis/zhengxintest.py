# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsTest(object):
    """Collections of Test APIS"""
    def __init__(self, client):
        self.client = client

        # create_task为组件名，method为请求组件使用的方法，path为组件路径，组件域名为系统默认域名
        self.zhengxin_test = ComponentAPI(
            client=self.client, method='GET', path='/api/c/self-service-api/zhengxin_test/zhengxin_test/',
            description=u'',
        )