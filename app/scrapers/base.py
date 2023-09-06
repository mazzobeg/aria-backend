# Load model of Article
from app.models import Article
from app import Application
from app.core import summarize_text

# Load your scraping code here
import requests
import bs4
import datetime as dt
import json

application:Application = Application()
db = application.db

def main():
    print('scraper main start')
    articles = []
    url = "https://www.jmir.org"
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a', attrs={'data-test': 'card-title'})
    for result in results :
        title = result['title'].replace(" ", "_").replace(":", "_").replace(",","_")[0:50]
        link = result['href']
        url_builded = f'{url}{link}'
        html = requests.get(url_builded).content
        soup = bs4.BeautifulSoup(html, 'html.parser')
        article_contents = soup.select("article .abstract p")
        article_content = " ".join([x.text for x in article_contents])
        #print(article_content.encode("utf-8"))
        timestamp = dt.datetime.now().strftime('%Y%m%d')
        title = title
        content = article_content.encode('utf-8').decode('utf-8')
        summary = ''
        article = Article(title, content, summary, "NA", "NA")
        articles.append(article)
    article:Article
    for article in articles:
        print('article')
        db.session.add(article)
        db.session.commit()

if __name__ == '__main__' :
    print('scraper start')
    articles = main()
    article:Article
    for article in articles:
        db.session.add(article)
        db.session.commit()