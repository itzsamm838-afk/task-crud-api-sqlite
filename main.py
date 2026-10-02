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
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }
        for row in rows
    ]


@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns a single task by its ID."
)
def get_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task with a title."
)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": False
    }


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and/or completion status of a task."
)
def update_task(task_id: int, task: TaskUpdate):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    current_title = row[1]
    current_done = bool(row[2])

    new_title = task.title if task.title is not None else current_title
    new_done = task.done if task.done is not None else current_done

    if not new_title.strip():
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (new_title, new_done, task_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": new_title,
        "done": new_done
    }


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    )

    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return None
