"""
This module contains the views for the articles blueprint.
"""
import re
from flask import Blueprint, render_template, redirect, request, url_for
from aria.articles.models import Article, ArticleGrade
from aria.articles.services import get_articles_without_summary
from aria.celery.core import summarize_articles_task
from aria import DB as db
from aria.celery.core import running_tasks

articles_blueprint = Blueprint("articles", __name__)


@articles_blueprint.route("/articles", methods=["GET"])
def articles():
    """
    Route to display all articles.
    """
    all_articles = Article.query.all()
    regex = re.compile(r"\.(.*)\.")
    articles_data = [
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "link": article.link,
            "summary": "" if article.summary is None else article.summary,
            "grade": "" if article.grade is None else article.grade.value,
            "domain": regex.search(article.link).group(1)
            if regex.search(article.link) is not None
            else "",
        }
        for article in all_articles
    ]
    return render_template("articles.html", articles=articles_data)


@articles_blueprint.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    """
    Route to display a single article.
    """
    article = Article.query.get(article_id)
    return render_template("article.html", article=article)


@articles_blueprint.route("/articles/bootstrap", methods=["GET"])
def bootstrap_article():
    """
    Route to bootstrap articles.
    """
    article1 = Article("TITLE1", "CONTENT1", "LINK1", "SUMMARY1", ArticleGrade.FROWN)
    article2 = Article("TITLE2", "CONTENT2", "LINK2", "SUMMARY2", ArticleGrade.FROWN)
    article3 = Article("TITLE3", "CONTENT3", "LINK3", "SUMMARY3", ArticleGrade.FROWN)
    db.session.add_all([article1, article2, article3])
    db.session.commit()
    return redirect("/articles")


@articles_blueprint.route("/articles/deleteAll", methods=["GET"])
def delete_all_articles():
    """
    Route to delete all articles.
    """
    Article.query.delete()
    db.session.commit()
    return redirect("/articles")


@articles_blueprint.route("/articles/<string:article_id>", methods=["GET"])
def get_article_by_id(article_id):
    """
    Route to get an article by its ID.
    """
    article = Article.query.get(article_id)
    return render_template("article.html", article=article)


summarizers = []


@articles_blueprint.route("/articles/summarize/start", methods=["GET"])
def start_summarize():
    """
    Route to start summarizing articles.
    """
    articles_without_summary = get_articles_without_summary()
    callback_endpoint = url_for("articles.article_add_summary", _external=True)
    uiid = summarize_articles_task.delay(
        [article.id for article in articles_without_summary],
        [article.content for article in articles_without_summary],
        callback_endpoint,
    )
    summarizers.append(uiid)
    return redirect("/articles")


@articles_blueprint.route("/articles/add/summary", methods=["POST"])
def article_add_summary():
    """
    Route to add a summary to an article.
    """
    data = request.get_json()
    article = Article.query.get(data["id"])
    article.summary = data["summary"]
    db.session.add(article)
    db.session.commit()
    return redirect("/articles")


@articles_blueprint.route(
    "/articles/<string:article_id>/grade/<string:grade>", methods=["GET"]
)
def update_article_grade(article_id, grade):
    """
    Route to update the grade of an article.
    """
    article = Article.query.get(article_id)
    article.grade = ArticleGrade.from_text(grade)
    db.session.add(article)
    db.session.commit()
    return redirect("/articles")


@articles_blueprint.route("/articles/summarize/status", methods=["GET"])
def summarize_status():
    """
    Route to check the status of the summarization task.
    """
    for running_task in running_tasks.values():
        if "summarize_articles" == running_task["name"]:
            return {"running": True}, 200
    return {"running": False}, 200
