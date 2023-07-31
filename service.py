from .repository import ArticleRepository

class ArticleService:
    def __init__(self):
        self.article_repository = ArticleRepository()

    def create_article(self, titre, contenu, sommaire=None, etat=None, avis=None):
        return self.article_repository.create_article(titre, contenu, sommaire, etat, avis)

    def get_article_by_id(self, article_id):
        return self.article_repository.get_article_by_id(article_id)

    def get_all_articles(self):
        return self.article_repository.get_all_articles()

    def update_article(self, article_id, titre, contenu, sommaire=None, etat=None, avis=None):
        return self.article_repository.update_article(article_id, titre, contenu, sommaire, etat, avis)

    def delete_article(self, article_id):
        return self.article_repository.delete_article(article_id)
