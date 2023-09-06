import unittest, pytest, os
from app import Application
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = "articles_test.db"
DATABASE_TEST_URI = f"sqlite:///{DATABASE_NAME}"

@pytest.fixture()
def application():
    app = Application(DATABASE_TEST_URI, True)
    app.init()
    yield app
    # clean up / reset resources here
    with app.app.app_context():
        from app.models import Article
        app.db.drop_all()
        os.remove(f'./instance/{DATABASE_NAME}')
    
def test_add_article(application):
    app = application.app
    db:SQLAlchemy = application.db
    from app.models import Article
    article = Article('Mon article test', 'LOREM IPSUM', 'LOREM IPSUM')
    with app.app_context():
        db.session.add(article)
        db.session.commit()
        articles = db.session.execute(db.select(Article))
        print(articles.size())
