#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms.renderers import get_default_renderer
from django.utils.safestring import mark_safe

__author__ = "xuzhao"
__email__ = "contact@xuzhao.xin"
__file__ = "widgets.py"
__description__ = ""
__created_time__ = "2018/9/11 13:41"


from django import VERSION, forms
from django.contrib.admin import widgets as admin_widgets
from django.utils.html import conditional_escape
# Django 1.7 compatibility
from .utils import compatible_staticpath
from . import settings as markdown_settings
try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

# Python 3 compatibility
# https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode


class MarkdownWidget(forms.Textarea):

    template_name = 'xuzhao_markdown/widgets/markdown.html'

    def __init__(self, *args, **kwargs):
        self.markdown_conf = {
            'width': '100%',
            'height': '540',
            'syncScrolling': 'single',
            'saveHTMLToTextarea': True,
            'emoji': True,
            'taskList': True,
            'tocm': True,
            'tex': True,
            'flowChart': True,
            'sequenceDiagram': True,
            'codeFold': True,
            'imageUpload': True,
            'imageFormats': markdown_settings.MARKDOWN_IMAGE_FORMATS,
            'imageUploadURL': markdown_settings.MARKDOWN_UP_IMAGE_URL,
            'theme': 'light',
            'previewTheme': 'light',
            'editorTheme': 'paraiso-light',
        }

        self.lib = markdown_settings.STATIC_URL+'xuzhao_markdown/lib/'

        super(MarkdownWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(
            css={
                "all": (compatible_staticpath("xuzhao_markdown/css/editormd.css"),)
            },
            js=(
                compatible_staticpath("xuzhao_markdown/js/jquery.min.js"),
                compatible_staticpath("xuzhao_markdown/js/editormd.min.js"),

            ))
    media = property(_media)

    def get_context(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, {'name': name})
        if 'class' not in final_attrs:
            final_attrs['class'] = ''
        final_attrs['class'] += ' wmd-input'
        context = {
            'widget': {
                "attrs": flatatt(final_attrs),
                "body": conditional_escape(force_unicode(value)) if value else '',
                'template_name': self.template_name
            },
            'id': final_attrs['id'],
            'markdown_conf': self.markdown_conf,
            'marklib': self.lib,
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)

    def _render(self, template_name, context, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))


class AdminMarkdownWidget(MarkdownWidget, admin_widgets.AdminTextareaWidget):
    def __init__(self, *args, **kwargs):
        super(AdminMarkdownWidget, self).__init__(*args, **kwargs)


class XAdminMarkdownWidget(AdminMarkdownWidget):
    def __init__(self, *args, **kwargs):
        super(XAdminMarkdownWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(
            css={
                'all': (compatible_staticpath('xuzhao_markdown/css/editormd.css'),)
            },
            js=(
                compatible_staticpath('xuzhao_markdown/js/editormd.min.js'),
            ))
    media = property(_media)
