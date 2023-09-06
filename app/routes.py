from flask import render_template
from app.models import Article
from app.scrapers import base
from app.core import remove_all_articles
from app import Application

app:Application = Application().app

@app.route('/articles', methods=['GET'])
def get_all_articles():
    articles = Article.query.all()
    articles_data = [{'id': article.id, 'titre': article.titre, 'contenu': article.contenu,
                      'sommaire': article.sommaire, 'etat': article.etat, 'avis': article.avis}
                     for article in articles]
    return render_template('articles.html',  articles=articles_data)

# @app.route('/articles/scrapers', methods=['GET'])
# def run_scrapers_on_articles():
#     base.main()
#     return get_all_articles()

@app.route('/')
def home():
    print('called')
    return render_template('index.html')

@app.route('/articles/remove', methods=['GET'])
def articles_remove():
    remove_all_articles()
    return get_all_articles()