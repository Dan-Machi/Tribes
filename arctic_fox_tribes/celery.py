from __future__ import absolute_import, unicode_literals
import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arctic_fox_tribes.settings')


app = Celery('arctic_fox_tribes')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
'gold_tick':{
        'task': 'kingdom.tasks.resource_tick',
        'schedule': 60,
        'args': 'G'
    },
    'food_tick':{
        'task': 'kingdom.tasks.resource_tick',
        'schedule':60,
        'args': 'F'
    },
    'food_consumption':{
        'task': 'troop.tasks.consume_food',
        'schedule': 120,
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {O!r}'.format(self.request))
