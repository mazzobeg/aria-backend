from aria import db
import hashlib
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ArticleGrade(Enum):
    MEH="MEH"
    SMILE="SMILE"
    FROWN="FROWN"
    @classmethod
    def from_text(cls, text:str):
        uppered_text = text.upper()
        if uppered_text in [v.value for v in cls] :
            return cls(uppered_text)
        else :
            raise ValueError("Value not allowed.")

class Article(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(nullable=True)
    grade: Mapped[ArticleGrade] = mapped_column(nullable=True)

    def __init__(self, title, link:str, content, summary=None, grade:ArticleGrade=None):
        self.id = hashlib.md5(link.encode('utf-8')).hexdigest()
        self.title = title
        self.link = link
        self.content = content
        self.summary = summary
        self.grade = grade