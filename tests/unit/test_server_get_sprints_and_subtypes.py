import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_sprints_arguments():
    """Provide valid arguments for getting sprints."""
    return {
        "ancestor_part_id": "part_123"
    }


@pytest.fixture
def valid_subtypes_arguments():
    """Provide valid arguments for listing subtypes."""
    return {
        "leaf_type": "issue"
    }


@responses.activate
@pytest.mark.asyncio
async def test_get_sprints_success(valid_sprints_arguments):
    """Test successful sprints retrieval."""
    expected_response = {
        "vista_group": [
            {"id": "sprint_1", "name": "Sprint 1"},
            {"id": "sprint_2", "name": "Sprint 2"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/vistas.groups.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="get_sprints",
        arguments=valid_sprints_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Sprints for 'part_123'" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_get_sprints_api_error(valid_sprints_arguments):
    """Test handling of API error for sprints."""
    error_response = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Internal server error"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/vistas.groups.list",
        json=error_response,
        status=500
    )

    result = await server.handle_call_tool(
        name="get_sprints",
        arguments=valid_sprints_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Get sprints failed with status 500" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_list_subtypes_success(valid_subtypes_arguments):
    """Test successful subtypes listing."""
    expected_response = {
        "subtypes": [
            {"id": "subtype_1", "name": "Bug"},
            {"id": "subtype_2", "name": "Feature"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/schemas.subtypes.list",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="list_subtypes",
        arguments=valid_subtypes_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Subtypes for 'issue'" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_list_subtypes_api_error(valid_subtypes_arguments):
    """Test handling of API error for subtypes."""
    error_response = {
        "error": {
            "code": "NOT_FOUND",
            "message": "Subtypes not found"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/schemas.subtypes.list",
        json=error_response,
        status=404
    )

    result = await server.handle_call_tool(
        name="list_subtypes",
        arguments=valid_subtypes_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "List subtypes failed with status 404" in result[0].text
