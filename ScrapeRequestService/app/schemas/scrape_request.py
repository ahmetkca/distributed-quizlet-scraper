from typing import List
from pydantic import BaseModel, HttpUrl

class QuizletLinkRequestBase(BaseModel):
    category_link: HttpUrl
    from_page: int
    to_page: int

class QuizletLinkRequest(QuizletLinkRequestBase):
    ...

class QuizletLinkRequestCreate(QuizletLinkRequestBase):
    request_id: str
    task_id: str

class TaskBase(BaseModel):
    task_id: str
    request_link: HttpUrl

class Task(TaskBase):
    ...

class ScrapeRequestBase(BaseModel):
    request_links: List[HttpUrl]

class ScrapeRequest(ScrapeRequestBase):
    ...

class ScrapeRequestCreate(ScrapeRequestBase):
    request_id: str
    task_ids: List[Task]