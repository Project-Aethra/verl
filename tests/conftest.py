"""Shared pytest fixtures for verl."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


@pytest.fixture(scope="module")
def client():
    from app.server import app
    yield TestClient(app)
