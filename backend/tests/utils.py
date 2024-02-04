"""
This module contains utility functions.
"""
import os


def get_resources(relative_path):
    """
    Function to get the absolute path of a resource.
    """
    return os.path.join(os.path.dirname(__file__), "resources", relative_path)
