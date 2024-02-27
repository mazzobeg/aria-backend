from aria_backend.scrapers.models import Scraper
import pytest


def test_model():
    scraper = Scraper(name="name", content="content", kwargs="{}")
    assert scraper.name == "name"
    assert scraper.content == "content"
    assert scraper.kwargs == "{}"
