from app import settings


def test_root_returns_version(client):
    body = client.get("/").json()
    assert body["app"] == "TaskFlow"
    assert "version" in body and "pod" in body


def test_failure_rate_breaks_requests_but_not_health(client, monkeypatch):
    monkeypatch.setattr(settings, "FAILURE_RATE", 1.0)
    assert client.get("/tasks").status_code == 500
    assert client.get("/health").status_code == 200


def test_no_failure_by_default(client):
    assert all(client.get("/tasks").status_code == 200 for _ in range(20))
