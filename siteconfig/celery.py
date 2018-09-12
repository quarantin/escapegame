# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from celery import Celery

import traceback

import time

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteconfig.settings')


app = Celery('siteconfig')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

