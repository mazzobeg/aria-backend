"""
This module contains the pytest fixtures for the application.
"""

import pytest
from src import create_app, init_db
from src.extensions import DB as db


@pytest.fixture(scope="module")
def test_app():
    """
    Pytest fixture for the application.
    """
    app = create_app(
        test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///test_aria.db",
        }
    )
    with app.app_context():
        init_db()
    yield app

    with app.app_context():
        db.drop_all()
