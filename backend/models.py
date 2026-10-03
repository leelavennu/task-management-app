from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    due_date = db.Column(db.DateTime(timezone=True), nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "due_date": self.due_date.isoformat() if self.due_date else None, "completed": self.completed, "created_at": self.created_at.isoformat(), "updated_at": self.updated_at.isoformat()}
