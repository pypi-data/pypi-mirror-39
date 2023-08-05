from django.test import TestCase

# Create your tests here.
from django import forms
from django.test import TestCase
from xuzhao_markdown.widgets import AdminMarkdownWidget, MarkdownWidget


class AdminMarkdownFieldTest(TestCase):

    class ArticleForm(forms.ModelForm):
        body = forms.CharField(widget=AdminMarkdownWidget())


class MarkdownFieldTest(TestCase):
    class ArticleForm(forms.ModelForm):
        body = forms.CharField(widget=MarkdownWidget())