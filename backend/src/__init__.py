from flask import Flask, jsonify
from flask_cors import CORS
from . import models, controllers
from .auth.auth import AuthError
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to Kanban'})

    models.init_app(app)
    controllers.init_app(app)

    # Error Handling
    def format_error(status_code, message):
        return jsonify({
            'success': False,
            'error': status_code,
            'message': message
        }), status_code

    @app.errorhandler(400)
    def bad_request(error):
        return format_error(400, "Bad request")

    @app.errorhandler(404)
    def not_found(error):
        return format_error(404, "Resource not found")

    @app.errorhandler(405)
    def method_not_allowed(error):
        return format_error(405, "Method not allowed")

    @app.errorhandler(409)
    def duplicated_found(error):
        return format_error(409, "Duplicated found")

    @app.errorhandler(422)
    def unprocessable(error):
        return format_error(422, "Unprocessable")

    @app.errorhandler(500)
    def server_error(error):
        return format_error(500, 'Internal server error')

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app
