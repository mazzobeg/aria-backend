"""
This module contains the ArticleAPI class.
"""

import logging as log
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError
from .models import article_input_model, article_model, Article
from ..extensions import DB as db
from .services import summarize, translate

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
        try:
            db.session.add(article)
            db.session.commit()
            return article, 201
        except IntegrityError:
            log.debug("Article already in database")
            return article, 500

    @NS.marshal_with(article_model)
    def get(self):
        """
        Get method for getting an article.
        """
        articles = db.session.query(Article).all()
        return articles, 201


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
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {"message": "Article not found"}, 404
        return article, 200

    @NS.marshal_with(article_model)
    def delete(self, article_id):
        """
        Delete method for deleting an article.
        """
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {"message": "Article not found"}, 404
        db.session.delete(article)
        db.session.commit()
        return {"message": "Article deleted"}, 200

    @NS.expect(article_input_model)
    @NS.marshal_with(article_model)
    def put(self, article_id):
        """
        Put method for updating an article.
        """
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {"message": "Article not found"}, 404
        article.title = NS.payload["title"]
        article.link = NS.payload["link"]
        article.content = NS.payload["content"]
        article.summary = NS.payload["summary"]
        article.state = NS.payload["state"]
        db.session.commit()
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
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {"message": "Article not found"}, 404
        summarize(article)
        return article, 200


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
        article = db.session.query(Article).filter_by(id=article_id).first()
        if article is None:
            return {"message": "Article not found"}, 404
        translate(article)
        return article, 200
