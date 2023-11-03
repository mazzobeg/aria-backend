"""
This module contains the tests for the articles services.
"""
import json
from tests.utils import get_resources
from aria.articles.services import summarize_text, SummarizerMode, get_articles_without_summary
from aria import DB as db
from aria.articles.models import Article

def test_summarize_text():
    """
    Test the summarize_text function.
    """
    with open(get_resources("long_article.txt"), "r", encoding="utf-8") as file:
        summary = summarize_text(file.read(), SummarizerMode.FAST)
    assert summary is not None


def test_post_article(test_app):
    """
    Test the post method of the ArticleAPI class.
    """
    # create a post request for articles
    client = test_app.test_client()
    content = {"title": "test", "link": "test", "content": "test"}
    response = client.post(
        "/api/articles", data=json.dumps(content), content_type="application/json"
    )

    # assert that the response is correct
    assert response.status_code == 201
    assert response.json["title"] == "test"
    assert response.json["link"] == "test"
    assert response.json["content"] == "test"

    # assert that data are present in the database
    with test_app.app_context():
        assert len(db.session.query(Article).all()) == 1


def test_get_articles_without_summary(test_app):
    """
    Test the get_articles_without_summary function.
    """
    test_app.app_context().push()
    with test_app.app_context():
        db.session.add(Article("TITLE1", "LINK1", "CONTENT1"))
        db.session.commit()

    articles = get_articles_without_summary()
    assert articles is not None
    assert len(articles) == 1
