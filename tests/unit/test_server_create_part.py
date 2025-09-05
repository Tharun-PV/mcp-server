import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_part_arguments():
    """Provide valid arguments for creating a part."""
    return {
        "type": "enhancement",
        "name": "Test Part",
        "owned_by": ["user_1"],
        "parent_part": ["parent_1"],
        "description": "Test description"
    }


@pytest.fixture
def minimal_part_arguments():
    """Provide minimal required arguments for creating a part."""
    return {
        "type": "enhancement",
        "name": "Minimal Part",
        "owned_by": ["user_1"],
        "parent_part": ["parent_1"]
    }


@responses.activate
@pytest.mark.asyncio
async def test_create_part_success(valid_part_arguments):
    """Test successful part creation."""
    expected_response = {
        "part": {
            "id": "part_123",
            "type": "enhancement",
            "name": "Test Part",
            "owned_by": ["user_1"],
            "parent_part": ["parent_1"]
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.create",
        json=expected_response,
        status=201
    )

    result = await server.handle_call_tool(
        name="create_part",
        arguments=valid_part_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Part created successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_part_success_minimal(minimal_part_arguments):
    """Test successful part creation with minimal parameters."""
    expected_response = {
        "part": {
            "id": "part_456",
            "type": "enhancement",
            "name": "Minimal Part",
            "owned_by": ["user_1"],
            "parent_part": ["parent_1"]
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.create",
        json=expected_response,
        status=201
    )

    result = await server.handle_call_tool(
        name="create_part",
        arguments=minimal_part_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Part created successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_create_part_api_error(valid_part_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid parameters"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.create",
        json=error_response,
        status=400
    )

    result = await server.handle_call_tool(
        name="create_part",
        arguments=valid_part_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Create part failed with status 400" in result[0].text


@pytest.mark.asyncio
async def test_create_part_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="create_part", arguments=None)


@pytest.mark.asyncio
async def test_create_part_missing_type(minimal_part_arguments):
    """Test error handling when type parameter is missing."""
    arguments = minimal_part_arguments.copy()
    del arguments["type"]
    
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="create_part", arguments=arguments)


@pytest.mark.asyncio
async def test_create_part_missing_name(minimal_part_arguments):
    """Test error handling when name parameter is missing."""
    arguments = minimal_part_arguments.copy()
    del arguments["name"]
    
    with pytest.raises(ValueError, match="Missing name parameter"):
        await server.handle_call_tool(name="create_part", arguments=arguments)


@pytest.mark.asyncio
async def test_create_part_missing_owned_by(minimal_part_arguments):
    """Test error handling when owned_by parameter is missing."""
    arguments = minimal_part_arguments.copy()
    del arguments["owned_by"]
    
    with pytest.raises(ValueError, match="Missing owned_by parameter"):
        await server.handle_call_tool(name="create_part", arguments=arguments)


@pytest.mark.asyncio
async def test_create_part_missing_parent_part(minimal_part_arguments):
    """Test error handling when parent_part parameter is missing."""
    arguments = minimal_part_arguments.copy()
    del arguments["parent_part"]
    
    with pytest.raises(ValueError, match="Missing parent_part parameter"):
        await server.handle_call_tool(name="create_part", arguments=arguments)
