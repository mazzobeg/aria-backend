from .models import Article
import requests
import logging as log
from ..extensions import DB as db


def add_article(title: str, link: str, content: str):
    article = Article(title, link, content)
    try:
        db.session.add(article)
        db.session.commit()
    except Exception as e:
        log.debug(e)
        db.session.rollback()
        log.debug("Article already in database")


def summarize(article: Article):
    result = execute_summarize(article)
    db.session.query(Article).filter_by(title=article.title).update(
        {Article.summary: result}
    )
    db.session.commit()


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
    db.session.query(Article).filter_by(title=article.title).update(
        {Article.summary_translation: result}
    )
    db.session.commit()


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
