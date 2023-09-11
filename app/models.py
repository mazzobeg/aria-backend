from flask_sqlalchemy import SQLAlchemy
from app import Application

application:Application = Application()
db:SQLAlchemy = application.db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    grade = db.Column(db.String(200))

    def __init__(self, title, link, content, summary=None, state=None, grade=None):
        self.id = hash(title)
        self.title = title
        self.link = link
        self.content = content
        self.summary = summary
        self.grade = grade
