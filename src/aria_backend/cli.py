from . import create_app
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

    # check if the file is .json
    if not config_path.endswith(".json"):
        log.error("Configuration file must be a .json file")
        sys.exit(1)

    with open(config_path, "r") as f:
        config_as_dict = json.load(f)
        app = create_app(config_as_dict)
        app.run(port=app.config["FLASK_RUN_PORT"], host="0.0.0.0")


if __name__ == "__main__":
    main()
