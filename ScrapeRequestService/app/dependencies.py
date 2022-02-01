

from functools import lru_cache
import logging

from pydantic import BaseSettings

from .config import Settings


log = logging.getLogger("uvicorn")

@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()