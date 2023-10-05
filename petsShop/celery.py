from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from api.tasks import send_payment_reminder_email

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petsShop.settings')

app = Celery('petsShop')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'send_payment_reminder_email': {
#         'task': send_payment_reminder_email,  
#         'schedule': crontab(hour=10, minute=0),
#     },
# }
app.autodiscover_tasks()