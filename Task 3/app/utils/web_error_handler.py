from http import HTTPStatus

from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(e):
        status = HTTPStatus.BAD_REQUEST
        return (render_template("error.html",
                                error=e, status=status), status)

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(e):
        status = HTTPStatus.NOT_FOUND
        return (render_template("error.html",
                                error=e,
                                status=status), status)

    @app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
    def method_not_allowed(e):
        status = HTTPStatus.METHOD_NOT_ALLOWED
        return (render_template("error.html",
                                error=e, status=status), status)

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(e):
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return (render_template("error.html",
                                error=e, status=status), status)
