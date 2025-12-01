import json
from src.app import app

def test_health():
	client = app.test_client()
	response = client.get("/health")
	assert response.status_code == 200
	assert response.json["status"] == "ok"

def test_upload_and_summary():
	client = app.test_client()
	payload = {"income": 3000, "rent": 1200, "food": 500, "transport": 200, "entertainment": 300}
	response = client.post("/upload", json=payload)
	assert response.status_code == 201

	summary = client.get("/summary")
	assert summary.status_code == 200
	assert "savings_rate" in summary.json

