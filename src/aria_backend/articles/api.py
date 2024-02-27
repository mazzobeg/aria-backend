"""
This module contains the ArticleAPI class.
"""

import logging as log
from flask_restx import Resource, Namespace, marshal
from sqlalchemy.exc import IntegrityError
from .models import article_input_model, article_model, Article

from .services import (
    summarize,
    translate,
    get_articles,
    add_article,
    get_article,
    delete_article,
    update_article,
)

NS = Namespace("articles")


@NS.route("/articles")
class ArticlesAPI(Resource):
    """
    API Resource for articles.
    """

    # pylint: disable=R0903
    @NS.expect(article_input_model)
    @NS.marshal_with(article_model)
    def post(self):
        """
        Post method for creating an article.
        """
        article = Article(
            title=NS.payload["title"],
            link=NS.payload["link"],
            content=NS.payload["content"],
        )
        add_article(article)
        return article, 201

    @NS.marshal_with(article_model)
    def get(self):
        """
        Get method for getting an article.
        """
        articles = get_articles()
        return articles, 200


@NS.route("/articles/<string:article_id>")
class ArticleAPI(Resource):
    """
    API Resource for articles.
    """

    @NS.marshal_with(article_model)
    def get(self, article_id):
        """
        Get method for getting an article.
        """
        try:
            article = get_article(article_id)
            return article, 200
        except ValueError:
            return {"message": "Article not found"}, 404

    @NS.marshal_with(article_model)
    def delete(self, article_id):
        """
        Delete method for deleting an article.
        """
        try:
            delete_article(article_id)
            return {"message": "Article deleted"}, 200
        except ValueError:
            return {"message": "Article not found"}, 404

    @NS.expect(article_input_model)
    @NS.marshal_with(article_model)
    def put(self, article_id):
        """
        Put method for updating an article.
        """
        # article = db.session.query(Article).filter_by(id=article_id).first()
        article = get_article(article_id)
        if article is None:
            return {"message": "Article not found"}, 404
        article.title = NS.payload["title"]
        article.link = NS.payload["link"]
        article.content = NS.payload["content"]
        article.summary = NS.payload["summary"]
        article.state = NS.payload["state"]
        update_article(article)
        return article, 200


@NS.route("/articles/<string:article_id>/summarize")
class ArticleSummarizeAPI(Resource):
    """
    API Resource for articles.
    """

    @NS.marshal_with(article_model)
    def get(self, article_id):
        """
        Post method for summarizing an article.
        """
        try:
            article = get_article(article_id)
            summarize(article)
            return article, 200
        except ValueError:
            return {"message": "Article not found"}, 404


@NS.route("/articles/<string:article_id>/translate")
class ArticleTranslateAPI(Resource):
    """
    API Resource for articles.
    """

    @NS.marshal_with(article_model)
    def get(self, article_id):
        """
        Post method for translating an article.
        """
        try:
            article = get_article(article_id)
            translate(article)
            return article, 200
        except ValueError:
            return {"message": "Article not found"}, 404
