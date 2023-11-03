"""
This module contains the Flask application factory and the database initialization command.
"""
# pylint: disable=R0401
# pylint: disable=C0415
from threading import Thread
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_restx import Api
import click

class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """
    # pylint: disable=R0903
    # pylint: disable=W0107
    pass

DB = SQLAlchemy(model_class=Base)
API = Api(doc="/doc")

def create_app(test_config=None):
    """
    Application factory function.
    """
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    DB.init_app(app)
    app.cli.add_command(init_db_cmd)

    from aria.articles.api import NS
    API.init_app(app)
    API.add_namespace(NS)

    from aria.celery.core import my_monitor, celery

    Thread(target=my_monitor, args=(celery,), daemon=True).start()

    # Load blueprints
    from aria.scrapers.views import scrapers_blueprint
    from aria.articles.views import articles_blueprint
    from aria.dashboard.views import dashboard_bp
    from aria.views import root

    app.register_blueprint(scrapers_blueprint)
    app.register_blueprint(articles_blueprint)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(root)
    return app


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
