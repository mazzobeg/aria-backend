from flask_sqlalchemy import SQLAlchemy
from app import Application

application:Application = Application()
db:SQLAlchemy = application.db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    sommaire = db.Column(db.String(500))
    etat = db.Column(db.String(50))
    avis = db.Column(db.String(200))

    def __init__(self, titre, contenu, sommaire=None, etat=None, avis=None):
        self.id = hash(titre)
        self.titre = titre
        self.contenu = contenu
        self.sommaire = sommaire
        self.etat = etat
        self.avis = avis
