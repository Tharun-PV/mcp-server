import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_add_timeline_entry_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/timeline-entries.create",
        json={"timeline_entry": {"id": "entry_1"}},
        status=201
    )
    result = await server.handle_call_tool(
        name="add_timeline_entry",
        arguments={"id": "work_1", "timeline_entry": "Test timeline entry"}
    )
    assert any("Timeline entry created successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_add_timeline_entry_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/timeline-entries.create",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="add_timeline_entry",
        arguments={"id": "work_1", "timeline_entry": "Test timeline entry"}
    )
    assert any(
        "Create timeline entry failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_add_timeline_entry_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="add_timeline_entry", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_add_timeline_entry_missing_id():
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(name="add_timeline_entry", arguments={"timeline_entry": "Test timeline entry"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_add_timeline_entry_missing_entry():
    with pytest.raises(ValueError, match="Missing timeline_entry parameter"):
        await server.handle_call_tool(name="add_timeline_entry", arguments={"id": "work_1"})
