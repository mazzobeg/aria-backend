"""
This module contains the tests for the articles services.
"""
from tests.utils import get_resources
from aria.articles.services import summarize_text, SummarizerMode


def test_summarize_text():
    """
    Test the summarize_text function.
    """
    with open(get_resources("long_article.txt"), "r", encoding="utf-8") as file:
        summary = summarize_text(file.read(), SummarizerMode.FAST)
    assert summary is not None
