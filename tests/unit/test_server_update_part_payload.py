import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_update_arguments():
    """Provide valid arguments for updating part with all fields."""
    return {
        "id": "part_123",
        "type": "enhancement",
        "name": "Updated Part Name",
        "owned_by": ["user_1"],
        "description": "Updated description",
        "target_close_date": "2025-12-31T00:00:00Z",
        "target_start_date": "2025-01-01T00:00:00Z",
        "stage": "Ready"
    }


@responses.activate
@pytest.mark.asyncio
async def test_update_part_all_fields(valid_update_arguments):
    """Test updating part with all optional fields."""
    expected_response = {
        "part": {
            "id": "part_123",
            "name": "Updated Part Name",
            "type": "enhancement",
            "stage": "Ready"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.update",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="update_part",
        arguments=valid_update_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Part updated successfully" in result[0].text
