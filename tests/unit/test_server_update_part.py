import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_part_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.update",
        json={"part": {"id": "part_2", "name": "Updated Part"}},
        status=200
    )
    result = await server.handle_call_tool(
        name="update_part",
        arguments={
            "id": "part_2",
            "type": "enhancement",
            "name": "Updated Part",
            "owned_by": ["user_1"],
            "description": "Updated part"
        }
    )
    assert any("Part updated successfully: part_2" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_part_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.update",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="update_part",
        arguments={
            "id": "part_2",
            "type": "enhancement"
        }
    )
    assert any("Update part failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_part_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="update_part", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_part_missing_id():
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(name="update_part", arguments={"type": "enhancement"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_update_part_missing_type():
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="update_part", arguments={"id": "part_2"})
