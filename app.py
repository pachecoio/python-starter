from flask import Flask
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__)
    register_error_handlers(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from views import user

    app.register_blueprint(user.bp)


def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return {"message": e.description}, e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        return {"message": f"Internal server error: {str(e)}"}, 500

    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_exception)

