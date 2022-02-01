from unicodedata import name
from .main import celery_app
from .quizlet_scraper import get_flashcards, get_quizlet_links

@celery_app.task(name="test_task")
def test_task(x: int, y: int, z: float):
    import time
    import random
    time.sleep(random.randint(30, 60))
    return x * y + z


@celery_app.task(name="scrape_flashcards")
def scrape_flashcards(quizlet_link: str):
    result = get_flashcards(quizlet_link=quizlet_link)
    print(result)


@celery_app.task(name="scrape_quizlet_links")
def scrape_quizlet_links(quizlet_category_link: str, from_page: int, to_page: int):
    result = get_quizlet_links(quizlet_category_link=quizlet_category_link, from_page=from_page, to_page=to_page)
    print(result)
