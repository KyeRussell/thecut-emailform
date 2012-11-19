# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


DEFAULT_FROM_EMAIL = getattr(settings, 'EMAILFORM_DEFAULT_FROM_EMAIL',
    settings.DEFAULT_FROM_EMAIL)

DEFAULT_TO_EMAIL = getattr(settings, 'EMAILFORM_DEFAULT_TO_EMAIL',
    getattr(settings, 'DEFAULT_TO_EMAIL',  None))

DEFAULT_TO_EMAILS = getattr(settings, 'EMAILFORM_DEFAULT_TO_EMAILS',
    [DEFAULT_TO_EMAIL] if DEFAULT_TO_EMAIL else [a[1] for a in settings.ADMINS])

EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAILFORM_EMAIL_SUBJECT_PREFIX',
    settings.EMAIL_SUBJECT_PREFIX)

