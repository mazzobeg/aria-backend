"""
This module contains the pytest fixtures for the application.
"""

import pytest
from aria_backend import create_app, init_db
from aria_backend.extensions import DB as db
from .utils import get_resources


@pytest.fixture(scope="module")
def test_app():
    """
    Pytest fixture for the application.
    """
    db_path = get_resources("test_aria.db")
    app = create_app(
        config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )
    with app.app_context():
        init_db()
    yield app

    with app.app_context():
        db.drop_all()
