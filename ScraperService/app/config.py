import os

CELERY_BROKER_URI = os.environ.get("CELERY_BROKER_URI")
CELERY_BACKEND_URI = os.environ.get("CELERY_BACKEND_URI")
