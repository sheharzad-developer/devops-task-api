import os
import sqlite3
from pathlib import Path


DATABASE_PATH = os.getenv("DATABASE_PATH", "tasks.db")


def get_connection():
    database_file = Path(DATABASE_PATH)

    database_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(database_file)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
        """
    )

    connection.commit()
    connection.close()