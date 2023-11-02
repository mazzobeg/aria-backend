from flask import Blueprint, render_template, redirect, request, url_for
from aria.articles.models import Article, ArticleGrade
from aria.celery.core import summarize_articles_task, celery
from aria.articles.services import summarize_articles
from aria import db
import logging as log
import re
from sqlalchemy.exc import IntegrityError

articles_blueprint = Blueprint('articles', __name__)

@articles_blueprint.route('/articles', methods=['GET'])
def articles():
    articles: list[Article] = Article.query.all()
     # get the group match the regex '\.(.*)\.' in the string article.link
    regex = re.compile('\.(.*)\.')
    articles_data = [{'id': article.id, 'title': article.title, 'content': article.content, 'link': article.link, 'summary': '' if article.summary is None else article.summary , 'grade': '' if article.grade is None else article.grade.value, 'domain': regex.search(article.link).group(1)}
                        for article in articles]
    return render_template('articles.html',  articles=articles_data)

@articles_blueprint.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get(article_id)
    return render_template('article.html', article=article)

@articles_blueprint.route('/articles/bootstrap', methods=['GET'])
def bootstrap_article():
    article1 = Article('TITLE1', 'CONTENT1', 'LINK1', 'SUMMARY1', ArticleGrade.FROWN)
    article2 = Article('TITLE2', 'CONTENT2', 'LINK2', 'SUMMARY2', ArticleGrade.FROWN)
    article3 = Article('TITLE3', 'CONTENT3', 'LINK3', 'SUMMARY3', ArticleGrade.FROWN)
    db.session.add_all([article1, article2, article3])
    db.session.commit()
    return redirect('/articles')

@articles_blueprint.route('/articles/deleteAll', methods=['GET'])
def delete_all_articles():
    Article.query.delete()
    db.session.commit()
    return redirect('/articles')

# create a PUT root to add article with text and content as parameters
@articles_blueprint.route('/articles/add', methods=['PUT'])
def add_article(): 
    # get the request data
    data = request.get_json()
    # create an article
    article = Article(data['title'], data['link'], data['content'])
    # add to database
    try:
        db.session.add(article)
        db.session.commit()
    except IntegrityError:
        log.debug("Article already in database")
    return str(article.id)

# create a root to acces unique article by id
@articles_blueprint.route('/articles/<string:article_id>', methods=['GET'])
def get_article_by_id(article_id):
    article = Article.query.get(article_id)
    return render_template('article.html', article=article)

summarizers = []

@articles_blueprint.route('/articles/summarize/start', methods=['GET'])
def start_summarize():
    articles: list[Article] = Article.query.filter(Article.summary == None).all()
    callback_endpoint = url_for('articles.article_add_summary', _external=True)
    uiid = summarize_articles_task.delay([article.id for article in articles], [article.content for article in articles], callback_endpoint)
    summarizers.append(uiid)
    return redirect('/articles')

@articles_blueprint.route('/articles/add/summary', methods=['POST'])
def article_add_summary():
    data = request.get_json()
    article = Article.query.get(data['id'])
    article.summary = data['summary']
    db.session.add(article)
    db.session.commit()
    return redirect('/articles')

# create a root (GET request) to update grade on article
@articles_blueprint.route('/articles/<string:article_id>/grade/<string:grade>', methods=['GET'])
def update_article_grade(article_id, grade):
    article = Article.query.get(article_id)
    article.grade = ArticleGrade.from_text(grade)
    db.session.add(article)
    db.session.commit()
    return redirect('/articles')

from aria.celery.core import running_tasks

# create a root (GET request) to check if summarization task running
@articles_blueprint.route('/articles/summarize/status', methods=['GET'])
def summarize_status():
    # active_task = celery.control.inspect().active()
    # # check if a task named 'summarize_articles' is running
    # names = [x['name'] for x in list(active_task.values())[0]]
    for running_task in running_tasks.values():
        if 'summarize_articles' == running_task['name']:
            return {'running': True}, 200
    return {'running': False}, 200



# # create a root (GET request) to check status of summarization task
# @articles_blueprint.route('/articles/summarize/status/<string:task_id>', methods=['GET'])
# def summarize_task_status(task_id):
#     if task_id
