"""
This module contains the ArticleAPI class.
"""
import logging as log
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError
from aria.articles.models import article_input_model, article_model, Article
from aria import DB as db

NS = Namespace("api")

@NS.route("/articles")
class ArticleAPI(Resource):
    """
    API Resource for articles.
    """
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
