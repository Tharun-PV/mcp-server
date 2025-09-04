import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_search_arguments():
    """Provide valid arguments for search functionality."""
    return {
        "query": "test query",
        "namespace": "issue"
    }


@responses.activate
@pytest.mark.asyncio
async def test_search_success(valid_search_arguments):
    """Test successful search."""
    expected_response = {
        "results": [
            {"id": "item1", "title": "Test Item 1"},
            {"id": "item2", "title": "Test Item 2"}
        ]
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/search.hybrid",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="search",
        arguments=valid_search_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Search results for 'test query'" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_search_api_error(valid_search_arguments):
    """Test handling of API error."""
    error_response = {
        "error": {
            "code": "UNAUTHORIZED",
            "message": "Invalid API key"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/search.hybrid",
        json=error_response,
        status=401
    )

    result = await server.handle_call_tool(
        name="search",
        arguments=valid_search_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Search failed with status 401" in result[0].text


@pytest.mark.asyncio
async def test_search_missing_arguments():
    """Test error handling when no arguments are provided."""
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="search", arguments=None)


@pytest.mark.asyncio
async def test_search_missing_query():
    """Test error handling when query parameter is missing."""
    with pytest.raises(ValueError, match="Missing query parameter"):
        await server.handle_call_tool(name="search", arguments={"namespace": "issue"})


@pytest.mark.asyncio
async def test_search_missing_namespace():
    """Test error handling when namespace parameter is missing."""
    with pytest.raises(ValueError, match="Missing namespace parameter"):
        await server.handle_call_tool(name="search", arguments={"query": "test"})
