[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/3DHX45S9)
# API

Small FastAPI service for managing users.

## Features

- Create users (stores hashed password)
- List users

## Endpoints

- POST /users
  - Request body: UserCreate { "username", "name", "role", "password" }
  - Response: UserPublic { "id", "username", "name", "role" }
  - Implementation: [`routers.user.create_user`](api/routers/user.py)
- GET /users
  - Response: list of UserPublic
  - Implementation: [`routers.user.get_users`](api/routers/user.py)

## Database

- Dev: SQLite file `database.db` (see [api/db/db.py](api/db/db.py))
- Prod: set environment variables `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` and `PROD=true`
- DB initialization is performed by [`db.db.create_db_and_tables`](api/db/db.py) at app startup.

## Local development

1. Sync dependencies

```sh
uv sync
```

2. Run app:

```sh
uv run fastapi run
```

3. Access the API docs at `http://localhost:8000/docs`


# Files and submission

- Place your `Dockerfile` on this directory.
- Place your `docker-compose.yml` on this directory.
- Place your report for 4.3 on this directory.
- Place your report for 4.4 on this directory.