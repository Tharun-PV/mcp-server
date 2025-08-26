import os
import responses
import requests
import pytest
from devrev_mcp import utils

import requests


def test_make_devrev_request_malformed_response(monkeypatch):
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
    def raise_timeout(*a, **k): raise requests.Timeout("Timeout!")
    monkeypatch.setattr(requests, "post", raise_timeout)
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    with pytest.raises(requests.Timeout):
        utils.make_devrev_request("endpoint", {})


def test_make_devrev_request_missing_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "")
    with pytest.raises(ValueError):
        utils.make_devrev_request("endpoint", {})


@pytest.fixture
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def clear_api_key(monkeypatch):
    monkeypatch.delenv("DEVREV_API_KEY", raising=False)


@responses.activate
def test_make_devrev_request_success(set_api_key):
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
    with pytest.raises(ValueError, match="DEVREV_API_KEY environment variable is not set"):
        utils.make_devrev_request("works.get", {"id": "work_1"})


@responses.activate
def test_make_devrev_request_error(set_api_key):
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
def test_make_internal_devrev_request_success(set_api_key):
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
    monkeypatch.setenv("DEVREV_API_KEY", "")
    with pytest.raises(ValueError):
        utils.make_internal_devrev_request("endpoint", {})


def test_make_internal_devrev_request_connection_error(monkeypatch):
    def raise_connection_error(
        *a, **k): raise requests.ConnectionError("Connection error!")
    monkeypatch.setattr(requests, "post", raise_connection_error)
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    with pytest.raises(requests.ConnectionError):
        utils.make_internal_devrev_request("endpoint", {})


def test_make_internal_devrev_request_malformed_response(monkeypatch):
    class DummyResponse:
        status_code = 200
        def json(self): raise ValueError("Malformed JSON")
        text = "not json"
    monkeypatch.setattr(requests, "post", lambda *a, **k: DummyResponse())
    monkeypatch.setenv("DEVREV_API_KEY", "dummy_key")
    resp = utils.make_internal_devrev_request("endpoint", {})
    with pytest.raises(ValueError):
        resp.json()
