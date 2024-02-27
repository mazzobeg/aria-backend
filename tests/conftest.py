"""
This module contains the pytest fixtures for the application.
"""

import pytest
from aria_backend import create_app
from .utils import get_resources


@pytest.fixture(scope="module")
def test_app():
    """
    Pytest fixture for the application.
    """

    app = create_app(
        {
            "TESTING": True,
            "MONGO_URI": "mongodb://localhost:27017/aria_test",
        }
    )
    yield app
