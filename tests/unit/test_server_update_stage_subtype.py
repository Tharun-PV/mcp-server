import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_update_work_stage():
    """Test update_work with stage parameter."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json={"work": {"id": "work_1"}},
        status=200
    )
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "stage": "In Progress"})
    assert any("Object updated successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_update_part_stage():
    """Test update_part with stage parameter."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.update",
        json={"part": {"id": "part_1"}},
        status=200
    )
    result = await server.handle_call_tool(name="update_part", arguments={
        "id": "part_1", "type": "enhancement", "stage": "Ready"})
    assert any("Part updated successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_update_work_subtype():
    """Test update_work with subtype parameter."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json={"work": {"id": "work_1"}},
        status=200
    )
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "subtype": {"drop": False, "subtype": "bug"}})
    assert any("Object updated successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_update_work_subtype_drop():
    """Test update_work with subtype drop parameter."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json={"work": {"id": "work_1"}},
        status=200
    )
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "subtype": {"drop": True}})
    assert any("Object updated successfully" in c.text for c in result)
