import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_get_current_user_success():
    """Test successful current user retrieval."""
    expected_response = {
        "user": {
            "id": "user_123",
            "name": "Test User",
            "email": "test@example.com"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/dev-users.self",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="get_current_user",
        arguments={}
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Current DevRev user details" in result[0].text
