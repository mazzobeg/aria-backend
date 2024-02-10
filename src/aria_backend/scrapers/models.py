"""
This module contains the Scraper model.
"""

import json
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String
from ..extensions import DB as db
from ..extensions import API as api
from flask_restx import fields


class Scraper(db.Model):
    """
    Scraper model class.
    """

    # pylint: disable=R0903
    name: Mapped[str] = Column(String, primary_key=True)
    content: Mapped[str] = Column(String, nullable=False)
    kwargs: Mapped[str] = Column(String)

    def __init__(self, name, content, kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.name = name
        self.content = content
        self.kwargs = json.dumps(kwargs)


scraper_model = api.model(
    "Scraper",
    {
        "name": fields.String(required=True),
        "content": fields.String(required=True),
        "kwargs": fields.String(required=False),
    },
)
