# Kanban Backend

## Getting Started

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `post:phases`
   - `patch:phases`
   - `delete:phases`
   - `post:tasks`
   - `patch:tasks`
   - `delete:tasks`
6. Create new roles for:
   - Team
     - can `"post:tasks", "patch:tasks" and "delete:tasks"`
   - Manager
     - can perform all actions

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Create the virtual enviroment by naviging to the `/backend` directory and running:

```
python3 -m venv env
source env/bin/activate
touch .env
```

**Open the `.env` file and configure the enviroment variables**

```
AUTH0_DOMAIN = <the Auth0 application Domain>
AUTH0_SECRET = <the Auth0 application Client Secret>
API_AUDIENCE = <the Auth0 API Identifier>
APP_SETTINGS = 'development'
DATABASE_URL = 'postgresql://localhost:5432/kanban'
TEST_DATABASE_URL = 'postgresql://localhost:5432/kanban_test'
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

## Database Setup

With Postgres running, create database:

```
createdb kanban
```

### Run migrations

From within the `/backend` directory ensure you are working using your created virtual environment, and then execute:

```
python3 manage.py db init
python3 manage.py db migrate
```

## Running the server

From within the `/backend` directory ensure you are working using your created virtual environment, and then execute:

```
export FLASK_APP=run.py;
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

- Base URL: Kanban app can be run using http://127.0.0.1:5000 (locally) or https://kanban-backend-fsnd.herokuapp.com.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": false,
    "error": 400,
    "message": "Bad request"
}
```

The API will return five error types when requests fail:

- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 409: Duplicated found
- 422: Unprocessable
- 500: Internal server error

### Endpoints

#### GET /phases

- General:
  - Fetches a list of phases
  - Request Arguments: None
  - Returns: A dictionary containing success value, and a list with all phases.
- Sample: `curl http://127.0.0.1:5000/phases` or `curl https://kanban-backend-fsnd.herokuapp.com/phases`

```
{
  "phases": [
    {
      "can_create_task": true,
      "id": 4,
      "order": 1,
      "title": "Backlog"
    },
    {
      "can_create_task": true,
      "id": 1,
      "order": 2,
      "title": "To Do"
    }
  ],
  "success": true
}
```

#### GET /phases/{phase_id}

- General:
  - Fetches the phase for the especific phase id.
  - Request Arguments: `phase_id: int`
  - Returns: A dictionary containing success value, and the phase.
- Sample: `curl http://127.0.0.1:5000/phases/1` or `curl https://kanban-backend-fsnd.herokuapp.com/phases/1`

```
{
  "phase":
    {
      "can_create_task": true,
      "id": 1,
      "order": 2,
      "title": "To Do"
    },
  "success":true
}
```

#### GET /phases-detail

- General:
  - Fetches a list of phases and its tasks.
  - Request Arguments: None
  - Returns: A dictionary containing success value, and a list with all phases and its tasks.
- Sample: `curl http://127.0.0.1:5000/phases-detail` or `curl https://kanban-backend-fsnd.herokuapp.com/phases-detail`

```
{
  "phases": [
    {
      "can_create_task": true,
      "id": 4,
      "order": 1,
      "tasks": [
        {
          "description": null,
          "due_date": null,
          "id": 2,
          "order": 1,
          "phase_id": 4,
          "title": "Back 1",
          "user_id":"auth0|5f8b7cda4361420078edc8a3"
        },
        {
          "description": null,
          "due_date": "Thu, 18 Feb 2021 00:00:00 GMT",
          "id": 3,
          "order": 3,
          "phase_id": 4,
          "title": "Back 2 **** ",
          "user_id": "auth0|5f8b7cda4361420078edc8a3"
        }
      ],
      "title": "Backlog"
    },
    {
      "can_create_task": true,
      "id": 1,
      "order": 2,
      "tasks": [
        {
          "description": null,
          "due_date": null,
          "id": 4,
          "order": 1,
          "phase_id": 1,
          "priority": "#ff0000",
          "title": "Back 3",
          "user_id": "auth0|5f8b7cda4361420078edc8a3"
        }
      ],
      "title": "To Do"
    }
  ],
  "success": true
}
```

#### GET /phases-detail/{phase_id}

- General:
  - Fetches the phase for the especific phase id and its tasks.
  - Request Arguments: `phase_id: int`
  - Returns: A dictionary containing success value, the phase and its tasks.
- Sample: `curl http://127.0.0.1:5000/phases-detail/1` or `curl https://kanban-backend-fsnd.herokuapp.com/phases-detail/1`

```
{
  "phase": {
    "can_create_task": true,
    "id": 1,
    "order": 2,
    "tasks": [
      {
        "description": null,
        "due_date": null,
        "id": 4,
        "order": 1,
        "phase_id": 1,
        "title": "Back 3",
        "user_id": "auth0|5f8b7cda4361420078edc8a3"
      }
    ],
    "title": "To Do"
  },
  "success": true}
```

#### POST /phases

- General:
  - Creates a new phase using the submitted title, and indication whether the phase can create a new task or not.
  - Request body:
  ```
    {
        "title": string,
        "can_create_task": boolean
    }
  ```
  - Returns: A dictionary containing success value, and phase.
- Sample:

```
  curl -X POST \
    https://kanban-backend-fsnd.herokuapp.com/phases \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "title": "Code Review",
      "can_create_task": false
  }'
```

```
{
  "phase": {
    "can_create_task": false,
    "id": 6,
    "order": 5,
    "title": "Code Review"
  },
  "success": true
}
```

#### PATCH /phases/{phase_id}

- General:
  - Updates the phase using the submitted title, order, or indication whether the phase can create a new task or not.
  - Request Arguments: `phase_id: int`
  - Request body: Inform "title", "can_create_task", or "order"
  - Returns: A dictionary containing success value, the updated phase, and all phases.
- Sample:

```
  curl -X PATCH \
    https://kanban-backend-fsnd.herokuapp.com/phases/6 \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "can_create_task": true
  }'
```

```
{
  "phase": {
    "can_create_task": false,
    "id": 6,
    "order": 5,
    "title": "Code Review ***"
  },
  "phases": [
    {
      "can_create_task": true,
      "id": 4,
      "order": 1,
      "title": "Backlog"
    },
    {
      "can_create_task": false,
      "id": 6,
      "order": 5,
      "title": "Code Review ***"
    }
  ],
  "success": true
}
```

#### DELETE /phases/{phase_id}

- General:
  - Delete the phase of the given id if it exists.
  - Request Arguments: `phase_id: int`
  - Returns: Phase id that was deleted and success value.
- Sample:

```
curl -X DELETE \
  https://kanban-backend-fsnd.herokuapp.com/phases/6 \
  -H 'Authorization: Bearer <TOKEN> '
```

```
{
  "phase_deleted": 6,
  "success": true
}
```

#### GET /tasks

- General:
  - Fetches a list of tasks
  - Request Arguments: None
  - Returns: A dictionary containing success value, and a list with all tasks created for an especific user.
- Sample:

```
curl -X GET \
  https://kanban-backend-fsnd.herokuapp.com/tasks \
  -H 'Authorization: Bearer <TOKEN>'
```

```
{
  "success": true,
  "tasks": [
    {
      "description": null,
      "due_date": null,
      "id": 4,
      "order": 1,
      "phase_id": 1,
      "title": "Back 3",
      "user_id": "auth0|5f8b7cda4361420078edc8a3"
    },
    {
      "description": null,
      "due_date": null,
      "id": 1,
      "order": 1,
      "phase_id": 2,
      "title": "Test to do",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    }
  ]
}
```

#### GET /phases/{phase_id}/tasks

- General:
  - Fetches tasks for an especific phase.
  - Request Arguments: `phase_id: int`
  - Returns: A dictionary containing success value, and tasks.
- Sample:

```
curl -X GET \
  https://kanban-backend-fsnd.herokuapp.com/phases/1/tasks \
  -H 'Authorization: Bearer <TOKEN>'
```

```
{
  "success": true,
  "tasks": [
    {
      "description": null,
      "due_date": null,
      "id": 4,
      "order": 1,
      "phase_id": 1,
      "title": "Back 3",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    }
  ]
}
```

#### POST /tasks

- General:
  - Creates a new task using the submitted phase id, title, description, and due date. Description and due date are not requested data.
  - Request body:
  ```
    {
        "phase_id": int,
        "title": string
    }
  ```
  - Returns: A dictionary containing success value, and task.
- Sample:

```
  curl -X POST \
    https://kanban-backend-fsnd.herokuapp.com/tasks \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "phase_id": 1,
      "title": "Test task 1 - phase 1"
  }'
```

```
{
  "success": true,
  "task": {
    "description": null,
    "due_date": null,
    "id": 15,
    "order": 2,
    "phase_id": 1,
    "title": "Test task 1 - phase 1",
    "user_id":"auth0|5f8b7cda4361420078edc8a3"
  }
}
```

#### PATCH /tasks/{task_id}

- General:
  - Updates the task using the submitted phase id, title, description, order, or due date.
  - Request Arguments: `task_id: int`
  - Request body: Inform "phase_id", "title", "description", "order", or "due_date".
  - Returns: A dictionary containing success value, the updated task, and all tasks for the especific user.
- Sample:

```
  curl -X PATCH \
    https://kanban-backend-fsnd.herokuapp.com/tasks/15 \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "title": "Test task 1 - phase 1 ***",
      "order": 1
  }'
```

```
{
  "success": true,
  "task": {
    "description": null,
    "due_date": null,
    "id": 15,
    "order": 1,
    "phase_id": 1,
    "title": "Test task 1 - phase 1 ***",
    "user_id": "auth0|5f8b7cda4361420078edc8a3"
  },
  "tasks":[
    {
      "description": null,
      "due_date": null,
      "id": 15,
      "order": 1,
      "phase_id": 1,
      "title": "Test task 1 - phase 1 ***",
      "user_id": "auth0|5f8b7cda4361420078edc8a3"
    },
    {
      "description": null,
      "due_date": null,
      "id": 4,
      "order": 2,
      "phase_id": 1,
      "title": "Back 3",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    }
  ]
}
```

#### DELETE /tasks/{task_id}

- General:
  - Delete the task of the given id if it exists.
  - Request Arguments: `task_id: int`
  - Returns: Task id that was deleted and success value.
- Sample:

```
curl -X DELETE \
  https://kanban-backend-fsnd.herokuapp.com/tasks/15 \
  -H 'Authorization: Bearer <TOKEN> '
```

```
{
  "success": true,
  "task_deleted": 15
}
```

#### Temporary Token - Manager permission

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2NkYTQzNjE0MjAwNzhlZGM4YTMiLCJhdWQiOlsia2FuYmFuIiwiaHR0cHM6Ly9zYW1oYXJyZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjEzNDMxMjYxLCJleHAiOjE2MTM1MTc2NjEsImF6cCI6InBHb2N5TUk2bFFkTzNWM2dBZWRpVzdrU0lxOFpSRUpqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwaGFzZXMiLCJkZWxldGU6dGFza3MiLCJwYXRjaDpwaGFzZXMiLCJwYXRjaDp0YXNrcyIsInBvc3Q6cGhhc2VzIiwicG9zdDp0YXNrcyJdfQ.FC_5NNIKFvVTPfPRLypDO83XueN1d9OqfoS-_RlhyFu7jXVryLlnPQkI9GBTTCfZ6pyJi5wS61X0HAIDtnlyuz5cKKCUFo_P0SEG4Z81TVLd1RKkjwUCmHADttz3QhAHsU1Jjnb2MkaSyjUIpydv_eQGUJ1oO7uI-wbCbwOKe0Qs6HWLxYhuNjmd8iYz3deup13d-HhQvb35TVPyJvKX9gKmyzYeaYdmcV2fPqygM0YKV3vYdFntiSvSgU2PR8GF98MEoSVnsmZmUJ6yjb-8bRKr2F7TvFjtCnttrEPSYqOgNXxIvsK2cTjBsEqzK4t07N9Kf2-hmKigYNmNJ7HZEw
```

#### Temporary Token - Team permission

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2Q2NzUzZDM0NzAwNmU5MTVmMTUiLCJhdWQiOlsia2FuYmFuIiwiaHR0cHM6Ly9zYW1oYXJyZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjEzNDM2OTM3LCJleHAiOjE2MTM1MjMzMzcsImF6cCI6InBHb2N5TUk2bFFkTzNWM2dBZWRpVzdrU0lxOFpSRUpqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0YXNrcyIsInBhdGNoOnRhc2tzIiwicG9zdDp0YXNrcyJdfQ.KllDIgy8EedLZIUzJSeXVmA4fTpVy_vQmrCzoPE0oSiTSUlLtl1D5s5Zm16Si-xAb3Uqk0YH2kT68N8jxE3blBE7AzX6P1rHNQWC92Qwko2RBUxfVBYaedanm90-eIGT5TWFBZ0-g7JOFSNYxp2ZHh2wcLLi1TP1bT_XMNkOr-ocTixRDkwzbnvd12kDu2yJIjnSdjTXIXdti9hcFHLHc7Vhvwp9097hY-XN6knJHUVOSj94MTln22RUKEEdxrDWeMmzQImxbINPatv_gxViIy_Fdz6Dnv1alNOiYfJc5B7lL6HX_xRDZpB0E5HEELJQpVnW5g2F14i1lVpAZWrLaQ
```

## Testing

```
dropdb kanban_test
createdb kanban_test
```

To execute tests, in your virtual enviroment run

```
python3 -m unittest tests/test_phase.py
python3 -m unittest tests/test_task.py
```
