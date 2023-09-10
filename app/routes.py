from flask import render_template, Response, request, jsonify
from app.models import Article
from app.core import remove_all_articles, trigger_scrapers
from app import Application
from app import services
import logging as log

app:Application = Application().app

@app.route('/articles', methods=['GET'])
def get_all_articles():
    articles = Article.query.all()
    articles_data = [{'id': article.id, 'title': article.title, 'content': article.content,
                      'summary': article.summary, 'state': article.state, 'grade': article.grade}
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

@app.route('/trigger_scraping', methods=['GET'])
def trigger_scraping():
    if trigger_scrapers() :
        message = "Opération réussie."
        return Response(message, status=200, content_type="text/plain")
    else : 
        message = "Already in activity."
        return Response(message, status=401, content_type="text/plain")
    
@app.route('/control/scraper/state', methods = ['GET'])
def get_control_scraper_state() :
    response = {'state' : Application().scraper.lock}
    return jsonify(response), 200

@app.route('/control/article', methods=['PUT'])
def add_article():
    data = request.get_json()
    print('Données reçues')
    if 'title' in data.keys() and 'content' in data.keys() :
        services.add_article(title = data['title'] , content=data['content'])
        reponse = {'message': 'Requête PUT réussie!', 'donnees': data}
        return jsonify(reponse), 200
    else :
        log.error('PUT request not contains required keys')
        reponse = {'message': 'Requête PUT échouée!', 'donnees': data}
        return jsonify(reponse), 400
