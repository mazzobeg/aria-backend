import os

def get_resources(relative_path):
    return os.path.dirname(__file__) + "/resources/" + relative_path