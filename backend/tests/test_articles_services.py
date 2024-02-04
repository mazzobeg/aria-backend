from src.articles.models import Article
from src.articles.services import execute_summarize
from tests.utils import get_resources
from tests.conftest import test_app


def test_execute_summarize():

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
        articles = Article("", "", content)
        response = execute_summarize(articles)
        assert response == "summary"
