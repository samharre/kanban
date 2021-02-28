import os
import unittest
import json

from src import create_app
from src.models.base import db
from src.models.phase import Phase
from src.models.task import Task

from . import (
    check_status_code_400,
    check_status_code_404,
    check_status_code_405,
    check_status_code_409,
    check_status_code_422
)

MANAGER_TOKEN = MANAGER_TOKEN = os.getenv('MANAGER_TOKEN')


class TaskTestCase(unittest.TestCase):
    '''This class represents the task api test case'''

    def create_phase(self, title):
        res = self.client().post(
            '/phases',
            json={
                'title': title
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )

        data = json.loads(res.data)
        return data['phase']

    def create_task(self, phase_id, title):
        res = self.client().post(
            '/tasks',
            json={
                'phase_id': phase_id,
                'title': title
            },
            headers={
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

    # ---------- Testes ---------- #

    def test_get_tasks(self):
        phase = self.create_phase('Backlog')
        self.create_task(phase['id'], 'Tasks endpoints')
        self.create_task(
            phase['id'], 'Implements authentication using Auth0 on the server')

        res = self.client().get(
            '/tasks',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['tasks']), 2)

    def test_get_tasks_by_phase(self):
        phase = self.create_phase('Backlog')
        self.create_task(phase['id'], 'Tasks endpoints')

        phase = self.create_phase('To Do')
        self.create_task(
            phase['id'], 'Implements authentication using Auth0 on the server')
        self.create_task(phase['id'], 'Creating data to test phases and tasks')

        res = self.client().get(
            '/phases/1/tasks',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        tasks = data['tasks']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(tasks[0]['phase_id'], 1)
        self.assertEqual(len(tasks), 1)

    def test_create_new_task(self):
        phase = self.create_phase('Backlog')
        res = self.create_task(phase['id'], 'Tasks endpoints')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['task'].get('title'), 'Tasks endpoints')

    def test_400_create_task_without_body(self):
        res = self.client().post(
            '/tasks',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_400(self, res.status_code, data)

    def test_422_create_task_without_title_or_phase_id(self):
        # Task without title
        phase = self.create_phase('Backlog')
        res = self.client().post(
            '/tasks',
            json={
                'phase_id': phase['id'],
                'title': ''
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_422(self, res.status_code, data)

        # Task without phase_id
        res = self.client().post(
            '/tasks',
            json={
                'phase_id': None,
                'title': 'Test test_422_create_task_without_title_or_phase_id'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_422(self, res.status_code, data)

    def test_405_create_new_phase_passing_id(self):
        res = self.client().post(
            '/tasks/1',
            json={
                'title': 'Test test_405_create_new_phase_passing_id'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_405(self, res.status_code, data)

    def test_update_task(self):
        phase = self.create_phase('Backlog')

        res = self.create_task(phase['id'], 'Tasks endpoints')
        data = json.loads(res.data)

        id = data['task'].get('id')
        res = self.client().patch(
            f'/tasks/{id}',
            json={
                'title': 'Tasks endpoints - Test'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['task'].get('title'), 'Tasks endpoints - Test')

    def test_404_update_task_id_inexistent(self):
        res = self.client().patch(
            f'/tasks/10',
            json={
                'title': 'Trying'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_404(self, res.status_code, data)

    def test_400_update_task_without_body(self):
        phase = self.create_phase('Backlog')

        res = self.create_task(phase['id'], 'Tasks endpoints')
        data = json.loads(res.data)

        id = data['task'].get('id')
        res = self.client().patch(
            f'/tasks/{id}',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_400(self, res.status_code, data)

    def test_422_update_task_without_phase_id_and_order(self):
        phase = self.create_phase('Backlog')

        res = self.create_task(phase['id'], 'Tasks endpoints')
        data = json.loads(res.data)

        id = data['task'].get('id')
        res = self.client().patch(
            f'/phases/{id}',
            json={
                'phase_id': None,
                'order': ''
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_422(self, res.status_code, data)

    def test_update_order_task_same_phase(self):
        phase = self.create_phase('Backlog')
        phase_id = phase['id']
        self.create_task(phase_id, 'Task A')
        self.create_task(
            phase_id, 'Task B')
        self.create_task(phase_id, 'Task C')
        res = self.create_task(phase_id, 'Task D')

        data = json.loads(res.data)
        id = data['task'].get('id')

        res = self.client().patch(
            f'/phases/{id}',
            json={
                'order': 2
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )

        res = self.client().get(f'/tasks')
        data = json.loads(res.data)
        tasks = data['tasks']

        for task in tasks:
            if task['title'].lower() == 'task a':
                self.assertEqual(phase['order'], 1)
            elif task['title'].lower() == 'task d':
                self.assertEqual(phase['order'], 2)
            elif task['title'].lower() == 'task c':
                self.assertEqual(phase['order'], 3)
            else:
                self.assertEqual(phase['order'], 4)

    def test_delete_task(self):
        phase = self.create_phase('Backlog')

        res = self.create_task(phase['id'], 'Task A')
        data = json.loads(res.data)
        id = data['task'].get('id')

        res = self.client().delete(
            f'/tasks/{id}',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['task_deleted'], id)

    def test_404_delete_task_inexistent_id(self):
        res = self.client().delete(
            f'/tasks/10',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_404(self, res.status_code, data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
