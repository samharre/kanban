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
export AUTH0_DOMAIN='<Auth0 application Domain>'
export AUTH0_SECRET='<Auth0 application Client Secret>'
export API_AUDIENCE='<Auth0 API Identifier>'
export APP_SETTINGS='development'
export DATABASE_URL='postgresql://localhost:5432/kanban'
export TEST_DATABASE_URL='postgresql://localhost:5432/kanban_test'
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```
pip3 install -r requirements.txt
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
source .env
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Running the server

From within the `/backend` directory ensure you are working using your created virtual environment, and then execute:

```
export FLASK_APP=run.py;
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

- Base URL: Kanban app can be run using localhost:5000 or https://kanban-backend-fsnd.herokuapp.com

#### Temporary Token - Manager permission

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2NkYTQzNjE0MjAwNzhlZGM4YTMiLCJhdWQiOlsia2FuYmFuIiwiaHR0cHM6Ly9zYW1oYXJyZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjE0NDUyMTI5LCJleHAiOjE2MTQ1Mzg1MjksImF6cCI6InBHb2N5TUk2bFFkTzNWM2dBZWRpVzdrU0lxOFpSRUpqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwaGFzZXMiLCJkZWxldGU6dGFza3MiLCJwYXRjaDpwaGFzZXMiLCJwYXRjaDp0YXNrcyIsInBvc3Q6cGhhc2VzIiwicG9zdDp0YXNrcyJdfQ.4IK-Y5VUc8hMvCwMzXWRGUkSsNu18zrwVVAJDSL1-755Sd8CPApb__0KNMtSO8KLwqUJPJMpTW9PzIxMyjxFclK2oOMnsMF90XVq7oeeyBGzZhbhJ7c-SH66YRir5AMJyMpYMSJJwkWzsKbyZB6KUDc3TI57p0k20dnCqu-zhXO71WSk2vg4SL965k_n2cysoGkdwjo8uMeI5zxsprng4YyoVn2knUyWZejuMCpi-VguT-p3en0fVUzKafpDKCTTOVJj9aISArsd-RY765CLhNAQsNVN5IKW8Oizh5wSgMeCtnxiEl4-ptif2uI9z8JMbKf3Obhwp3vGfaCUs3n_fQ
```

#### Temporary Token - Team permission

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtaGF5UUdIODhfbnF0Ql9jMFVPbyJ9.eyJpc3MiOiJodHRwczovL3NhbWhhcnJlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhiN2Q2NzUzZDM0NzAwNmU5MTVmMTUiLCJhdWQiOlsia2FuYmFuIiwiaHR0cHM6Ly9zYW1oYXJyZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjE0NDUyMTc4LCJleHAiOjE2MTQ1Mzg1NzgsImF6cCI6InBHb2N5TUk2bFFkTzNWM2dBZWRpVzdrU0lxOFpSRUpqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0YXNrcyIsInBhdGNoOnRhc2tzIiwicG9zdDp0YXNrcyJdfQ.oFxg77g1AUlFfZUXQj58X1fftvb29GIRJ3GWkPOnUnMbcgg5R5T-pe7ONHaSX_CJJPR8YuUdC1AqBVGpDmvvmGWRSkXhlBhK3g_ByNOul6CJkSTeEWKaShkmCyD8hFcl3UnAcmDtaD-MQ0dgjsIWR-okaeXZSXNullJByVehxUSakVolgm2AaOOcEs6HSyfXdAYaMSUPWrc8r-LakiGOhKJ0DmuhswmerPmDFba-qsDzPJzFAxGTi0S_kSjbEXA_lBPARKkYiMfCgFAhIl2Zp11sKaExtWrkRJYZ0rZ3lUH-gsRhB39FnX5qNp3S2QSQxsJsQGH0XfPK64M7oykaKg
```

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
- Sample: `curl https://kanban-backend-fsnd.herokuapp.com/phases`

```
{
  "phases": [
    {
      "can_create_task":true,
      "id":27,
      "order":1,
      "title":"To Do"
    },
    {
      "can_create_task":true,
      "id":28,
      "order":2,
      "title":"Doing"
    },
    {
      "can_create_task":false,
      "id":31,
      "order":3,
      "title":"Done"}
    ],
  "success":true
}
```

#### GET /phases/{phase_id}

- General:
  - Fetches the phase for the especific phase id.
  - Request Arguments: `phase_id: int`
  - Returns: A dictionary containing success value, and the phase.
- Sample: `curl https://kanban-backend-fsnd.herokuapp.com/phases/27`

```
{
  "phase":
    {
      "can_create_task": true,
      "id": 27,
      "order": 1,
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
- Sample: `curl https://kanban-backend-fsnd.herokuapp.com/phases-detail`

```
{
  "phases": [
    {
      "can_create_task":true,
      "id":27,
      "order":1,
      "tasks": [
        {
          "description":null,
          "due_date":null,
          "id":36,
          "order":1,
          "phase_id":27,
          "title":"Task 2",
          "user_id":"auth0|5f8b7cda4361420078edc8a3"
        }
      ],
      "title":"To Do"
    },
    {
      "can_create_task":true,
      "id":28,
      "order":2,
      "tasks": [
        {
          "description":null,
          "due_date":"Mon, 22 Feb 2021 00:00:00 GMT",
          "id":35,
          "order":1,
          "phase_id":28,
          "title":"Task 1",
          "user_id":"auth0|5f8b7cda4361420078edc8a3"
        }
      ],
      "title":"Doing"
    },
    {
      "can_create_task":false,
      "id":31,
      "order":3,
      "tasks":[],
      "title":"Done"
    }
  ],
  "success":true
}
```

#### GET /phases-detail/{phase_id}

- General:
  - Fetches the phase for the especific phase id and its tasks.
  - Request Arguments: `phase_id: int`
  - Returns: A dictionary containing success value, the phase and its tasks.
- Sample: `curl https://kanban-backend-fsnd.herokuapp.com/phases-detail/27`

```
{
  "phase":
  {
    "can_create_task":true,
    "id":27,
    "order":1,
    "tasks": [
      {
        "description":null,
        "due_date":null,
        "id":36,
        "order":1,
        "phase_id":27,
        "title":"Task 2",
        "user_id":"auth0|5f8b7cda4361420078edc8a3"
      }
    ],
    "title":"To Do"
  },
  "success":true
}
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
  "phase":
  {
    "can_create_task":false,
    "id":32,
    "order":4,
    "title":
    "Code Review"
  },
  "success":true
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
    https://kanban-backend-fsnd.herokuapp.com/phases/32 \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "title": "Code Review - TEST EDIT"
  }'
```

```
{
  "phase":
  {
    "can_create_task":false,
    "id":32,
    "order":4,
    "title":"Code Review - TEST"
  },
  "phases":[
    {
      "can_create_task":true,
      "id":27,
      "order":1,
      "title":"To Do"
    },
    {
      "can_create_task":true,
      "id":28,
      "order":2,
      "title":"Doing"
    },
    {
      "can_create_task":false,
      "id":31,
      "order":3,
      "title":"Done"
    },
    {
      "can_create_task":false,
      "id":32,
      "order":4,
      "title":"Code Review - TEST"
    }
  ],
  "success":true
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
  https://kanban-backend-fsnd.herokuapp.com/phases/32 \
  -H 'Authorization: Bearer <TOKEN> '
```

```
{
  "phase_deleted": 32,
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
  "success":true,
  "tasks":[
    {
      "description":null,
      "due_date":null,
      "id":36,
      "order":1,
      "phase_id":27,
      "title":"Task 2",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    },
    {
      "description":null,
      "due_date":"Mon, 22 Feb 2021 00:00:00 GMT",
      "id":35,
      "order":1,
      "phase_id":28,
      "title":"Task 1",
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
  https://kanban-backend-fsnd.herokuapp.com/phases/27/tasks \
  -H 'Authorization: Bearer <TOKEN>'
```

```
{
  "success":true,
  "tasks":[
    {
      "description":null,
      "due_date":null,
      "id":36,
      "order":1,
      "phase_id":27,
      "title":"Task 2",
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
      "phase_id": 27,
      "title": "Test task 1 - phase 27"
  }'
```

```
{
  "success":true,
  "task":
  {
    "description":null,
    "due_date":null,
    "id":38,
    "order":2,
    "phase_id":27,
    "title":
    "Test task 1 - phase 27",
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
    https://kanban-backend-fsnd.herokuapp.com/tasks/38 \
    -H 'Authorization: Bearer <TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "title": "Test task 1 - phase 1 ***",
      "order": 1
  }'
```

```
{
  "success":true,
  "task":
  {
    "description":null,
    "due_date":null,
    "id":38,
    "order":1,
    "phase_id":27,
    "title":"Test task 1 - phase 1 ***",
    "user_id":"auth0|5f8b7cda4361420078edc8a3"
  },
  "tasks":[
    {
      "description":null,
      "due_date":null,
      "id":38,
      "order":1,
      "phase_id":27,
      "title":"Test task 1 - phase 1 ***",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    },
    {
      "description":null,
      "due_date":null,
      "id":36,
      "order":2,
      "phase_id":27,
      "title":"Task 2",
      "user_id":"auth0|5f8b7cda4361420078edc8a3"
    },
    {
      "description":null,
      "due_date":"Mon, 22 Feb 2021 00:00:00 GMT",
      "id":35,
      "order":1,
      "phase_id":28,
      "title":"Task 1",
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
  https://kanban-backend-fsnd.herokuapp.com/tasks/38 \
  -H 'Authorization: Bearer <TOKEN> '
```

```
{
  "success": true,
  "task_deleted": 38
}
```

## Testing

```
dropdb kanban_test
createdb kanban_test
```

To execute tests, on your virtual enviroment run

```
python3 -m unittest tests/test_phase.py
python3 -m unittest tests/test_task.py
```
