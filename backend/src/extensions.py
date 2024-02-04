from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_restx import Api
from flask_migrate import Migrate


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """

    # pylint: disable=R0903
    # pylint: disable=W0107
    pass


DB = SQLAlchemy(model_class=Base)
API = Api(doc="/doc")
MIGRATE = Migrate()
