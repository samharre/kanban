import os
import unittest
import json

from src import create_app
from src.models.base import db
from src.models.phase import Phase

from . import check_status_code_400, check_status_code_404, check_status_code_405, check_status_code_409, check_status_code_422

MANAGER_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2NkYTQzNjE0MjAwNzhlZGM4YTMiLCJhdWQiOlsia2FuYmFuIiwiaHR0cHM6Ly9zYW1oYXJyZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjEyNDg5NDE5LCJleHAiOjE2MTI1NzU4MTksImF6cCI6InBHb2N5TUk2bFFkTzNWM2dBZWRpVzdrU0lxOFpSRUpqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwaGFzZXMiLCJkZWxldGU6dGFza3MiLCJwYXRjaDpwaGFzZXMiLCJwYXRjaDp0YXNrcyIsInBvc3Q6cGhhc2VzIiwicG9zdDp0YXNrcyJdfQ.F9PlVY0UB0qjIYlRtNekxm5K-TqRjka3WEXqbXmszsajgi0ktwre76AN0RCkhT1iFdSxbP1mPTjpf5plbUNt-5m2h0_7MFizqGL3RIQ2RM3bbIk7LAgtAwCCaZWZhlMqXTH5__1IKzw0FlFms7bF03kiFFDH_aecWoR6UwirZ2clO0nOjVjFJCxdXMhhxGmCWF2ZSWc8AXjSPCRDFecudqVAYmhME6gmlysqqRBgssCwKB74U9r_Yu7fgRdPdwEdxAj0xwYk9w2mqNt2dXj6LfaxqL4Dg0uoGqwjLlWKRVRuQCDXKI7zivCLZjEXI_wMxB4buBdvuzAUdFn52aH1BQ'


class PhaseTestCase(unittest.TestCase):
    '''This class represents the phase api test case'''

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

    def test_400_create_phase_without_body(self):
        res = self.client().post(
            '/phases',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_400(self, res.status_code, data)

    def test_422_create_phase_without_title(self):
        res = self.client().post(
            '/phases',
            json={
                'title': ''
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_422(self, res.status_code, data)

    def test_409_create_new_phase_duplicated_title(self):
        res = self.create_phase('Backlog')
        res = self.create_phase('Backlog')
        data = json.loads(res.data)

        check_status_code_409(self, res.status_code, data)

    def test_405_create_new_phase_passing_id(self):
        res = self.client().post(
            '/phases/1',
            json={
                'title': 'To Do'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)

        check_status_code_405(self, res.status_code, data)

    def test_update_phase(self):
        res = self.create_phase('Backlog')
        data = json.loads(res.data)

        id = data['phase'].get('id')
        res = self.client().patch(
            f'/phases/{id}',
            json={
                'title': 'Backlog - Test'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['phase'].get('title'), 'Backlog - Test')

        res = self.client().get(f'/phases/{id}')
        data = json.loads(res.data)
        self.assertEqual(data['phase'].get('title'), 'Backlog - Test')

    def test_404_update_phase_inexistent_id(self):
        res = self.create_phase('Backlog')
        data = json.loads(res.data)

        id = data['phase'].get('id') + 1
        res = self.client().patch(
            f'/phases/{id}',
            json={
                'title': 'Trying'
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_404(self, res.status_code, data)

    def test_400_update_phase_without_body(self):
        res = self.create_phase('Backlog')
        data = json.loads(res.data)

        id = data['phase'].get('id')
        res = self.client().patch(
            f'/phases/{id}',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_400(self, res.status_code, data)

    def test_422_update_phase_without_title_and_order(self):
        res = self.create_phase('Backlog')
        data = json.loads(res.data)

        id = data['phase'].get('id')
        res = self.client().patch(
            f'/phases/{id}',
            json={
                'title': '',
                'order': ''
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_422(self, res.status_code, data)

    def test_409_update_phase_duplicating(self):
        self.create_phase('Backlog')
        res = self.create_phase('To Do')

        data = json.loads(res.data)
        id = data['phase'].get('id')

        res = self.client().patch(
            f'/phases/{id}',
            json={
                'title': 'Backlog',
                'order': 2
            },
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_409(self, res.status_code, data)

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
                'order': 2
            },
            headers={
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
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['phase_deleted'], id)

        res = self.client().get(f'/phases/{id}')
        data = json.loads(res.data)
        check_status_code_404(self, res.status_code, data)

    def test_404_delete_phase_inexistent_id(self):
        res = self.create_phase('Backlog')
        data = json.loads(res.data)
        id = data['phase'].get('id') + 1

        res = self.client().delete(
            f'/phases/{id}',
            headers={
                'Authorization': MANAGER_TOKEN
            }
        )
        data = json.loads(res.data)
        check_status_code_404(self, res.status_code, data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
