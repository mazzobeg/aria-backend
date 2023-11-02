"""
This module contains the Scraper model.
"""
import json
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String
from aria import DB as db


class Scraper(db.Model):
    """
    Scraper model class.
    """

    # pylint: disable=R0903
    name: Mapped[str] = Column(String, primary_key=True)
    path: Mapped[str] = Column(String, nullable=False)
    kwargs: Mapped[str] = Column(String)

    def __init__(self, name, path, kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.name = name
        self.path = path
        self.kwargs = json.dumps(kwargs)
