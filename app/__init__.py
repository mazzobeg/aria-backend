from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Application(metaclass=SingletonMeta):
    app:Flask = None
    db:SQLAlchemy = None

    def __init__(self, database_uri, testing=False) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        self.app.config['TESTING'] = testing
        self.db = SQLAlchemy(app=self.app)
    
    def init(self):
        from app import models
        with self.app.app_context():
            self.db.create_all()
        from app import routes