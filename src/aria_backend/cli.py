from . import create_app, init_db
import os, sys
import logging as log
import urllib.parse
import argparse
import json

log.basicConfig(level=log.INFO)


def main():
    # TODO add argument to the config file
    parser = argparse.ArgumentParser(description="Aria backend")
    parser.add_argument("-c", "--config", help="The configuration path", required=True)
    args = parser.parse_args()
    config_path = args.config

    with open(config_path, "r") as f:
        config = json.load(f)

        # executable_path = os.path.dirname(sys.executable)
        # log.info(f"Executable path: {executable_path}")

        app = create_app(config=config)

        # assume the path is absolute
        db_path = urllib.parse.urlparse(app.config["SQLALCHEMY_DATABASE_URI"]).path
        log.info(f"Database path: {db_path}")
        if not os.path.exists(db_path):
            log.info("Database not found, creating a new one")
            with app.app_context():
                init_db()
        app.run()


if __name__ == "__main__":
    main()
