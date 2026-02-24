"""Signup and unregister flow tests (Arrange-Act-Assert).

These tests use the in-memory `activities` object and rely on the
`reset_activities` fixture to restore state between tests.
"""

from urllib.parse import quote


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "testuser@example.com"
    encoded_name = quote(activity_name, safe="")

    # Ensure not present beforehand
    before = client.get("/activities").json()[activity_name]["participants"]
    assert email not in before

    # Act
    resp = client.post(f"/activities/{encoded_name}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    after = client.get("/activities").json()[activity_name]["participants"]
    assert email in after


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = client.get("/activities").json()[activity_name]["participants"][0]
    encoded_name = quote(activity_name, safe="")

    # Act
    resp = client.post(f"/activities/{encoded_name}/signup", params={"email": existing_email})

    # Assert
    assert resp.status_code == 400
    assert "already" in resp.json().get("detail", "").lower()


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Drama Club"
    email = "remove_me@example.com"
    encoded_name = quote(activity_name, safe="")

    # Sign up first so we have a participant to remove
    signup = client.post(f"/activities/{encoded_name}/signup", params={"email": email})
    assert signup.status_code == 200

    # Act
    delete = client.delete(f"/activities/{encoded_name}/participants", params={"email": email})

    # Assert
    assert delete.status_code == 200
    data = client.get("/activities").json()[activity_name]["participants"]
    assert email not in data


def test_unregister_nonexistent_returns_404(client):
    # Arrange
    activity_name = "Science Club"
    email = "noone@example.com"
    encoded_name = quote(activity_name, safe="")

    # Act
    resp = client.delete(f"/activities/{encoded_name}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()
