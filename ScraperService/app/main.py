from celery import Celery
from .config import CELERY_BROKER_URI, CELERY_BACKEND_URI

celery_app = Celery(
    'scraper-service',
    broker=CELERY_BROKER_URI,
    backend=CELERY_BACKEND_URI,
    include=['app.tasks']
)
