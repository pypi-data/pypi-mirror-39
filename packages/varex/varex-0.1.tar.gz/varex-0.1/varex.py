"""
Module docstring goes here.
"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index() -> str:
    """A one-line function docstring is needed if the function is exported"""
    return '<h1>Hello World!</h1>'
