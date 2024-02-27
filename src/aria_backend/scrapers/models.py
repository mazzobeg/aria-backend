"""
This module contains the Scraper model.
"""

from ..extensions import API as api
from flask_restx import fields
from mongoengine import Document, StringField
import json


class Scraper(Document):
    """
    Represents a scraper object used for scraping content.

    Attributes:
        name (str): The name of the scraper.
        content (str): The content to be scraped.
        kwargs (str, optional): Additional keyword arguments for the scraper.
    """

    name = StringField(required=True)
    content = StringField(required=True)
    kwargs = StringField()


scraper_model = api.model(
    "Scraper",
    {
        "name": fields.String(required=True),
        "content": fields.String(required=True),
        "kwargs": fields.String(required=False),
    },
)
