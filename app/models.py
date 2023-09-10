from flask_sqlalchemy import SQLAlchemy
from app import Application

application:Application = Application()
db:SQLAlchemy = application.db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    state = db.Column(db.String(50))
    grade = db.Column(db.String(200))

    def __init__(self, title, content, summary=None, state=None, grade=None):
        self.id = hash(title)
        self.title = title
        self.content = content
        self.summary = summary
        self.state = state
        self.grade = grade
