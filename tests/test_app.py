import json
import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_summary_endpoint(client):
    sample_data = {
        "income": 3000,
        "expenses": {
            "rent": 1200,
            "food": 500,
            "transport": 200,
            "entertainment": 100
        }
    }
    client.post("/upload", json=sample_data)

    response = client.get("/summary")
    data = response.get_json()

    assert response.status_code == 200
    assert data["income"] == 3000
    assert data["total_expenses"] == 2000
    assert data["savings"] == 1000
    assert "savings_rate" in data
    assert data["largest_expense"] == "rent"

def test_forecast_endpoint(client):
    response = client.get("/forecast")
    data = response.get_json()

    assert response.status_code == 200
    assert "inflation_forecast" in data
    assert len(data["inflation_forecast"]) >= 5
