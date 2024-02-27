from aria_backend.scrapers.models import Scraper
from aria_backend.scrapers.services import (
    add_scraper,
    get_scrapers,
    delete_scraper,
    update_scraper,
    get_scraper,
    execute_scraper,
)
from tests.conftest import test_app
import pytest
import io, sys


@pytest.fixture(autouse=True)
def setup():
    Scraper.drop_collection()


def test_add_scraper(test_app):
    scraper = Scraper(name="scraper_test", content="content", kwargs="{}")
    add_scraper(scraper)
    scraper = Scraper.objects.get(name="scraper_test")
    assert scraper.name == "scraper_test"
    assert scraper.content == "content"
    assert scraper.kwargs == "{}"


def test_get_scrapers(test_app):
    scraper = Scraper(name="scraper_test", content="content", kwargs="{}")
    scraper.save()
    scrapers = get_scrapers()
    assert len(scrapers) == 1
    assert scrapers[0].name == "scraper_test"
    assert scrapers[0].content == "content"
    assert scrapers[0].kwargs == "{}"


def test_delete_scraper(test_app):
    scraper = Scraper(name="scraper_test", content="content", kwargs="{}")
    scraper.save()
    delete_scraper("scraper_test")
    scrapers = get_scrapers()
    assert len(scrapers) == 0
    with pytest.raises(ValueError):
        scraper = delete_scraper("scraper_test2")


def test_update_scraper(test_app):
    scraper = Scraper(name="scraper_test", content="content", kwargs="{}")
    scraper.save()
    scraper.name = "new_name"
    update_scraper(scraper)
    scraper = get_scraper("new_name")
    assert scraper.name == "new_name"
    assert scraper.content == "content"
    assert scraper.kwargs == "{}"
    with pytest.raises(ValueError):
        scraper = get_scraper("scraper_test")
    scrapers = get_scrapers()
    assert len(scrapers) == 1
    assert scrapers[0].name == "new_name"
    assert scrapers[0].content == "content"
    assert scrapers[0].kwargs == "{}"


def test_execute_scrapper(test_app):
    """
    Test the execute_scrapper function.
    """
    script = """def main(kwargs):
    print(f'Hello World {kwargs["a"]}')
    return {"result":[], "message":""}"""
    scraper = Scraper(name="scraper_test", content=script, kwargs='{"a": 1}')

    # Capture the stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    execute_scraper(scraper)

    # Reset the stdout
    sys.stdout = sys.__stdout__

    print(captured_output.getvalue())
    # Assert that "Hello World" is printed
    assert captured_output.getvalue().strip() == "Hello World 1"
