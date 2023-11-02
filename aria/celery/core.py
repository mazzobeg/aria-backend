from celery import Celery
from aria.scrapers.core import trigger_scraper
from aria.articles.services import summarize_articles
from threading import Thread
import logging as log
import signal

celery = Celery(__name__)
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"

running_tasks = {}

def my_monitor(celery):
    state = celery.events.State()

    def announce_failed_tasks(event):
        log.debug("FAILED TASK:" + str(event['uuid']))
        running_tasks.pop(event['uuid'])

    def announce_succeeded_tasks(event):
        log.debug("SUCCESS TASK:" + str(event['uuid']))
        running_tasks.pop(event['uuid'])

    def announce_reveived_tasks(event):
        log.debug("REVEIVED TASK:" + str(event['uuid']))
        running_tasks[event['uuid']] = {'name': event['name'],'args': event['args']}

    with celery.connection() as connection:
        recv = celery.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-succeeded': announce_succeeded_tasks,
                'task-received': announce_reveived_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

@celery.task(name="trigger_scraper")
def trigger_scraper_task(scraper_name, scraper_path, scraper_kwargs):
    trigger_scraper(scraper_path, scraper_kwargs)

@celery.task(name="summarize_articles")
def summarize_articles_task(articles_id:list[str], articles_content:list[str], callback_endpoint:str):
    summarize_articles(articles_id, articles_content, callback_endpoint)