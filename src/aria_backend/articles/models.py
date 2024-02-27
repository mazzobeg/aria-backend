"""
This module contains the ArticleGrade Enum and the Article model.
"""

from enum import Enum
from flask_restx import fields
from ..extensions import API as api
from mongoengine import Document, StringField


# pylint: disable=R0913
class State(Enum):

    READ = "READ"
    UNREAD = "UNREAD"

    @classmethod
    def from_text(cls, text: str):
        uppered_text = text.upper()
        if uppered_text in [v.value for v in cls]:
            return cls(uppered_text)
        raise ValueError("Value not allowed.")


class Article(Document):
    """
    Model for Articles
    """

    title = StringField(required=True)
    link = StringField(required=True)
    content = StringField(required=True)
    summary = StringField()
    state = StringField(default=State.UNREAD.value)
    summary_translation = StringField()

    @classmethod
    def new(cls, title, link, content):
        return Article(title=title, link=link, content=content)


article_model = api.model(
    "Article",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "link": fields.String(required=True),
        "content": fields.String(required=True),
        "summary": fields.String(required=False),
        "state": fields.String(required=False),
        "summary_translation": fields.String(required=False),
    },
)

article_input_model = api.model(
    "ArticleInput",
    {
        "title": fields.String(required=True),
        "link": fields.String(required=True),
        "content": fields.String(required=True),
    },
)
