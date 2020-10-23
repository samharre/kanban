import os
import unittest
import json

from src import create_app
from src.models.base import db
from src.models.phase import Phase

MANAGER_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2NkYTQzNjE0MjAwNzhlZGM4YTMiLCJhdWQiOiJrYW5iYW4iLCJpYXQiOjE2MDMzOTk3MDQsImV4cCI6MTYwMzQ4NjEwNCwiYXpwIjoicEdvY3lNSTZsUWRPM1YzZ0FlZGlXN2tTSXE4WlJFSmoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwaGFzZXMiLCJkZWxldGU6dGFza3MiLCJwYXRjaDpwaGFzZXMiLCJwYXRjaDp0YXNrcyIsInBvc3Q6cGhhc2VzIiwicG9zdDp0YXNrcyJdfQ.yic-OTr4XSgAeP4LzDunWwoncr9tVInAsT3BdWnq1wHopVUVhIEzmbVSuHUMGK3VD7aOxoTZ6kRdn95UYQDMyNOCnegQo3LOrnUjo6K9KCS5s9tEAgsZwHHm-Eidgl8azAkeO0U_dnpdU88Zp0JMovawMV4Z6t-_jzmrM6s0HbMw4xs9q61bVWFclv-_JncDVGMHVeXJyPa9qVAIASFoJAtvlxHalycTTTUr5yjU8hCmNlBrWb1VDqFb42Ln03aJcsCZEh164V3AsxdBe6bugaflEfNHVbfKi3DKTgjJFw745HzYK5t2vu0kf0AMglXfbKv43IsH5wIW_PDxRJIixg'

class PhaseTestCase(unittest.TestCase):
  '''This class represents the phase api test case'''

  def create_phase(self, title):
    res = self.client().post(
      '/phases', 
      json = {
        'title': title
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    return res
    

  def setUp(self):
    self.app = create_app(config_name="testing")
    self.client = self.app.test_client

    # binds the app to the current context
    with self.app.app_context():
      db.create_all()


  def tearDown(self):
    """teardown all initialized variables."""
    with self.app.app_context():
      db.session.remove()
      db.drop_all()


  def check_status_code_400(self, status_code, data):
    self.assertEqual(status_code, 400)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'].lower(), 'bad request')


  def check_status_code_404(self, status_code, data):
    self.assertEqual(status_code, 404)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'].lower(), 'resource not found')

  
  def check_status_code_405(self, status_code, data):
    self.assertEqual(status_code, 405)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'].lower(), 'method not allowed')


  def check_status_code_409(self, status_code, data):
    self.assertEqual(status_code, 409)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'].lower(), 'duplicated found')


  def check_status_code_422(self, status_code, data):
    self.assertEqual(status_code, 422)
    self.assertFalse(data['success'])
    self.assertEqual(data['message'].lower(), 'unprocessable')


  # ---------- Testes ---------- #
  
  def test_get_phases(self):
    self.create_phase('Backlog')

    res = self.client().get('/phases')
    data = json.loads(res.data)
    
    self.assertEqual(res.status_code, 200)
    self.assertEqual(len(data['phases']), 1)


  def test_get_phases_by_id(self):
    self.create_phase('Backlog')

    res = self.client().get('/phases/1')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['phase'].get('id'), 1)


  def test_get_phases_with_tasks(self):
    self.create_phase('Backlog')

    res = self.client().get('/phases-detail')
    data = json.loads(res.data)

    phases = data['phases']
    self.assertEqual(res.status_code, 200)
    self.assertEqual(len(phases), 1)
    self.assertEqual(len(phases[0].get('tasks')), 0)


  def test_get_phases_by_id_with_tasks(self):
    self.create_phase('Backlog')

    res = self.client().get('/phases-detail/1')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['phase'].get('id'), 1)
    self.assertEqual(len(data['phase'].get('tasks')), 0)


  def test_create_new_phase(self):
    res = self.create_phase('To Do')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['phase'].get('title'), 'To Do')

    res = self.client().get(f'/phases/1')
    data = json.loads(res.data)
    self.assertEqual(data['phase'].get('title'), 'To Do')


  def test_create_phase_without_body(self):
    res = self.client().post(
      '/phases',
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_400(res.status_code, data)


  def test_create_phase_without_title(self):
    res = self.client().post(
      '/phases',
      json={
        'title':''
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_422(res.status_code, data)


  def test_create_new_phase_duplicated_title(self):
    res = self.create_phase('Backlog')
    res = self.create_phase('Backlog')
    data = json.loads(res.data)
    
    self.check_status_code_409(res.status_code, data)


  def test_create_new_phase_passing_id(self):
    res = self.client().post(
      '/phases/1',
      json={
        'title':'To Do'
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    
    self.check_status_code_405(res.status_code, data)


  def test_update_phase(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)

    id = data['phase'].get('id')
    res = self.client().patch(
      f'/phases/{id}',
      json={
        'title': 'Backlog - Test'
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['phase'].get('title'), 'Backlog - Test')

    res = self.client().get(f'/phases/{id}')
    data = json.loads(res.data)
    self.assertEqual(data['phase'].get('title'), 'Backlog - Test')


  def test_update_phase_inexistent_id(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)

    id = data['phase'].get('id') + 1
    res = self.client().patch(
      f'/phases/{id}',
      json={
        'title': 'Trying'
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_404(res.status_code, data)


  def test_update_phase_without_body(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)

    id = data['phase'].get('id')
    res = self.client().patch(
      f'/phases/{id}',
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_400(res.status_code, data)

  
  def test_update_phase_without_title_and_order(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)

    id = data['phase'].get('id')
    res = self.client().patch(
      f'/phases/{id}',
      json={
        'title':'',
        'order':''
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_422(res.status_code, data)


  def test_update_phase_duplicating(self):
    self.create_phase('Backlog')
    res = self.create_phase('To Do')

    data = json.loads(res.data)
    id = data['phase'].get('id')
    
    res = self.client().patch(
      f'/phases/{id}',
      json={
        'title':'Backlog',
        'order':2
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_409(res.status_code, data)


  def test_update_order_phases(self):
    self.create_phase('Backlog')
    self.create_phase('Doing')
    self.create_phase('Code Review')
    res = self.create_phase('To Do')

    data = json.loads(res.data)
    id = data['phase'].get('id')
    
    res = self.client().patch(
      f'/phases/{id}',
      json={
        'order':2
      },
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    
    res = self.client().get(f'/phases')
    data = json.loads(res.data)
    phases = data['phases']

    for phase in phases:
      if phase['title'].lower() == 'backlog':
        self.assertEqual(phase['order'], 1)
      elif phase['title'].lower() == 'to do':
        self.assertEqual(phase['order'], 2)
      elif phase['title'].lower() == 'doing':
        self.assertEqual(phase['order'], 3)
      else:
        self.assertEqual(phase['order'], 4)


  def test_delete_phase(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)
    id = data['phase'].get('id')

    res = self.client().delete(
      f'/phases/{id}',
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['phase_deleted'], id)

    res = self.client().get(f'/phases/{id}')
    data = json.loads(res.data)
    self.check_status_code_404(res.status_code, data)


  def test_delete_phase_inexistent_id(self):
    res = self.create_phase('Backlog')
    data = json.loads(res.data)
    id = data['phase'].get('id') + 1

    res = self.client().delete(
      f'/phases/{id}',
      headers = {
        'Authorization': MANAGER_TOKEN
      }
    )
    data = json.loads(res.data)
    self.check_status_code_404(res.status_code, data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()