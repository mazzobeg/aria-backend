"""
This module contains the views for the dashboard blueprint.
"""
from flask import Blueprint, render_template
from aria.articles.models import Article

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    """
    Route to display the dashboard.
    """
    # get the number of articles in database
    articles = Article.query.all()
    article_number = len(articles)
    # get the number of unclassified articles in database
    unclassified_articles = Article.query.filter(Article.grade is None).all()
    unclassified_article_number = len(unclassified_articles)
    data = {
        "article_number": article_number,
        "unclassified_article_number": unclassified_article_number,
        "last_scraper_trigger": "N/A",
    }
    return render_template("dashboard.html", datas=data)
