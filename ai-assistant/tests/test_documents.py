from fastapi.testclient import TestClient

from app.main import app


def test_create_document() -> None:
    client = TestClient(app)

    response = client.post(
        "/documents",
        json={
            "title": "First document",
            "content": "This is my first test document.",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["title"] == "First document"
    assert body["content"] == "This is my first test document."
    assert "id" in body


def test_list_documents() -> None:
    client = TestClient(app)

    client.post(
        "/documents",
        json={
            "title": "List test document",
            "content": "Testing list endpoint.",
        },
    )

    response = client.get("/documents")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_missing_document_returns_404() -> None:
    client = TestClient(app)

    response = client.get("/documents/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404