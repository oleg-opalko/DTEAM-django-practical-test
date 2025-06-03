import os
from celery import Celery
from celery.signals import after_setup_logger
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings')

app = Celery('CVProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Get Redis URL from environment variable or use local Redis as fallback
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

app.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    broker_connection_retry_on_startup=True,
    broker_use_ssl=os.getenv('REDIS_SSL', 'False').lower() == 'true',
    task_routes={
        'main.tasks.send_cv_pdf_email': {'queue': 'email'},
    },
    task_default_queue='default',
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
        'email': {
            'exchange': 'email',
            'routing_key': 'email',
        },
    }
)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler) 