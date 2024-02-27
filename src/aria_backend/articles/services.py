from .models import Article
import requests
import logging as log
from bson import ObjectId


def add_article(article: Article) -> Article:
    return article.save()


def get_articles() -> list[Article]:
    articles = Article.objects.all()
    return list(articles)


def get_article(id: str) -> Article:
    """
    Raises:
        ValueError: If the article does not exist
    """
    article = Article.objects.with_id(id)
    if not article or len(article) == 0:
        raise ValueError(f"Article {id} does not exist")
    else:
        return article


def delete_article(id):
    """
    Raises:
        ValueError: If the article does not exist
    """
    article = Article.objects(id=id).first()
    if article is None:
        raise ValueError(f"Article {id} does not exist")
    article.delete()


def update_article(article: Article):
    article.save()


def summarize(article: Article):
    result = execute_summarize(article)
    article = get_article(article.title)
    article.summary = result
    update_article(article)


def execute_summarize(article: Article):
    content = article.content
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama2",
        "prompt": f"""Write a summary of the following text delimited by triple backticks.
Return your response which covers the key points of the text.
```{content}```
SUMMARY:
        """,
        "stream": False,
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # Request was successful
            return response.json()["response"]
        else:
            # Request failed
            return ""
    except requests.exceptions.ConnectionError:
        log.warning("Connection error, ensure ollama serve is running.")
        return ""


def translate(article: Article):
    result = execute_translation(article)
    # db.session.query(Article).filter_by(title=article.title).update(
    #     {Article.summary_translation: result}
    # )
    # db.session.commit()
    article = MONGO.db.articles.find_one({"title": article.title})
    article.summary_translation = result
    MONGO.db.articles.update_one(
        {"title": article.title}, {"$set": {"summary_translation": result}}
    )


def execute_translation(article: Article):
    if article.summary is None:
        log.warning("Article has no summary")
        return ""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "frenchy",
        "prompt": f"${article.summary}",
        "stream": False,
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return ""
    except requests.exceptions.ConnectionError:
        log.warning("Connection error, ensure ollama serve is running.")
        return ""
