import os
import responses
import requests
import pytest
from devrev_mcp import utils


@pytest.fixture
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def clear_api_key(monkeypatch):
    """Clear API key from environment."""
    monkeypatch.delenv("DEVREV_API_KEY", raising=False)


def test_make_devrev_request_malformed_response(monkeypatch):
    """Test make_devrev_request with malformed JSON response."""
    class DummyResponse:
        status_code = 200
        def json(self): raise ValueError("Malformed JSON")
        text = "not json"
    monkeypatch.setattr(requests, "post", lambda *a, **k: DummyResponse())
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    resp = utils.make_devrev_request("endpoint", {})
    with pytest.raises(ValueError):
        resp.json()


def test_make_devrev_request_timeout(monkeypatch):
    """Test make_devrev_request with timeout error."""
    def raise_timeout(*a, **k): raise requests.Timeout("Timeout!")
    monkeypatch.setattr(requests, "post", raise_timeout)
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    with pytest.raises(requests.Timeout):
        utils.make_devrev_request("endpoint", {})


def test_make_devrev_request_missing_api_key(monkeypatch):
    """Test make_devrev_request with missing API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "")
    with pytest.raises(ValueError):
        utils.make_devrev_request("endpoint", {})


@responses.activate
def test_make_devrev_request_success(setup_environment):
    """Test make_devrev_request with successful response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"result": "ok"},
        status=200
    )
    resp = utils.make_devrev_request("works.get", {"id": "work_1"})
    assert resp.status_code == 200
    assert resp.json()["result"] == "ok"


def test_make_devrev_request_no_api_key(clear_api_key):
    """Test make_devrev_request with no API key in environment."""
    with pytest.raises(ValueError, match="DEVREV_API_KEY environment variable is not set"):
        utils.make_devrev_request("works.get", {"id": "work_1"})


@responses.activate
def test_make_devrev_request_error(setup_environment):
    """Test make_devrev_request with API error response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"error": "Unauthorized"},
        status=401
    )
    resp = utils.make_devrev_request("works.get", {"id": "work_1"})
    assert resp.status_code == 401
    assert resp.json()["error"] == "Unauthorized"


@responses.activate
def test_make_internal_devrev_request_success(setup_environment):
    """Test make_internal_devrev_request with successful response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/internal/test",
        json={"result": "internal_ok"},
        status=200
    )
    resp = utils.make_internal_devrev_request("test", {"foo": "bar"})
    assert resp.status_code == 200
    assert resp.json()["result"] == "internal_ok"


def test_make_internal_devrev_request_missing_api_key(monkeypatch):
    """Test make_internal_devrev_request with missing API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "")
    with pytest.raises(ValueError):
        utils.make_internal_devrev_request("endpoint", {})


def test_make_internal_devrev_request_connection_error(monkeypatch):
    """Test make_internal_devrev_request with connection error."""
    def raise_connection_error(*a, **k): raise requests.ConnectionError("Connection error!")
    monkeypatch.setattr(requests, "post", raise_connection_error)
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    with pytest.raises(requests.ConnectionError):
        utils.make_internal_devrev_request("endpoint", {})


def test_make_internal_devrev_request_malformed_response(monkeypatch):
    """Test make_internal_devrev_request with malformed JSON response."""
    class DummyResponse:
        status_code = 200
        def json(self): raise ValueError("Malformed JSON")
        text = "not json"
    monkeypatch.setattr(requests, "post", lambda *a, **k: DummyResponse())
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    resp = utils.make_internal_devrev_request("endpoint", {})
    with pytest.raises(ValueError):
        resp.json()
