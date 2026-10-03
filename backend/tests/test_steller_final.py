def test_missing_title_post_400(client):
    assert client.post("/api/tasks", json={"description": "no title"}, headers={"Authorization": "Bearer test-token"}).status_code == 400
def test_invalid_due_date_post_400(client):
    assert client.post("/api/tasks", json={"title": "t", "due_date": "invalid"}, headers={"Authorization": "Bearer test-token"}).status_code == 400
def test_invalid_token_401(client):
    assert client.get("/api/tasks", headers={"Authorization": "Bearer wrong-token"}).status_code == 401
def test_filter_completed(client):
    h = {"Authorization": "Bearer test-token"}
    assert client.get("/api/tasks?completed=true", headers=h).status_code == 200
    assert client.get("/api/tasks?completed=false", headers=h).status_code == 200
def test_special_chars_safe(client):
    assert client.post("/api/tasks", json={"title": "<script>😀"}, headers={"Authorization": "Bearer test-token"}).status_code in [200,201]
