from flask_restx import Namespace, Resource

from .models import Scraper, scraper_model

import logging as log

from .services import (
    get_scraper,
    execute_scraper,
    update_scraper,
    delete_scraper,
    add_scraper,
    get_scrapers,
)

NS = Namespace("scrapers")


@NS.route("/scrapers")
class ScrapersAPI(Resource):
    @NS.expect(scraper_model)
    @NS.marshal_with(scraper_model)
    def post(self):
        scraper = Scraper(
            name=NS.payload["name"],
            content=NS.payload["content"],
            kwargs=NS.payload["kwargs"],
        )
        add_scraper(scraper)
        return scraper, 201

    @NS.marshal_with(scraper_model)
    def get(self):
        return get_scrapers(), 201


@NS.route("/scrapers/<string:scraper_name>")
class ScraperAPI(Resource):
    @NS.marshal_with(scraper_model)
    def get(self, scraper_name):
        try:
            scraper = get_scraper(scraper_name)
            return scraper, 200
        except ValueError:
            return {"message": "Scraper not found"}, 404

    @NS.expect(scraper_model)
    def delete(self, scraper_name):
        try:
            delete_scraper(scraper_name)
            return {"message": "Scraper deleted"}, 200
        except ValueError:
            return {"message": "Scraper not found"}, 404

    @NS.expect(scraper_model)
    @NS.marshal_with(scraper_model)
    def put(self, scraper_name):
        scraper = get_scraper(scraper_name)
        if scraper is None:
            return {"message": "Scraper not found"}, 404
        scraper.name = NS.payload["name"]
        scraper.content = NS.payload["content"]
        scraper.kwargs = NS.payload["kwargs"]
        update_scraper(scraper_name, scraper)
        return scraper, 200


@NS.route("/scrapers/<string:scraper_name>/execute")
class ScraperExecuteAPI(Resource):
    def get(self, scraper_name):
        scraper = get_scraper(scraper_name)
        result = execute_scraper(scraper)
        return result, 200
