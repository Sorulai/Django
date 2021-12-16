import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geekshop.settings')

app = Celery('geekshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'get_value_every_2_minute': {
#         'task': 'mainapp.tasks.get_currency_beat_celery',
#         'schedule': crontab(minute='*/1')
#     },
# }
