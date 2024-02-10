from flask_restx import Namespace, Resource
from .models import Scraper, scraper_model
from ..extensions import DB as db
from sqlalchemy.exc import IntegrityError
import logging as log
from .services import get_scraper, execute_scraper

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
        try:
            db.session.add(scraper)
            db.session.commit()
            return scraper, 201
        except IntegrityError:
            log.debug("Scraper already in database")
            return scraper, 500

    @NS.marshal_with(scraper_model)
    def get(self):
        scrapers = db.session.query(Scraper).all()
        return scrapers, 201


@NS.route("/scrapers/<string:scraper_name>")
class ScraperAPI(Resource):
    @NS.marshal_with(scraper_model)
    def get(self, scraper_name):
        scraper = get_scraper(scraper_name)
        if scraper is None:
            return {"message": "Scraper not found"}, 404
        return scraper, 200

    @NS.expect(scraper_model)
    def delete(self, scraper_name):
        scraper = get_scraper(scraper_name)
        if scraper is None:
            return {"message": "Scraper not found"}, 404
        db.session.delete(scraper)
        db.session.commit()
        return {"message": "Scraper deleted"}, 200

    @NS.expect(scraper_model)
    @NS.marshal_with(scraper_model)
    def put(self, scraper_name):
        scraper = get_scraper(scraper_name)
        if scraper is None:
            return {"message": "Scraper not found"}, 404
        scraper.name = NS.payload["name"]
        scraper.content = NS.payload["content"]
        scraper.kwargs = NS.payload["kwargs"]
        db.session.commit()
        return scraper, 200


@NS.route("/scrapers/<string:scraper_name>/execute")
class ScraperExecuteAPI(Resource):
    def get(self, scraper_name):
        scraper = get_scraper(scraper_name)
        result = execute_scraper(scraper)
        return result, 200
