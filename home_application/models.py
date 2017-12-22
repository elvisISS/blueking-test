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

from django.db import models



class User(models.Model):
    """用户"""
    username = models.CharField(u"用户名", max_length=30)
    qq = models.CharField(u"QQ", max_length=30)
    phone = models.CharField(u"QQ", max_length=30)

    def __unicode__(self):
        return self.name

class Taskhistory(models.Model):
    """任务结果"""

    name = models.CharField(u"业务名称", max_length=64)
    username = models.CharField(u"用户名",default="", max_length=64)
    instance_id = models.CharField(u"任务ID", max_length=30)
    result = models.CharField(u"结果", max_length=255)
    start_time = models.DateTimeField(u"开始时间")
    end_time = models.DateTimeField(u"完成时间")
    ip = models.CharField(u"IP", max_length=30)
    type = models.CharField(u"任务类型", max_length=30)

    def __unicode__(self):
        return self.name



class Publisher(models.Model):
    """出版社"""

    name = models.CharField(u"名称", max_length=30)
    address = models.CharField(u"地址", max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"出版社"
        verbose_name_plural = u"出版社"
        app_label = "home_application"


class Author(models.Model):
    """作家"""

    name = models.CharField(u"姓名", max_length=30)
    email = models.EmailField(u"邮箱")
    # sex = models.SmallIntegerField(u"性别", choices=[(0, u"男人"), (1, u"女人")], default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"作家"
        verbose_name_plural = u"作家"
        app_label = "home_application"


class Book(models.Model):
    """书籍"""

    name = models.CharField(u"名称", max_length=100)
    authors = models.ManyToManyField(Author, help_text=u"作者信息")
    publisher = models.ForeignKey(Publisher, help_text=u"出版商")
    publication_date = models.DateField(u"出版日期")
    price = models.IntegerField(u"价格")
    update_at = models.DateTimeField(u"更新时间", auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"书籍"
        verbose_name_plural = u"书籍"
        app_label = "home_application"
        ordering = ['-publication_date']
        db_table = 'book'


def create_test_data(print_only=False):
    """生成测试数据"""

    import datetime
    import random

    if not print_only:

        publishers = ['shenzhen', 'beijing', 'shanghai', 'test']
        authors = ['zhangsan', 'lisi', 'wangwu', 'test']
        books = ["java", "javascript", "python", "django", "c", "c++"]

        # reset
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

        # bulk_create
        Author.objects.bulk_create([Author(name=name, email=name) for name in authors])
        Publisher.objects.bulk_create([Publisher(name=name, address=name) for name in publishers])

        authors = Author.objects.all()
        publishers = Publisher.objects.all()

        # batch_create
        for book in books:
            author = random.choice(authors)
            publisher = random.choice(publishers)
            book = Book.objects.create(
                name=book,
                publisher=publisher,
                publication_date=datetime.datetime.today(),
                price=random.randint(1, 250)
            )
            book.authors.add(author)

    # print what we create
    spliter = '=' * 40
    print '%s%s%s\n' % (spliter, 'Author', spliter)
    for item in Author.objects.values_list():
        print item

    print '%s%s%s\n' % (spliter, 'Publisher', spliter)
    for item in Publisher.objects.values_list():
        print item

    print '%s%s%s\n' % (spliter, 'Book', spliter)
    for item in Book.objects.select_related().values_list():
        print item

