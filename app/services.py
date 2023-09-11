from app.models import Article
from app import Application
import logging as log
from sqlite3 import IntegrityError

application = Application()

def add_article(title:str, content:str, link:str) :
    article = Article(title=title, content=content, link=link)
    with application.app.app_context():
        try :
            application.db.session.add(article)
            application.db.session.commit()
            log.info(f'New article registred {article.title}')
        except :
            log.info(f'Article already registred {article.title}')


