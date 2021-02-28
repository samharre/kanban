from flask import jsonify
from .phase_controller import phase_bp
from .task_controller import task_bp


def init_app(app):
    app.register_blueprint(phase_bp)
    app.register_blueprint(task_bp)
