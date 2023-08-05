#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

from .widgets import MarkdownWidget, AdminMarkdownWidget, XAdminMarkdownWidget

__author__ = "xuzhao"
__email__ = "contact@xuzhao.xin"
__file__ = "forms.py"
__description__ = ""
__created_time__ = "2018/9/11 18:24"


class MarkdownField(forms.CharField):
    widget = MarkdownWidget


class AdminMarkdownField(forms.CharField):
    widget = AdminMarkdownWidget


class XAdminMarkdownField(forms.CharField):
    widget = XAdminMarkdownWidget


