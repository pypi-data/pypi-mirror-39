from celery import Celery
from django.conf import settings


class ServiceConfig(object):
    name = 'boris'
    broker_url = settings.MESSAGE_BROKER.get('URL')


app = Celery()
app.config_from_object(ServiceConfig)
app.autodiscover_tasks()
