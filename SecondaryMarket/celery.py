from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.

# yourprojectname代表你工程的名字，在下面替换掉
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SecondaryMarket.settings')

app = Celery()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


