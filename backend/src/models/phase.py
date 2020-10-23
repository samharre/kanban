from .base import db
from sqlalchemy import Column, String, Integer, func
from sqlalchemy.orm import relationship
import json

class Phase(db.Model):
  __tablename__ = 'phase'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False, unique=True)
  order = Column(Integer, nullable=False)
  tasks = relationship('Task', backref='phase', lazy=True, cascade='all, delete-orphan')
  
  def serialize(self):
    return {
      'id': self.id,
      'title': self.title,
      'order': self.order
    }

  def serialize_with_tasks(self):
    return {
      'id': self.id,
      'title': self.title,
      'order': self.order,
      'tasks': [task.serialize() for task in self.tasks]
    }

  def insert(self):
    self.order = db.session.query(func.count(Phase.id)).scalar() + 1
    db.session.add(self)
    # db.session.commit()

  def add_phase_to_session(self, phase):
    db.session.add(phase)

  # def update(self):
    # db.session.commit()

  def delete(self):
    db.session.delete(self)
    # db.session.commit()

  def rollback(self):
    db.session.rollback()

  def commit(self):
    db.session.commit()

  # def close(self):
  #   print('PASSOU PELO CLOSE')
  #   db.session.close()

  def __repr__(self):
      return json.dumps(self.serialize())