from transformers import pipeline
import concurrent.futures
from app import Application
import importlib, os

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

def trigger_scrapers() -> bool:
    if not Application().scraper.lock :
        Application().scraper.lock = True
        # Nom du package
        PACKAGE_NAME = 'scrapers'
        # Récupérer la liste des fichiers (modules) dans le package
        package_dir = os.path.dirname(__file__) if '__file__' in globals() else '.'
        module_files = [f[:-3] for f in os.listdir(package_dir + '/' + PACKAGE_NAME) if f.endswith('.py') and f != '__init__.py']
        # Importer et exécuter la fonction 'main' de chaque module
        for module_name in module_files:
            module = importlib.import_module(f'app.{PACKAGE_NAME}.{module_name}')
            if hasattr(module, 'main') and callable(module.main):
                print(f'Exécution de la fonction main dans le module {module_name}')
                module.main()
            else:
                print(f'Le module {module_name} ne contient pas de fonction main.')
        Application().scraper.lock = False
        return True
    else :
        return False
