"""
This module contains the views for the scrapers blueprint.
"""
from flask import Blueprint, render_template, redirect, request
from aria import DB as db
from aria.scrapers.models import Scraper
from aria.scrapers.core import register_scrapers
from aria.celery.core import trigger_scraper_task, celery, running_tasks

scrapers_blueprint = Blueprint("scrapers", __name__)


@scrapers_blueprint.route("/scrapers")
def scrapers(kwargs=None):
    """
    Route to display the scrapers.
    """
    register_scrapers()
    # query all scrapers and render it
    scrapers_all = Scraper.query.all()
    scrapers_data = [
        {"name": scraper.name, "path": scraper.path, "kwargs": scraper.kwargs}
        for scraper in scrapers_all
    ]
    return render_template(
        "scrapers.html",
        scrapers=scrapers_data,
        datas=kwargs if kwargs is not None else {},
    )


@scrapers_blueprint.route("/scrapers/bootstrap", methods=["GET"])
def bootstrap_scrapers():
    """
    Route to create fake scrapers for testing purpose.
    """
    scraper1 = Scraper(
        name="scraper1", path="aria02.scrapers.scraper1", kwargs={"arg1": "arg1"}
    )
    scraper2 = Scraper(
        name="scraper2", path="aria02.scrapers.scraper2", kwargs={"arg2": "arg2"}
    )
    scraper3 = Scraper(
        name="scraper3", path="aria02.scrapers.scraper3", kwargs={"arg3": "arg3"}
    )
    # add to database
    db.session.add_all([scraper1, scraper2, scraper3])
    db.session.commit()
    # redirect to scrapers page
    return redirect("/scrapers")


@scrapers_blueprint.route("/scrapers/deleteAll", methods=["GET"])
def delete_scrapers():
    """
    Route to delete all scrapers.
    """
    Scraper.query.delete()
    db.session.commit()
    # redirect to scrapers page
    return redirect("/scrapers")


@scrapers_blueprint.route("/scrapers/start/<scraper_name>", methods=["GET"])
def trigger_scraper_by_name(scraper_name):
    """
    Route to trigger a scraper by name.
    """
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # trigger the scraper as a celery task
    trigger_scraper_task.delay(scraper.path, scraper.kwargs)
    # redirect to scrapers page
    return redirect("/scrapers")


@scrapers_blueprint.route("/scrapers/stop/<scraper_name>", methods=["GET"])
def stop_scraper_by_name(scraper_name):
    """
    Route to stop a scraper by name.
    """
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # get celery task_id by args
    tasks = list(celery.control.inspect().active().values())[0]
    task_id = None
    for task in tasks:
        if task["args"] == [scraper.name, scraper.path, scraper.kwargs]:
            task_id = task["id"]
    # stop the task
    celery.control.revoke(task_id, terminate=True)
    # redirect to scrapers page
    return redirect("/scrapers")


@scrapers_blueprint.route("/scrapers/status/<scraper_name>", methods=["GET"])
def summarize_status(scraper_name):
    """
    Route to get the status of a scraper by name.
    """
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    for running_task in running_tasks.values():
        print("---------")
        print("Comparaison")
        print(running_task["args"])
        print([scraper.path, scraper.kwargs])
        print(running_task["args"] == [scraper.path, scraper.kwargs])
        print("---------")
        if (scraper.path in running_task["args"]) and ( scraper.kwargs in running_task["args"]):
            return {"is_running": True}, 200
    return {"is_running": False}, 200


@scrapers_blueprint.route("/scrapers/<string:scraper_name>/kwargs", methods=["POST"])
def update_scraper_kwargs(scraper_name):
    """
    Route to update kwargs for a scraper.
    """
    # get the scraper
    scraper = Scraper.query.filter_by(name=scraper_name).first()
    # update the scraper kwargs
    scraper.kwargs = request.form.get("kwargs")
    # add to database
    db.session.add(scraper)
    db.session.commit()
    # return the scraper name
    return scrapers({scraper_name: {"form_success": True}})
