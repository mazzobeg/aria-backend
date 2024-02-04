from tests.utils import get_resources
from src.scrapers.services import get_scraper, execute_scraper
from src.scrapers.models import Scraper
from src.extensions import DB
from tests.conftest import test_app
import io
import sys


def test_get_scraper(test_app):
    """
    Test the get_scraper function.
    """
    test_app.app_context().push()
    scraper = Scraper("scraper_test", "content", {})
    DB.session.add(scraper)
    DB.session.commit()
    # assert that db contains the scraper
    scrapers = DB.session.query(Scraper).all()
    assert len(scrapers) == 1
    # assert that scraper is correctly retrieved
    scraper_retrieved = get_scraper("scraper_test")
    assert scraper_retrieved is not None
    assert scraper_retrieved.name == "scraper_test"
    assert scraper_retrieved.content == "content"
    assert scraper_retrieved.kwargs == "{}"


def test_execute_scrapper():
    """
    Test the execute_scrapper function.
    """
    script = """def main(kwargs):
    print(f'Hello World {kwargs["a"]}')
    return {"result":[], "message":""}"""
    scraper = Scraper("scraper_test", script, {"a": 1})

    # Capture the stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    execute_scraper(scraper)

    # Reset the stdout
    sys.stdout = sys.__stdout__

    print(captured_output.getvalue())
    # Assert that "Hello World" is printed
    assert captured_output.getvalue().strip() == "Hello World 1"
