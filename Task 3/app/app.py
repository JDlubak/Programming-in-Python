from flask import Flask

from app.routes import register_routes
from app.utils import register_error_handlers, generate_prediction_model


def create_app():
    app = Flask(__name__)
    register_routes(app)
    register_error_handlers(app)
    model = generate_prediction_model()
    app.config['model'] = model
    return app
