from .models import Article
from .app import db

class ArticleRepository:
    def create_article(self, titre, contenu, sommaire=None, etat=None, avis=None):
        article = Article(titre=titre, contenu=contenu, sommaire=sommaire, etat=etat, avis=avis)
        db.session.add(article)
        db.session.commit()
        return article

    def get_article_by_id(self, article_id):
        return Article.query.get(article_id)

    def get_all_articles(self):
        return Article.query.all()

    def update_article(self, article_id, titre, contenu, sommaire=None, etat=None, avis=None):
        article = Article.query.get(article_id)
        if article:
            article.titre = titre
            article.contenu = contenu
            article.sommaire = sommaire
            article.etat = etat
            article.avis = avis
            db.session.commit()
        return article

    def delete_article(self, article_id):
        article = Article.query.get(article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
        return article
