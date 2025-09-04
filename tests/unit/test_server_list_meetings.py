import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_list_meetings_success():
    """Test list_meetings with valid arguments."""
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
async def test_list_meetings_api_error():
    """Test list_meetings with API error response."""
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
async def test_list_meetings_no_arguments():
    """Test list_meetings with no arguments."""
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
