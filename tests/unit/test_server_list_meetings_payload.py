import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_meetings_arguments():
    """Provide valid arguments for listing meetings with all optional fields."""
    return {
        "channel": ["zoom"],
        "created_by": ["user_1"],
        "created_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "cursor": {"next_cursor": "abc", "mode": "after"},
        "ended_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "external_ref": ["ref_1"],
        "limit": 10,
        "members": ["member_1"],
        "modified_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "organizer": ["org_1"],
        "scheduled_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "sort_by": ["created_date:asc"],
        "state": ["scheduled"]
    }


@responses.activate
@pytest.mark.asyncio
async def test_list_meetings_payload_branches(valid_meetings_arguments):
    """Test listing meetings with all optional fields."""
    expected_response = {
        "meetings": [
            {"id": "meeting_1", "title": "Test Meeting 1"},
            {"id": "meeting_2", "title": "Test Meeting 2"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/meetings.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="list_meetings",
        arguments=valid_meetings_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Meetings listed successfully" in result[0].text
