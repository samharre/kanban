from .base import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
import json


class Task(db.Model):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    phase_id = Column(Integer, ForeignKey('phase.id'))
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    due_date = Column(DateTime)
    order = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'phase_id': self.phase_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'order': self.order,
            'user_id': self.user_id
        }

    def insert(self):
        db.session.add(self)
        self.commit()

    def add_task_to_session(self, task):
        db.session.add(task)
        self.commit()

    def update(self):
        self.commit()

    def delete(self):
        db.session.delete(self)
        self.commit()

    def rollback(self):
        db.session.rollback()

    def commit(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.serialize())
