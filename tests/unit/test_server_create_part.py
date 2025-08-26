import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.create",
        json={"part": {"id": "part_2", "name": "Created Part"}},
        status=201
    )
    result = await server.handle_call_tool(
        name="create_part",
        arguments={
            "type": "enhancement",
            "name": "Created Part",
            "owned_by": ["user_1"],
            "parent_part": ["parent_1"],
            "description": "Test part"
        }
    )
    assert any("Part created successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.create",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="create_part",
        arguments={
            "type": "enhancement",
            "name": "Created Part",
            "owned_by": ["user_1"],
            "parent_part": ["parent_1"],
            "description": "Test part"
        }
    )
    assert any("Create part failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="create_part", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_missing_type():
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="create_part", arguments={"name": "Created Part", "owned_by": ["user_1"], "parent_part": ["parent_1"]})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_missing_name():
    with pytest.raises(ValueError, match="Missing name parameter"):
        await server.handle_call_tool(name="create_part", arguments={"type": "enhancement", "owned_by": ["user_1"], "parent_part": ["parent_1"]})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_missing_owned_by():
    with pytest.raises(ValueError, match="Missing owned_by parameter"):
        await server.handle_call_tool(name="create_part", arguments={"type": "enhancement", "name": "Created Part", "parent_part": ["parent_1"]})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_create_part_missing_parent_part():
    with pytest.raises(ValueError, match="Missing parent_part parameter"):
        await server.handle_call_tool(name="create_part", arguments={"type": "enhancement", "name": "Created Part", "owned_by": ["user_1"]})
