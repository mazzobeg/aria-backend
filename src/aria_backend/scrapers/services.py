from .models import Scraper

from ..articles.services import add_article
import json
import logging as log
from ..articles.models import Article


def get_scrapers() -> list[Scraper]:
    """
    Returns:
        list[Scraper]: List of all scrapers
    """
    scrapers = Scraper.objects.all()
    return list(scrapers)


def get_scraper(name) -> Scraper:
    """
    Raises:
        ValueError: If the scraper does not exist
    """
    scraper = Scraper.objects().filter(name=name).first()
    if scraper is None:
        raise ValueError(f"Scraper {name} does not exist")
    return scraper


def add_scraper(scraper: Scraper):
    scraper.save()


def delete_scraper(name):
    """
    Raises:
        ValueError: If the scraper does not exist
    """
    scraper = Scraper.objects(name=name).first()
    if scraper is None:
        raise ValueError(f"Scraper {name} does not exist")
    scraper.delete()


def update_scraper(scraper: Scraper):
    scraper.save()


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
        article_as_object = Article.new(
            article["title"], article["link"], article["content"]
        )
        add_article(article_as_object)
    return result
