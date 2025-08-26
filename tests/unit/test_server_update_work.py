import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json={"work": {"id": "work_1", "title": "Updated Work"}},
        status=200
    )
    result = await server.handle_call_tool(
        name="update_work",
        arguments={
            "id": "work_1",
            "type": "issue",
            "title": "Updated Work",
            "body": "Updated body",
            "owned_by": ["user_1"],
            "applies_to_part": ["part_1"],
            "stage": "in_progress"
        }
    )
    assert any("Object updated successfully: work_1" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="update_work",
        arguments={
            "id": "work_1",
            "type": "issue"
        }
    )
    assert any("Update object failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="update_work", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_missing_id():
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(name="update_work", arguments={"type": "issue"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_missing_type():
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="update_work", arguments={"id": "work_1"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_empty_response():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        body="",
        status=200
    )
    result = await server.handle_call_tool(
        name="update_work",
        arguments={
            "id": "work_1",
            "type": "issue"
        }
    )
    assert any("Object updated successfully: work_1" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_work_malformed_response():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        body="not a json",
        status=200
    )
    result = await server.handle_call_tool(
        name="update_work",
        arguments={
            "id": "work_1",
            "type": "issue"
        }
    )
    assert any("Object updated successfully: work_1" in c.text for c in result)
