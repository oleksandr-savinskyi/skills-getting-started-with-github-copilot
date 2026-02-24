"""Tests for activity listing using Arrange-Act-Assert pattern."""


def test_get_activities_returns_known_activities(client):
    # Arrange: `client` fixture provides an in-process test client

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)
