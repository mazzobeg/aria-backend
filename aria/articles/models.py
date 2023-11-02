"""
This module contains the ArticleGrade Enum and the Article model.
"""
import hashlib
from enum import Enum
from sqlalchemy.orm import Mapped
from aria import DB as db

# pylint: disable=R0913


class ArticleGrade(Enum):
    """
    Enum for Article Grades
    """

    MEH = "MEH"
    SMILE = "SMILE"
    FROWN = "FROWN"

    @classmethod
    def from_text(cls, text: str):
        """
        Returns the ArticleGrade corresponding to the given text.
        """
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
    grade: Mapped[ArticleGrade] = db.Column(db.Enum(ArticleGrade), nullable=True)

    def __init__(
        self, title, link: str, content, summary=None, grade: ArticleGrade = None
    ):
        self.id = hashlib.md5(link.encode("utf-8")).hexdigest()
        self.title = title
        self.link = link
        self.content = content
        self.summary = summary
        self.grade = grade
