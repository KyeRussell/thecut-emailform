# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut.emailform.forms import BaseEmailForm


class EmailForm(BaseEmailForm):

    foo = forms.CharField(required=False)
