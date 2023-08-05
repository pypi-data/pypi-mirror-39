#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = "xuzhao"
__email__ = "contact@xuzhao.xin"
__file__ = "settings.py"
__description__ = ""
__created_time__ = "2018/9/11 13:36"

MARKDOWN_WIDGET_TEMPLATE = getattr(settings, "MARKDOWN_WIDGET_TEMPLATE", "xuzhao_markdown/widgets/markdown.html")
MARKDOWN_IMAGE_FORMATS = getattr(settings, "MARKDOWN_IMAGE_FORMATS", ["jpg", "jpeg", "gif", "png", "bmp", "webp"])
MARKDOWN_UP_IMAGE_URL = getattr(settings, "MARKDOWN_UP_IMAGE_URL", "/xuzhao_markdown/uploadimage/")
MARKDOWN_IMAGE_FLODER=getattr(settings, "MARKDOWN_IMAGE_FLODER", "xuzhao_markdown")
MEDIA_URL = getattr(settings, "MEDIA_URL")
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")
STATIC_URL = getattr(settings, "STATIC_URL", "/static/")
