#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "xuzhao"
__email__ = "contact@xuzhao.xin"
__file__ = "urls.py"
__description__ = ""
__created_time__ = "2018/9/11 18:26"


from django import VERSION

from .views import upload_image
if VERSION < (1, 9):
    from django.conf.urls import patterns, url
    urlpatterns = patterns('',
        url(r'^uploadimage/$', upload_image),
    )
else:
    from django.conf.urls import url

    app_name = 'xuzhao_markdown'
    urlpatterns = [
        url(r'^uploadimage/$', upload_image),

    ]