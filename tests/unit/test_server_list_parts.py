import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_parts_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.list",
        json={"parts": [{"id": "part_1"}, {"id": "part_2"}]},
        status=200
    )
    result = await server.handle_call_tool(
        name="list_parts",
        arguments={"type": "enhancement"}
    )
    assert any("Parts listed successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_parts_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.list",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="list_parts",
        arguments={"type": "enhancement"}
    )
    assert any("List parts failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_parts_missing_type():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="list_parts", arguments={})
