import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # apply the blueprints to the app
    from . import search

    app.register_blueprint(search.bp)
    

    return app