import pytest
import responses
import requests
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_work_arguments():
    """Provide valid arguments for creating a work item."""
    return {
        "type": "issue",
        "title": "Test Issue",
        "applies_to_part": "part_123",
        "body": "Test description",
        "owned_by": ["user_456"]
    }


@pytest.fixture
def minimal_work_arguments():
    """Provide minimal required arguments for creating a work item."""
    return {
        "type": "ticket",
        "title": "Minimal Ticket",
        "applies_to_part": "part_123"
    }


@responses.activate
@pytest.mark.asyncio
async def test_create_work_success(valid_work_arguments):
    """Test successful work creation."""
    expected_response = {
        "work": {
            "id": "work_123",
            "type": "issue",
            "title": "Test Issue",
            "applies_to_part": "part_123"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        json=expected_response,
        status=201
    )

    result = await server.handle_call_tool(
        name="create_work",
        arguments=valid_work_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object created successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_work_success_minimal(minimal_work_arguments):
    """Test successful work creation with minimal parameters."""
    expected_response = {
        "work": {
            "id": "work_456",
            "type": "ticket",
            "title": "Minimal Ticket",
            "applies_to_part": "part_123"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        json=expected_response,
        status=201
    )

    result = await server.handle_call_tool(
        name="create_work",
        arguments=minimal_work_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object created successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_work_api_error(valid_work_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="create_work",
        arguments=valid_work_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Create object failed with status 400" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_work_empty_response(valid_work_arguments):
    """Test handling of empty response body."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        body="",
        status=201,
        content_type="application/json"
    )

    result = await server.handle_call_tool(
        name="create_work",
        arguments=valid_work_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object created successfully: {}" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_work_malformed_response(valid_work_arguments):
    """Test handling of malformed JSON response."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        body="Invalid JSON",
        status=201,
        content_type="application/json"
    )

    result = await server.handle_call_tool(
        name="create_work",
        arguments=valid_work_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Malformed response" in result[0].text


@pytest.mark.asyncio
async def test_create_work_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="create_work", arguments=None)


@pytest.mark.asyncio
async def test_create_work_missing_type(minimal_work_arguments):
    """Test error handling when type parameter is missing."""
    arguments = minimal_work_arguments.copy()
    del arguments["type"]
    
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="create_work", arguments=arguments)


@pytest.mark.asyncio
async def test_create_work_missing_title(minimal_work_arguments):
    """Test error handling when title parameter is missing."""
    arguments = minimal_work_arguments.copy()
    del arguments["title"]
    
    with pytest.raises(ValueError, match="Missing title parameter"):
        await server.handle_call_tool(name="create_work", arguments=arguments)


@pytest.mark.asyncio
async def test_create_work_missing_applies_to_part(minimal_work_arguments):
    """Test error handling when applies_to_part parameter is missing."""
    arguments = minimal_work_arguments.copy()
    del arguments["applies_to_part"]
    
    with pytest.raises(ValueError, match="Missing applies_to_part parameter"):
        await server.handle_call_tool(name="create_work", arguments=arguments)


@pytest.mark.asyncio
async def test_create_work_empty_parameters(minimal_work_arguments):
    """Test error handling when parameters are empty."""
    arguments = minimal_work_arguments.copy()
    arguments["type"] = ""
    arguments["title"] = ""
    arguments["applies_to_part"] = ""
    
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="create_work", arguments=arguments)


@responses.activate
@pytest.mark.asyncio
async def test_create_work_network_error(valid_work_arguments):
    """Test handling of network errors."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.create",
        body=requests.Timeout("Request timed out")
    )

    with pytest.raises(requests.Timeout):
        await server.handle_call_tool(
            name="create_work",
            arguments=valid_work_arguments
        )


@responses.activate
@pytest.mark.asyncio
async def test_create_work_different_types():
    """Test creating different work types."""
    work_types = ["issue", "ticket"]
    
    for work_type in work_types:
        with responses.RequestsMock() as rsps:
            expected_response = {
                "work": {
                    "id": f"work_{work_type}_123",
                    "type": work_type,
                    "title": f"Test {work_type.title()}",
                    "applies_to_part": "part_123"
                }
            }
            
            rsps.add(
                responses.POST,
                "https://api.devrev.ai/works.create",
                json=expected_response,
                status=201
            )

            result = await server.handle_call_tool(
                name="create_work",
                arguments={
                    "type": work_type,
                    "title": f"Test {work_type.title()}",
                    "applies_to_part": "part_123"
                }
            )

            assert len(result) == 1
            assert result[0].type == "text"
            assert "Object created successfully" in result[0].text
