from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing tasks."
)

DATABASE = "tasks.db"


def get_db():
    return sqlite3.connect(DATABASE)


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Test with Swagger", 1)
            ]
        )

    conn.commit()
    conn.close()


init_db()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks currently stored in SQLite."
)
def get_tasks():
    return []


@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns a single task by its ID."
)
def get_task(task_id: int):
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task with a title."
)
def create_task(task: TaskCreate):
    raise HTTPException(
        status_code=501,
        detail="Not implemented in Stage 0"
    )


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and/or completion status of a task."
)
def update_task(task_id: int, task: TaskUpdate):
    raise HTTPException(
        status_code=501,
        detail="Not implemented in Stage 0"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(task_id: int):
    raise HTTPException(
        status_code=501,
        detail="Not implemented in Stage 0"
    )