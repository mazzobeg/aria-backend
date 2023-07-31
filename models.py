from .app import db
from flask_sqlalchemy import SQLAlchemy

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    sommaire = db.Column(db.String(500))
    etat = db.Column(db.String(50))
    avis = db.Column(db.String(200))

    def __init__(self, titre, contenu, sommaire=None, etat=None, avis=None):
        self.titre = titre
        self.contenu = contenu
        self.sommaire = sommaire
        self.etat = etat
        self.avis = avis
