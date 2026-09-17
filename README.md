
# Task Management API

A containerized REST API built with FastAPI, SQLite, and Docker.

This project is being developed as a practical Cloud/DevOps assignment.

## Features

- Health check endpoint
- Create tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update tasks
- Delete tasks
- SQLite database
- Docker containerization

## Technology Stack

- Python 3.12
- FastAPI
- Pydantic
- SQLite
- Docker

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

## Run with Docker

Build the image:

```bash
docker build -t task-api:1.0 .
```

Run the container:

```bash
docker run --name task-api-container -p 8000:8000 task-api:1.0
```

Open:

http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Get one task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |