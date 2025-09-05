import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_valid_stage_transition_success():
    """Test valid_stage_transition with successful API responses."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}},
        status=200
    )
    responses.add(
        responses.POST,
        "https://api.devrev.ai/schemas.aggregated.get",
        json={"schema": {"stage_diagram_id": {"id": "diagram_1"}}},
        status=200
    )
    responses.add(
        responses.POST,
        "https://api.devrev.ai/stage-diagrams.get",
        json={"stage_diagram": {"stages": [{"stage": {"id": "stage_1"}, "transitions": ["to_stage_2"]}]}},
        status=200
    )
    result = await server.handle_call_tool(
        name="valid_stage_transition",
        arguments={"type": "issue", "id": "work_1"}
    )
    assert any("Valid Transitions for 'work_1'" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_valid_stage_transition_work_not_found():
    """Test valid_stage_transition when work item not found."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"error": "Not Found"},
        status=404
    )
    result = await server.handle_call_tool(
        name="valid_stage_transition",
        arguments={"type": "issue", "id": "work_1"}
    )
    assert any("Get work item failed with status 404" in c.text for c in result)
