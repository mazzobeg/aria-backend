from transformers import pipeline
import concurrent.futures
from app import Application

executor = concurrent.futures.ThreadPoolExecutor

def summarize_text(full_text) :
    print('convert full_text')
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer(full_text, max_length=len(full_text), min_length=len(full_text), do_sample=False)

def summarize_article(article):
    article.sommaire = summarize_text(article.contenu)
    db = Application().db
    db.session.add(article)
    db.session.commit()

def submit_article_summarization(article_id):
    executor.submit(summarize_article, article_id)

def remove_all_articles():
    from app.models import Article
    db = Application().db
    db.session.query(Article).delete()
