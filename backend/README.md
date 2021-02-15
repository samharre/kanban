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
