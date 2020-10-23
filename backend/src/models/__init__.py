from .base import db
from .phase import Phase
from .task import Task

def init_app(app):
    db.init_app(app)