import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_search_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/search.hybrid",
        json={"results": ["item1", "item2"]},
        status=200
    )
    result = await server.handle_call_tool(
        name="search",
        arguments={"query": "test", "namespace": "issue"}
    )
    assert any("Search results for 'test'" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_search_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/search.hybrid",
        json={"error": "Unauthorized"},
        status=401
    )
    result = await server.handle_call_tool(
        name="search",
        arguments={"query": "test", "namespace": "issue"}
    )
    assert any("Search failed with status 401" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_search_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="search", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_search_missing_query():
    with pytest.raises(ValueError, match="Missing query parameter"):
        await server.handle_call_tool(name="search", arguments={"namespace": "issue"})


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_search_missing_namespace():
    with pytest.raises(ValueError, match="Missing namespace parameter"):
        await server.handle_call_tool(name="search", arguments={"query": "test"})
