# meter_readings/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meter_readings.settings')

app = Celery('meter_readings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
