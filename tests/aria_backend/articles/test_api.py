from aria_backend.articles.api import ArticlesAPI
from aria_backend.articles.models import Article
from tests.conftest import test_app
from aria_backend.articles.services import get_article
import pytest


@pytest.fixture(autouse=True)
def setup():
    Article.drop_collection()


def test_create_article(test_app):
    with test_app.test_client() as client:
        response = client.post(
            "/articles/articles",
            json={"title": "new_article", "link": "url", "content": "content"},
        )
        assert response.status_code == 201
    article = Article.objects.get(title="new_article")
    assert article.title == "new_article"
    assert article.link == "url"
    assert article.content == "content"


def test_get_articles(test_app):
    article = Article.new("new_article", "url", "content")
    article.save()
    with test_app.test_client() as client:
        response = client.get("/articles/articles")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["title"] == "new_article"
        assert response.json[0]["link"] == "url"
        assert response.json[0]["content"] == "content"


def test_get_article_by_id(test_app):
    article = Article.new("new_article", "url", "content")
    article.save()
    article_id = article.id
    with test_app.test_client() as client:
        response = client.get(f"/articles/articles/{article_id}")
        assert response.status_code == 200
        assert response.json["title"] == "new_article"
        assert response.json["link"] == "url"
        assert response.json["content"] == "content"
    with test_app.test_client() as client:
        response = client.get("/articles/articles/5f91ad8c1f6e5a3b3c8b4567")
        assert response.status_code == 404


def test_delete_article_by_id(test_app):
    article = Article.new("new_article", "url", "content")
    article.save()
    article_id = article.id
    with test_app.test_client() as client:
        response = client.delete(f"/articles/articles/{article_id}")
        assert response.status_code == 200
    with test_app.test_client() as client:
        response = client.delete("/articles/articles/5f91ad8c1f6e5a3b3c8b4567")
        assert response.status_code == 404


def test_update_article_by_id(test_app):
    article = Article.new("new_article", "url", "content")
    article = article.save()
    article_id = article.id
    with test_app.test_client() as client:
        response = client.put(
            f"/articles/articles/{article_id}",
            json={
                "title": "new_article2",
                "link": "url2",
                "content": "content2",
                "summary": "summary2",
                "state": "state2",
            },
        )
        assert response.status_code == 200
    article = get_article(article_id)
    assert article.title == "new_article2"
    assert article.link == "url2"
    assert article.content == "content2"
