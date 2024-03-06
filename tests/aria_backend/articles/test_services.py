from aria_backend.articles.services import (
    add_article,
    get_articles,
    delete_article,
    update_article,
    get_article,
    execute_summarize,
)
from tests.conftest import test_app
import pytest
from aria_backend.articles.models import Article
from tests.utils import get_resources
from bson import ObjectId


@pytest.fixture(autouse=True)
def setup():
    Article.drop_collection()


def test_add_article(test_app):
    article = Article.new("new_article", "url", "content")
    add_article(article)
    article = Article.objects.get(title="new_article")
    assert article.title == "new_article"
    assert article.link == "url"
    assert article.content == "content"


def test_get_articles(test_app):
    article = Article.new("new_article", "url", "content")
    article.save()
    articles = get_articles()
    assert len(articles) == 1
    assert articles[0].title == "new_article"
    assert articles[0].link == "url"
    assert articles[0].content == "content"


def test_get_article(test_app):
    article = Article.new("new_article", "url", "content")
    article = article.save()
    article = get_article(article.id)
    assert article.title == "new_article"
    assert article.link == "url"
    assert article.content == "content"
    with pytest.raises(ValueError):
        article = get_article(ObjectId())


def test_delete_article(test_app):
    article = Article.new("new_article", "url", "content")
    article = article.save()
    delete_article(article.id)
    articles = get_articles()
    assert len(articles) == 0
    with pytest.raises(ValueError):
        article = delete_article(ObjectId())


def test_update_article(test_app):
    article = Article.new("new_article", "url", "content")
    article = article.save()
    article.title = "new_name"
    update_article(article)
    article = get_article(article.id)
    assert article.title == "new_name"
    assert article.link == "url"
    assert article.content == "content"
    with pytest.raises(ValueError):
        article = get_article(ObjectId())
    articles = get_articles()
    assert len(articles) == 1
    assert articles[0].title == "new_name"
    assert articles[0].link == "url"
    assert articles[0].content == "content"


def test_execute_summarize(test_app):

    # create a mock for post request
    class MockResponse:
        def __init__(self, status_code, json):
            self.status_code = status_code
            self.response = json

        def json(self):
            return self.response

    def mock_post(url, json):
        return MockResponse(200, {"response": "summary"})

    # patch the requests.post method
    import requests

    requests.post = mock_post

    file_path = get_resources("long_article.txt")
    with open(file_path, "r") as f:
        content = f.read()
        articles = Article.new("", "", content)
        with test_app.app_context():
            response = execute_summarize(articles)
            assert response == "summary"
