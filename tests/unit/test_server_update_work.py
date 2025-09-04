import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_update_arguments():
    """Provide valid arguments for updating a work item."""
    return {
        "id": "work_123",
        "type": "issue",
        "title": "Updated Work",
        "body": "Updated description",
        "owned_by": ["user_1"],
        "stage": "in_progress"
    }


@pytest.fixture
def minimal_update_arguments():
    """Provide minimal required arguments for updating a work item."""
    return {
        "id": "work_123",
        "type": "issue"
    }


@responses.activate
@pytest.mark.asyncio
async def test_update_work_success(valid_update_arguments):
    """Test successful work update."""
    expected_response = {
        "work": {
            "id": "work_123",
            "title": "Updated Work",
            "type": "issue",
            "stage": "in_progress"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="update_work",
        arguments=valid_update_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object updated successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_update_work_api_error(minimal_update_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="update_work",
        arguments=minimal_update_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Update object failed with status 400" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_update_work_empty_response(minimal_update_arguments):
    """Test handling of empty response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        body="",
        status=200,
        content_type="application/json"
    )

    result = await server.handle_call_tool(
        name="update_work",
        arguments=minimal_update_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object updated successfully" in result[0].text


@pytest.mark.asyncio
async def test_update_work_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="update_work", arguments=None)


@pytest.mark.asyncio
async def test_update_work_missing_id():
    """Test error handling when id parameter is missing."""
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(name="update_work", arguments={"type": "issue"})


@pytest.mark.asyncio
async def test_update_work_missing_type():
    """Test error handling when type parameter is missing."""
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="update_work", arguments={"id": "work_123"})
