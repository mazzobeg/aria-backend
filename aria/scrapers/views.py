from flask import Blueprint, render_template, redirect, request
from aria import db
from aria.scrapers.models import Scraper
from aria.scrapers.core import register_scrapers
from aria.celery.core import trigger_scraper_task, celery
import datetime as dt
import logging as log

scrapers_blueprint = Blueprint("scrapers", __name__)

@scrapers_blueprint.route('/scrapers')
def scrapers(kwargs=None):
    register_scrapers()
    # query all scrapers and render it
    scrapers:list[Scraper] = Scraper.query.all()
    scrapers_data = [{'name': scraper.name, 'path': scraper.path, 'kwargs': scraper.kwargs}
                        for scraper in scrapers]    
    return render_template('scrapers.html', scrapers=scrapers_data, datas = kwargs if kwargs is not None  else {})

@scrapers_blueprint.route('/scrapers/bootstrap', methods=['GET'])
def bootstrap_scrapers():
    # create fake scrapers for testing purpose
    scraper1 = Scraper(name='scraper1', path='aria02.scrapers.scraper1', kwargs={'arg1': 'arg1'})  
    scraper2 = Scraper(name='scraper2', path='aria02.scrapers.scraper2', kwargs={'arg2': 'arg2'})
    scraper3 = Scraper(name='scraper3', path='aria02.scrapers.scraper3', kwargs={'arg3': 'arg3'})
    # add to database
    db.session.add_all([scraper1, scraper2, scraper3])
    db.session.commit()
    # redirect to scrapers page
    return redirect('/scrapers')

@scrapers_blueprint.route('/scrapers/deleteAll', methods=['GET'])
def delete_scrapers():
    # delete all scraperss
    Scraper.query.delete()
    db.session.commit()
    # redirect to scrapers page
    return redirect('/scrapers')

# add a route to trigger a scraper by name
@scrapers_blueprint.route('/scrapers/start/<scraper_name>', methods=['GET'])
def trigger_scraper_by_name(scraper_name):
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # trigger the scraper as a celery task
    trigger_scraper_task.delay(scraper.name, scraper.path, scraper.kwargs)
    # redirect to scrapers page
    return redirect('/scrapers')

# add a route to stop a celery task by scraper_name
@scrapers_blueprint.route('/scrapers/stop/<scraper_name>', methods=['GET'])
def stop_scraper_by_name(scraper_name):
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # get celery task_id by args
    tasks = list(celery.control.inspect().active().values())[0]
    task_id = None
    for task in tasks:
        if task['args'] == [scraper.name, scraper.path, scraper.kwargs]:
            task_id = task['id']
    # stop the task
    celery.control.revoke(task_id, terminate=True)
    # redirect to scrapers page
    return redirect('/scrapers')

# # add a route to get the celery task status by scraper_name
# @scrapers_blueprint.route('/scrapers/status/<scraper_name>', methods=['GET'])
# def get_scraper_status_by_name(scraper_name):
#     start_dt = dt.datetime.now()
#     scraper = Scraper.query.filter_by(name=scraper_name).first()
#     # get celery task_id by args
#     tasks = list(celery.control.inspect().active().values())[0]
#     task_id = None
#     for task in tasks:
#         if task['args'] == [scraper.name, scraper.path, scraper.kwargs]:
#             task_id = task['id']
#     # get the task status
#     task_status = {'is_running': False}
#     if task_id is not None:
#         task_status = celery.AsyncResult(task_id).status
#         task_status = {'is_running': True}
#     # return a http response with status code 200 and the task_status
#     log.info(f'Perform get_scraper_status_by_name in {(dt.datetime.now() - start_dt).seconds} s.')
#     return task_status, 200

from aria.celery.core import running_tasks

@scrapers_blueprint.route('/scrapers/status/<scraper_name>', methods=['GET'])
def summarize_status(scraper_name):
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    for running_task in running_tasks.values():
        print(running_task['args'])
        print([scraper.name, scraper.path, scraper.kwargs])
        if running_task['args'] == [scraper.name, scraper.path, scraper.kwargs]:
            return {'is_running': True}, 200
    return {'is_running': False}, 200

# create a root (POST request) to update kwargs for a scraper
@scrapers_blueprint.route('/scrapers/<string:scraper_name>/kwargs', methods=['POST'])
def update_scraper_kwargs(scraper_name):
    # get the scraper
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # update the scraper kwargs
    scraper.kwargs = request.form.get('kwargs')
    # add to database
    db.session.add(scraper)
    db.session.commit()
    # return the scraper name
    return scrapers({scraper_name : {
        'form_success' : True
    }})
    