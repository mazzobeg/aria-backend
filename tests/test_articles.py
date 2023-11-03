"""
This module contains the tests for the articles services.
"""
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
