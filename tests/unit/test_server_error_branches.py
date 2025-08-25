import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_invalid_tool():
    # Test unknown tool name
    with pytest.raises(ValueError, match="Unknown tool: invalid_tool"):
        await server.handle_call_tool(name="invalid_tool", arguments={})


@pytest.mark.asyncio
async def test_handle_call_tool_missing_required_param():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_vista", arguments={})


@pytest.mark.asyncio
async def test_handle_call_tool_missing_arguments():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_vista", arguments=None)


@pytest.mark.asyncio
async def test_handle_call_tool_invalid_type_param():
    # Test invalid type for valid_stage_transition
    with pytest.raises(ValueError, match="Invalid type parameter"):
        await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "invalid", "id": "work_1"})


@pytest.mark.asyncio
async def test_handle_call_tool_missing_required_param_valid_stage_transition():
    # Test missing id for valid_stage_transition
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue"})
    # Test missing type for valid_stage_transition
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="valid_stage_transition", arguments={"id": "work_1"})
