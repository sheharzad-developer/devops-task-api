
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from app.database import get_connection, init_db
from app.schemas import TaskCreate, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    lifespan=lifespan,
)


def row_to_dict(row):
    return dict(row)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Task Management API - CI/CD"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "task-api",
        "version": "1.0.0",
    }


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
        """,
        (task.title, task.description, task.status),
    )

    connection.commit()

    task_id = cursor.lastrowid

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


@app.get("/tasks")
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    return [row_to_dict(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return row_to_dict(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    updates = task.model_dump(exclude_unset=True)

    if not updates:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    set_clause = ", ".join(
        f"{field} = ?" for field in updates
    )

    values = list(updates.values())
    values.append(task_id)

    connection.execute(
        f"UPDATE tasks SET {set_clause} WHERE id = ?",
        values,
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(updated_task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task deleted successfully",
        "task_id": task_id,
    }