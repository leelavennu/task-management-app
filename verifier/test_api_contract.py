from datetime import datetime, timedelta, timezone

TOKEN = {"Authorization": "Bearer test-token"}
BAD = {"Authorization": "Bearer wrong-token"}


def test_accepts_valid_create_and_filter(client):
    due = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    created = client.post(
        "/api/tasks",
        json={"title": "Verifier task", "due_date": due},
        headers=TOKEN,
    )
    assert created.status_code == 201
    assert client.get("/api/tasks?completed=false", headers=TOKEN).status_code == 200


def test_rejects_missing_auth(client):
    assert client.get("/api/tasks").status_code == 401


def test_rejects_bad_auth(client):
    assert client.get("/api/tasks", headers=BAD).status_code == 401


def test_rejects_missing_title(client):
    assert client.post("/api/tasks", json={}, headers=TOKEN).status_code == 400


def test_rejects_bad_due_date(client):
    assert client.post(
        "/api/tasks",
        json={"title": "Bad date", "due_date": "yesterday"},
        headers=TOKEN,
    ).status_code == 400


def test_rejects_unknown_id(client):
    assert client.get("/api/tasks/999999", headers=TOKEN).status_code == 404


def test_rejects_invalid_filter(client):
    assert client.get("/api/tasks?completed=maybe", headers=TOKEN).status_code == 400
