import abc
from typing import List
import httpx
import bs4
import lxml
from fake_useragent import UserAgent

def get_headers_with_random_useragent():
    ua = UserAgent()
    return {
        'User-Agent': ua.random
    }


def get_quizlet_links(quizlet_category_link: str, from_page: int, to_page: int):
    if quizlet_category_link[-1] != '/':
        quizlet_category_link += '/'

    quizlet_links: List[str] = []
    for page_num in range(from_page, to_page + 1):
        resp = httpx.get(url=quizlet_category_link + f"page/{page_num}/", headers=get_headers_with_random_useragent())
        tree = lxml.etree.HTML(resp.text)
        quizlet_link_index = 1
        quiz_link_xpath = "/html/body/div[2]/main/div/section[2]/div/div/div/div[2]/div[{quiz_link_index}]/div/div/div[1]/div/div[1]/div[1]/a[@title]/@href"
        while len(tree.xpath(quiz_link_xpath.format(quiz_link_index=quizlet_link_index))) != 0:
            quiz_link = tree.xpath(quiz_link_xpath.format(quiz_link_index=quizlet_link_index))
            quizlet_links.append(quiz_link[0])
            quizlet_link_index += 1
    return quizlet_links




def get_flashcards(quizlet_link: str) -> list:
    quiz_resp = httpx.get(url=quizlet_link, headers=get_headers_with_random_useragent())

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(quiz_resp.text, 'lxml')

    flashcards: List[dict] = []

    qitem: bs4.element.Tag
    for qitem in soup.select('div.SetPageTerms-term'):
        question = qitem.select_one('a.SetPageTerm-wordText')
        answer = qitem.select_one('a.SetPageTerm-definitionText')
        flashcards.append({
            'question': question.text,
            'answer': answer.text
        })
    return flashcards
