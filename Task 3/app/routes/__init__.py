from flask import Flask

from .api import api_bp
from .web import web_bp


def register_routes(app: Flask):
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
