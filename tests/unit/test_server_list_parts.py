import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_list_arguments():
    """Provide valid arguments for listing parts."""
    return {
        "type": "enhancement"
    }


@responses.activate
@pytest.mark.asyncio
async def test_list_parts_success(valid_list_arguments):
    """Test successful parts listing."""
    expected_response = {
        "parts": [
            {"id": "part_1", "name": "Part 1", "type": "enhancement"},
            {"id": "part_2", "name": "Part 2", "type": "enhancement"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="list_parts",
        arguments=valid_list_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Parts listed successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_list_parts_api_error(valid_list_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.list",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="list_parts",
        arguments=valid_list_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "List parts failed with status 400" in result[0].text


@pytest.mark.asyncio
async def test_list_parts_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="list_parts", arguments={})
