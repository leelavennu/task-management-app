from datetime import datetime, timezone
from functools import wraps
from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from sqlalchemy.exc import SQLAlchemyError
from models import db, Task

tasks_bp = Blueprint("tasks", __name__)

class TaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    due_date: str | None = None
    completed: bool = False
    @field_validator("title")
    @classmethod
    def title_required(cls, value):
        value = value.strip()
        if not value: raise ValueError("Title is required")
        return value
    @field_validator("due_date")
    @classmethod
    def valid_due_date(cls, value):
        if value is None or value == "": return None
        try: parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc: raise ValueError("due_date must be ISO-8601") from exc
        if parsed.tzinfo is None: parsed = parsed.replace(tzinfo=timezone.utc)
        if parsed < datetime.now(timezone.utc): raise ValueError("due_date cannot be in the past")
        return value

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("Authorization") != "Bearer test-token": return jsonify(error="Unauthorized", message="A valid Bearer token is required"), 401
        return fn(*args, **kwargs)
    return wrapper

def payload_or_400():
    if not request.is_json: return None, (jsonify(error="Bad request", message="JSON body required"), 400)
    try: return TaskPayload.model_validate(request.get_json()), None
    except (ValidationError, TypeError): return None, (jsonify(error="Bad request", message="Invalid task data"), 400)

@tasks_bp.get("/tasks")
@auth_required
def list_tasks():
    completed = request.args.get("completed")
    if completed is not None and completed not in ("true", "false"): return jsonify(error="Bad request", message="completed must be true or false"), 400
    query = Task.query
    if completed is not None: query = query.filter_by(completed=completed == "true")
    return jsonify([t.to_dict() for t in query.order_by(Task.completed.asc(), Task.due_date.asc().nullslast(), Task.created_at.desc()).all()])

@tasks_bp.post("/tasks")
@auth_required
def create_task():
    payload, error = payload_or_400()
    if error: return error
    task = Task(title=payload.title, description=payload.description, completed=payload.completed, due_date=datetime.fromisoformat(payload.due_date.replace("Z", "+00:00")) if payload.due_date else None)
    db.session.add(task); db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.get("/tasks/<int:task_id>")
@auth_required
def get_task(task_id):
    task = db.session.get(Task, task_id)
    return jsonify(task.to_dict()) if task else (jsonify(error="Not found", message="Task not found"), 404)

@tasks_bp.put("/tasks/<int:task_id>")
@auth_required
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task: return jsonify(error="Not found", message="Task not found"), 404
    payload, error = payload_or_400()
    if error: return error
    task.title, task.description, task.completed = payload.title, payload.description, payload.completed
    task.due_date = datetime.fromisoformat(payload.due_date.replace("Z", "+00:00")) if payload.due_date else None
    db.session.commit()
    return jsonify(task.to_dict())

@tasks_bp.delete("/tasks/<int:task_id>")
@auth_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task: return jsonify(error="Not found", message="Task not found"), 404
    db.session.delete(task); db.session.commit()
    return "", 204
