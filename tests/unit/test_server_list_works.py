import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_works_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.list",
        json={"works": [{"id": "work_1"}, {"id": "work_2"}]},
        status=200
    )
    result = await server.handle_call_tool(
        name="list_works",
        arguments={"type": ["issue", "ticket"]}
    )
    assert any("Works listed successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_works_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.list",
        json={"error": "Bad Request"},
        status=400
    )
    result = await server.handle_call_tool(
        name="list_works",
        arguments={"type": ["issue", "ticket"]}
    )
    assert any("List works failed with status 400" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_list_works_missing_type():
    with pytest.raises(ValueError, match="Missing type parameter"):
        await server.handle_call_tool(name="list_works", arguments={})
