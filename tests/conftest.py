"""Shared pytest fixtures for backend API tests."""

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for endpoint tests."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities_state():
    """Reset in-memory activity data before each test for isolation."""
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)
