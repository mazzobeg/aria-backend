from aria_backend.articles.models import Article


def test_model():
    article = Article(title="title", link="link", content="content")
    assert article.title == "title"
    assert article.link == "link"
    assert article.content == "content"
