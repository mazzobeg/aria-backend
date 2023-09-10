from app.models import Article
from app import Application
import logging as log
from sqlite3 import IntegrityError

application = Application()

def add_article(title='title', content='content') :
    article = Article(title=title, content=content)
    with application.app.app_context():
        try :
            application.db.session.add(article)
            application.db.session.commit()
            log.info(f'New article registred {article.title}')
        except IntegrityError :
            log.info(f'Article already registred {article.title}')


