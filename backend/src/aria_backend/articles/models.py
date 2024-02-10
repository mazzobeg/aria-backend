"""
This module contains the ArticleGrade Enum and the Article model.
"""

import hashlib
from enum import Enum
from sqlalchemy.orm import Mapped
from flask_restx import fields
from ..extensions import DB as db
from ..extensions import API as api


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


class Article(db.Model):
    """
    Model for Articles
    """

    # pylint: disable=R0903
    id: Mapped[str] = db.Column(db.String, primary_key=True)
    title: Mapped[str] = db.Column(db.String, nullable=False)
    link: Mapped[str] = db.Column(db.String, nullable=False)
    content: Mapped[str] = db.Column(db.String, nullable=False)
    summary: Mapped[str] = db.Column(db.String, nullable=True)
    state: Mapped[str] = db.Column(
        db.String, nullable=False, default=State.UNREAD.value
    )
    summary_translation: Mapped[str] = db.Column(db.String, nullable=True)

    def __init__(
        self,
        title,
        link: str,
        content,
        summary=None,
        state: State = None,
        summary_translation=None,
    ):
        self.id = hashlib.md5(link.encode("utf-8")).hexdigest()
        self.title = title
        self.link = link
        self.content = content
        self.summary = summary
        self.state = state
        self.summary_translation = summary_translation


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
