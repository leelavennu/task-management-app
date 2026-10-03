import os, sys
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app
from models import db

TOKEN={"Authorization":"Bearer test-token"}
def setup_function():
    global app, client
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///:memory:"})
    client=app.test_client()

def test_auth_required():
    assert client.get('/api/tasks').status_code == 401

def test_crud_and_validation():
    due=(datetime.now(timezone.utc)+timedelta(days=2)).isoformat()
    response=client.post('/api/tasks',json={"title":"Plan release","description":"Ship v1","due_date":due},headers=TOKEN)
    assert response.status_code==201
    task=response.get_json(); assert task["completed"] is False
    assert client.get('/api/tasks/999999',headers=TOKEN).status_code==404
    assert client.put(f'/api/tasks/{task["id"]}',json={"title":"", "due_date":due},headers=TOKEN).status_code==400
    assert client.put(f'/api/tasks/{task["id"]}',json={"title":"Done", "due_date":"yesterday"},headers=TOKEN).status_code==400
    assert client.delete(f'/api/tasks/{task["id"]}',headers=TOKEN).status_code==204

def test_malformed_json_and_query():
    assert client.post('/api/tasks',data='not-json',content_type='application/json',headers=TOKEN).status_code==400
    assert client.get('/api/tasks?completed=maybe',headers=TOKEN).status_code==400
    assert client.get('/api/tasks',headers=TOKEN).json==[]
