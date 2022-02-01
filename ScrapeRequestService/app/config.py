from functools import lru_cache
import logging
import os

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    celery_broker_uri: str = os.getenv("CELERY_BROKER_URI")
    celery_backend_uri: str = os.getenv("CELERY_BACKEND_URI")

