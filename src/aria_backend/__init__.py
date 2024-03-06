"""
aria_backend package initialization.
"""

__version__ = "0.1.0"

from flask import Flask, render_template
from .extensions import API
import click
from flask.cli import with_appcontext
import logging as log
from flask_cors import CORS
from flask_migrate import Migrate
import os
from mongoengine import connect

log.basicConfig(level=log.DEBUG)


def create_app(config_as_dict):
    """
    Application factory function.
    """
    app = Flask(__name__)
    CORS(app)  # TODO remove this in production

    app.config.update(config_as_dict)

    connect(host=app.config["MONGO_URI"])

    from .articles.api import NS
    from .scrapers.api import NS as NS_SCRAPERS

    API.init_app(app)
    API.add_namespace(NS)
    API.add_namespace(NS_SCRAPERS)

    # display all roots of app
    log.debug(app.url_map)

    return app
