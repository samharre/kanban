from .base import db
from sqlalchemy import Column, String, Integer, Boolean, func
from sqlalchemy.orm import relationship
import json


class Phase(db.Model):
    __tablename__ = 'phase'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    can_create_task = Column(Boolean, nullable=False, default=True)
    tasks = relationship('Task', backref='phase', lazy=True,
                         cascade='all, delete-orphan')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'order': self.order,
            'can_create_task': self.can_create_task
        }

    def serialize_with_tasks(self):
        return {
            'id': self.id,
            'title': self.title,
            'order': self.order,
            'can_create_task': self.can_create_task,
            'tasks': [task.serialize() for task in self.tasks]
        }

    def insert(self):
        self.order = db.session.query(func.count(Phase.id)).scalar() + 1
        db.session.add(self)

    def add_phase_to_session(self, phase):
        db.session.add(phase)

    def delete(self):
        db.session.delete(self)

    def rollback(self):
        db.session.rollback()

    def commit(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.serialize())
