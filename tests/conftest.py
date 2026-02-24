import copy

import pytest
from fastapi.testclient import TestClient

from urllib.parse import quote

from src.app import app, activities


# Snapshot original activities so tests can restore state between runs
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Arrange: reset the in-memory activities before each test and restore after."""
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    """Act: provide an in-process TestClient bound to the FastAPI app."""
    with TestClient(app) as client:
        yield client
