# Load your scraping code here
import requests
import bs4
import datetime as dt
import json
import logging as log

def registration(title:str, content:str):
    headers = {'Content-Type': 'application/json'}
    data = {'title':title,'content':content}
    data_json = json.dumps(data)
    response = requests.put(url = 'http://localhost:5000/control/article',data = data_json, headers=headers)
    if response.status_code == 200 :
        log.info(f'New article registred ${title}')
    else :
        log.error(f'PUT article failed ${title}')

import time
def main():
    log.info('IMIR scrap start.')
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
        registration(title, article_content.encode('utf-8').decode('utf-8'))