import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_part_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.get",
        json={"part": {"id": "part_1", "name": "Test Part"}},
        status=200
    )
    result = await server.handle_call_tool(
        name="get_part",
        arguments={"id": "part_1"}
    )
    assert any("Part information for 'part_1'" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_part_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.get",
        json={"error": "Not found"},
        status=404
    )
    result = await server.handle_call_tool(
        name="get_part",
        arguments={"id": "part_1"}
    )
    assert any("Get part failed with status 404" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_part_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_part", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_part_missing_id():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_part", arguments={})
