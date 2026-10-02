# Task CRUD API — SQLite

A simple REST API built with Python and FastAPI for managing a to-do list, using SQLite for persistent storage.

The API supports the four main CRUD operations:

- Create tasks
- Read tasks
- Update tasks
- Delete tasks

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Swagger UI / OpenAPI

## Features

- REST API endpoints
- SQLite database for persistent storage
- Automatic database and table creation
- Example tasks inserted only when the database is empty
- Request validation
- Proper HTTP status codes
- 404 handling for missing tasks
- Interactive Swagger UI documentation

## Storage

Tasks are stored in a SQLite database named `tasks.db`.

The database is automatically created when the application starts. The `tasks` table is also created automatically if it does not already exist.

Three example tasks are inserted only when the database is empty.

Unlike the previous in-memory version, task data persists when the server is restarted.

## Installation

Clone the repository:

```bash
git clone https://github.com/itzsamm838-afk/task-crud-api-sqlite.git
cd task-crud-api-sqlite
