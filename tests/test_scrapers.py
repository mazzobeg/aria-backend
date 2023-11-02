from aria.scrapers.core import trigger_scraper, create_scrapers
from aria import db
from aria.scrapers.models import Scraper
from tests.utils import get_resources

def test_trigger_scraper(test_app) :
    script_path = get_resources("scrapers/scraper_test.py")
    trigger_scraper(script_path, "{}")

# def test_register_scraper(test_app):
#     script_path = get_resources("scraper_test.py")
#     register_scraper(script_path, None)
#     scrapers = db.session.query
#     assert len(scrapers) == 1

def test_create_scrapers():
    """
    Test create scrapers using ./resources/scrapers
    """
    scrapers = create_scrapers(get_resources("scrapers"))
    assert len(scrapers) == 2
    scraper1 = scrapers[1]
    assert scraper1.name == 'scraper_test'
    assert scraper1.path ==  f'{get_resources("scrapers")}/scraper_test.py'
    assert scraper1.kwargs == '{}'
    scraper2 = scrapers[0]
    assert scraper2.name == 'scraper_with_conf'
    assert scraper2.path ==  f'{get_resources("scrapers")}/scraper_with_conf.py'
    assert scraper2.kwargs == '{"a": 0}'

    
