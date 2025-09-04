import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_list_meetings_api_error():
    """Test list_meetings with API error response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/meetings.list",
        json={"error": "Internal Error"},
        status=500
    )
    result = await server.handle_call_tool(name="list_meetings", arguments={})
    assert any("List meetings failed with status 500" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_valid_stage_transition_schema_error():
    """Test valid_stage_transition with schema API error."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}},
        status=200
    )
    responses.add(
        responses.POST,
        "https://api.devrev.ai/schemas.aggregated.get",
        json={"error": "Schema Error"},
        status=500
    )
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any("Get schema failed with status 500" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_valid_stage_transition_stage_diagram_error():
    """Test valid_stage_transition with stage diagram API error."""
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
        json={"error": "Stage Diagram Error"},
        status=500
    )
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any("Get stage diagram for Get stage transitions failed with status 500" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_valid_stage_transition_no_transitions():
    """Test valid_stage_transition when no valid transitions found."""
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
        json={"stage_diagram": {"stages": [{"stage": {"id": "other_stage"}, "transitions": ["to_stage_2"]}]}},
        status=200
    )
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any("No valid transitions found for 'work_1'" in c.text for c in result)
