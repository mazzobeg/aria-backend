from ..extensions import DB
from .models import Scraper
from ..articles.services import add_article
import json
import logging as log


def get_scraper(name) -> Scraper:
    scraper = DB.session.query(Scraper).filter_by(name=name).first()
    if scraper is None:
        raise ValueError("Scraper not found")
    return scraper


class Module:
    def main(self, kwargs) -> str:
        return ""


def execute_scraper(scraper: Scraper):
    content = scraper.content
    kwargs = scraper.kwargs
    if not "def main(" in content:
        raise ValueError("Scraper does not contain a main function")
    module = Module()
    exec(content, module.__dict__)
    result = module.main(json.loads(kwargs))
    if len(result["result"]) == 0:
        log.warning("No articles found")
        return
    for article in result["result"]:
        add_article(article["title"], article["link"], article["content"])
    return result
