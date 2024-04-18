# Located in <your_project>/<your_project>/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Marketplace.settings')

app = Celery('Marketplace')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send-email-to-cart-owners-daily': {
        'task': 'app.tasks.send_email_to_cart_owners',
        'schedule': crontab(hour=11, minute=11),  # Runs daily at 9 AM
    },
}