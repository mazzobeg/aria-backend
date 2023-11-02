import pytest
from aria import create_app, init_db

@pytest.fixture(scope="module")
def test_app() :
    app = create_app(test_config={"TESTING":True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test_aria.db"})
    with app.app_context():
        init_db()
    yield app