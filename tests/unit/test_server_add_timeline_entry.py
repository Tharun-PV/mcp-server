import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_timeline_arguments():
    """Provide valid arguments for adding timeline entry."""
    return {
        "id": "work_123",
        "timeline_entry": "Test timeline entry"
    }


@responses.activate
@pytest.mark.asyncio
async def test_add_timeline_entry_success(valid_timeline_arguments):
    """Test successful timeline entry creation."""
    expected_response = {
        "timeline_entry": {
            "id": "entry_123",
            "work_id": "work_123",
            "entry": "Test timeline entry"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/timeline-entries.create",
        json=expected_response,
        status=201
    )

    result = await server.handle_call_tool(
        name="add_timeline_entry",
        arguments=valid_timeline_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Timeline entry created successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_add_timeline_entry_api_error(valid_timeline_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/timeline-entries.create",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="add_timeline_entry",
        arguments=valid_timeline_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Create timeline entry failed with status 400" in result[0].text


@pytest.mark.asyncio
async def test_add_timeline_entry_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="add_timeline_entry", arguments=None)


@pytest.mark.asyncio
async def test_add_timeline_entry_missing_id():
    """Test error handling when id parameter is missing."""
    with pytest.raises(ValueError, match="Missing id parameter"):
        await server.handle_call_tool(
            name="add_timeline_entry", 
            arguments={"timeline_entry": "Test timeline entry"}
        )


@pytest.mark.asyncio
async def test_add_timeline_entry_missing_entry():
    """Test error handling when timeline_entry parameter is missing."""
    with pytest.raises(ValueError, match="Missing timeline_entry parameter"):
        await server.handle_call_tool(
            name="add_timeline_entry", 
            arguments={"id": "work_123"}
        )
