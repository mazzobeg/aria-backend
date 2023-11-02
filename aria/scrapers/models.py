from aria import db
import json
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Scraper(db.Model):
    name: Mapped[str] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)
    kwargs: Mapped[str] = mapped_column()

    def __init__(self, name, path, kwargs={}) -> None:
        self.name = name
        self.path = path
        self.kwargs = json.dumps(kwargs)