import pytest
import responses
import requests
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        json={"work": {"id": "work_2", "title": "Created Work"}},
        status=201
    )
    result = await server.handle_call_tool(
        name="create_work",
        arguments={
            "type": "issue",
            "title": "Created Work",
            "applies_to_part": "part_1",
            "body": "Test body",
            "owned_by": ["user_1"]
        }
    )
    assert any("Object created successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="create_work",
        arguments={
            "type": "issue",
            "title": "Created Work",
            "applies_to_part": "part_1",
            "body": "Test body",
            "owned_by": ["user_1"]
        }
    )
    assert any("Create object failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="create_work", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_missing_type():
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="create_work", arguments={"title": "Created Work", "applies_to_part": "part_1"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_missing_title():
    with pytest.raises(ValueError, match="Missing title parameter"):
        await server.handle_call_tool(name="create_work", arguments={"type": "issue", "applies_to_part": "part_1"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_missing_applies_to_part():
    with pytest.raises(ValueError, match="Missing applies_to_part parameter"):
        await server.handle_call_tool(name="create_work", arguments={"type": "issue", "title": "Created Work"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_empty_response():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        body="",
        status=201
    )
    result = await server.handle_call_tool(
        name="create_work",
        arguments={
            "type": "issue",
            "title": "Created Work",
            "applies_to_part": "part_1",
            "body": "Test body",
            "owned_by": ["user_1"]
        }
    )
    assert any("Object created successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_malformed_response():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        body="not a json",
        status=201
    )
    # Should not raise, but may return a text error or empty dict
    result = await server.handle_call_tool(
        name="create_work",
        arguments={
            "type": "issue",
            "title": "Created Work",
            "applies_to_part": "part_1",
            "body": "Test body",
            "owned_by": ["user_1"]
        }
    )
    assert any("Object created successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_work_timeout(monkeypatch):
    def timeout_post(*args, **kwargs):
        raise requests.Timeout("Request timed out")
    monkeypatch.setattr(server, "make_devrev_request", timeout_post)
    with pytest.raises(requests.Timeout):
        await server.handle_call_tool(
            name="create_work",
            arguments={
                "type": "issue",
                "title": "Created Work",
                "applies_to_part": "part_1",
                "body": "Test body",
                "owned_by": ["user_1"]
            }
        )
