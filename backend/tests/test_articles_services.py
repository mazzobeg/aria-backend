from src.articles.models import Article
from src.articles.services import summarize
from tests.utils import get_resources


def test_summarize():
    file_path = get_resources("long_article.txt")
    with open(file_path, "r") as f:
        content = f.read()
        articles = Article("", "", content)
        response = summarize(articles)
        assert response != ""
