from typing import List
from uuid import uuid4
from fastapi import FastAPI, Depends
from celery import Celery
from celery.result import AsyncResult

from .config import Settings
from .dependencies import get_settings

from .schemas.scrape_request import QuizletLinkRequest, QuizletLinkRequestCreate, ScrapeRequest, ScrapeRequestCreate, Task


celery_app = Celery(
    'scrape_request_service',
    broker=get_settings().celery_broker_uri,
    backend=get_settings().celery_backend_uri
)

fastapi_app = FastAPI()


@fastapi_app.get("/")
async def read_root():
    return {
        "Hello": "World!"
    }

@fastapi_app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
        "celery_broker_uri": settings.celery_broker_uri,
        "celery_backend_uri": settings.celery_backend_uri
    }


@fastapi_app.post("/send-scrape-flashcards")
async def send_scrape_flashcards(scrape_request: ScrapeRequest):
    scrape_request_create = ScrapeRequestCreate(
        request_links=scrape_request.request_links,
        request_id=str(uuid4()),
        task_ids=[]
    )
    for scrape_req_link in scrape_request.request_links:
        scrape_task: AsyncResult = celery_app.send_task('scrape_flashcards', kwargs={'quizlet_link': scrape_req_link})
        s_task_create = Task(task_id=scrape_task.task_id, request_link=scrape_req_link)
        scrape_request_create.task_ids.append(s_task_create)
    return scrape_request_create

@fastapi_app.post("/send-scrape-quizlet-links")
async def send_scrape_quizlet_links(quizlet_link_request: QuizletLinkRequest):
    scrape_task = celery_app.send_task(
        'scrape_quizlet_links', 
        kwargs={
            'quizlet_category_link': quizlet_link_request.category_link, 
            'from_page': quizlet_link_request.from_page, 
            'to_page': quizlet_link_request.to_page
        }
    )
    quizlet_link_request_create = QuizletLinkRequestCreate(
        request_id=str(uuid4()),
        task_id=scrape_task.task_id
    )
    return quizlet_link_request_create

