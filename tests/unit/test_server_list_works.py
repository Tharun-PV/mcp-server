import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_list_arguments():
    """Provide valid arguments for listing works."""
    return {
        "type": ["issue", "ticket"]
    }


@responses.activate
@pytest.mark.asyncio
async def test_list_works_success(valid_list_arguments):
    """Test successful works listing."""
    expected_response = {
        "works": [
            {"id": "work_1", "title": "Issue 1", "type": "issue"},
            {"id": "work_2", "title": "Ticket 1", "type": "ticket"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="list_works",
        arguments=valid_list_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Works listed successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_list_works_api_error(valid_list_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.list",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="list_works",
        arguments=valid_list_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "List works failed with status 400" in result[0].text


@pytest.mark.asyncio
async def test_list_works_missing_type():
    """Test error handling when type parameter is missing."""
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="list_works", arguments={})
