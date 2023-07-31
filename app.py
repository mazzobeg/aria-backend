from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisez l'extension SQLAlchemy
db = SQLAlchemy(app)

from .service import ArticleService

# Initialisez le service ArticleService
article_service = ArticleService()

@app.route('/articles', methods=['GET'])
def get_all_articles():
    articles = article_service.get_all_articles()
    articles_data = [{'id': article.id, 'titre': article.titre, 'contenu': article.contenu,
                      'sommaire': article.sommaire, 'etat': article.etat, 'avis': article.avis}
                     for article in articles]
    return render_template('tables.html',  articles=articles_data)

@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article_by_id(article_id):
    article = article_service.get_article_by_id(article_id)
    if article:
        article_data = {'id': article.id, 'titre': article.titre, 'contenu': article.contenu,
                        'sommaire': article.sommaire, 'etat': article.etat, 'avis': article.avis}
        return render_template('article.html', article=article_data)
    else:
        return render_template('404.html')

@app.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    titre = data.get('titre')
    contenu = data.get('contenu')
    sommaire = data.get('sommaire')
    etat = data.get('etat')
    avis = data.get('avis')

    if titre and contenu:
        article = article_service.create_article(titre, contenu, sommaire, etat, avis)
        article_data = {'id': article.id, 'titre': article.titre, 'contenu': article.contenu,
                        'sommaire': article.sommaire, 'etat': article.etat, 'avis': article.avis}
        return jsonify(article_data), 201
    else:
        return jsonify({'message': 'Le titre et le contenu sont requis'}), 400

@app.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = article_service.get_article_by_id(article_id)
    if article:
        data = request.get_json()
        titre = data.get('titre')
        contenu = data.get('contenu')
        sommaire = data.get('sommaire')
        etat = data.get('etat')
        avis = data.get('avis')

        if titre and contenu:
            updated_article = article_service.update_article(article_id, titre, contenu, sommaire, etat, avis)
            article_data = {'id': updated_article.id, 'titre': updated_article.titre,
                            'contenu': updated_article.contenu, 'sommaire': updated_article.sommaire,
                            'etat': updated_article.etat, 'avis': updated_article.avis}
            return jsonify(article_data)
        else:
            return jsonify({'message': 'Le titre et le contenu sont requis'}), 400
    else:
        return jsonify({'message': 'Article non trouvé'}), 404

@app.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = article_service.get_article_by_id(article_id)
    if article:
        article_service.delete_article(article_id)
        return jsonify({'message': 'Article supprimé avec succès'}), 200
    else:
        return jsonify({'message': 'Article non trouvé'}), 404

if __name__ == '__main__':
    app.run(debug=True)


