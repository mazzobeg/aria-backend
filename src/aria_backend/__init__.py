"""
aria_backend package initialization.
"""

__version__ = "0.1.0"

from flask import Flask
from .extensions import DB, API, MIGRATE
import click
from flask.cli import with_appcontext
import logging as log
from flask_cors import CORS
from flask_migrate import Migrate
import os

log.basicConfig(level=log.DEBUG)


def init_db():
    """
    Initialize the database.
    """
    DB.drop_all()
    DB.create_all()


@click.command("init-db")
@with_appcontext
def init_db_cmd():
    """
    Database initialization command.
    """
    init_db()
    click.echo("Database initialized.")


def create_app(config_path: str):
    """
    Application factory function.
    """
    app = Flask(__name__)
    CORS(app)  # TODO remove this in production

    app.config.from_pyfile(config_path, silent=False)

    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    app.cli.add_command(init_db_cmd)

    from .articles.api import NS
    from .scrapers.api import NS as NS_SCRAPERS

    API.init_app(app)
    API.add_namespace(NS)
    API.add_namespace(NS_SCRAPERS)

    # display all roots of app
    log.debug(app.url_map)

    return app
