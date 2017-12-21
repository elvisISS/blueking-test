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

from django.contrib import admin
from home_application.models import Book, Publisher, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'update_at', 'publisher', 'authors_list']
    list_filter = ['name']
    search_fields = ['name']

    def publisher(self, obj):
        return obj.publisher

    def authors_list(self, obj):
        return obj.authors.values_list('name', flat=True)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    list_filter = ['name']
    search_fields = ['name']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
