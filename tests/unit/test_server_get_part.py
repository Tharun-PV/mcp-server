import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_part_id():
    """Provide valid part ID for testing."""
    return "part_123"


@responses.activate
@pytest.mark.asyncio
async def test_get_part_success(valid_part_id):
    """Test successful part retrieval."""
    expected_response = {
        "part": {
            "id": valid_part_id,
            "name": "Test Part",
            "type": "enhancement"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.get",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="get_part",
        arguments={"id": valid_part_id}
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert f"Part information for '{valid_part_id}'" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_get_part_not_found(valid_part_id):
    """Test handling of part not found."""
    error_response = {
        "error": {
            "code": "NOT_FOUND",
            "message": "Part not found"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.get",
        json=error_response,
        status=404
    )

    result = await server.handle_call_tool(
        name="get_part",
        arguments={"id": valid_part_id}
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Get part failed with status 404" in result[0].text


@pytest.mark.asyncio
async def test_get_part_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_part", arguments=None)


@pytest.mark.asyncio
async def test_get_part_missing_id():
    """Test error handling when id parameter is missing."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_part", arguments={})
