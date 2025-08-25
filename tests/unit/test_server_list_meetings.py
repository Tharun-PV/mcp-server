import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_meetings_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/meetings.list",
        json={"meetings": [{"id": "meeting_1"}, {"id": "meeting_2"}]},
        status=200
    )
    result = await server.handle_call_tool(
        name="list_meetings",
        arguments={"channel": ["zoom"], "limit": 2}
    )
    assert any("Meetings listed successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_meetings_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/meetings.list",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="list_meetings",
        arguments={"channel": ["zoom"], "limit": 2}
    )
    assert any("List meetings failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_meetings_no_args():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/meetings.list",
        json={"meetings": []},
        status=200
    )
    result = await server.handle_call_tool(
        name="list_meetings",
        arguments=None
    )
    assert any("Meetings listed successfully" in c.text for c in result)
