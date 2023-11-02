"""
This module contains the core functionality for the Celery tasks.
"""
import logging as log
from celery import Celery
from aria.scrapers.core import trigger_scraper
from aria.articles.services import summarize_articles

celery = Celery(__name__)
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"

running_tasks = {}

def my_monitor(celery_app):
    """
    Monitor the Celery tasks.
    """
    def announce_failed_tasks(event):
        """
        Log and remove failed tasks.
        """
        task_id = event['uuid']
        log.debug("FAILED TASK: %s", task_id)
        running_tasks.pop(task_id, None)

    def announce_succeeded_tasks(event):
        """
        Log and remove succeeded tasks.
        """
        task_id = event['uuid']
        log.debug("SUCCESS TASK: %s", task_id)
        running_tasks.pop(task_id, None)

    def announce_received_tasks(event):
        """
        Log and add received tasks.
        """
        task_id = event['uuid']
        log.debug("RECEIVED TASK: %s", task_id)
        running_tasks[task_id] = {'name': event['name'], 'args': event['args']}

    with celery_app.connection() as connection:
        recv = celery_app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-succeeded': announce_succeeded_tasks,
                'task-received': announce_received_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

@celery.task(name="trigger_scraper")
def trigger_scraper_task(scraper_path, scraper_kwargs):
    """
    Celery task to trigger a scraper.
    """
    trigger_scraper(scraper_path, scraper_kwargs)

@celery.task(name="summarize_articles")
def summarize_articles_task(articles_id, articles_content, callback_endpoint):
    """
    Celery task to summarize articles.
    """
    summarize_articles(articles_id, articles_content, callback_endpoint)