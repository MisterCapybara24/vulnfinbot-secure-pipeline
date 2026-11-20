import pytest
from app import create_app
from app.ai import ModelUnavailable


@pytest.fixture
def client():
    return create_app({"TESTING": True, "AI_BACKEND": "mock"}).test_client()


def test_health(client):
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json == {"status": "healthy"}


def test_chat(client):
    result = client.post("/api/chat", json={"message": "How do I budget?"})
    assert result.status_code == 200
    assert result.json["response"]
    assert result.json["backend"] == "mock"


@pytest.mark.parametrize("payload", [{}, {"message": ""}, {"message": "  "}, {"message": "x" * 2001}, {"message": None}, {"message": 5}, {"message": []}, [], None])
def test_invalid_payload(client, payload):
    result = client.post("/api/chat", data=__import__("json").dumps(payload), content_type="application/json")
    assert result.status_code == 400
    assert "error" in result.json


def test_invalid_json(client):
    assert client.post("/api/chat", data='{"message":', content_type="application/json").status_code == 400


def test_content_type(client):
    assert client.post("/api/chat", data="hello").status_code == 415


def test_size_limit(client):
    assert client.post("/api/chat", data="x" * 20000, content_type="application/json").status_code == 413


def test_exact_limit(client):
    assert client.post("/api/chat", json={"message": "x" * 2000}).status_code == 200


def test_headers_and_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert b"Mini-VulnFinBot" in response.data


def test_unavailable_has_no_silent_mock(client, monkeypatch):
    def fail(*args):
        raise ModelUnavailable("private backend details")
    monkeypatch.setattr("app.routes.call_model", fail)
    result = client.post("/api/chat", json={"message": "Budget"})
    assert result.status_code == 503
    assert b"private backend details" not in result.data


def test_unexpected_error_is_sanitized(client, monkeypatch):
    def fail(*args):
        raise RuntimeError("SECRET_STACK_TRACE")
    monkeypatch.setattr("app.routes.call_model", fail)
    result = client.post("/api/chat", json={"message": "Budget"})
    assert result.status_code == 500
    assert b"SECRET_STACK_TRACE" not in result.data
