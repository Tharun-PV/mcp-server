import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_work_id():
    """Provide valid work ID for testing."""
    return "work_123"


@responses.activate
@pytest.mark.asyncio
async def test_get_work_success(valid_work_id):
    """Test successful work retrieval."""
    expected_response = {
        "work": {
            "id": valid_work_id,
            "title": "Test Work",
            "type": "issue",
            "state": "open"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="get_work",
        arguments={"id": valid_work_id}
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert f"Object information for '{valid_work_id}'" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_get_work_not_found(valid_work_id):
    """Test handling of work not found."""
    error_response = {
        "error": {
            "code": "NOT_FOUND",
            "message": "Work not found"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json=error_response,
        status=404
    )

    result = await server.handle_call_tool(
        name="get_work",
        arguments={"id": valid_work_id}
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Get object failed with status 404" in result[0].text


@pytest.mark.asyncio
async def test_get_work_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_work", arguments=None)


@pytest.mark.asyncio
async def test_get_work_missing_id():
    """Test error handling when id parameter is missing."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_work", arguments={})
