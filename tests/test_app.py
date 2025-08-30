import pytest
from app import app
from messenger import forwarded_notifications
from storage import notifications

@pytest.fixture

def client():
    with app.test_client() as client:
        yield client

def  test_warning_forwarded(client):
    payload = {"Type": "Warning", "Name": "Backup Failure", "Description": "Backup failed"}
    response = client.post("/notifications", json=payload)
    assert response.status_code == 200
    assert forwarded_notifications[-1]["Name"] == "Backup Failure"
    assert notifications[-1]["status"] == "forwarded"


def test_info_ignored(client):
    payload = {"Type": "Info", "Name": "Quota Exceeded", "Description": "Compute quota exceeded"}
    response = client.post("/notifications", json=payload)
    assert response.status_code == 200
    assert notifications[-1]["status"] == "ignored"


def test_invalid_payload(client):
    payload = {"Name": "No Type"}
    response = client.post("/notifications", json=payload)
    assert response.status_code == 400