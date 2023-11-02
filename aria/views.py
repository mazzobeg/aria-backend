"""
This module contains the views for the root blueprint.
"""
from flask import Blueprint, render_template

root = Blueprint("commons", __name__)


@root.route("/", methods=["GET"])
def home():
    """
    Route to display the home page.
    """
    return render_template("index.html")
