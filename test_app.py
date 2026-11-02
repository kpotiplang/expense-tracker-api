import os

# Use a throwaway in-memory database so tests never touch expenses.db.
# This must be set before app.py is imported.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client


def create_rent(client):
    return client.post("/expenses", json={"title": "Rent", "amount": 1200, "category": "Housing"})


def test_list_is_empty_at_start(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_expense(client):
    response = create_rent(client)
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 1
    assert body["title"] == "Rent"
    assert body["amount"] == 1200


def test_get_single_expense(client):
    create_rent(client)
    response = client.get("/expenses/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Rent"


def test_get_missing_expense_returns_404(client):
    response = client.get("/expenses/999")
    assert response.status_code == 404


@pytest.mark.parametrize("payload", [
    {"amount": 50},                       # missing title
    {"title": "Coffee"},                  # missing amount
    {"title": "", "amount": 5},           # empty title
    {"title": "Coffee", "amount": "5"},   # amount is a string
    {"title": "Coffee", "amount": -5},    # negative amount
])
def test_create_rejects_invalid_input(client, payload):
    response = client.post("/expenses", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_rejects_non_json_body(client):
    response = client.post("/expenses", data="not json", content_type="text/plain")
    assert response.status_code == 400


def test_update_expense(client):
    create_rent(client)
    response = client.put("/expenses/1", json={"amount": 1300})
    assert response.status_code == 200
    body = response.get_json()
    assert body["amount"] == 1300
    assert body["title"] == "Rent"  # unchanged fields are kept


def test_update_rejects_invalid_amount(client):
    create_rent(client)
    response = client.put("/expenses/1", json={"amount": 0})
    assert response.status_code == 400


def test_delete_expense(client):
    create_rent(client)
    assert client.delete("/expenses/1").status_code == 200
    assert client.get("/expenses/1").status_code == 404
