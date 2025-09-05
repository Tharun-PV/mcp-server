import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_sprints_arguments():
    """Provide valid arguments for getting sprints."""
    return {
        "ancestor_part_id": "part_123"
    }


@responses.activate
@pytest.mark.asyncio
async def test_get_sprints_state_default(valid_sprints_arguments):
    """Test get_sprints with no state provided (should default to 'active')."""
    expected_response = {
        "vista_group": [
            {"id": "sprint_1", "name": "Active Sprint 1"},
            {"id": "sprint_2", "name": "Active Sprint 2"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/vistas.groups.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="get_sprints",
        arguments=valid_sprints_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Sprints for 'part_123'" in result[0].text
