"""
This module contains the core functionality for creating and registering scrapers.
"""
import os
import json
import importlib.util
from aria import DB as db
from aria.scrapers.models import Scraper
from flask import current_app


def create_scrapers(path: str) -> list[Scraper]:
    """
    Create a scraper from a directory path.
    Given a directory path containing python files, load all python files in it
    and create scrapers using the model.
    """
    module_files = [
        f[:-3] for f in os.listdir(path) if f.endswith(".py") and f != "__init__.py"
    ]
    scrapers = []
    for module_name in module_files:
        # load module from an absolute path
        module_path = f"{path}/{module_name}.py"
        json_path = f"{path}/{module_name}.json"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        scraper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scraper_module)
        if hasattr(scraper_module, "main") and callable(scraper_module.main):
            kwargs = {}
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as file:
                    kwargs = json.load(file)
            scraper = Scraper(module_name, module_path, kwargs)
            scrapers.append(scraper)
    return scrapers


def register_scrapers():
    """
    Register all scrapers in the database.
    """
    # TODO replace hardcoded path by a config variable
    scrapers_path = current_app.config["SCRAPERS_PATH"]
    scrapers = create_scrapers(scrapers_path)
    # register all scrapers in database if not already registered
    for scraper in scrapers:
        if not Scraper.query.filter_by(name=scraper.name).first():
            db.session.add(scraper)
    db.session.commit()


def trigger_scraper(scraper_path, scraper_kwargs):
    """
    Trigger a scraper.
    """
    spec = importlib.util.spec_from_file_location("scraper", scraper_path)
    scraper_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scraper_module)
    kwargs = json.loads(scraper_kwargs)
    if kwargs:
        scraper_module.main(kwargs)
    else:
        scraper_module.main()
