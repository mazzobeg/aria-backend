from flask import Blueprint, render_template

root = Blueprint("commons", __name__)

@root.route('/', methods=['GET'])
def home():
    return render_template('index.html')