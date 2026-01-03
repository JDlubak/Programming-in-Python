from flask import Flask

from .data import data_bp


def register_routes(app: Flask):
    app.register_blueprint(data_bp)
