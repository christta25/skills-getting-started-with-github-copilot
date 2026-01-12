from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Spot check a known activity
    assert "Art Studio" in data
    assert "participants" in data["Art Studio"]


def test_signup_and_unregister_flow():
    activity = "Art Studio"
    email = "pytest-user@example.com"

    # Ensure clean state for the test email
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup should succeed
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up again should return 400
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400

    # Unregister should succeed
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 400
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400


def test_signup_invalid_activity():
    resp = client.post("/activities/Nonexistent/signup", params={"email": "x@example.com"})
    assert resp.status_code == 404


def test_unregister_invalid_activity():
    resp = client.post("/activities/Nonexistent/unregister", params={"email": "x@example.com"})
    assert resp.status_code == 404
